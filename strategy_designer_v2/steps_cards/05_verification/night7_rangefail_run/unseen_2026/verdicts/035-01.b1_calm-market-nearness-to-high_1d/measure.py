import numpy as np
import pandas as pd

NH_RAW = "debug_info.components.near_high.last_history_value"
NH_POST = "debug_info.components.near_high.post_pipeline_value"
OF_RAW = "debug_info.components.offset.last_history_value"
OF_POST = "debug_info.components.offset.post_pipeline_value"
H = 5


def _standardise(raw, window=60, min_periods=20):
    """Engine's standardise: x(t) * 10 / mean(|x| over the last `window` past values, t excluded), capped at +-20.

    Returns NaN where the window holds fewer than `min_periods` past values, so the caller can fall back to the
    recorded post_pipeline_value."""
    past_abs = raw.abs().shift(1)
    denom = past_abs.rolling(window, min_periods=min_periods).mean()
    out = raw * 10.0 / denom
    out = out.where(denom != 0, 0.0)
    out = out.where(denom.notna())
    return out.clip(-20, 20)


def _raw_near_high(df):
    """Recompute the raw component from prices: (close - max of the prior 20 closes) / that max / std of the last 20 daily returns."""
    c = df["close"].astype(float)
    prior_high = c.shift(1).rolling(20, min_periods=20).max()
    vol = c.pct_change().rolling(20, min_periods=20).std()
    return (c - prior_high) / prior_high / vol


def _clustered_slope(x, y, groups):
    """OLS of y on [1, x], with the standard error clustered by day (score contributions summed per day)."""
    X = np.column_stack([np.ones_like(x), x])
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    scores = pd.DataFrame(X * u[:, None]).groupby(np.asarray(groups)).sum().values
    G = scores.shape[0]
    meat = scores.T @ scores
    V = XtX_inv @ meat @ XtX_inv
    if G > 1:
        V = V * G / (G - 1)
    se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
    slope = float(beta[1])
    t = slope / se if (se is not None and np.isfinite(se) and se > 0) else np.nan
    return slope, t, G


def measure(bars):
    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].copy().reset_index(drop=True)
            if len(df) == 0 or "forecast" not in df:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            regime = df["regime"].astype(str) if "regime" in df else pd.Series([""] * len(df))
            nh_rec = pd.to_numeric(df[NH_RAW], errors="coerce") if NH_RAW in df else pd.Series(np.nan, index=df.index)
            of_rec = pd.to_numeric(df[OF_RAW], errors="coerce") if OF_RAW in df else pd.Series(np.nan, index=df.index)
            nh_post = pd.to_numeric(df[NH_POST], errors="coerce") if NH_POST in df else pd.Series(np.nan, index=df.index)
            of_post = pd.to_numeric(df[OF_POST], errors="coerce") if OF_POST in df else pd.Series(np.nan, index=df.index)

            # raw history: the recorded value where present, recomputed from prices elsewhere
            nh_raw = nh_rec.combine_first(_raw_near_high(df))
            of_const = of_rec.dropna().iloc[0] if of_rec.notna().any() else 1.0
            of_raw = of_rec.fillna(of_const)

            nh_std = _standardise(nh_raw).combine_first(nh_post)
            of_std = _standardise(of_raw).combine_first(of_post)
            expected = (nh_std + of_std) / 2.0  # equal weights, then clipped
            expected = expected.clip(-20, 20)

            # the plan's situation: a calm bar (not vetoed to chop) where the idea's component runs
            calm = (regime != "chop") & nh_rec.notna()
            active = fc.notna() & (fc != 0)
            agree = active & calm & expected.notna() & (np.sign(expected) == np.sign(fc))
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    main_name = "day-clustered slope of 5-bar excess return on forecast"
    threshold = "slope > 0 with t >= 2 confirms (with tercile difference > 0); t <= -2 rejects"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("no active bars to compare with the plan's situation" if n_active == 0 else
                           "fewer than 90 % of the active bars are calm bars where the forecast's sign matches the "
                           "sign of the rebuilt centred nearness-to-high (nearer than usual long, further short)"),
            "reading": "the calm situation is a bar whose regime is not 'chop' with near_high recorded; the expected "
                       "side is the sign of the mean of the rebuilt standardised near_high and offset.",
        }

    # ---------------- 2. criterion ----------------
    rows = []
    for coin in sorted(bars):
        drift_rets = []
        cases = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) <= H:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            nh = (pd.to_numeric(df[NH_RAW], errors="coerce").values if NH_RAW in df
                  else np.full(len(df), np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df) - H, H):
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                drift_rets.append(r)
                if np.isfinite(nh[i]) and np.isfinite(fc[i]):
                    cases.append((ts.iloc[i].strftime("%Y-%m-%d"), fc[i], r))
        if not drift_rets:
            continue
        drift = float(np.mean(drift_rets))
        for d, f, r in cases:
            rows.append((coin, d, f, r - drift))

    cases = pd.DataFrame(rows, columns=["coin", "day", "forecast", "excess"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}
    reading = ("Cases are the non-overlapping 5-bar grid bars (positions 0, 5, 10, ... of each window) with near_high "
               "recorded, excess return = 5-bar return minus the coin's mean 5-bar grid return over all its windows; "
               "'cases of one day summed together' is read as an OLS slope with standard errors clustered by day; "
               "terciles are three equal-count groups of the pooled cases ranked by forecast (ties by order).")

    if n_cases < 200 or n_days < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": "top-minus-bottom forecast tercile mean excess 5-bar return",
                                 "value": None, "passed": None},
            "counts": counts,
            "decided_by": "the plan's minimum of 200 grid cases on at least 100 distinct days is not reached",
            "reading": reading,
        }

    x = cases["forecast"].values.astype(float)
    y = cases["excess"].values.astype(float)
    if np.std(x) == 0:
        slope, t = float("nan"), float("nan")
    else:
        slope, t, _ = _clustered_slope(x, y, cases["day"].values)

    ranks = cases["forecast"].rank(method="first")
    terc = pd.qcut(ranks, 3, labels=[0, 1, 2])
    top = cases.loc[terc == 2, "excess"].mean()
    bot = cases.loc[terc == 0, "excess"].mean()
    tdiff = float(top - bot)
    sup_pass = bool(tdiff > 0)

    if np.isfinite(t) and slope > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "the slope is positive with t >= 2 and the top-minus-bottom tercile difference is above 0"
    elif np.isfinite(t) and slope < 0 and t <= -2:
        status = "rejected"
        decided = "the slope is negative with t <= -2"
    elif np.isfinite(t) and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the top-minus-bottom tercile difference is at or below 0"
    else:
        status = "inconclusive"
        decided = "the slope t lies between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name,
                         "value": float(slope) if np.isfinite(slope) else None,
                         "statistic": {"name": "day-clustered OLS slope t",
                                       "value": float(t) if np.isfinite(t) else None},
                         "threshold": threshold},
        "supporting_check": {"name": "top-minus-bottom forecast tercile mean excess 5-bar return",
                             "value": tdiff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
