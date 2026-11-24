import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.run14.last_history_value"
    H = 2

    def recompute_raw(df):
        # 14-day simple return over the std of the last 20 daily returns (sign is what matters)
        c = df["close"].astype(float)
        ret14 = c / c.shift(14) - 1.0
        vol = c.pct_change().rolling(20).std()
        return ret14 / vol

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    cases = []  # (coin, date, forecast, r2)
    coin_mu = {}

    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            raw_rec = (pd.to_numeric(df[LHV], errors="coerce") if LHV in df.columns
                       else pd.Series(np.nan, index=df.index))
            raw = raw_rec.where(raw_rec.notna(), recompute_raw(df)).values
            friday = (ts.dt.weekday == 4).values  # daily bar opening Friday closes at Friday's close; next bar is Saturday

            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            ok = active & friday & np.isfinite(raw) & (np.sign(fc) == np.sign(raw))
            n_agree += int(ok.sum())

            # coin's 2-day returns on the non-overlapping grid of each window
            n = len(df)
            for i in range(0, n - H, H):
                if close[i] > 0 and np.isfinite(close[i]) and np.isfinite(close[i + H]):
                    grid_rets.append(close[i + H] / close[i] - 1.0)

            # Friday-close cases (regime trending)
            reg = df["regime"].astype(str).values
            for i in range(n - H):
                if reg[i] == "trending" and np.isfinite(fc[i]) and close[i] > 0 \
                        and np.isfinite(close[i + H]):
                    cases.append((coin, ts.iloc[i].normalize(), float(fc[i]),
                                  close[i + H] / close[i] - 1.0))
        coin_mu[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = agreement >= 0.9
    sit = {"agreement": float(agreement), "passed": bool(passed)}

    main_name = "mean position-weighted unusual weekend move (forecast/10 x (2-day return - coin mean 2-day return))"
    thr = "confirm: mean > 0 with t >= 2 over >= 100 distinct Fridays and size check > 0; reject: mean < 0 with t <= -2 over >= 100 distinct Fridays"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on its side": int(n_agree)},
            "decided_by": "fewer than 90% of the active bars are Friday-close bars whose forecast sign follows the sign of the 14-day volatility-scaled return, as the plan's Fidelity requires",
            "reading": "the situation is a bar opening on Friday UTC (next bar Saturday) with the expected side the sign of the raw scaled 14-day return (recorded, else recomputed from prices).",
        }

    # ---------- 2. criterion ----------
    df = pd.DataFrame(cases, columns=["coin", "date", "f", "r2"])
    if len(df):
        df["mu"] = df["coin"].map(coin_mu)
        df = df.dropna(subset=["f", "r2", "mu"])
    n_cases = int(len(df))
    n_days = int(df["date"].nunique()) if n_cases else 0

    mean_w = None
    t = None
    if n_cases > 0:
        df["unusual"] = df["r2"] - df["mu"]
        df["x"] = df["f"] / 10.0 * df["unusual"]
        m = float(df["x"].mean())
        mean_w = m
        if n_days > 1:
            d = (df["x"] - m).groupby(df["date"]).sum().values
            var = (d ** 2).sum() * n_days / (n_days - 1)
            se = np.sqrt(var) / n_cases
            t = float(m / se) if se > 0 else None

    diff = None
    sup_pass = None
    if n_cases > 0:
        af = df["f"].abs()
        med = af.median()
        dirmove = np.sign(df["f"]) * df["unusual"]
        up = dirmove[af > med]
        lo = dirmove[af <= med]
        if len(up) and len(lo):
            diff = float(up.mean() - lo.mean())
            sup_pass = bool(diff > 0)

    counts = {"distinct Fridays": n_days, "Friday cases (coin x Friday)": n_cases}

    if n_days < 100:
        status = "not observable"
        decided = f"only {n_days} distinct Fridays with cases, below the plan's minimum of 100."
    elif mean_w is not None and t is not None and mean_w > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "the mean weighted unusual move is above 0 with t >= 2 over at least 100 distinct Fridays, and the size check's difference is above 0."
    elif mean_w is not None and t is not None and mean_w < 0 and t <= -2:
        status = "rejected"
        decided = "the mean weighted unusual move is below 0 with t <= -2 over at least 100 distinct Fridays."
    else:
        status = "inconclusive"
        if t is not None and t >= 2 and mean_w > 0:
            decided = "t >= 2 but the size check (upper minus lower half of |forecast|) does not pass, which the plan calls inconclusive."
        else:
            decided = "|t| < 2 (or t undefined), which neither confirms nor rejects."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {
            "name": main_name,
            "value": mean_w,
            "statistic": ({"name": "t of the mean, cases of one Friday summed across coins", "value": t}
                          if t is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean unusual move in forecast direction, upper minus lower half of |forecast|",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "All regime-'trending' bars with a close two bars later in the same window are cases (forecast 0 included, weighing 0), the coin's mean 2-day return is taken on the non-overlapping 0,2,4,... grid of all its windows pooled, and the median split puts |forecast| above the median in the upper half and the rest in the lower half.",
    }
