import numpy as np
import pandas as pd


def measure(bars):
    MOVE_COL = "debug_info.components.move.last_history_value"
    VOL_PERIOD = 20
    MIN_QUALIFYING = 60

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    case_frames = []

    for coin, windows in bars.items():
        for w, df in windows.items():
            df = df.reset_index(drop=True).copy()
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)

            # Up bar: the one-bar percent move. Use the move component's raw value, or the close change if it is missing.
            move = df[MOVE_COL].astype(float) if MOVE_COL in df.columns else pd.Series(np.nan, index=df.index)
            move = move.where(move.notna(), close.pct_change())
            vol_mean = vol.rolling(VOL_PERIOD, min_periods=VOL_PERIOD).mean()  # current bar included
            computable = move.notna() & vol_mean.notna() & vol.notna()
            situation = computable & (move > 0) & (vol < vol_mean)

            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0) & computable
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # ---------- Cases for the criterion ----------
            nxt = close.shift(-1) / close - 1.0  # inside this window only
            uncond_mean = nxt.dropna().mean()
            alloc = df["postRebalance_current_allocation"].astype(float)
            sel = situation & nxt.notna() & alloc.notna()
            if sel.any():
                case_frames.append(pd.DataFrame({
                    "alloc": alloc[sel].values,
                    "adj": (nxt[sel] - uncond_mean).values,
                }))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    reading = ("Up bar = one-bar close-to-close move > 0, and thin = volume < its 20-bar mean with the current bar included, "
               "computed inside each window. Bars without 20 bars of volume history are left out of the check. "
               "Qualifying cases are all thin up bars with a next-bar return. The main measure is the |position|-weighted mean "
               "of the short's drift-adjusted next-bar return, -(r - window mean). Its t is the ordinary t of the per-case "
               "gains alloc x (r - window mean) over cases with a non-zero position. Thirds are made by sorting the qualifying "
               "cases on |position| and splitting them with array_split.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars of the plan's situation "
                           "(an up bar with volume below its 20-bar mean)."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    cases = pd.concat(case_frames, ignore_index=True) if case_frames else pd.DataFrame(columns=["alloc", "adj"])
    n_qual = int(len(cases))

    w = cases["alloc"].abs()
    value = None
    t_stat = None
    nz = cases[cases["alloc"] != 0]
    n_pos = int(len(nz))
    if w.sum() > 0:
        value = float((w * (-cases["adj"])).sum() / w.sum())
        g = nz["alloc"] * nz["adj"]
        if n_pos >= 2 and g.std(ddof=1) > 0:
            t_stat = float(g.mean() / (g.std(ddof=1) / np.sqrt(n_pos)))

    # Supporting check: split into thirds by |position|.
    sup_val = None
    sup_pass = None
    if n_qual >= 3:
        order = np.argsort(cases["alloc"].abs().values, kind="mergesort")
        parts = np.array_split(order, 3)
        drop_small = -cases["adj"].values[parts[0]].mean()
        drop_large = -cases["adj"].values[parts[-1]].mean()
        sup_val = float(drop_large - drop_small)
        sup_pass = bool(sup_val > 0)

    if n_qual < MIN_QUALIFYING:
        status = "inconclusive"
        decided = f"Fewer than {MIN_QUALIFYING} qualifying bars across all windows is inconclusive."
    elif value is None or t_stat is None:
        status = "inconclusive"
        decided = "The position-weighted measure or its t-stat cannot be computed, so the result is inconclusive."
    elif value > 0 and t_stat >= 2.0 and sup_pass:
        status = "confirmed"
        decided = ("The drift-adjusted, position-weighted next-bar return of the short is above 0 with t >= 2.0, "
                   "and the largest third reverts more than the smallest third.")
    elif value <= 0 and t_stat <= 0:
        status = "rejected"
        decided = "The short earns 0 or less after the drift adjustment, with a t-stat of 0 or below."
    else:
        status = "inconclusive"
        if value > 0 and t_stat >= 2.0:
            decided = "The mean is confirmed but the size ordering is not, so the result is inconclusive."
        else:
            decided = "The drift-adjusted result has a t-stat between 0 and 2, so the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "position-weighted, drift-adjusted next-bar return of the short after thin up bars",
            "value": value,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": "above 0 with a t-stat of at least 2.0 (reject: 0 or less with t of 0 or below)",
        },
        "supporting_check": {
            "name": "largest third minus smallest third of |position|, mean drift-adjusted next-bar drop",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"qualifying bars": n_qual, "cases with non-zero position": n_pos, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
