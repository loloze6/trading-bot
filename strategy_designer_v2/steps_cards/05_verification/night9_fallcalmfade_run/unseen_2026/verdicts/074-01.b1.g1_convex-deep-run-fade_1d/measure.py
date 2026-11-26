import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.run_depth.last_history_value"

    sit_total = 0
    sit_ok = 0
    cases = []  # (day, excess_short, weight, depth)

    # First pass: each coin's normal daily drift, its mean 1-bar return over all its windows.
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            c = df["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            lhv = df[LHV].astype(float) if LHV in df.columns else pd.Series(np.nan, index=df.index)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)

            # The bar that breaks the run: an up close right after a down close.
            up = close.diff() > 0
            prev_down = close.shift(1).diff() < 0
            computable_run = close.shift(2).notna()
            run_break = np.where(computable_run, up & prev_down, lhv.fillna(0) > 0)

            # The falling market: 60-bar price change below 0 where the window holds it, else the recorded regime.
            ch60 = close / close.shift(60) - 1.0
            falling = np.where(ch60.notna(), ch60 < 0, regime == "mean_reversion")

            situation = np.asarray(run_break, dtype=bool) & np.asarray(falling, dtype=bool)
            active = (fc != 0).values
            sit_total += int(active.sum())
            sit_ok += int((active & situation & (fc < 0).values).sum())

            # The cases: signal bars, with the next-day return inside the window.
            nxt = close.shift(-1) / close - 1.0
            day = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            for i in np.where((fc < 0).values)[0]:
                r = nxt.iloc[i]
                if not np.isfinite(r) or not np.isfinite(drift[coin]):
                    continue
                cases.append((day.iloc[i], -(r - drift[coin]), abs(fc.iloc[i]), lhv.iloc[i]))

    agreement = float(sit_ok / sit_total) if sit_total > 0 else 0.0
    passed_sit = sit_total > 0 and agreement >= 0.9
    threshold = "confirm: weighted mean > 0 with t >= 2 over >= 30 case-days and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 case-days"
    reading = ("Situation rebuilt from prices as an up close right after a down close (the raw depth > 0 on a window's first two bars) "
               "with the 60-bar price change below 0 (the recorded regime where 60 bars are not in the window); "
               "drift is each coin's mean 1-bar return over all its windows; t is cluster-by-day "
               "(weighted deviations summed per day); the deepest third is the top round(n/3) cases by raw depth, "
               "compared by unweighted mean excess over mean depth; fewer than 30 case-days is reported as not observable.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "weighted mean next-day short-side excess fall", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"case-days": None, "active bars": int(sit_total)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are short forecasts on run-breaking up days in a falling market.",
            "reading": reading,
        }

    cdf = pd.DataFrame(cases, columns=["day", "x", "w", "depth"])
    n_days = int(cdf["day"].nunique()) if len(cdf) else 0
    n_cases = int(len(cdf))

    mean_w = None
    t = None
    if n_cases > 0 and cdf["w"].sum() > 0:
        W = cdf["w"].sum()
        mean_w = float((cdf["x"] * cdf["w"]).sum() / W)
        D = (cdf["w"] * (cdf["x"] - mean_w)).groupby(cdf["day"]).sum().values
        if n_days > 1:
            var = (n_days / (n_days - 1)) * np.sum(D ** 2) / W ** 2
            se = np.sqrt(var)
            t = float(mean_w / se) if se > 0 else None

    # Supporting check.
    sup_val = None
    sup_pass = None
    sd = cdf.dropna(subset=["depth"]).sort_values("depth", ascending=False).reset_index(drop=True)
    if len(sd) >= 3:
        k = int(round(len(sd) / 3.0))
        k = min(max(k, 1), len(sd) - 1)
        deep = sd.iloc[:k]
        rest = sd.iloc[k:]
        md, mr = deep["depth"].mean(), rest["depth"].mean()
        if md != 0 and mr != 0:
            pd_ = deep["x"].mean() / md
            pr_ = rest["x"].mean() / mr
            sup_val = float(pd_ - pr_)
            sup_pass = bool(pd_ > pr_)

    counts = {"case-days": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} case-days, below the plan's minimum of 30 case-days."
    elif mean_w is None or t is None:
        status = "inconclusive"
        decided = "The t of the weighted mean could not be computed."
    elif mean_w > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Weighted mean short-side excess fall above 0 with t >= 2 over at least 30 case-days, and the deepest third gains more per unit of depth."
        else:
            status = "inconclusive"
            decided = "A confirming t with a failed supporting check is inconclusive."
    elif mean_w < 0 and t <= -2:
        status = "rejected"
        decided = "Weighted mean short-side excess fall below 0 with t <= -2 over at least 30 case-days."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "weighted mean next-day short-side excess fall",
                         "value": mean_w,
                         "statistic": {"name": "t of weighted mean, cases of one day pooled", "value": t} if t is not None else None,
                         "threshold": threshold},
        "supporting_check": {"name": "deepest third excess per unit depth minus the rest's",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
