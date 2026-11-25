import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    CL_RAW = "debug_info.components.close_loc.last_history_value"

    # ---------- gather per-coin frames, per window (never joined) ----------
    rows = []          # in-profile active cases for the main measure
    n_active = 0
    n_agree = 0
    coin_rets = {}     # all 1-bar returns per coin, over all windows

    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0
            rets_all.append(nxt.dropna().values)
        coin_rets[coin] = np.concatenate(rets_all) if rets_all else np.array([])

    coin_mean = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in coin_rets.items()}

    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce").fillna(0.0)
            regime = d["regime"].astype(str)
            in_profile = regime != "chop"

            # close location from the high: recorded raw value, else from prices
            rng = (high - low).replace(0, np.nan)
            loc_px = (high - close) / rng
            if CL_RAW in d.columns:
                loc = pd.to_numeric(d[CL_RAW], errors="coerce").fillna(loc_px)
            else:
                loc = loc_px

            # situation: falling agitated profile, close low in its range (lower half), side long
            situation = in_profile & (loc >= 0.5)

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # main measure cases
            nxt = close.shift(-1) / close - 1.0
            m = coin_mean.get(coin, np.nan)
            sel = in_profile & active & nxt.notna()
            if sel.any() and np.isfinite(m):
                ts = pd.to_datetime(d.loc[sel, "timestamp"], utc=True)
                vals = fc[sel] * (nxt[sel] - m)
                for t, v in zip(ts.dt.floor("D"), vals.values):
                    rows.append((t, float(v)))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t of the mean daily sum of forecast x (next-day return - coin mean daily return)"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 100 days of cases"
    reading = ("The plan's situation is read as regime not 'chop' (the profile, as the detector decided it) and the "
               "close in the lower half of the day's range ((high-close)/(high-low) >= 0.5), on the long side; "
               "the coin's mean daily return is the mean of all its 1-bar returns over all windows, and days are UTC "
               "calendar days of the bar's timestamp.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are in-profile bars with the close low in its range "
                           "and a long forecast: the config also takes positions (short or long) where the plan's "
                           "situation on its long side does not hold."),
            "reading": reading,
        }

    if rows:
        cases = pd.DataFrame(rows, columns=["day", "v"])
        daily = cases.groupby("day")["v"].sum()
    else:
        daily = pd.Series(dtype=float)
    n_days = int(len(daily))
    n_cases = int(len(rows))

    mean = float(daily.mean()) if n_days > 0 else None
    t = None
    if n_days > 1:
        sd = float(daily.std(ddof=1))
        t = float(mean / (sd / np.sqrt(n_days))) if sd > 0 else None

    counts = {"days of cases": n_days, "in-profile cases": n_cases}

    if n_days < 100:
        status = "not observable"
        decided = f"Only {n_days} days with in-profile cases, below the plan's minimum of 100 days."
    elif t is not None and mean > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean of the daily sums is positive with t >= 2 over at least 100 days (confirm rule)."
    elif t is not None and mean < 0 and t <= -2:
        status = "rejected"
        decided = "The mean of the daily sums is negative with t <= -2 over at least 100 days (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 over at least 100 days (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
