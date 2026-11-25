import numpy as np
import pandas as pd


def measure(bars):
    LOC_COL = "debug_info.components.below_mid.last_history_value"
    MIN_DAYS = 100

    def close_location(df):
        # CloseLocationInRange, reference "high": (high - close) / (high - low); >= 0.5 means close at/below mid-range
        hi = df["high"].astype(float)
        lo = df["low"].astype(float)
        cl = df["close"].astype(float)
        rng = hi - lo
        loc = (hi - cl) / rng.where(rng > 0)
        if LOC_COL in df.columns:
            rec = pd.to_numeric(df[LOC_COL], errors="coerce")
            loc = rec.where(rec.notna(), loc)
        return loc

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            loc = close_location(df)
            rng = (df["high"].astype(float) - df["low"].astype(float))
            short = rng.rolling(30, min_periods=30).mean()
            long_ = rng.rolling(90, min_periods=90).mean()
            rr = long_ / short.where(short > 0)
            rr_cond_prices = rr < 1.0
            # where 90 bars of in-window history are not available (warm-up not recorded),
            # fall back on the detector's own recorded decision
            rr_cond_regime = df["regime"].astype(str) == "mean_reversion"
            rr_cond = np.where(rr.notna(), rr_cond_prices, rr_cond_regime)
            loc_cond = (loc >= 0.5).fillna(False).values
            situ = rr_cond & loc_cond
            active = (fc != 0).values
            long_side = (fc > 0).values
            n_active += int(active.sum())
            n_agree += int((active & situ & long_side).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "forecast-weighted mean next-day return minus coin's mean daily return (bars with forecast > 0)"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; else inconclusive; fewer than 100 distinct days -> not observable"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "fewer than 90% of bars with a non-zero forecast are long bars where the 90/30 mean range ratio is below 1 and the close is in the lower half of the bar's range",
            "reading": "the 90/30 range ratio is recomputed from high-low inside each window where 90 bars exist, elsewhere the recorded regime stands for it; close location is the recorded raw value or (high-close)/(high-low).",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            cl = df["close"].astype(float)
            r = cl.shift(-1) / cl - 1.0
            all_rets.append(r.dropna().values)
            frames.append((df, r))
        if not all_rets:
            continue
        allr = np.concatenate(all_rets)
        if allr.size == 0:
            continue
        coin_mean = float(np.mean(allr))
        for df, r in frames:
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ts = pd.to_datetime(df["timestamp"], utc=True)
            m = (fc > 0) & r.notna() & fc.notna()
            if m.any():
                rows.append(pd.DataFrame({
                    "day": ts[m].dt.floor("D").values,
                    "f": fc[m].values.astype(float),
                    "x": (r[m] - coin_mean).values.astype(float),
                }))

    if rows:
        cases = pd.concat(rows, ignore_index=True)
    else:
        cases = pd.DataFrame({"day": [], "f": [], "x": []})

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    value = None
    tstat = None
    if n_cases > 0 and cases["f"].sum() > 0:
        sf = float(cases["f"].sum())
        value = float((cases["f"] * cases["x"]).sum() / sf)
        if n_days > 1:
            dev = cases["f"] * (cases["x"] - value)
            per_day = dev.groupby(cases["day"]).sum().values
            var = (n_days / (n_days - 1)) * float(np.sum(per_day ** 2)) / sf ** 2
            se = np.sqrt(var)
            tstat = float(value / se) if se > 0 else None

    counts = {"distinct days with a positive forecast": n_days, "bars with a positive forecast": n_cases}

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"only {n_days} distinct days with a positive forecast, fewer than the plan's minimum of 100."
    elif tstat is None:
        status = "inconclusive"
        decided = "the t could not be computed, so no confirm or reject rule is met."
    elif value > 0 and tstat >= 2:
        status = "confirmed"
        decided = "the forecast-weighted mean excess next-day return is above 0 with t >= 2 (confirm rule)."
    elif value < 0 and tstat <= -2:
        status = "rejected"
        decided = "the forecast-weighted mean excess next-day return is below 0 with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "the t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": value,
            "statistic": None if tstat is None else {"name": "t of the forecast-weighted mean, cases of one day summed", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": "every bar with forecast > 0 and a next close in the same window is a case, the coin's mean is the mean of all its in-window 1-bar returns, the t is the weighted mean over a standard error built from the forecast-weighted deviations summed per UTC day, and days are counted over these usable cases.",
    }
