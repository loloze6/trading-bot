import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 7
    LHV = "debug_info.components.vsr.last_history_value"
    ALLOC = "postRebalance_current_allocation"
    POSTV = "postRebalance_total_value"

    def _sorted(df):
        if "timestamp" in df.columns:
            df = df.copy()
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            df = df.sort_values("timestamp")
        return df.reset_index(drop=True)

    data = {}
    for coin, wins in bars.items():
        data[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            data[coin][w] = _sorted(df)

    # ---------------- situation check ----------------
    # Situation: the coin's 14-day return scaled by its 20-day volatility; expected side = sign of that scaled return
    # (a rise -> long, a fall -> short). Raw value from last_history_value, recomputed from the window's prices
    # when the column is missing.
    n_active = 0
    n_agree = 0
    for coin, wins in data.items():
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # fallback recomputation inside the window only
            dr = close.pct_change()
            vol = dr.rolling(20, min_periods=20).std()
            ret14 = close / close.shift(14) - 1.0
            recomputed = ret14 / (vol * np.sqrt(14))
            raw = raw.where(raw.notna(), recomputed)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw != 0) & (np.sign(fc) == np.sign(raw))
            n_agree += int(ok.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "pooled mean of forecast x 7-bar excess return (non-overlapping cases)"
    thr = "confirm: mean > 0 with t >= 2 (and timing part > 0); reject: mean < 0 with t <= -2; at least 300 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"independent 7-bar cases": 0},
            "decided_by": "The forecast's sign does not follow the sign of the 14-day volatility-scaled return on at least 90% of active bars, so the config does not do what the plan's situation and outcome state.",
            "reading": "Active bars are bars with a non-zero forecast; a bar agrees when the forecast's sign equals the sign of the raw vsr value (recomputed from the window's prices where not recorded); bars with no computable raw value count as not agreeing.",
        }

    # ---------------- main measure ----------------
    cases = []  # (coin, forecast, fwd return)
    for coin, wins in data.items():
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 != 0 and np.isfinite(fc[t]):
                    cases.append((coin, float(fc[t]), float(c1 / c0 - 1.0)))

    prods = []
    if cases:
        cdf = pd.DataFrame(cases, columns=["coin", "fc", "r"])
        coin_mean = cdf.groupby("coin")["r"].mean()
        cdf["ex"] = cdf["r"] - cdf["coin"].map(coin_mean)
        prods = (cdf["fc"] * cdf["ex"]).values
    prods = np.asarray(prods, dtype=float)
    n_cases = int(len(prods))
    mean_prod = float(np.mean(prods)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = np.std(prods, ddof=1)
        if sd > 0:
            t_stat = float(mean_prod / (sd / np.sqrt(n_cases)))

    # ---------------- supporting check: timing part of the book ----------------
    # coin's mean daily return over all windows
    coin_mu = {}
    for coin, wins in data.items():
        rs = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce")
            rs.append((close / close.shift(1) - 1.0).dropna())
        allr = pd.concat(rs) if rs else pd.Series(dtype=float)
        coin_mu[coin] = float(allr.mean()) if len(allr) else np.nan

    rows = []
    for coin, wins in data.items():
        for w, df in wins.items():
            if POSTV not in df.columns or ALLOC not in df.columns:
                continue
            d = df.copy()
            d["day"] = d["timestamp"].dt.floor("D")
            daily = d.groupby("day").tail(1).reset_index(drop=True)
            v = pd.to_numeric(daily[POSTV], errors="coerce")
            a = pd.to_numeric(daily[ALLOC], errors="coerce")
            book_r = v / v.shift(1) - 1.0
            mkt = a.shift(1) * coin_mu[coin]
            tmp = pd.DataFrame({"day": daily["day"], "book": book_r, "mkt": mkt}).dropna()
            if len(tmp):
                tmp["coin"] = coin
                rows.append(tmp)

    timing = None
    book_mean = None
    if rows:
        allrows = pd.concat(rows, ignore_index=True)
        per_day = allrows.groupby("day")[["book", "mkt"]].mean()
        if len(per_day):
            book_mean = float(per_day["book"].mean())
            timing = float(book_mean - per_day["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------------- decision ----------------
    if n_cases < 300:
        status = "not observable"
        decided = f"Only {n_cases} independent 7-bar cases, below the plan's minimum of 300."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (no dispersion in the products), so no confirm or reject rule is met."
    elif t_stat >= 2 and mean_prod > 0:
        if timing_pass:
            status = "confirmed"
            decided = "The pooled mean of the product is positive with t >= 2 and the timing part of the book's mean daily return is above 0."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the timing part of the book's mean daily return is not above 0, which the plan calls inconclusive."
    elif t_stat <= -2 and mean_prod < 0:
        status = "rejected"
        decided = "The pooled mean of the product is negative with t <= -2: fading the two-week trend wins."
    else:
        status = "inconclusive"
        decided = "The t of the pooled mean lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_prod,
            "statistic": None if t_stat is None else {"name": "t of the mean", "value": t_stat},
            "threshold": thr,
        },
        "supporting_check": {
            "name": "timing part of the book's mean daily return (book mean minus position x coin mean daily return)",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": {"independent 7-bar cases": n_cases},
        "decided_by": decided,
        "reading": "The coin's mean 7-bar return is the mean over that coin's non-overlapping grid cases pooled across all its windows; the book's daily return is the change in postRebalance_total_value between consecutive day-end bars inside a window, averaged across coins per day, with the market part being the previous day's post-rebalance allocation times the coin's mean daily close return over all windows; the plan's 'fewer than 300 cases' is treated as a minimum count and reported as not observable.",
    }
