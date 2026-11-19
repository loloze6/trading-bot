import numpy as np
import pandas as pd
from scipy import stats

RAW = "debug_info.components.rsi_above.last_history_value"
H = 240


def _slope(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    if n < 3 or np.nanstd(x) == 0:
        return None, None, n
    r = stats.linregress(x, y)
    se = r.stderr if (r.stderr is not None and r.stderr > 0) else None
    return float(r.slope), (float(se) if se is not None else None), n


def measure(bars):
    reading = ("The raw rsi_above value is read as 50 minus the 336-bar RSI, so the situation is raw < 0 "
               "(RSI above 50) on the long side; the main regression uses every grid bar (forecast zero included) "
               "and the coin mean is the mean of that coin's grid 240-bar returns over all windows; "
               "the regime slopes are OLS slopes whose difference is divided by the root sum of their squared "
               "standard errors (Welch t); the plan's minimum counts, when unmet, give 'not observable'.")

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0)
            situation = raw < 0  # RSI = 50 - raw > 50
            n_active += int(active.sum())
            n_agree += int((active & situation & (f > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "OLS slope of 240-bar forward return minus coin mean, on forecast (non-overlapping grid, pooled)"
    threshold = "confirm: slope t >= 2 and supporting Welch t >= 2; reject: slope t <= -2"
    sup_name = "slope on trending minus slope on unknown grid bars (Welch t)"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars with RSI above 50 "
                           "with a long forecast, as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- grid samples ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            reg = df["regime"].astype(str).to_numpy()
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not np.isfinite(c0) or not np.isfinite(c1) or c0 == 0 or not np.isfinite(f[i]):
                    continue
                rows.append((coin, w, c1 / c0 - 1.0, f[i], reg[i]))
    g = pd.DataFrame(rows, columns=["coin", "window", "ret", "forecast", "regime"])

    if len(g) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"grid cases with forecast above 0": 0,
                       "trending grid cases with forecast above 0": 0,
                       "unknown grid cases with forecast above 0": 0},
            "decided_by": "No grid cases: the minimum of 300 grid cases with a forecast above 0 is not reached.",
            "reading": reading,
        }

    g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")

    pos = g["forecast"] > 0
    n_pos = int(pos.sum())
    n_pos_tr = int((pos & (g["regime"] == "trending")).sum())
    n_pos_un = int((pos & (g["regime"] == "unknown")).sum())
    counts = {"grid cases with forecast above 0": n_pos,
              "trending grid cases with forecast above 0": n_pos_tr,
              "unknown grid cases with forecast above 0": n_pos_un,
              "grid cases": int(len(g))}

    b, se, n = _slope(g["forecast"], g["excess"])
    t_main = float(b / se) if (b is not None and se is not None) else None

    tr = g[g["regime"] == "trending"]
    un = g[g["regime"] == "unknown"]
    b1, se1, _ = _slope(tr["forecast"], tr["excess"])
    b2, se2, _ = _slope(un["forecast"], un["excess"])
    diff = None
    t_sup = None
    if b1 is not None and b2 is not None:
        diff = float(b1 - b2)
        if se1 is not None and se2 is not None:
            t_sup = float(diff / np.sqrt(se1 ** 2 + se2 ** 2))
    sup_passed = (t_sup is not None and t_sup >= 2)

    main = {"name": main_name, "value": b,
            "statistic": ({"name": "OLS slope t", "value": t_main} if t_main is not None else None),
            "threshold": threshold}
    sup = {"name": sup_name, "value": t_sup, "passed": (bool(sup_passed) if t_sup is not None else None)}

    if n_pos < 300 or n_pos_tr < 100 or n_pos_un < 100:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_pos} grid cases with forecast above 0 (need 300), "
                   f"{n_pos_tr} trending and {n_pos_un} unknown (need 100 each).")
    elif t_main is None:
        status = "inconclusive"
        decided = "The main slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_main >= 2 and sup_passed:
        status = "confirmed"
        decided = "Confirm: the main slope has t >= 2 and the trending-minus-unknown slope difference has Welch t >= 2."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "Inconclusive: the main slope has t >= 2 but the supporting difference has t below 2."
    elif t_main <= -2:
        status = "rejected"
        decided = "Reject: the main slope has t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the main slope has t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
