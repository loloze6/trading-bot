import numpy as np
import pandas as pd


def measure(bars):
    H = 36
    BAND = 2.0
    BRK = "debug_info.components.break.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            high = d["high"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            n = len(d)
            # break: raw component value > 0 where recorded, else recomputed from prices
            raw = pd.to_numeric(d[BRK], errors="coerce").values if BRK in d.columns else np.full(n, np.nan)
            prior_hh = pd.Series(high).shift(1).rolling(12, min_periods=12).max().values
            brk_price = np.where(np.isnan(prior_hh), np.nan, (close > prior_hh).astype(float))
            brk = np.where(~np.isnan(raw), (raw > 0).astype(float), brk_price)
            # gate: 42-bar return > 0 from prices; where not computable in the window, the recorded regime
            ret42 = pd.Series(close).pct_change(42).values
            reg = d["regime"].astype(str).values if "regime" in d.columns else np.array([""] * n)
            gate = np.where(~np.isnan(ret42), (ret42 > 0).astype(float),
                            (reg == "trending").astype(float))
            for i in range(n):
                if fc[i] != 0:
                    n_active += 1
                    ok = (not np.isnan(brk[i])) and brk[i] == 1.0 and gate[i] == 1.0 and fc[i] > 0
                    if ok:
                        n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    reading = ("The break is read from the component's raw value > 0 (recomputed as close above the prior 12 highs where "
               "not recorded) and the 7-day gate from close/close[-42]-1 > 0, falling back to the recorded regime on a "
               "window's first 42 bars; a case is the first bet (forecast rise of >= 2 points from its lowest positive "
               "level since the last bet, from 0 after flat) in each 36-bar grid cell counted from the window's first "
               "row, with a full 36-bar return inside the window; the median split puts forecasts above the median in "
               "the larger half and the rest in the smaller half; fewer than 30 cases is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are long bars on a close above the prior "
                           "12-bar high with a positive 42-bar return, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    case_moves = []
    case_fc = []
    for coin, wins in bars.items():
        # normal drift: mean 36-bar return on the non-overlapping grid over all windows
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            n = len(d)
            for p in range(0, n - H, H):
                if close[p] > 0 and np.isfinite(close[p]) and np.isfinite(close[p + H]):
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            # bets
            ref = 0.0
            seen_cells = set()
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    ref = f
                    cell = i // H
                    if cell not in seen_cells:
                        seen_cells.add(cell)
                        if i + H < n and close[i] > 0 and np.isfinite(close[i]) and np.isfinite(close[i + H]):
                            coin_cases.append((close[i + H] / close[i] - 1.0, f))
                else:
                    ref = min(ref, f)
        if len(grid_rets) == 0 or len(coin_cases) == 0:
            continue
        drift = float(np.mean(grid_rets))
        for r, f in coin_cases:
            case_moves.append(r - drift)
            case_fc.append(f)

    x = np.array(case_moves, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n_cases = int(len(x))

    mean_u = float(np.mean(x)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = float(np.std(x, ddof=1))
        t = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None

    supp_val = None
    n_hi = n_lo = 0
    if n_cases > 1:
        med = float(np.median(fcs))
        hi = x[fcs > med]
        lo = x[fcs <= med]
        n_hi, n_lo = int(len(hi)), int(len(lo))
        if n_hi > 0 and n_lo > 0:
            supp_val = float(np.mean(hi) - np.mean(lo))
    supp_pass = None if supp_val is None else bool(supp_val > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} independent cases, below the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed (zero dispersion), so it meets neither rule."
    elif mean_u > 0 and t >= 2:
        if supp_pass:
            status = "confirmed"
            decided = "The mean unusual move is above 0 with t >= 2 and the larger-forecast half beats the smaller one."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check is at or below 0, which the plan calls inconclusive."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 36-bar unusual move of the bets (return minus coin's normal drift)",
            "value": mean_u,
            "statistic": None if t is None else {"name": "ordinary t of the mean", "value": t},
            "threshold": "confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean unusual move, larger-forecast half minus smaller-forecast half",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": {
            "independent cases": n_cases,
            "larger-forecast half": n_hi,
            "smaller-forecast half": n_lo,
        },
        "decided_by": decided,
        "reading": reading,
    }
