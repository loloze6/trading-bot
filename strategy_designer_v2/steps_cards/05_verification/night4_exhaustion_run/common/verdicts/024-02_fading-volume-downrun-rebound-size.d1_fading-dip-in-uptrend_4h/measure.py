import numpy as np
import pandas as pd


def measure(bars):
    H = 18
    BAND = 2.0
    MIN_CASES = 30
    RISE_COL = "debug_info.components.rise.last_history_value"

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            vol = df["volume"].astype(float).values
            fc = df["forecast"].astype(float).values
            n = len(df)

            # rise30: 180-bar return, from the recorded component (same definition) or recomputed from prices
            rise = np.full(n, np.nan)
            if RISE_COL in df.columns:
                rise = df[RISE_COL].astype(float).values.copy()
            for t in range(n):
                if np.isnan(rise[t]) and t >= 180 and close[t - 180] > 0:
                    rise[t] = close[t] / close[t - 180] - 1.0

            # fade: current unbroken down-streak of closes (>= 2 falling bars, at most 180),
            # negated slope of volume over the streak's bars > 0
            streak = np.zeros(n, dtype=int)
            for t in range(1, n):
                if close[t] < close[t - 1]:
                    streak[t] = min(streak[t - 1] + 1, 180)
            fade = np.full(n, np.nan)
            for t in range(n):
                L = streak[t]
                if L >= 2:
                    v = vol[t - L + 1:t + 1]
                    x = np.arange(L, dtype=float)
                    xm = x - x.mean()
                    slope = np.sum(xm * (v - v.mean())) / np.sum(xm * xm)
                    fade[t] = -slope

            for t in range(n):
                f = fc[t]
                if np.isnan(f) or f == 0:
                    continue
                n_active += 1
                in_sit = (not np.isnan(rise[t]) and rise[t] > 0
                          and streak[t] >= 2 and not np.isnan(fade[t]) and fade[t] > 0)
                if in_sit and f > 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)
    situation = {"agreement": agreement, "passed": passed}

    mm_name = "forecast-weighted mean 18-bar excess return over normal drift, per bet, pooled"
    mm_thr = "positive with t >= 2 over at least 30 cases to confirm; negative with t <= -2 over at least 30 cases to reject"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation,
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": mm_thr},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": "fewer than 90% of the bars with a non-zero forecast are long bars of the plan's situation "
                          "(180-bar return above 0 and a down-streak of at least 2 bars with fading volume).",
            "reading": "none",
        }

    # ---------------- 2. main measure ----------------
    # normal drift per coin: mean 18-bar return on the non-overlapping grid of all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for t in range(0, len(c) - H, H):
                rets.append(c[t + H] / c[t] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    xs, ws = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            n = len(c)
            # bets: rise of the forecast on its side of at least the band from its lowest level since last bet
            bets = []
            side = 0
            base = 0.0
            for t in range(n):
                f = fc[t]
                s = int(np.sign(f))
                if s == 0:
                    side, base = 0, 0.0
                    continue
                if s != side:
                    side, base = s, 0.0
                a = abs(f)
                if a - base >= BAND:
                    bets.append((t, s, a))
                    base = a
                else:
                    base = min(base, a)
            seen = set()
            for t, s, a in bets:
                cell = t // H
                if cell in seen:
                    continue
                seen.add(cell)
                if t + H >= n or np.isnan(drift[coin]):
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                xs.append(s * (r - drift[coin]))
                ws.append(a)

    xs = np.array(xs, dtype=float)
    ws = np.array(ws, dtype=float)
    n_cases = int(len(xs))
    mval, tval = None, None
    if n_cases >= 2 and ws.sum() > 0:
        m = float(np.sum(ws * xs) / np.sum(ws))
        se = np.sqrt(np.sum(ws ** 2 * (xs - m) ** 2) * n_cases / (n_cases - 1)) / np.sum(ws)
        mval = m
        tval = float(m / se) if se > 0 else None
    elif n_cases == 1:
        mval = float(xs[0])

    # ---------------- 3. supporting check: timing gain ----------------
    coin_mu = {}
    day_rows = []
    for coin, wins in bars.items():
        all_daily = []
        per_win = []
        for w, df in wins.items():
            d = df.copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d["date"] = d["ts"].dt.floor("D")
            d = d.reset_index(drop=True)
            last = d.groupby("date").tail(1)
            pv = last["postRebalance_total_value"].astype(float).values
            cl = last["close"].astype(float).values
            dates = last["date"].values
            alloc = d["postRebalance_current_allocation"].astype(float).values
            bar_date = d["date"].values
            # position held during each day: mean of allocations held over bars whose return ends in that day
            pos_by_day = {}
            for t in range(len(d) - 1):
                pos_by_day.setdefault(bar_date[t + 1], []).append(alloc[t])
            for i in range(1, len(last)):
                br = pv[i] / pv[i - 1] - 1.0
                cr = cl[i] / cl[i - 1] - 1.0
                all_daily.append(cr)
                p = pos_by_day.get(dates[i], [])
                pos = float(np.nanmean(p)) if len(p) else np.nan
                per_win.append((w, dates[i], br, pos))
        coin_mu[coin] = float(np.nanmean(all_daily)) if all_daily else np.nan
        for w, dt, br, pos in per_win:
            day_rows.append((coin, w, dt, br, pos * coin_mu[coin]))

    timing = None
    if day_rows:
        dd = pd.DataFrame(day_rows, columns=["coin", "w", "date", "book", "mkt"])
        g = dd.groupby(["w", "date"])
        book_mean = g["book"].mean().mean()
        mkt_mean = g["mkt"].mean().mean()
        if np.isfinite(book_mean) and np.isfinite(mkt_mean):
            timing = float(book_mean - mkt_mean)
    sup_passed = None if timing is None else bool(timing > 0)

    # ---------------- 4. decision ----------------
    if n_cases < MIN_CASES or tval is None:
        status = "not observable"
        decided = f"only {n_cases} independent cases, below the plan's minimum of 30."
    elif mval > 0 and tval >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "weighted mean excess return positive with t >= 2 over at least 30 cases, and timing gain positive."
        else:
            status = "inconclusive"
            decided = "a confirming t with a timing gain of 0 or below is inconclusive."
    elif mval < 0 and tval <= -2:
        status = "rejected"
        decided = "weighted mean excess return negative with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2 (or sign and t disagree) over at least 30 cases."

    return {
        "status": status,
        "situation_check": situation,
        "main_measure": {
            "name": mm_name,
            "value": mval,
            "statistic": None if tval is None else {"name": "t of the weighted mean", "value": tval},
            "threshold": mm_thr,
        },
        "supporting_check": {"name": "timing gain: mean daily book return minus position x coin mean daily return",
                             "value": timing, "passed": sup_passed},
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": "The down-streak is the run of consecutive closes below the previous close (capped at 180 bars) with the volume slope fitted on those falling bars, the first bet in each 18-bar grid cell is the case, the t of the forecast-weighted mean uses the weighted standard error sqrt(n/(n-1)*sum(w^2(x-m)^2))/sum(w), and the daily position for the market part is the mean allocation held over the bars of that day.",
    }
