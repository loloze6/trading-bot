import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.below_high.last_history_value"

    def raw_from_prices(close):
        # (close - highest close of the prior 20 days) / that high / 20-day std of daily returns
        prior_high = close.shift(1).rolling(20, min_periods=20).max()
        vol = close.pct_change().rolling(20, min_periods=20).std()
        return (close - prior_high) / prior_high / vol

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), raw_from_prices(close))
            regime = df["regime"].astype(str)
            rising = (regime != "chop") & (regime != "nan")
            active = fc.notna() & (fc != 0)
            situation = rising & raw.notna() & (raw < 0)
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    main_name = "OLS slope of excess 5-bar return on forecast (forecast < 0, non-overlapping grid, pooled)"
    main_thr = "slope > 0 with t >= 2 confirms (with supporting check); slope < 0 with t <= -2 rejects"
    sup_name = "mean excess 5-bar return on grid bars with forecast <= -10 is below 0"
    reading = ("Rising market read as the recorded regime not being 'chop' (the profile veto), the raw distance taken "
               "from last_history_value or recomputed from closes where missing; each coin's mean 5-bar return is taken "
               "on the non-overlapping grid of all its windows; the plan's 'inconclusive' for too few cases is reported "
               "as 'not observable' per the workflow's rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with the close below its "
                           "prior 20-day high in a rising (non-chop) market, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                allr.append(r)
                rows.append((coin, fc[i], r))
        coin_rets[coin] = float(np.mean(allr)) if allr else np.nan

    if rows:
        d = pd.DataFrame(rows, columns=["coin", "fc", "r"])
        d["mu"] = d["coin"].map(coin_rets)
        d["ex"] = d["r"] - d["mu"]
        d = d.dropna(subset=["fc", "ex"])
        s = d[d["fc"] < 0]
    else:
        s = pd.DataFrame(columns=["fc", "ex"])

    n_neg = int(len(s))
    deep = s[s["fc"] <= -10] if n_neg else s
    n_deep = int(len(deep))
    counts = {"grid cases with forecast below 0": n_neg, "grid cases with forecast -10 or below": n_deep}

    slope = None
    tval = None
    if n_neg >= 3 and s["fc"].nunique() > 1:
        x = s["fc"].values.astype(float)
        y = s["ex"].values.astype(float)
        res = stats.linregress(x, y)
        slope = float(res.slope)
        tval = float(res.slope / res.stderr) if res.stderr and res.stderr > 0 else None

    deep_mean = float(deep["ex"].mean()) if n_deep > 0 else None
    sup_pass = (deep_mean < 0) if deep_mean is not None else None

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tval} if tval is not None else None),
            "threshold": main_thr}
    sup = {"name": sup_name, "value": deep_mean, "passed": sup_pass}

    if n_neg < 100:
        status = "not observable"
        decided = f"Only {n_neg} grid cases with a forecast below 0, fewer than the 100 the plan requires."
    elif n_deep < 30:
        status = "not observable"
        decided = f"Only {n_deep} grid cases with a forecast of -10 or below, fewer than the 30 the plan requires."
    elif slope is None or tval is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif slope > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 and the deep group's mean excess return is below 0 (confirm rule)."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the deep group's mean excess return is not below 0 (inconclusive rule)."
    elif slope < 0 and tval <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2: deeper below the high means a higher excess return (reject rule)."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
