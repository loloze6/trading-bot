import numpy as np
import pandas as pd


def measure(bars):
    DEPTH_COL = "debug_info.components.depth.last_history_value"

    def _num(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        if not np.isfinite(x):
            return None
        return x

    # ---------- 1. Situation check ----------
    n_active_checked = 0
    n_agree = 0
    n_active_total = 0
    n_active_uncomputable = 0

    # ---------- collect cases for the criterion ----------
    case_rows = []  # (day, coin, excess, depth_raw)

    for coin, wins in bars.items():
        # coin's mean daily (1-bar) return over all windows together
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").reset_index(drop=True)
            r = (c.shift(-1) / c - 1.0).iloc[:-1]
            all_rets.append(r.dropna())
        if all_rets:
            allr = pd.concat(all_rets)
            coin_mean = float(allr.mean()) if len(allr) else np.nan
        else:
            coin_mean = np.nan

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if DEPTH_COL in df.columns:
                depth_rec = pd.to_numeric(df[DEPTH_COL], errors="coerce")
            else:
                depth_rec = pd.Series(np.nan, index=df.index)

            # recomputed raw values from prices (inside this window only)
            prior_low = low.shift(1).rolling(20, min_periods=20).min()
            depth_calc = (close / prior_low - 1.0) * 100.0
            depth_raw = depth_rec.where(depth_rec.notna(), depth_calc)
            ret60 = (close / close.shift(60) - 1.0) * 100.0

            active = fc != 0
            computable = depth_raw.notna() & ret60.notna()
            situation = (depth_raw < 0) & (ret60 >= -10) & (ret60 <= 10)
            n_active_total += int(active.sum())
            n_active_uncomputable += int((active & ~computable).sum())
            chk = active & computable
            n_active_checked += int(chk.sum())
            n_agree += int((chk & situation & (fc > 0)).sum())

            # criterion cases: bars in the mean_reversion regime, 1-bar horizon
            regime = df["regime"].astype(str)
            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D")
            mask = (regime == "mean_reversion") & nxt.notna() & day.notna()
            if not np.isfinite(coin_mean):
                continue
            for i in np.where(mask.values)[0]:
                case_rows.append((day.iloc[i], coin, float(nxt.iloc[i]) - coin_mean,
                                  _num(depth_rec.iloc[i])))

    agreement = (n_agree / n_active_checked) if n_active_checked > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("The situation check uses the recorded depth (else the close against the prior 20 bars' lowest low) "
               "and the 60-bar close return in percent, inclusive of -10 and +10, and leaves out of its share the "
               "active bars whose 60-bar return or 20-bar low cannot be computed inside the window; the depth slope "
               "is the least-squares slope of each coin-bar's next-day excess return on its depth below the low "
               "(minus last_history_value), fitted over the coin-bar observations of the cases.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": _num(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active_total,
                       "active bars checked": n_active_checked,
                       "active bars uncomputable": n_active_uncomputable},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars where the close is "
                           "below the prior 20-day low inside the choppy profile (60-day return within +/-10 %)."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    if case_rows:
        cdf = pd.DataFrame(case_rows, columns=["day", "coin", "excess", "depth_raw"])
        daily = cdf.groupby("day")["excess"].sum()
    else:
        cdf = pd.DataFrame(columns=["day", "coin", "excess", "depth_raw"])
        daily = pd.Series(dtype=float)

    n_days = int(len(daily))
    n_cases = int(len(cdf))
    mean_ex = float(daily.mean()) if n_days > 0 else None
    t_val = None
    if n_days >= 2:
        sd = float(daily.std(ddof=1))
        if sd > 0:
            t_val = mean_ex / (sd / np.sqrt(n_days))

    # supporting check: slope of excess on depth below the low
    slope = None
    sub = cdf.dropna(subset=["depth_raw", "excess"]) if n_cases else cdf
    if len(sub) >= 3:
        x = -sub["depth_raw"].astype(float).values
        y = sub["excess"].astype(float).values
        if np.var(x) > 0:
            slope = float(np.polyfit(x, y, 1)[0])
    slope_pass = None if slope is None else bool(slope > 0)

    counts = {"days with a case": n_days, "cases (coin-bars)": n_cases,
              "cases with depth": int(len(sub))}

    if n_days < 30:
        status = "not observable"
        decided_by = f"Fewer than 30 days with a case ({n_days}): the plan's minimum count is not reached."
    elif t_val is None:
        status = "inconclusive"
        decided_by = "The t of the mean excess next-day return cannot be computed (zero spread), so it is not beyond +/-2."
    elif mean_ex > 0 and t_val >= 2 and slope_pass is True:
        status = "confirmed"
        decided_by = ("The mean excess next-day return is above 0 with t >= 2 on at least 30 days, "
                      "and the depth slope is above 0.")
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "The mean excess next-day return is below 0 with t <= -2 on at least 30 days."
    elif mean_ex > 0 and t_val >= 2:
        status = "inconclusive"
        decided_by = "A positive mean with t >= 2 whose depth slope is not above 0 is inconclusive."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean excess next-day return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": _num(agreement), "passed": passed},
        "main_measure": {
            "name": "mean next-day excess return over the coin's mean, cases summed per day",
            "value": _num(mean_ex),
            "statistic": ({"name": "t of the mean", "value": _num(t_val)} if t_val is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 on >= 30 days; reject: mean < 0 with t <= -2 on >= 30 days",
        },
        "supporting_check": {"name": "slope of next-day excess return on depth below the prior 20-day low",
                             "value": _num(slope), "passed": slope_pass},
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
