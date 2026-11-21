import numpy as np
import pandas as pd


def measure(bars):
    H = 72
    BAND = 2.0
    RAW = "debug_info.components.fall24.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            # 30-day return recomputed from prices inside the window; where not computable, the regime decision (r30 > 0 -> trending)
            r30 = close / close.shift(720) - 1.0
            regime_up = df["regime"].astype(str).eq("trending") if "regime" in df.columns else pd.Series(False, index=df.index)
            up30 = np.where(r30.notna(), r30 > 0, regime_up)
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            fall = (raw < 0).fillna(False).values
            active = (fc != 0).values
            ok = active & up30.astype(bool) & fall & (fc > 0).values
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars with a positive 30-day return and a falling 24-hour return, as the plan's situation requires.",
            "reading": "The situation is read as 30-day return > 0 (recomputed from prices, else the regime) and fall24 raw value < 0, with a long forecast.",
        }

    # ---------- 2. criterion ----------
    case_ret, case_fc, case_coin = [], [], []
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            n = len(df)
            # normal drift sample: grid positions 0, H, 2H, ...
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            # long bets: rise of >= BAND from the lowest level since last bet (from 0 after flat)
            trough = 0.0
            seen_cells = set()
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    trough = 0.0
                    continue
                if f - trough >= BAND:
                    trough = f
                    cell = t // H
                    if cell not in seen_cells:
                        seen_cells.add(cell)
                        if t + H < n and np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                            coin_cases.append((close[t + H] / close[t] - 1.0, f))
                else:
                    trough = min(trough, f)
        drift[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan
        for r, f in coin_cases:
            if np.isfinite(drift[coin]):
                case_ret.append(r - drift[coin])
                case_fc.append(f)
                case_coin.append(coin)

    u = np.array(case_ret, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n_cases = int(len(u))

    mean_u = float(np.mean(u)) if n_cases > 0 else None
    t_u = None
    if n_cases > 1:
        sd = float(np.std(u, ddof=1))
        t_u = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    supp_val, supp_pass = None, None
    n_hi = n_lo = 0
    if n_cases >= 2:
        med = float(np.median(fcs))
        hi = u[fcs > med]
        lo = u[fcs <= med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            supp_val = float(np.mean(hi) - np.mean(lo))
            supp_pass = bool(supp_val > 0)
        else:
            supp_pass = False

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, below the plan's minimum of 30."
    elif t_u is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean_u > 0 and t_u >= 2:
        if supp_pass:
            status = "confirmed"
            decided = "Mean unusual 72-bar return above 0 with t >= 2, and the larger-forecast half beats the smaller half."
        else:
            status = "inconclusive"
            decided = "Mean unusual 72-bar return above 0 with t >= 2, but the larger-forecast half does not beat the smaller half."
    elif mean_u < 0 and t_u <= -2:
        status = "rejected"
        decided = "Mean unusual 72-bar return below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic of the mean unusual 72-bar return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 72-bar return of the bets (return minus coin's normal drift), pooled",
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t_u} if t_u is not None else None,
            "threshold": "confirm if mean > 0 with t >= 2 (and supporting check passes); reject if mean < 0 with t <= -2; at least 30 independent cases",
        },
        "supporting_check": {
            "name": "mean unusual return of larger-forecast half minus smaller-forecast half > 0",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": {"independent cases": n_cases, "larger-forecast half": n_hi, "smaller-forecast half": n_lo},
        "decided_by": decided,
        "reading": "Bets are long forecast rises of at least 2 points from the lowest level since the last bet (reset to 0 when flat), the first per 72-bar grid cell counted from each window's first row, with cases lacking 72 bars ahead in the window dropped; the median split puts forecasts above the median in the larger half and those at or below it in the smaller half; a missed 30-case minimum is reported as not observable.",
    }
