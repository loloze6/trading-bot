import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.calm_move.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation (adapted, graded): raw value = day's move / 60-day mean abs move x (1 - vol rank), nonzero.
    # Expected side (continuation): long after an up day, short after a down day.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = (pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns
                   else pd.Series(np.nan, index=df.index))
            ret1 = close / close.shift(1) - 1.0  # inside the window only
            mask = fc.notna() & (fc != 0) & ret1.notna()
            for i in np.where(mask.values)[0]:
                n_active += 1
                r = raw.iloc[i]
                d = np.sign(ret1.iloc[i])
                s = np.sign(fc.iloc[i])
                in_sit = pd.notna(r) and r != 0 and d != 0 and np.sign(r) == d
                if in_sit and s == d:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars have a nonzero graded calm-move value with the "
                           "forecast on the side of the day's move (continuation), as the Fidelity requires."),
            "reading": ("The situation is a nonzero raw component value whose sign equals the day's close-to-close "
                        "move, and the expected side is that move's sign; a window's first bar, without a previous "
                        "close, is left out."),
        }

    # ---------- 2. Criterion ----------
    top_vals, other_vals = [], []
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H < n and np.isfinite(close[i]) and np.isfinite(close[i + H]) \
                        and close[i] != 0 and np.isfinite(fc[i]):
                    rows.append((fc[i], close[i + H] / close[i] - 1.0))
        if not rows:
            continue
        g = pd.DataFrame(rows, columns=["f", "r"])
        coin_mean = g["r"].mean()  # coin's mean 5-bar return over all windows
        g["x"] = np.sign(g["f"]) * (g["r"] - coin_mean)
        m = len(g)
        rk = g["f"].abs().rank(method="first", ascending=True)
        is_top = rk > 0.8 * m
        top_vals.extend(g.loc[is_top, "x"].tolist())
        other_vals.extend(g.loc[~is_top, "x"].tolist())

    top = np.array(top_vals, dtype=float)
    oth = np.array(other_vals, dtype=float)
    n_top = int(len(top))
    n_oth = int(len(oth))

    mean_top = float(top.mean()) if n_top > 0 else None
    t = None
    if n_top > 1:
        sd = top.std(ddof=1)
        t = float(mean_top / (sd / np.sqrt(n_top))) if sd > 0 else None
    diff = float(top.mean() - oth.mean()) if (n_top > 0 and n_oth > 0) else None
    sup_pass = (diff > 0) if diff is not None else None

    counts = {"top-quintile cases": n_top, "other-quintile cases": n_oth}

    if n_top < 30:
        status = "not observable"
        decided = f"Only {n_top} top-quintile cases, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the top-quintile mean could not be computed (zero spread), so neither rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm: t >= 2 with at least 30 top-quintile cases and a positive top-minus-other difference."
    elif t <= -2:
        status = "rejected"
        decided = "Reject: t <= -2 with at least 30 top-quintile cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "Inconclusive: t >= 2 but the top-minus-other difference is not positive."
    else:
        status = "inconclusive"
        decided = "Inconclusive: t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean sign(forecast) x excess 5-bar return, top |forecast| quintile, pooled",
            "value": mean_top,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": "confirm t >= 2, reject t <= -2, with at least 30 top-quintile cases",
        },
        "supporting_check": {
            "name": "top-quintile mean minus other-four-quintiles mean of signed excess return",
            "value": diff,
            "passed": (bool(sup_pass) if sup_pass is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The top quintile of each coin is the 20% of its grid cases with the largest |forecast| "
                    "(ranked with ties broken by time order, cases with rank above 0.8 x n), zero forecasts included "
                    "with sign 0, and fewer than 30 top-quintile cases is reported as not observable."),
    }
