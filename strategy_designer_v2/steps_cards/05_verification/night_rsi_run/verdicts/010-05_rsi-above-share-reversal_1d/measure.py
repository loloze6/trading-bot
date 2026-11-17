import numpy as np
import pandas as pd


def measure(bars):
    H = 14
    MIN_CASES = 300
    RAW = "debug_info.components.rsi_share.last_history_value"

    def _rsi_share_from_prices(close, period=14, window=30):
        # Fallback only: Wilder RSI(14), then the share of the last 30 bars with RSI > 50, minus 0.5.
        c = pd.Series(np.asarray(close, dtype=float))
        d = c.diff()
        up = d.clip(lower=0.0)
        dn = (-d).clip(lower=0.0)
        au = up.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        ad = dn.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        rs = au / ad.replace(0.0, np.nan)
        rsi = 100.0 - 100.0 / (1.0 + rs)
        rsi = rsi.where(ad != 0.0, 100.0).where(au.notna())
        above = (rsi > 50.0).astype(float).where(rsi.notna())
        share = above.rolling(window, min_periods=window).mean()
        return (share - 0.5).values

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values.astype(float)
            else:
                raw = np.full(len(df), np.nan)
            if np.isnan(raw).any():
                rec = _rsi_share_from_prices(df["close"].values)
                raw = np.where(np.isnan(raw), rec, raw)
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            # Larger share (raw > 0) -> lower return -> short; smaller share (raw < 0) -> long.
            agree = active & np.isfinite(raw) & (
                ((raw > 0) & (fc < 0)) | ((raw < 0) & (fc > 0))
            )
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars are short when the 30-bar share of RSI(14) above 50 exceeds one half "
                          "(raw value > 0) or long when it is below one half, as the plan's Fidelity requires.",
            "reading": "none",
        }

    # ---------- 2. main measure ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            n = len(df)
            for t in range(0, n - H, H):
                r = close[t + H] / close[t] - 1.0
                rows.append((coin, r, fc[t]))
    grid = pd.DataFrame(rows, columns=["coin", "ret", "fc"])
    grid = grid[np.isfinite(grid["ret"])]
    coin_mean = grid.groupby("coin")["ret"].mean()
    grid["ex"] = grid["ret"] - grid["coin"].map(coin_mean)
    grid = grid[np.isfinite(grid["fc"]) & np.isfinite(grid["ex"])]
    n_cases = int(len(grid))

    slope, t_stat = None, None
    if n_cases >= 3:
        x = grid["fc"].values
        y = grid["ex"].values
        xm = x - x.mean()
        sxx = float((xm ** 2).sum())
        if sxx > 0:
            b = float((xm * (y - y.mean())).sum() / sxx)
            a = y.mean() - b * x.mean()
            resid = y - a - b * x
            s2 = float((resid ** 2).sum() / (n_cases - 2))
            se = np.sqrt(s2 / sxx)
            slope = b
            t_stat = float(b / se) if se > 0 else None

    # ---------- 3. supporting check: timing part of the book's mean daily return, before costs ----------
    coin_daily_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        coin_daily_mean[coin] = float(allr.mean()) if len(allr) else np.nan

    recs = []
    for coin, wins in bars.items():
        mu = coin_daily_mean[coin]
        for w, df in wins.items():
            if len(df) < 2:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            day = ts.dt.floor("D").values
            c = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            pos = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").values.astype(float)
            d = pd.DataFrame({"day": day, "close": c, "pos": pos}).groupby("day", sort=True).last()
            cc = d["close"].values
            pp = d["pos"].values
            r = cc[1:] / cc[:-1] - 1.0
            held = pp[:-1]
            gross = held * r
            market = held * mu
            for dd, g, m in zip(d.index[1:], gross, market):
                if np.isfinite(g) and np.isfinite(m):
                    recs.append((w, dd, coin, g, m))
    timing = None
    if recs:
        book = pd.DataFrame(recs, columns=["w", "day", "coin", "gross", "market"])
        daily = book.groupby(["w", "day"])[["gross", "market"]].mean()
        timing = float(daily["gross"].mean() - daily["market"].mean())
    check_passed = None if timing is None else bool(timing > 0)

    # ---------- 4. decision ----------
    if n_cases < MIN_CASES or slope is None or t_stat is None:
        status = "not observable"
        decided = f"Only {n_cases} independent 14-bar cases, below the plan's minimum of 300."
    elif slope > 0 and t_stat >= 2:
        if check_passed:
            status = "confirmed"
            decided = "The slope is positive with t >= 2 on at least 300 independent cases and the timing gain is above 0."
        else:
            status = "inconclusive"
            decided = "The slope is positive with t >= 2 but the timing gain is not above 0."
    elif slope < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The slope is negative with t <= -2 on at least 300 independent cases."
    else:
        status = "inconclusive"
        decided = "The slope t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "OLS slope of coin-demeaned 14-bar forward return on forecast",
            "value": None if slope is None else float(slope),
            "statistic": None if t_stat is None else {"name": "OLS slope t", "value": float(t_stat)},
            "threshold": "confirm if slope > 0 with t >= 2, reject if slope < 0 with t <= -2, on at least 300 independent cases",
        },
        "supporting_check": {
            "name": "book mean daily timing gain before costs (> 0)",
            "value": timing,
            "passed": check_passed,
        },
        "counts": {"independent cases": n_cases},
        "decided_by": decided,
        "reading": "Grid bars at positions 0, 14, 28, ... of each window with a full 14-bar forward return inside the window, coin mean = mean of those grid returns over all its windows, pooled OLS with intercept; the timing check uses the position held after each day's trade times the next day's close-to-close return (before costs) minus that position times the coin's all-window mean daily return, averaged over coins per day, then over days.",
    }
