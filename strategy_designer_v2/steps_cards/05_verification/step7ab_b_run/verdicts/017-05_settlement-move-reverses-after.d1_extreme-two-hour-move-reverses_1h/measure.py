import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    BAND = 2.0
    MIN_CASES = 30
    RAW = "debug_info.components.move2h.last_history_value"

    def raw_from_prices(df):
        c = df["close"].astype(float)
        r1 = c.pct_change()
        r2 = c / c.shift(2) - 1.0
        vol = r1.rolling(20, min_periods=20).std() * np.sqrt(2.0)
        out = r2 / vol
        return out.replace([np.inf, -np.inf], np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), raw_from_prices(df))
            else:
                raw = raw_from_prices(df)
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            # situation: a non-zero 2-hour vol-scaled move; expected side: fade it
            ok = active & raw.notna() & (raw != 0) & (np.sign(f) == -np.sign(raw))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 24-bar move per case, pooled, in the signal's direction"
    main_thr = "confirm t >= 2 over >= 30 cases (with top-quartile difference > 0); reject t <= -2 over >= 30 cases"
    sup_name = "mean unusual move of top-quartile |forecast| cases minus that of other cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active_bars": int(n_active)},
            "decided_by": "Fewer than 90% of active forecast bars have the sign opposite to the 2-hour volatility-scaled move (a fade), so the config does not do what the Fidelity says.",
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    unusual = []
    absf = []
    for coin, wins in bars.items():
        # normal 24-bar drift: grid returns over all windows of the coin
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            for i in range(0, len(c) - H, H):
                a, b = c[i], c[i + H]
                if np.isfinite(a) and np.isfinite(b) and a > 0:
                    grid_rets.append(b / a - 1.0)
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(f)
            side = 0
            low = 0.0
            taken_cells = set()
            for t in range(n):
                s = int(np.sign(f[t]))
                a = abs(f[t])
                if s == 0:
                    side, low = 0, 0.0
                    continue
                if s != side:
                    side, low = s, 0.0
                if a - low >= BAND:
                    low = a
                    cell = t // H
                    if cell in taken_cells:
                        continue
                    taken_cells.add(cell)
                    if t + H < n:
                        p0, p1 = c[t], c[t + H]
                        if np.isfinite(p0) and np.isfinite(p1) and p0 > 0:
                            ret = p1 / p0 - 1.0
                            unusual.append(s * (ret - drift))
                            absf.append(a)
                else:
                    low = min(low, a)

    u = np.array(unusual, dtype=float)
    af = np.array(absf, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        if sd > 0:
            t_stat = float(mean_u / (sd / np.sqrt(n_cases)))

    diff = None
    n_top = n_other = 0
    if n_cases > 0:
        q = float(np.quantile(af, 0.75))
        top = af >= q
        n_top = int(top.sum())
        n_other = int((~top).sum())
        if n_top > 0 and n_other > 0:
            diff = float(np.mean(u[top]) - np.mean(u[~top]))
    sup_pass = (diff > 0) if diff is not None else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n_cases}), the plan's minimum count, so the data could not show the idea."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed (zero dispersion), so neither confirm nor reject rule is met."
    elif t_stat >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The main measure has t >= 2 over at least 30 cases and the top-quartile difference is above 0."
    elif t_stat <= -2:
        status = "rejected"
        decided = "The main measure has t <= -2 over at least 30 cases: extreme moves continue rather than reverse."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top-quartile difference is not above 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2 over at least 30 cases, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": ({"name": "ordinary t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": {"cases": n_cases, "top_quartile_cases": n_top, "other_cases": n_other},
        "decided_by": decided,
        "reading": "A case is the first bet (a rise of |forecast| of >= 2 points on its side from its lowest level since the last bet, reset at flat or side change) in each 24-bar grid cell counted from each window's first row, the drift is the mean of the coin's 24-bar returns on that grid over all its windows, and the top quartile is the cases with |forecast| at or above the 75th percentile of the cases' |forecast|.",
    }
