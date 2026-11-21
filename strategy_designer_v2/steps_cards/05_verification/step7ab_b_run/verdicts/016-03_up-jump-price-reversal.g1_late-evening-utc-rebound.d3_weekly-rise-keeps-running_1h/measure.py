import numpy as np
import pandas as pd


def measure(bars):
    H = 72
    LOOK = 168
    RAW = "debug_info.components.rise_7d.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            recomputed = close / close.shift(LOOK) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "t of mean (72-bar forward excess return x forecast/10), non-overlapping grid, pooled"
    main_thr = "confirm t >= 2 with supporting check passing; reject t <= -2"
    sup_name = "mean excess 72-bar return of cells with forecast above median positive forecast minus that of zero-forecast cells"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are bars with a positive 168-bar return and a long forecast, as the Fidelity's situation (7-day rise, long only) requires.",
            "reading": "The situation is a positive raw 168-bar return (last_history_value, recomputed from closes where missing) with a positive forecast.",
        }

    # ---------- 2. Grid and drift ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, fc[p]))
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc"])

    if len(g) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"grid cases with a positive forecast": 0, "grid cases with a zero forecast": 0},
            "decided_by": "No grid cases: the minimum of 200 positive-forecast and 200 zero-forecast grid cases is not reached.",
            "reading": "none",
        }

    drift = g.groupby("coin")["ret"].mean()
    g["excess"] = g["ret"] - g["coin"].map(drift)
    gf = g[g["fc"].notna()].copy()

    n_pos = int((gf["fc"] > 0).sum())
    n_zero = int((gf["fc"] == 0).sum())
    counts = {"grid cases with a positive forecast": n_pos, "grid cases with a zero forecast": n_zero}

    # main measure
    prod = gf["excess"] * gf["fc"] / 10.0
    nm = int(len(prod))
    mean_prod = float(prod.mean()) if nm > 0 else None
    if nm > 1:
        sd = float(prod.std(ddof=1))
        t = float(mean_prod / (sd / np.sqrt(nm))) if sd > 0 else 0.0
    else:
        t = None

    # supporting check
    pos = gf[gf["fc"] > 0]
    sup_val = None
    sup_pass = None
    if n_pos > 0 and n_zero > 0:
        med = float(pos["fc"].median())
        top = pos[pos["fc"] > med]
        zero = gf[gf["fc"] == 0]
        if len(top) > 0:
            sup_val = float(top["excess"].mean() - zero["excess"].mean())
            sup_pass = bool(sup_val > 0)
    counts["grid cases in product"] = nm

    reading = ("The drift is each coin's mean 72-bar return over the non-overlapping grid of all its windows; "
               "the median of positive forecasts is taken over all pooled grid cells with a positive forecast; "
               "the plan's 'fewer than 200 cases' rule is treated as a minimum count giving 'not observable'.")

    main = {"name": main_name, "value": mean_prod,
            "statistic": {"name": "ordinary t of the mean", "value": t} if t is not None else None,
            "threshold": main_thr}
    sup = {"name": sup_name, "value": sup_val, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_pos < 200 or n_zero < 200:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": f"Minimum count not reached: {n_pos} positive-forecast and {n_zero} zero-forecast grid cases, the plan needs at least 200 of each.",
                "reading": reading}

    if t is None:
        status, why = "inconclusive", "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass is True:
        status, why = "confirmed", "The main measure has t >= 2 and the top-half minus zero-forecast excess return is > 0 (confirm rule)."
    elif t <= -2:
        status, why = "rejected", "The main measure has t <= -2 (reject rule)."
    elif t >= 2:
        status, why = "inconclusive", "The main measure has t >= 2 but the supporting check fails (inconclusive rule)."
    else:
        status, why = "inconclusive", "The main measure's t lies between -2 and 2 (inconclusive rule)."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": why, "reading": reading}
