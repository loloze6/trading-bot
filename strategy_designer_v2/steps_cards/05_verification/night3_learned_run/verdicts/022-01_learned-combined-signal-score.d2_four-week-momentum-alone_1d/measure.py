import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    COMP = "debug_info.components.mom28.last_history_value"

    # ---------- 1. Situation check: forecast sign must follow the 28-day return's sign ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            if COMP in d.columns:
                raw = pd.to_numeric(d[COMP], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # fallback where the component is not recorded: 28-bar return from prices (inside the window)
            price_ret = close / close.shift(28) - 1.0
            raw = raw.where(raw.notna(), price_ret)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (np.sign(raw) == np.sign(fc)) & (raw != 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x (5-day return minus coin's normal drift), non-overlapping 5-bar grid, before costs"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 300 grid cases with a non-zero forecast"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars agreeing": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast have a forecast whose sign follows the "
                          "sign of the coin's 28-day return, as the plan's situation (long on a 4-week rise, short on a fall) requires.",
            "reading": "The situation is taken as the sign of the recorded mom28 raw value (28-bar return), recomputed from prices where missing.",
        }

    # ---------- 2. Criterion ----------
    # grid cells per coin/window
    cells = {}  # coin -> list of (forecast, ret)
    for coin, wins in bars.items():
        lst = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                lst.append((fc[i], c1 / c0 - 1.0))
        cells[coin] = lst

    values = []
    n_nonzero = 0
    n_cells = 0
    for coin, lst in cells.items():
        if not lst:
            continue
        rets = np.array([r for _, r in lst], dtype=float)
        drift = float(np.mean(rets))
        for f, r in lst:
            if not np.isfinite(f):
                continue
            n_cells += 1
            if f != 0:
                n_nonzero += 1
            values.append(f / 10.0 * (r - drift))

    values = np.array(values, dtype=float)
    mean = float(np.mean(values)) if len(values) > 0 else None
    if len(values) > 1:
        sd = float(np.std(values, ddof=1))
        t = float(mean / (sd / np.sqrt(len(values)))) if sd > 0 else 0.0
    else:
        t = None

    counts = {"grid cases with a non-zero forecast": int(n_nonzero), "grid cases": int(n_cells)}

    if n_nonzero < 300 or t is None:
        status = "not observable"
        decided = f"Only {n_nonzero} grid cases have a non-zero forecast, below the plan's minimum of 300 independent cases."
    elif mean > 0 and t >= 2:
        status = "confirmed"
        decided = "Confirm rule met: the mean is positive with t >= 2 from at least 300 independent cases."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Reject rule met: the mean is negative with t <= -2 from at least 300 independent cases."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule met: -2 < t < 2 with at least 300 grid cases with a non-zero forecast."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean,
            "statistic": {"name": "ordinary t of the mean", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": "The mean and t are taken over every grid cell (bars 0, 5, 10, ... of each window with a 5-bar return inside it, zero-forecast cells contributing 0), the normal drift is each coin's mean 5-bar return over that grid in all its windows, and the 300 minimum is counted on grid cells with a non-zero forecast.",
    }
