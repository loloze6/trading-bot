import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.depth.last_history_value"
    STRAT_REGIME = "unknown"  # the only regime with a strategy in the config (the choppy profile)

    def to_time(s):
        if np.issubdtype(s.dtype, np.number):
            v = float(np.nanmax(np.abs(s.values))) if len(s) else 0.0
            unit = "s" if v < 1e11 else ("ms" if v < 1e14 else ("us" if v < 1e17 else "ns"))
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            situ = (reg == STRAT_REGIME) & raw.notna() & (raw < 0)
            agree = active & situ & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    reading = ("Choppy profile read from the recorded regime (the config's strategy regime 'unknown', since the "
               "detector's PriceEvolution component is not recorded), close below the 20-day high as raw depth < 0, "
               "expected side short (forecast < 0); slope t is OLS with intercept, CR1 cluster-robust by UTC day; "
               "the deepest third is the floor(n/3) cases with the most negative forecasts; the plan's minimum "
               "counts (100 cases, 60 days) are applied as 'not observable' when not reached.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of excess 3-bar forward return on forecast", "value": None,
                             "statistic": None, "threshold": "slope > 0 with clustered t >= 2 to confirm; < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"non-overlapping cases": None, "distinct days": None, "active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the {n_active} bars with a nonzero forecast are short bars in the "
                           "choppy profile with the close below its 20-day high, under the 90% required by the plan's Fidelity."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_grid = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = to_time(d["timestamp"])
            n = len(d)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_grid.append(r)
                if np.isfinite(fc[i]) and fc[i] != 0:
                    coin_cases.append((fc[i], r, ts.iloc[i].floor("D")))
        if len(coin_grid) == 0:
            continue
        drift = float(np.mean(coin_grid))
        for f, r, day in coin_cases:
            rows.append({"coin": coin, "f": float(f), "ex": r - drift, "day": day})

    cases = pd.DataFrame(rows, columns=["coin", "f", "ex", "day"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope = None
    t = None
    if n_cases >= 3 and cases["f"].var() > 0:
        X = np.column_stack([np.ones(n_cases), cases["f"].values])
        y = cases["ex"].values
        XtX_inv = np.linalg.inv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        meat = np.zeros((2, 2))
        codes = pd.factorize(cases["day"])[0]
        G = int(codes.max() + 1)
        for g in range(G):
            m = codes == g
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
        k = 2
        corr = (G / (G - 1)) * ((n_cases - 1) / (n_cases - k)) if G > 1 and n_cases > k else 1.0
        V = corr * XtX_inv @ meat @ XtX_inv
        se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
        slope = float(beta[1])
        t = float(slope / se) if np.isfinite(se) and se > 0 else None

    deep_mean = None
    sup_passed = None
    if n_cases >= 3:
        k3 = n_cases // 3
        srt = cases.sort_values("f", kind="mergesort")
        deep = srt.iloc[:k3]
        if len(deep) > 0:
            deep_mean = float(deep["ex"].mean())
            sup_passed = bool(deep_mean < 0)

    main = {"name": "slope of excess 3-bar forward return (minus coin's normal drift) on forecast, pooled, day-clustered",
            "value": slope,
            "statistic": {"name": "OLS t clustered by day", "value": t} if t is not None else None,
            "threshold": "confirm: slope > 0 with t >= 2 (and deepest third mean excess < 0); reject: slope < 0 with t <= -2; else inconclusive"}
    sup = {"name": "deepest third of forecasts: mean excess 3-bar return below 0",
           "value": deep_mean, "passed": sup_passed}
    counts = {"non-overlapping cases": n_cases, "distinct days": n_days}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"The plan's minimum of 100 non-overlapping cases on 60 distinct days is not reached "
                   f"({n_cases} cases on {n_days} days).")
    elif slope is None or t is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and t >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the deepest third's mean excess return is below 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the deepest third's mean excess return is not below 0 (inconclusive rule)."
    elif slope < 0 and t <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: deeper closes are followed by larger excess rises (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's |t| is below 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
