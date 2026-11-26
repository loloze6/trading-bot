import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.vol_growth.last_history_value"
    PPV = "debug_info.components.vol_growth.post_pipeline_value"
    H = 20
    MIN_CASES = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            ret20 = (close / close.shift(20) - 1.0) * 100.0
            ret60 = (close / close.shift(60) - 1.0) * 100.0
            m_recent = vol.rolling(30).mean()
            m_before = vol.shift(30).rolling(30).mean()
            with np.errstate(divide="ignore", invalid="ignore"):
                vr_re = np.log(m_recent / m_before)
            lhv = df[LHV].astype(float) if LHV in df.columns else pd.Series(np.nan, index=df.index)
            ppv = df[PPV].astype(float) if PPV in df.columns else pd.Series(np.nan, index=df.index)
            for i in range(len(df)):
                f = fc.iloc[i]
                if pd.isna(f) or f == 0:
                    continue
                n_active += 1
                in_mr = regime.iloc[i] == "mean_reversion"
                r20 = ret20.iloc[i]
                c20 = (r20 < -10.0) if not pd.isna(r20) else in_mr
                r60 = ret60.iloc[i]
                c60 = (r60 < -10.0) if not pd.isna(r60) else in_mr
                if not (c20 and c60):
                    continue
                raw = lhv.iloc[i]
                if pd.isna(raw):
                    raw = vr_re.iloc[i]
                if pd.isna(raw) or not np.isfinite(raw):
                    raw = ppv.iloc[i]
                if pd.isna(raw) or raw == 0:
                    continue
                if np.sign(raw) == np.sign(f):
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast/10 x (20-bar forward return - coin mean 20-bar return) on grid cases"
    threshold = "mean > 0 with t >= 2 (confirm), mean < 0 with t <= -2 (reject), from at least 30 cases"
    reading = ("Situation taken as price-computed 20-day return < -10 % and 60-day return < -10 % (falling profile), "
               "falling back to regime == mean_reversion where a window lacks the history, with the expected side the sign "
               "of the raw log volume ratio; the coin's mean 20-bar return is taken over all windows' non-overlapping grid "
               "bars, the t is the day-clustered t of the case mean (per-day summed deviations), and fewer than 30 cases "
               "gives 'not observable' as the minimum-count rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases with a non-zero forecast": None},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars with a 20-day return below -10 % "
                           "inside the falling profile with the forecast's sign equal to the volume growth's sign."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin mean 20-bar return over all windows (non-overlapping grid)
    coin_mean = {}
    grid_data = []
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                if np.isnan(close[i]) or np.isnan(close[i + H]) or close[i] == 0:
                    continue
                r = close[i + H] / close[i] - 1.0
                all_rets.append(r)
                if not np.isnan(fc[i]) and fc[i] != 0:
                    grid_data.append((coin, ts.iloc[i].normalize(), fc[i], r))
        coin_mean[coin] = float(np.mean(all_rets)) if all_rets else np.nan

    vals, days = [], []
    for coin, day, f, r in grid_data:
        mu = coin_mean.get(coin, np.nan)
        if np.isnan(mu):
            continue
        vals.append(f / 10.0 * (r - mu))
        days.append(day)
    n = len(vals)
    vals = np.array(vals, dtype=float)
    n_days = int(len(set(days)))

    mean_v = float(vals.mean()) if n > 0 else None
    t_val = None
    if n > 0:
        s = pd.DataFrame({"d": days, "v": vals}).groupby("d")["v"].agg(["sum", "count"])
        D = len(s)
        if D > 1:
            resid = s["sum"].values - s["count"].values * mean_v
            var = (D / (D - 1)) * np.sum(resid ** 2)
            se = np.sqrt(var) / n
            if se > 0:
                t_val = float(mean_v / se)

    counts = {"grid cases with a non-zero forecast": int(n), "days": n_days}
    stat = {"name": "t of the mean, cases of one day pooled", "value": t_val} if t_val is not None else None
    mm = {"name": main_name, "value": mean_v, "statistic": stat, "threshold": threshold}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} grid cases with a non-zero forecast, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed (fewer than two days or zero spread), so neither confirm nor reject is met."
    elif mean_v > 0 and t_val >= 2:
        status = "confirmed"
        decided = "The mean is above 0 with t >= 2, from at least 30 cases (confirm rule)."
    elif mean_v < 0 and t_val <= -2:
        status = "rejected"
        decided = "The mean is below 0 with t <= -2, from at least 30 cases (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": mm,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
