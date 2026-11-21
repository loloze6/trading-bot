import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    C_PPV = "debug_info.components.combined.post_pipeline_value"
    B_PPV = "debug_info.components.best.post_pipeline_value"
    R_LHV = "debug_info.components.ret90.last_history_value"

    def col(df, name):
        if name in df.columns:
            return pd.to_numeric(df[name], errors="coerce").to_numpy(dtype=float)
        return np.full(len(df), np.nan)

    # ---------------- situation check ----------------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            r90 = col(df, R_LHV)
            # fallback: recompute the 90-day return from prices inside the window
            r90_px = np.full(len(df), np.nan)
            if len(df) > 90:
                r90_px[90:] = close[90:] / close[:-90] - 1.0
            r90_use = np.where(np.isnan(r90), r90_px, r90)
            comb = col(df, C_PPV)
            for i in range(len(df)):
                f = fc[i]
                if np.isnan(f) or f == 0:
                    continue
                n_active += 1
                in_sit = (not np.isnan(r90_use[i])) and r90_use[i] > 0
                side_ok = (not np.isnan(comb[i])) and np.sign(comb[i]) == np.sign(f)
                if in_sit and side_ok:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The idea claims no rise or fall, so the expected side on each active bar is the sign of the "
               "combined score, and the situation is ret90 > 0 (recorded value, else recomputed from prices "
               "inside the window); trending cases are bars with regime 'trending' at grid positions 0,5,10,... "
               "of each window with a full 5-bar forward return; each coin's mean 5-day return is taken over "
               "the same grid on all its windows' bars; the pooled standard deviations are taken over all cases "
               "of all coins; the median split puts ret90 above the median in the upper half and the rest in "
               "the lower half; the plan's 200-case minimum, when not met, gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent cases in the regime": None},
            "decided_by": ("Fewer than 90% of the active bars are bars with a positive 90-day return whose "
                           "forecast sign follows the combined score, so the config does not do what the "
                           "Fidelity's situation (90-day return above 0) states."),
            "reading": reading,
        }

    # ---------------- main measure ----------------
    rows = []
    for coin in sorted(bars):
        coin_rets = []
        coin_cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            reg = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * n)
            comb = col(df, C_PPV)
            best = col(df, B_PPV)
            r90 = col(df, R_LHV)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                if np.isnan(close[i]) or np.isnan(close[i + H]) or close[i] == 0:
                    continue
                fr = close[i + H] / close[i] - 1.0
                coin_rets.append(fr)
                if reg[i] == "trending":
                    coin_cases.append((fr, comb[i], best[i], r90[i]))
        if len(coin_rets) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for fr, c, b, r in coin_cases:
            if np.isnan(c) or np.isnan(b):
                continue
            rows.append((fr - mu, c, b, r))

    n_cases = len(rows)
    counts = {"independent cases in the regime": int(n_cases), "active bars": int(n_active)}
    main_name = "mean of d = (scaled combined - scaled best) x excess 5-day return"
    threshold = "confirm if t >= 2 with the check above 0; reject if t <= -2; at least 200 cases"

    mean_d = None
    t_val = None
    check_val = None
    check_pass = None
    if n_cases >= 2:
        arr = np.array(rows, dtype=float)
        ex, c, b, r = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]
        sc = np.std(c, ddof=1)
        sb = np.std(b, ddof=1)
        if sc > 0 and sb > 0:
            d = (c / sc - b / sb) * ex
            mean_d = float(np.mean(d))
            sd = float(np.std(d, ddof=1))
            t_val = float(mean_d / (sd / np.sqrt(len(d)))) if sd > 0 else None
            ok = ~np.isnan(r)
            if ok.sum() >= 2:
                med = np.median(r[ok])
                up = d[ok][r[ok] > med]
                lo = d[ok][r[ok] <= med]
                if len(up) > 0 and len(lo) > 0:
                    check_val = float(np.mean(up) - np.mean(lo))
                    check_pass = bool(check_val > 0)

    main = {"name": main_name, "value": mean_d,
            "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": threshold}
    support = {"name": "mean d upper ret90 half minus lower half", "value": check_val, "passed": check_pass}

    if n_cases < 200:
        status = "not observable"
        decided = f"Only {n_cases} independent trending cases, fewer than the plan's minimum of 200."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of mean d could not be computed (zero spread), so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and check_pass:
        status = "confirmed"
        decided = "Mean d has t >= 2 and the upper-minus-lower ret90 half difference is above 0 (confirm rule)."
    elif t_val <= -2:
        status = "rejected"
        decided = "Mean d has t <= -2 (reject rule)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "Mean d has t >= 2 but the supporting check is at or below 0 (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "The t of mean d lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
