import numpy as np
import pandas as pd


def measure(bars):
    BAND = 2.0
    MIN_CASE_DAYS = 30
    FALL_COL = "debug_info.components.prior_fall.last_history_value"
    EPS = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []      # (coin, day, ret, size)
    drift = {}

    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            all_rets.append(r1.dropna().values)
        allr = np.concatenate(all_rets) if all_rets else np.array([])
        drift[coin] = float(np.mean(allr)) if len(allr) else np.nan

        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            h = df["high"].astype(float)
            l = df["low"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)
            in_reg = (df["regime"].astype(str) == "mean_reversion")

            # up day: 1-bar return > 0
            up = c.pct_change()
            up_ok = (up > 0)
            up_ok = up_ok.where(up.notna(), in_reg)

            # wide: range / mean range of last 20 bars (current included) > 1
            rng = h - l
            mrng = rng.rolling(20, min_periods=20).mean()
            ratio = rng / mrng
            wide_ok = (ratio > 1.0)
            wide_ok = wide_ok.where(ratio.notna(), in_reg)

            # fall5: recorded raw value where present, else recomputed
            rr = c.pct_change()
            vol = rr.rolling(20, min_periods=20).std().shift(1)
            ret5 = c.shift(1) / c.shift(6) - 1.0
            fall_re = ret5 / (vol * np.sqrt(5.0))
            if FALL_COL in df.columns:
                fall = pd.to_numeric(df[FALL_COL], errors="coerce").combine_first(fall_re)
            else:
                fall = fall_re
            fall_ok = (fall <= -1.0 + EPS)
            fall_ok = fall_ok.where(fall.notna(), in_reg)

            # falling profile: 60-bar price evolution (percent) < -10
            pe = (c / c.shift(60) - 1.0) * 100.0
            prof_ok = (pe < -10.0)
            prof_ok = prof_ok.where(pe.notna(), in_reg)

            situ = up_ok.astype(bool) & wide_ok.astype(bool) & fall_ok.astype(bool) & prof_ok.astype(bool)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situ & (fc < 0)).sum())

            # ---------- cases: short bets of at least the band ----------
            fwd = c.shift(-1) / c - 1.0
            ref = 0.0
            days = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            for i in range(len(df)):
                f = fc.iloc[i]
                m = -f if f < 0 else 0.0
                if m == 0.0:
                    ref = 0.0
                    continue
                if m - ref >= BAND - EPS:
                    ref = m
                    if pd.notna(fwd.iloc[i]):
                        case_rows.append((coin, days.iloc[i], float(fwd.iloc[i]), m))
                else:
                    ref = min(ref, m)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean unusual next-day move on short cases (return minus coin drift, short direction)"
    thr = "confirm: mean > 0 with day-pooled t >= 2 on >= 30 case-days and check passes; reject: mean < 0 with t <= -2 on >= 30 case-days"
    reading = ("Cases are short bets per the holding-period rule (forecast magnitude rising >= 2 from its lowest level since the last bet, from 0 after flat); "
               "the t is cluster-robust with deviations summed per UTC day; the larger half is size above the median |forecast|, the smaller half at or below it; "
               "for the situation check the falling profile is 60-bar change in percent < -10 and conditions not computable from a window's prices fall back to the recorded regime.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "case-days": None},
            "decided_by": ("Fewer than 90% of active bars are short bars on an up, wide day after a 5-day fall of at least one usual move in a falling market "
                           f"(agreement {agreement:.3f})."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    if case_rows:
        cdf = pd.DataFrame(case_rows, columns=["coin", "day", "ret", "size"])
        cdf["drift"] = cdf["coin"].map(drift)
        cdf["x"] = -(cdf["ret"] - cdf["drift"])
        cdf = cdf.dropna(subset=["x"])
    else:
        cdf = pd.DataFrame(columns=["coin", "day", "ret", "size", "drift", "x"])

    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    mean_x = float(cdf["x"].mean()) if n_cases else None
    t_val = None
    if n_cases and n_days >= 2:
        dev = cdf["x"] - mean_x
        s = dev.groupby(cdf["day"]).sum().values
        var = (n_days / (n_days - 1.0)) * np.sum(s ** 2) / (n_cases ** 2)
        if var > 0:
            t_val = float(mean_x / np.sqrt(var))

    sup_val = None
    sup_pass = None
    if n_cases:
        med = float(cdf["size"].median())
        big = cdf.loc[cdf["size"] > med, "x"]
        small = cdf.loc[cdf["size"] <= med, "x"]
        if len(big) and len(small):
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    counts = {"case-days": n_days, "cases": n_cases, "active bars": int(n_active)}

    if n_days < MIN_CASE_DAYS:
        status = "not observable"
        decided = f"Fewer than 30 case-days ({n_days}), the plan's minimum count, so the data could not show the idea."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t could not be computed (no dispersion), so neither confirm nor reject is met."
    elif mean_x > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 on at least 30 case-days and the larger-size half beats the smaller-size half."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting check fails (larger-size half minus smaller-size half not above 0)."
    elif mean_x < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2 on at least 30 case-days: the next day rises more than the coin's drift."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2 on at least 30 case-days."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_x,
            "statistic": ({"name": "t of the mean, cases pooled by day", "value": t_val} if t_val is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean unusual move, larger-size half minus smaller-size half",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
