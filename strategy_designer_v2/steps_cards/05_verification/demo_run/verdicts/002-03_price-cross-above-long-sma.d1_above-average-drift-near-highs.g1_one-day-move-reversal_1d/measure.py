import numpy as np
import pandas as pd


def measure(bars):
    COMP = "debug_info.components.vsr.last_history_value"
    MIN_ACTIVE = 1000

    # ---------- 1. Situation check ----------
    # Situation: a one-day move, scaled by the usual daily move.
    # Expected side: long after a fall, short after a rise, so the forecast sign should be the opposite of the move's sign.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # raw component value (1-day return / 20-day std of 1-day returns), fallback to the price move
            if COMP in df.columns:
                raw = pd.to_numeric(df[COMP], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            ret1 = close / close.shift(1) - 1.0
            move = raw.where(raw.notna(), ret1)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & move.notna() & (move != 0) & (np.sign(fc) == -np.sign(move))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Situation bars are those with a non-zero recorded raw vsr value (the one-day move over the 20-day "
               "std, price return used where it is missing), with the expected side being the opposite sign of that "
               "move; the slope is plain OLS with an intercept on every in-window bar with a next close (horizon 1, "
               "so the non-overlapping grid is every bar), the count is bars with a non-zero forecast in that "
               "regression, and the timing gain uses per-coin daily returns of postRebalance_total_value averaged "
               "across coins by day.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "OLS slope of next-bar excess return on forecast", "value": None,
                             "statistic": None, "threshold": "slope t >= 2 confirms, <= -2 rejects"},
            "supporting_check": None,
            "counts": {"bars with a non-zero forecast": int(n_active)},
            "decided_by": ("The plan expects a long after a down day and a short after an up day, but fewer than "
                           "90% of the active bars have a forecast opposite in sign to the day's volatility-scaled move."),
            "reading": reading,
        }

    # ---------- 2. Coin mean daily return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            df = df.sort_values("timestamp")
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            r = c[1:] / c[:-1] - 1.0
            rs.append(r[np.isfinite(r)])
        allr = np.concatenate(rs) if rs else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- 3. Main measure: pooled OLS slope ----------
    xs, ys = [], []
    book_rows = []
    for coin, wins in bars.items():
        mu = coin_mean.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            nxt = c[1:] / c[:-1] - 1.0
            ex = nxt - mu
            ff = f[:-1]
            m = np.isfinite(ex) & np.isfinite(ff)
            xs.append(ff[m])
            ys.append(ex[m])

            # book daily returns (value after rebalance and fee, last bar of each day)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            v = pd.to_numeric(df["postRebalance_total_value"], errors="coerce")
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            d = pd.DataFrame({"day": ts.dt.floor("D"), "v": v, "pos": pos})
            d = d.groupby("day", sort=True).last()
            if len(d) < 2:
                continue
            br = d["v"] / d["v"].shift(1) - 1.0
            mg = d["pos"].shift(1) * mu
            tmp = pd.DataFrame({"day": d.index[1:], "coin": coin,
                                "book": br.to_numpy()[1:], "mkt": mg.to_numpy()[1:]})
            book_rows.append(tmp)

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n_bars = int(len(x))
    n_nonzero = int(np.sum(x != 0)) if n_bars else 0

    slope, t_slope = None, None
    if n_bars >= 3 and np.var(x) > 0:
        xm = x - x.mean()
        ym = y - y.mean()
        sxx = float(np.sum(xm ** 2))
        b = float(np.sum(xm * ym) / sxx)
        a = float(y.mean() - b * x.mean())
        resid = y - (a + b * x)
        s2 = float(np.sum(resid ** 2) / (n_bars - 2))
        se = np.sqrt(s2 / sxx) if s2 > 0 else np.nan
        slope = b
        t_slope = float(b / se) if np.isfinite(se) and se > 0 else None

    # ---------- 4. Supporting check: timing gain ----------
    timing = None
    if book_rows:
        bk = pd.concat(book_rows, ignore_index=True)
        bk = bk.dropna(subset=["book", "mkt"])
        if len(bk):
            daily = bk.groupby("day")[["book", "mkt"]].mean()
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    counts = {"bars with a non-zero forecast": n_nonzero, "bars in the regression": n_bars}

    main = {"name": "OLS slope of next-bar excess return on forecast, pooled",
            "value": slope,
            "statistic": {"name": "OLS slope t", "value": t_slope} if t_slope is not None else None,
            "threshold": "slope t >= 2 (with positive timing gain) confirms; slope t <= -2 rejects"}
    sup = {"name": "book timing gain before costs (mean daily)", "value": timing, "passed": timing_pass}

    # ---------- 5. Decision ----------
    if n_nonzero < MIN_ACTIVE or t_slope is None:
        status = "not observable"
        decided = (f"Only {n_nonzero} bars with a non-zero forecast, fewer than the required {MIN_ACTIVE}."
                   if n_nonzero < MIN_ACTIVE else "The slope's t-statistic could not be computed.")
    elif t_slope >= 2 and timing_pass:
        status = "confirmed"
        decided = "The slope t is 2 or more and the book's timing gain is positive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less: next-day moves continue in the direction of the day's move."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope t is 2 or more but the book's timing gain is zero or below."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
