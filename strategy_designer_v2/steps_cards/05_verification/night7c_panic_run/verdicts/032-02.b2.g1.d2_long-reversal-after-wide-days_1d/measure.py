import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.low_close_wide_day.last_history_value"
    H = 1

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            close = d["close"].astype(float)
            rng = high - low
            prior_mean = rng.shift(1).rolling(20, min_periods=20).mean()
            recomputed = (high - close) / prior_mean
            if LHV in d.columns:
                raw = pd.to_numeric(d[LHV], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            # The situation: the close sits below the day's high, so the graded
            # product (close-location share x range multiple) is positive.
            situation = (raw > 0) & (high > close)
            f = pd.to_numeric(d["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (f > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = agreement >= 0.9

    main_name = "next-bar excess return, top forecast tercile minus bottom tercile"
    thr = "difference > 0 with Welch t >= 2 confirms (with timing part > 0); difference < 0 with t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the close "
                           "sits below a day's high relative to the prior 20-day mean range, as the plan's "
                           "situation requires."),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    rows = []
    book_rows = []
    for coin, wins in bars.items():
        coin_rows = []
        coin_rets = []
        coin_book = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            fwd = close.shift(-H) / close - 1.0
            f = pd.to_numeric(d["forecast"], errors="coerce")
            coin_rets.append(fwd.dropna().values)
            coin_rows.append(pd.DataFrame({
                "coin": coin, "day": ts.dt.floor("D"), "forecast": f.values, "fwd": fwd.values
            }))
            # book daily returns inside the window
            v = pd.to_numeric(d["postRebalance_total_value"], errors="coerce")
            alloc = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce")
            day = ts.dt.floor("D")
            tmp = pd.DataFrame({"day": day, "v": v.values, "alloc": alloc.values})
            tmp = tmp.groupby("day", sort=True).last().reset_index()
            tmp["book_ret"] = tmp["v"] / tmp["v"].shift(1) - 1.0
            tmp["held"] = tmp["alloc"].shift(1)
            tmp = tmp.iloc[1:]
            tmp["coin"] = coin
            coin_book.append(tmp[["coin", "day", "book_ret", "held"]])
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        mu = float(np.mean(allr)) if allr.size else np.nan
        cr = pd.concat(coin_rows, ignore_index=True)
        cr = cr.dropna(subset=["forecast", "fwd"])
        cr["excess"] = cr["fwd"] - mu
        if len(cr) >= 3:
            rk = cr["forecast"].rank(method="first")
            cr["terc"] = pd.qcut(rk, 3, labels=[0, 1, 2]).astype(int)
        else:
            cr["terc"] = -1
        rows.append(cr)
        cb = pd.concat(coin_book, ignore_index=True)
        cb["market"] = cb["held"] * mu
        book_rows.append(cb)

    R = pd.concat(rows, ignore_index=True)
    top = R[R["terc"] == 2].groupby("day")["excess"].mean()
    bot = R[R["terc"] == 0].groupby("day")["excess"].mean()
    n_top, n_bot = int(len(top)), int(len(bot))

    B = pd.concat(book_rows, ignore_index=True)
    Bb = B.dropna(subset=["book_ret"]).groupby("day")["book_ret"].mean()
    Bm = B.dropna(subset=["market"]).groupby("day")["market"].mean()
    timing = float(Bb.mean() - Bm.mean()) if len(Bb) and len(Bm) else None
    sup_pass = None if timing is None else bool(timing > 0)

    diff = float(top.mean() - bot.mean()) if n_top and n_bot else None
    t = None
    if n_top >= 2 and n_bot >= 2:
        t = float(stats.ttest_ind(top.values, bot.values, equal_var=False).statistic)

    counts = {"days in top tercile": n_top, "days in bottom tercile": n_bot}

    if n_top < 300 or n_bot < 300:
        status = "not observable"
        decided = "Fewer than 300 days in a tercile (top %d, bottom %d), below the plan's minimum." % (n_top, n_bot)
    elif t is None or diff is None or not np.isfinite(t):
        status = "inconclusive"
        decided = "The Welch t could not be computed, so neither the confirm nor the reject rule is met."
    elif diff > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Top-minus-bottom difference positive with t >= 2 and timing part above 0."
    elif diff < 0 and t <= -2:
        status = "rejected"
        decided = "Top-minus-bottom difference negative with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the timing part is at or below 0 (or the difference is not positive)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": diff,
                         "statistic": None if t is None else {"name": "Welch t", "value": t},
                         "threshold": thr},
        "supporting_check": {"name": "book mean daily return minus market-rise gain (timing part)",
                             "value": timing, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Terciles are equal-count thirds of each coin's bars ranked by forecast with ties broken by "
                    "time order, every bar is a 1-day case, cases of one UTC day are averaged per tercile before "
                    "Welch's t, and the plan's 300-day minimum per tercile, when unmet, gives 'not observable'."),
    }
