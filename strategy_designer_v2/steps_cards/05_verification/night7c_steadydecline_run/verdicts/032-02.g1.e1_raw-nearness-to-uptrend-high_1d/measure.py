import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    LOOKBACK = 28
    FC = "forecast"
    RAW = "debug_info.components.high_prox.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0)
            prev = close.shift(LOOKBACK)
            ret28 = close / prev - 1.0
            computable = prev.notna() & close.notna()
            # Bars whose 28-bar-ago close falls in the unrecorded warm-up use the detector's own regime.
            if "regime" in df.columns:
                reg_trend = df["regime"].astype(str).eq("trending")
            else:
                reg_trend = pd.Series(False, index=df.index)
            situation = np.where(computable, ret28 > 0, reg_trend)
            situation = pd.Series(situation, index=df.index).astype(bool)
            # The graded proximity must exist on the bar: positive, at most 1.
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw_ok = raw.notna() & (raw > 0) & (raw <= 1.0 + 1e-9)
            else:
                raw_ok = pd.Series(False, index=df.index)
            active = fc != 0
            agree = active & situation & raw_ok & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "t of the OLS slope of excess 5-bar return on forecast (grid bars, forecast > 0)"
    threshold = "confirm: t >= 2 with forecast-weighted mean excess > 0; reject: t <= -2"
    reading_base = (
        "The situation is close above the close 28 bars before, recomputed from the window's prices, "
        "using the recorded regime on the first 28 bars of a window where that close is not recorded, "
        "with a recorded proximity in (0, 1] and a long forecast. The coin's mean 5-bar return is "
        "taken over the non-overlapping grid (positions 0, 5, 10, ...) of all its windows. Grid "
        "bars without a full 5-bar forward return inside their window are left out. The plan's "
        "fewer-than-100-cases rule is applied as the minimum count, giving 'not observable'."
    )

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars in situation on long side": n_agree},
            "decided_by": (
                f"Only {agreement:.1%} of the {n_active} active bars are long bars with a 28-bar "
                "return above 0 and a recorded proximity, below the 90% needed: the config does not "
                "do what the plan's Fidelity says."
            ),
            "reading": reading_base,
        }

    # ---------- 2. Criterion ----------
    xs, ys = [], []
    for coin, wins in bars.items():
        grid_rets = []
        cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                f = fc[i]
                if np.isfinite(f) and f > 0:
                    cases.append((f, r))
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for f, r in cases:
            xs.append(float(f))
            ys.append(r - mu)

    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    n_cases = int(len(x))

    slope = None
    t_val = None
    if n_cases >= 3 and np.var(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_val = float(res.slope / res.stderr) if res.stderr > 0 else (float("inf") * np.sign(res.slope) if res.slope != 0 else 0.0)
    wmean = float(np.sum(x * y) / np.sum(x)) if n_cases > 0 and np.sum(x) > 0 else None
    sup_pass = (wmean > 0) if wmean is not None else None

    counts = {"grid cases with forecast > 0": n_cases}

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with forecast > 0, fewer than the plan's minimum of 100."
    elif t_val is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed (no variation in the forecast), so neither confirm nor reject is met."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = f"The slope's t is {t_val:.2f} >= 2 and the forecast-weighted mean excess return is {wmean:.5f} > 0."
    elif t_val <= -2:
        status = "rejected"
        decided = f"The slope's t is {t_val:.2f} <= -2."
    elif t_val >= 2:
        status = "inconclusive"
        decided = f"The slope's t is {t_val:.2f} >= 2 but the forecast-weighted mean excess return is {wmean:.5f} <= 0."
    else:
        status = "inconclusive"
        decided = f"The slope's t is {t_val:.2f}, between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "t of OLS slope", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "forecast-weighted mean excess 5-bar return > 0",
            "value": wmean,
            "passed": None if sup_pass is None else bool(sup_pass),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
