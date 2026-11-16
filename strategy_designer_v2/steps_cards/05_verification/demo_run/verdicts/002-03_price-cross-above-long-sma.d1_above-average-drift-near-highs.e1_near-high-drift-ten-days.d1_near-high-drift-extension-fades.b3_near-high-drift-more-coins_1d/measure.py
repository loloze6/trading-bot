import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    MIN_MAIN = 100
    MIN_EXT = 30
    EXT_CUT = -5.0
    FC = "forecast"
    R_LH = "debug_info.components.range20.last_history_value"
    R_PP = "debug_info.components.range20.post_pipeline_value"
    E_LH = "debug_info.components.ext30.last_history_value"
    E_PP = "debug_info.components.ext30.post_pipeline_value"

    def col(df, name):
        if name in df.columns:
            return pd.to_numeric(df[name], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    def ols(x, y):
        x = np.asarray(x, float)
        y = np.asarray(y, float)
        m = np.isfinite(x) & np.isfinite(y)
        x, y = x[m], y[m]
        n = len(x)
        if n < 3 or np.var(x) == 0:
            return None, None, n
        res = stats.linregress(x, y)
        t = res.slope / res.stderr if res.stderr and res.stderr > 0 else None
        return float(res.slope), (float(t) if t is not None and np.isfinite(t) else None), n

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = col(df, FC)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            rpp = col(df, R_PP)
            epp = col(df, E_PP)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: close at or above its 200-day SMA (the detector's decision 'trending'),
            # with the extension part only ever a penalty (<= 0)
            in_situation = (regime == "trending") & rpp.notna() & epp.notna() & (epp <= 1e-12)
            # expected side: sign of the graded idea, range position minus graded extension
            expected = np.sign(0.5 * (rpp + epp))
            agree = active & in_situation & (np.sign(fc) == expected)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "OLS slope of coin-excess 10-bar forward return on forecast, trending-regime grid bars"
    main_thr = "slope t >= +2 confirms (with check), t <= -2 rejects; at least 100 independent cases"
    sup_name = "slope of excess 10-bar return on raw 30-day return, grid bars with ext30 post value <= -5"
    reading = ("Situation taken as the 'trending' regime (close >= 200-day SMA, which cannot be recomputed from "
               "windows shorter than 200 bars) with the expected side the sign of the graded idea "
               "(mean of range20 and ext30 post values, ext30 never positive); the coin's mean 10-bar return is "
               "the mean over all its grid bars in all windows and regimes; regressions are OLS with intercept; "
               "the 100 trending grid cases is treated as the plan's minimum count, while the 30 extended cases "
               "is part of the supporting check as the plan writes it (fewer gives inconclusive).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of active forecast bars lie in the trending regime (close >= 200-day SMA) "
                           "with the sign of range position minus graded extension, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = col(df, FC).values
            epp = col(df, E_PP).values
            elh = col(df, E_LH).values
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            for i in range(0, len(df) - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({"coin": coin, "ret": c1 / c0 - 1.0, "fc": fc[i], "epp": epp[i],
                             "elh": elh[i], "trend": regime[i] == "trending"})
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc", "epp", "elh", "trend"])
    if len(g):
        g["excess"] = g["ret"] - g.groupby("coin")["ret"].transform("mean")
    else:
        g["excess"] = []

    tr = g[g["trend"].astype(bool)] if len(g) else g
    tr_main = tr[np.isfinite(tr["fc"].astype(float)) & np.isfinite(tr["excess"].astype(float))] if len(tr) else tr
    slope, t, n_main = ols(tr_main["fc"], tr_main["excess"]) if len(tr_main) else (None, None, 0)

    ext = tr[(tr["epp"].astype(float) <= EXT_CUT)] if len(tr) else tr
    ext = ext[np.isfinite(ext["elh"].astype(float)) & np.isfinite(ext["excess"].astype(float))] if len(ext) else ext
    s_slope, s_t, n_ext = ols(ext["elh"], ext["excess"]) if len(ext) else (None, None, 0)
    sup_passed = bool(s_slope is not None and s_slope < 0 and n_ext >= MIN_EXT)

    counts = {"trending-regime grid cases": int(n_main), "extended cases": int(n_ext)}

    if n_main < MIN_MAIN:
        status = "not observable"
        decided = f"Only {n_main} trending-regime grid cases, fewer than the plan's minimum of 100."
    elif t is None:
        status = "inconclusive"
        decided = "The main slope's t could not be computed (no variation in the forecast)."
    elif t >= 2:
        if sup_passed:
            status = "confirmed"
            decided = ("Main slope t >= +2 with at least 100 cases, and the extended-run slope is negative "
                       "on at least 30 extended cases.")
        else:
            status = "inconclusive"
            decided = ("Main slope t >= +2 but the supporting check fails or has fewer than 30 extended cases.")
    elif t <= -2:
        status = "rejected"
        decided = "Main slope t <= -2 with at least 100 independent cases."
    else:
        status = "inconclusive"
        decided = "Main slope t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name,
                         "value": slope,
                         "statistic": ({"name": "OLS slope t", "value": t} if t is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": s_slope,
                             "passed": (sup_passed if s_slope is not None else (False if n_main >= MIN_MAIN else None))},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
