import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    NARROW_RAW = "debug_info.components.narrow.last_history_value"
    NARROW_POST = "debug_info.components.narrow.post_pipeline_value"
    OFFSET_POST = "debug_info.components.offset.post_pipeline_value"

    def rebuild_post(raw):
        # standardise(window 60, min_periods 20) on the recorded raw values, bar t left out, then negate
        r = pd.Series(raw, dtype=float)
        denom = r.abs().shift(1).rolling(60, min_periods=20).mean()
        s = (r * 10.0 / denom).clip(-20, 20)
        s[(denom == 0) | denom.isna()] = 0.0
        return -s

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str)
            falling = regime == "unknown"  # not vetoed to chop: 60-bar price evolution below -10

            if NARROW_POST in df.columns:
                npost = pd.to_numeric(df[NARROW_POST], errors="coerce")
            else:
                npost = pd.Series(np.nan, index=df.index)
            if NARROW_RAW in df.columns:
                rebuilt = rebuild_post(pd.to_numeric(df[NARROW_RAW], errors="coerce").values)
                npost = npost.fillna(rebuilt)
            if OFFSET_POST in df.columns:
                opost = pd.to_numeric(df[OFFSET_POST], errors="coerce").fillna(10.0)
            else:
                opost = pd.Series(10.0, index=df.index)

            # narrower than usual: standardised ratio below the offset's +10 level
            narrow = (npost + opost) > 0
            situation = falling & narrow.fillna(False)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of 3-day forward return minus coin's normal drift on forecast"
    threshold = "confirm if slope t >= 2 and supporting check passes; reject if t <= -2; else inconclusive; at least 100 non-overlapping cases"
    supp_name = "mean 3-day excess return on grid bars with forecast > 0 above 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are falling-profile days narrower than usual with a long forecast: the config also takes positions (e.g. shorts on wider-than-usual days) outside the plan's situation.",
            "reading": "The falling profile is read from the recorded regime ('unknown' = not vetoed), a narrow day as the narrow component's standardised value (post_pipeline_value, rebuilt from last_history_value where missing) plus the offset being above 0, and the expected side is long.",
        }

    # ---------- 2. criterion ----------
    xs, ys, pos_ex = [], [], []
    for coin, wins in bars.items():
        grid_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append((c1 / c0 - 1.0, fc[i]))
        if not grid_rows:
            continue
        rets = np.array([g[0] for g in grid_rows])
        fcs = np.array([g[1] for g in grid_rows], dtype=float)
        drift = float(np.mean(rets))
        ok = np.isfinite(fcs) & (fcs != 0)
        ex = rets[ok] - drift
        xs.extend(fcs[ok].tolist())
        ys.extend(ex.tolist())
        pos_ex.extend(ex[fcs[ok] > 0].tolist())

    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)
    n_cases = int(len(xs))
    n_pos = int(len(pos_ex))

    slope, t = None, None
    if n_cases >= 3 and np.std(xs) > 0:
        res = stats.linregress(xs, ys)
        slope = float(res.slope)
        t = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    supp_val = float(np.mean(pos_ex)) if n_pos > 0 else None
    supp_pass = (supp_val > 0) if supp_val is not None else None

    counts = {"non-overlapping cases": n_cases, "cases with forecast > 0": n_pos}

    if n_cases < 100:
        status = "not observable"
        decided = f"Fewer than 100 non-overlapping cases ({n_cases})."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither confirm nor reject is met."
    elif t >= 2 and supp_pass is True:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the supporting check passes."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": supp_name, "value": supp_val, "passed": supp_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases from all coins are pooled in one regression, each coin's normal drift being the mean of its non-overlapping 3-bar returns over all its windows (all grid bars), and the plan's 'fewer than 100 non-overlapping cases' is applied as a minimum count giving 'not observable'.",
    }
