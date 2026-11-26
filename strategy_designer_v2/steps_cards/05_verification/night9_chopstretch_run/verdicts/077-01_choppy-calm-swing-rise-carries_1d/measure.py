import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    BAND = 2.0
    VSR_COL = "debug_info.components.carry.last_history_value"

    def recompute_vsr(close):
        r = close.pct_change()
        ret14 = close / close.shift(14) - 1.0
        sd = r.rolling(30, min_periods=30).std()
        return ret14 / (sd * np.sqrt(14))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            close = pd.to_numeric(df["close"], errors="coerce")
            vsr_re = recompute_vsr(close)
            if VSR_COL in df.columns:
                vsr = pd.to_numeric(df[VSR_COL], errors="coerce").combine_first(vsr_re)
            else:
                vsr = vsr_re
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            active = fc != 0
            situ = (regime == "trending") & (vsr >= 1.0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 7-bar move over forecast-rise cases (long)"
    main_thr = "confirm: mean > 0 with day-grouped t >= 2 and supporting check passing; reject: mean < 0 with t <= -2"
    sup_name = "mean unusual move above median forecast minus below median forecast > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are long bars of the plan's situation "
                          "(choppy calm profile, regime 'trending', 14-day swing-scaled return >= 1.0).",
            "reading": "The situation is read as regime == 'trending' (the detector's profile vetoes plus vsr >= 1) "
                       "with the carry raw value (recomputed from prices if missing) >= 1.0 and a positive forecast.",
        }

    # ---------- 2. drift per coin (non-overlapping grid, all windows) ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(close) - H, H):
                a, b = close[i], close[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    rets.append(b / a - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    cases = []  # (day, unusual, forecast)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            ref = 0.0
            bets = []
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    bets.append(t)
                    ref = f
                else:
                    ref = min(ref, f)
            seen_cells = set()
            for t in bets:
                cell = t // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if t + H >= n:
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a > 0) or not np.isfinite(drift[coin]):
                    continue
                u = (b / a - 1.0) - drift[coin]
                cases.append((ts.iloc[t].strftime("%Y-%m-%d"), u, fc[t]))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)

    mean_u = None
    tval = None
    if n_cases > 0:
        u = np.array([c[1] for c in cases])
        mean_u = float(u.mean())
        if n_days > 1:
            e = u - mean_u
            dsum = {}
            for c, ei in zip(cases, e):
                dsum[c[0]] = dsum.get(c[0], 0.0) + ei
            E = np.array(list(dsum.values()))
            var = (n_days / (n_days - 1.0)) * np.sum(E ** 2) / (n_cases ** 2)
            tval = float(mean_u / np.sqrt(var)) if var > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        f = np.array([c[2] for c in cases])
        u = np.array([c[1] for c in cases])
        med = np.median(f)
        hi, lo = u[f > med], u[f < med]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"cases": n_cases, "case-days": n_days}
    reading = ("Cases are the first long forecast rise of >= 2 points (from its lowest level since the last bet, "
               "reset to 0 when flat) in each 7-bar grid cell from each window's first row; the day-grouped t uses "
               "the cluster standard error of the mean with deviations summed per UTC day (small-sample factor G/(G-1)); "
               "cases equal to the median forecast are left out of both halves of the supporting check; fewer than 30 "
               "case-days is reported as not observable.")

    if n_days < 30 or tval is None:
        status = "not observable"
        decided = f"Only {n_days} case-days, below the plan's minimum of 30 case-days."
    elif mean_u > 0 and tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is above 0 with t >= 2 and the supporting check passes."
    elif mean_u < 0 and tval <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": {"name": "t of the mean, cases grouped by day", "value": tval} if tval is not None else None,
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
