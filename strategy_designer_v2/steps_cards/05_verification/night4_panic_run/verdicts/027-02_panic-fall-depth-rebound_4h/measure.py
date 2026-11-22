import numpy as np
import pandas as pd
from scipy import stats


def _component(df, cid, field):
    col = "debug_info.components.%s.%s" % (cid, field)
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for v in df["debug_info.components"].values:
            val = np.nan
            d = v
            if isinstance(d, str):
                try:
                    import json
                    d = json.loads(d)
                except Exception:
                    d = None
            if isinstance(d, dict):
                c = d.get(cid)
                if isinstance(c, dict):
                    x = c.get(field)
                    try:
                        val = float(x) if x is not None else np.nan
                    except Exception:
                        val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def _bets(fc):
    """Bets of the holding-period rule: a rise of the forecast on its side of >= 2 points
    from its lowest level on that side since the last bet (from 0 after a flat or a side change)."""
    n = len(fc)
    bet = np.zeros(n, dtype=bool)
    ref = 0.0
    side = 0
    for i in range(n):
        f = fc[i]
        if not np.isfinite(f) or f == 0:
            ref = 0.0
            side = 0
            continue
        s = 1 if f > 0 else -1
        a = abs(f)
        if s != side:
            ref = 0.0
            side = s
        if a - ref >= 2.0 - 1e-12:
            bet[i] = True
            ref = a
        else:
            ref = min(ref, a)
    return bet


def measure(bars):
    H = 84
    LONG, SHORT = 180, 6

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce")
            rng = pd.to_numeric(df["high"], errors="coerce") - pd.to_numeric(df["low"], errors="coerce")
            long_m = rng.rolling(LONG, min_periods=LONG).mean()
            short_m = rng.rolling(SHORT, min_periods=SHORT).mean()
            panic = (short_m >= 3.0 * long_m * (1 - 1e-4)) & (long_m > 0)
            panic_known = long_m.notna() & short_m.notna()
            regime_mr = df["regime"].astype(str).values == "mean_reversion"
            panic_v = np.where(panic_known.values, panic.values, regime_mr)
            fall_raw = _component(df, "fall", "last_history_value")
            fall_px = (close / close.shift(6) - 1.0) * 100.0
            fall_v = fall_raw.where(fall_raw.notna(), fall_px).values
            active = fc != 0
            n_active += int(active.sum())
            ok = active & panic_v & (fc > 0) & (fall_v < 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled OLS slope of 84-bar excess return (in usual moves) on 6-bar fall depth"
    thr = "confirm: slope > 0 with t >= 2, mean excess > 0, >= 30 cases; reject: slope < 0 with t <= -2, >= 30 cases"
    reading = ("Situation recomputed as mean(high-low) over the last 6 bars >= 3x its 180-bar mean within each window "
               "(the regime column where history is too short), side long on a negative 6-bar change; a case is a "
               "holding-period bet (forecast rise >= 2 points) in the mean_reversion regime, the first per 84-bar grid "
               "cell counted from each window's first row, cases without close[t+84] in the window dropped; the coin's "
               "drift and usual move are the mean and standard deviation of its 84-bar returns on that grid over all "
               "windows; the slope's t is the ordinary OLS t; fewer than 30 cases gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": None, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars of a 6-bar fall while the "
                           "6-bar mean bar range is at least 3x its 180-bar mean (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- criterion ----------
    depths, excess = [], []
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
        grid_rets = np.array(grid_rets)
        if len(grid_rets) < 2:
            continue
        mu = float(np.mean(grid_rets))
        sd = float(np.std(grid_rets, ddof=1))
        if not np.isfinite(sd) or sd <= 0:
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            c = pd.to_numeric(df["close"], errors="coerce").values
            reg = df["regime"].astype(str).values
            fall = _component(df, "fall", "last_history_value").values
            bet = _bets(fc) & (reg == "mean_reversion") & (fc > 0)
            seen = set()
            for i in np.nonzero(bet)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= len(c):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0 and np.isfinite(fall[i])):
                    continue
                r = c[i + H] / c[i] - 1.0
                depths.append(-float(fall[i]))
                excess.append((r - mu) / sd)

    x = np.array(depths, dtype=float)
    y = np.array(excess, dtype=float)
    n = int(len(x))
    slope = t = mean_ex = None
    if n >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else (float("inf") if res.slope > 0 else float("-inf"))
    if n > 0:
        mean_ex = float(np.mean(y))
    sup_pass = None if mean_ex is None else bool(mean_ex > 0)

    if n < 30:
        status = "not observable"
        decided = "Only %d cases, under the plan's minimum of 30." % n
    elif slope is None:
        status = "inconclusive"
        decided = "The slope could not be estimated (no spread in fall depth)."
    elif slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope is positive with t >= 2, the mean excess return is above 0, and there are at least 30 cases."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2, with at least 30 cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope t is >= 2 but the mean excess return is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t is None else {"name": "OLS slope t", "value": t},
            "threshold": thr,
        },
        "supporting_check": {"name": "mean excess return of the cases above 0", "value": mean_ex, "passed": sup_pass},
        "counts": {"cases": n},
        "decided_by": decided,
        "reading": reading,
    }
