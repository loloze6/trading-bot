import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_move.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp") if "timestamp" in df.columns else df
            close = pd.to_numeric(df["close"], errors="coerce")
            r = close.pct_change(1)
            vol = r.rolling(24).std()
            raw_re = r / vol.replace(0, np.nan)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), raw_re)
            else:
                raw = raw_re
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            # expected side: opposite to the move (after an up hour short, after a down hour long)
            agree = active & raw.notna() & (raw != 0) & (np.sign(fc) == -np.sign(raw))
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"bars of nonzero forecast": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast have the sign opposite to the last "
                          "volatility-scaled 1-hour move, as the plan's reversal situation requires.",
            "reading": "Situation taken as every bar with a nonzero raw value, expected side the opposite of the raw move's sign.",
        }

    # ---------- 2. main measure: pooled OLS slope of next-hour excess return on forecast ----------
    xs, ys = [], []
    # book pieces
    book_rows = []  # (date, coin, book_ret, mean_alloc)
    coin_mu_daily = {}
    for coin, wins in bars.items():
        coin_fr = []
        per_win = []
        daily_rets = []
        for w, df in wins.items():
            df = df.copy()
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fr = close.shift(-1) / close - 1.0
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            alloc = pd.to_numeric(df[ALLOC], errors="coerce") if ALLOC in df.columns else pd.Series(np.nan, index=df.index)
            coin_fr.append(fr)
            per_win.append((df, fr, fc, alloc))
            # coin daily returns from closes at each day's last bar
            dates = df["timestamp"].dt.floor("D")
            dclose = close.groupby(dates).last()
            daily_rets.append(dclose.pct_change().dropna())
        allfr = pd.concat(coin_fr).dropna()
        mu_h = float(allfr.mean()) if len(allfr) else 0.0
        dr = pd.concat(daily_rets) if daily_rets else pd.Series(dtype=float)
        mu_d = float(dr.mean()) if len(dr) else 0.0
        coin_mu_daily[coin] = mu_d
        for df, fr, fc, alloc in per_win:
            y = fr - mu_h
            m = y.notna() & fc.notna()
            xs.append(fc[m].values)
            ys.append(y[m].values)
            # book before costs: gain of bar t = alloc[t] * fr[t], assigned to the day of bar t+1
            g = alloc * fr
            day_next = df["timestamp"].shift(-1).dt.floor("D")
            mm = g.notna() & day_next.notna()
            tmp = pd.DataFrame({"day": day_next[mm], "g": g[mm], "a": alloc[mm]})
            if len(tmp):
                agg = tmp.groupby("day").agg(
                    ret=("g", lambda s: float(np.prod(1.0 + s.values) - 1.0)),
                    a=("a", "mean"))
                for d, row in agg.iterrows():
                    book_rows.append((d, coin, row["ret"], row["a"] * mu_d))

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n = len(x)
    slope, tstat = None, None
    if n > 2 and np.var(x) > 0:
        xm, ym = x.mean(), y.mean()
        sxx = np.sum((x - xm) ** 2)
        slope = float(np.sum((x - xm) * (y - ym)) / sxx)
        intercept = ym - slope * xm
        resid = y - intercept - slope * x
        s2 = np.sum(resid ** 2) / (n - 2)
        se = np.sqrt(s2 / sxx)
        tstat = float(slope / se) if se > 0 else None

    # ---------- supporting check ----------
    sup_val = None
    if book_rows:
        bd = pd.DataFrame(book_rows, columns=["day", "coin", "ret", "mkt"])
        daily = bd.groupby("day")[["ret", "mkt"]].mean()
        sup_val = float(daily["ret"].mean() - daily["mkt"].mean())
    sup_pass = None if sup_val is None else bool(sup_val > 0)

    counts = {"bars of nonzero forecast": int(n_active), "bars in the regression": int(n)}

    if n_active < 10000:
        status = "not observable"
        decided = "Fewer than 10,000 bars of nonzero forecast, the plan's minimum count, so the data cannot show the idea."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is at least 2 and the book's mean daily return before costs minus its market gain is above 0."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: the next hour follows the move instead of reversing it."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "pooled OLS slope of next-hour excess return on forecast",
            "value": slope,
            "statistic": None if tstat is None else {"name": "OLS slope t", "value": tstat},
            "threshold": "t >= 2 (with the check) confirms; t <= -2 rejects",
        },
        "supporting_check": {
            "name": "book mean daily return before costs minus market-rise gain",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "The slope is an OLS with intercept and classic standard errors over all bars (including zero forecasts), "
                   "the book before costs is rebuilt from the held allocation times the next-hour return compounded per UTC day "
                   "and averaged over coins, its market gain is the day's mean allocation times the coin's mean daily return, "
                   "and the plan's 10,000-bar minimum is applied as 'not observable'.",
    }
