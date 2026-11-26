import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0
    DEPTH = "debug_info.components.depth.last_history_value"

    def recompute_depth(df):
        c = df["close"].astype(float)
        prior_high = c.shift(1).rolling(20, min_periods=20).max()
        vol = c.pct_change().rolling(20, min_periods=20).std()
        return (c / prior_high - 1.0) / vol

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            if DEPTH in df.columns:
                d = pd.to_numeric(df[DEPTH], errors="coerce")
            else:
                d = pd.Series(np.nan, index=df.index)
            d = d.where(d.notna(), recompute_depth(df))
            act = f != 0
            n_active += int(act.sum())
            ok = act & (f < 0) & (d <= -2.0 + 1e-9)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    main_name = "mean unusual move over 5 bars of short cases (day-clustered t)"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2"
    reading = ("A case is the first short bet (forecast magnitude rising by at least 2 points from its "
               "lowest level since the last bet, from 0 after a flat or side change) in each 5-bar grid cell "
               "of a window, its return taken from that bar's close over 5 bars inside the window; the normal "
               "drift is the coin's mean 5-bar return on the grid over all its windows; the day-clustered t uses "
               "per-day summed deviations with a G/(G-1) correction; the deeper half is depth at or below the "
               "median, the shallower half above it; fewer than 30 case days is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "distinct case days": 0, "cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with a close at "
                           "least 2 daily swings below the prior 20-day closing high, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. cases ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            for p in range(0, n - H, H):
                if c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            if DEPTH in df.columns:
                d = pd.to_numeric(df[DEPTH], errors="coerce")
            else:
                d = pd.Series(np.nan, index=df.index)
            d = d.where(d.notna(), recompute_depth(df)).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            side = 0
            ref = 0.0
            bet = np.zeros(n, dtype=bool)
            for t in range(n):
                ft = f[t]
                if ft == 0:
                    side, ref = 0, 0.0
                    continue
                s = 1 if ft > 0 else -1
                if s != side:
                    side, ref = s, 0.0
                mag = abs(ft)
                if mag - ref >= BAND - 1e-12:
                    if s < 0:
                        bet[t] = True
                    ref = mag
                else:
                    ref = min(ref, mag)
            for start in range(0, n, H):
                idx = [t for t in range(start, min(start + H, n)) if bet[t]]
                if not idx:
                    continue
                t = idx[0]
                if t + H >= n or not (c[t] > 0) or np.isnan(c[t + H]):
                    continue
                coin_cases.append({
                    "coin": coin,
                    "ret": c[t + H] / c[t] - 1.0,
                    "depth": d[t],
                    "day": ts.iloc[t].strftime("%Y-%m-%d"),
                })
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan
        for r in coin_cases:
            r["unusual"] = -(r["ret"] - drift)
            rows.append(r)

    cases = pd.DataFrame(rows, columns=["coin", "ret", "depth", "day", "unusual"])
    cases = cases.dropna(subset=["unusual"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean = float(cases["unusual"].mean()) if n_cases else None
    tval = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["unusual"] - mean
        S = dev.groupby(cases["day"]).sum().values
        G = len(S)
        se = np.sqrt(G / (G - 1.0) * np.sum(S ** 2)) / n_cases
        tval = float(mean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    cd = cases.dropna(subset=["depth"])
    if len(cd) >= 2:
        med = cd["depth"].median()
        deep = cd.loc[cd["depth"] <= med, "unusual"]
        shal = cd.loc[cd["depth"] > med, "unusual"]
        if len(deep) > 0 and len(shal) > 0:
            sup_val = float(deep.mean() - shal.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"distinct case days": n_days, "cases": n_cases, "active bars": int(n_active)}

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 distinct case days ({n_days}), the plan's minimum count, so the data cannot show the idea."
    elif mean is not None and tval is not None and mean > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the deeper half beats the shallower half (confirm rule)."
    elif mean is not None and tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        if mean is not None and tval is not None and mean > 0 and tval >= 2:
            decided = "The mean unusual move is above 0 with t >= 2 but the supporting check failed (inconclusive rule)."
        else:
            decided = "The t of the mean unusual move lies between -2 and 2, meeting neither confirm nor reject (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "t of the mean, clustered by day", "value": tval} if tval is not None else None,
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean unusual move deeper half minus shallower half (median depth split)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
