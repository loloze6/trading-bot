import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 6
    BAND = 2.0
    MIN_CASES = 100
    FALL = "debug_info.components.fall.last_history_value"
    FXV = "debug_info.components.fall_x_volume.last_history_value"

    n_active = 0
    n_agree = 0
    case_rows = []  # (coin, unusual move, v)

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        # normal drift: mean 6-bar return on the non-overlapping grid of all windows of the coin
        grid_rets = []
        prepared = {}
        for w in sorted(wins.keys(), key=lambda s: (len(str(s)), str(s))):
            df = wins[w].reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            n = len(df)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            for p in range(0, n - H, H):
                if np.isfinite(fwd[p]):
                    grid_rets.append(fwd[p])
            prepared[w] = (df, fwd)
        drift = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for w, (df, fwd) in prepared.items():
            n = len(df)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = df["close"].astype(float).to_numpy()
            if FALL in df.columns:
                fall = pd.to_numeric(df[FALL], errors="coerce").to_numpy(dtype=float)
            else:
                fall = np.full(n, np.nan)
            # where the component is not recorded, recompute the hour's sign from prices
            r = np.full(n, np.nan)
            if n > 1:
                r[1:] = close[1:] / close[:-1] - 1.0
            fall_sign_src = np.where(np.isfinite(fall), fall, r)
            fxv = (pd.to_numeric(df[FXV], errors="coerce").to_numpy(dtype=float)
                   if FXV in df.columns else np.full(n, np.nan))

            # situation check: active bars that are down hours with a long forecast
            active = np.isfinite(fc) & (fc != 0)
            agree = active & np.isfinite(fall_sign_src) & (fall_sign_src < 0) & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            # long bets: rise of the forecast on the long side >= band from its lowest level since last bet
            ref = 0.0
            used_cells = set()
            for t in range(n):
                f = fc[t]
                if not np.isfinite(f) or f <= 0:
                    ref = 0.0
                    continue
                if f - ref >= BAND:
                    ref = f
                    cell = t // H
                    if cell in used_cells:
                        continue
                    used_cells.add(cell)
                    if np.isfinite(fwd[t]) and np.isfinite(drift):
                        v = np.nan
                        if np.isfinite(fall[t]) and np.isfinite(fxv[t]) and fall[t] != 0:
                            v = fxv[t] / fall[t]
                        case_rows.append((coin, fwd[t] - drift, v))
                else:
                    ref = min(ref, f)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = agreement >= 0.9
    sit = {"agreement": agreement, "passed": bool(passed_sit)}
    main_name = "mean 6-bar unusual move after long bets (return minus coin's normal 6-bar drift), before costs"
    thr = "confirm: mean > 0 with t >= 2 and thin-minus-heavy > 0; reject: mean < 0 with t <= -2"
    reading_base = ("Situation taken as a down hour (raw fall < 0, or the price return where unrecorded) with a positive "
                    "forecast; bets per the holding-period rule with one case per 6-bar cell; volume halves split as "
                    "v <= median (thinner) versus v > median (heavier), cases without a valid v left out of the split.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are down hours with a long forecast, "
                           "so the config does not take the long side on the plan's falls as the Fidelity says."),
            "reading": reading_base,
        }

    um = np.array([c[1] for c in case_rows], dtype=float)
    vv = np.array([c[2] for c in case_rows], dtype=float)
    n_cases = int(len(um))

    mean = float(np.mean(um)) if n_cases > 0 else None
    tval = None
    if n_cases > 1:
        sd = float(np.std(um, ddof=1))
        tval = float(mean / (sd / np.sqrt(n_cases))) if sd > 0 else None

    diff = None
    n_thin = n_heavy = 0
    ok = np.isfinite(vv)
    if ok.sum() >= 2:
        med = float(np.median(vv[ok]))
        thin = um[ok][vv[ok] <= med]
        heavy = um[ok][vv[ok] > med]
        n_thin, n_heavy = int(len(thin)), int(len(heavy))
        if n_thin > 0 and n_heavy > 0:
            diff = float(np.mean(thin) - np.mean(heavy))
    sup_pass = None if diff is None else bool(diff > 0)

    counts = {"long cases pooled over both coins and all windows": n_cases,
              "thinner-volume half": n_thin, "heavier-volume half": n_heavy}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} long cases pooled over both coins and all windows ({n_cases})."
    elif tval is not None and mean > 0 and tval >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Mean unusual move after long cases is positive with t >= 2 and the thin-minus-heavy difference is > 0."
    elif tval is not None and mean < 0 and tval <= -2:
        status = "rejected"
        decided = "Mean unusual move after long cases is negative with t <= -2."
    elif tval is not None and tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the thin-minus-heavy difference is <= 0 (or not measurable), which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {"name": main_name,
                         "value": mean,
                         "statistic": None if tval is None else {"name": "t of the mean", "value": tval},
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move, thinner-volume half minus heavier-volume half",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
