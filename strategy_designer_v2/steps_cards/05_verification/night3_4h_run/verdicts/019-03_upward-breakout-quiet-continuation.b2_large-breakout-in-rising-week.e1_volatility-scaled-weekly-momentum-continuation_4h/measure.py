import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 18
    RAW = "debug_info.components.vs_ret_7d.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        return d

    data = {c: {w: prep(df) for w, df in wins.items() if df is not None and len(df) > 0}
            for c, wins in bars.items()}

    # ---------------- situation check ----------------
    # Situation: the vol-scaled 7-day return; expected side: forecast's sign = sign of that return.
    n_active = 0
    n_agree = 0
    for c, wins in data.items():
        for w, d in wins.items():
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # recompute from prices where the raw value is not recorded
            close = pd.to_numeric(d["close"], errors="coerce")
            r1 = close.pct_change()
            rec = (close / close.shift(42) - 1) / (r1.rolling(20).std() * np.sqrt(42))
            raw = raw.where(raw.notna(), rec)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & raw.notna() & (raw != 0) & (np.sign(raw) == np.sign(fc))
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    main_name = "slope of 18-bar forward return minus coin mean, regressed on forecast"
    threshold = "t >= 2 over at least 300 non-overlapping cases confirms (with timing gain > 0); t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping cases": 0, "active bars": n_active},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast have a forecast whose sign matches "
                          "the sign of the vol-scaled 7-day return, as the Fidelity (rise = long) requires.",
            "reading": "none",
        }

    # ---------------- main measure ----------------
    xs, ys = [], []
    for c, wins in data.items():
        samples = []
        for w, d in wins.items():
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            n = len(d)
            for i in range(0, n - H, H):
                if np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0:
                    samples.append((fc[i], close[i + H] / close[i] - 1))
        if not samples:
            continue
        arr = np.array(samples, dtype=float)
        rets = arr[:, 1]
        coin_mean = np.nanmean(rets)
        ok = np.isfinite(arr[:, 0]) & np.isfinite(rets)
        xs.extend(arr[ok, 0].tolist())
        ys.extend((rets[ok] - coin_mean).tolist())
    x = np.array(xs, dtype=float)
    y = np.array(ys, dtype=float)
    n_cases = int(len(x))
    slope, t_slope = None, None
    if n_cases >= 3 and np.std(x) > 0:
        res = stats.linregress(x, y)
        slope = float(res.slope)
        t_slope = float(res.slope / res.stderr) if res.stderr > 0 else None

    # ---------------- supporting check: timing gain before costs ----------------
    book_rows = []  # (date, coin, gross daily return, mean position over the day)
    coin_daily = {}
    for c, wins in data.items():
        cd = []
        rows_c = []
        for w, d in wins.items():
            close = pd.to_numeric(d["close"], errors="coerce").values
            alloc = pd.to_numeric(d[ALLOC], errors="coerce").values
            dates = d["timestamp"].dt.date.values
            n = len(d)
            if n < 2:
                continue
            last_idx = []
            for i in range(n):
                if i == n - 1 or dates[i + 1] != dates[i]:
                    last_idx.append(i)
            for k in range(1, len(last_idx)):
                a, b = last_idx[k - 1], last_idx[k]
                if not (np.isfinite(close[a]) and np.isfinite(close[b]) and close[a] > 0):
                    continue
                cd.append(close[b] / close[a] - 1)
                seg_al = alloc[a:b]
                seg_r = close[a + 1:b + 1] / close[a:b] - 1
                ok = np.isfinite(seg_al) & np.isfinite(seg_r)
                if ok.sum() == 0:
                    continue
                gross = float(np.prod(1 + seg_al[ok] * seg_r[ok]) - 1)
                rows_c.append((dates[b], gross, float(np.mean(seg_al[ok]))))
        if cd:
            coin_daily[c] = float(np.mean(cd))
            for dt, g, p in rows_c:
                book_rows.append((dt, c, g, p))
    timing = None
    if book_rows:
        bd = pd.DataFrame(book_rows, columns=["date", "coin", "gross", "pos"])
        bd["market"] = bd["pos"] * bd["coin"].map(coin_daily)
        daily = bd.groupby("date")[["gross", "market"]].mean()
        book_mean = float(daily["gross"].mean())
        market_mean = float(daily["market"].mean())
        timing = book_mean - market_mean
    sup_passed = None if timing is None else bool(timing > 0)

    # ---------------- decision ----------------
    if n_cases < 300 or t_slope is None:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases, fewer than the plan's minimum of 300."
    elif t_slope >= 2 and sup_passed:
        status = "confirmed"
        decided = "The slope's t is 2 or more over at least 300 non-overlapping cases and the timing gain before costs is above 0."
    elif t_slope >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the book's timing gain before costs is not above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less over at least 300 non-overlapping cases."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": slope,
                         "statistic": None if t_slope is None else {"name": "OLS t of slope", "value": t_slope},
                         "threshold": threshold},
        "supporting_check": {"name": "book's timing gain before costs (mean daily)", "value": timing,
                             "passed": sup_passed},
        "counts": {"non-overlapping cases": n_cases},
        "decided_by": decided,
        "reading": "The regression is OLS with an intercept on all grid bars (forecast zero included), the coin's mean "
                   "18-bar return is taken over its grid samples of all windows, and the gross daily book return "
                   "compounds each bar's position gain between consecutive days' last bars, with the market part as the "
                   "day's mean position times the coin's mean daily return over all windows.",
    }
