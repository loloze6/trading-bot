import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 336
    SMA_N = 200
    RAW = "debug_info.components.prox_mom.last_history_value"

    def _prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = _prep(df)
            close = d["close"].astype(float)
            sma = close.rolling(SMA_N, min_periods=SMA_N).mean()
            above = close > sma
            # Where the 200-bar SMA cannot be rebuilt inside the window, use the recorded regime decision.
            regime_ok = np.where(sma.notna(), above, d["regime"] == "trending")
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            ret20 = close / close.shift(20) - 1.0
            # positive proximity-weighted rise: recorded raw value if present, else the 20-bar return
            rise_pos = np.where(raw.notna(), raw > 0, ret20 > 0)
            situation = np.asarray(regime_ok, dtype=bool) & np.asarray(rise_pos, dtype=bool)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are long bars with the close above its 200-bar SMA "
                           "and a positive proximity-weighted 20-bar rise"
                           if n_active > 0 else "The forecast is never active, so the situation cannot be checked"),
            "reading": "none",
        }

    # ---------- 2. main measure ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_rows = []
        for w, df in wins.items():
            d = _prep(df)
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                coin_rets.append(r)
                if reg[i] == "trending" and np.isfinite(fc[i]):
                    coin_rows.append((r, float(fc[i])))
        if len(coin_rets) == 0:
            continue
        mu = float(np.mean(coin_rets))
        for r, f in coin_rows:
            rows.append((r - mu, f))

    n_grid = len(rows)
    n_pos = int(sum(1 for _, f in rows if f > 0))
    slope = None
    tval = None
    if n_grid >= 3:
        y = np.array([r for r, _ in rows])
        x = np.array([f for _, f in rows])
        if np.var(x) > 0:
            lr = stats.linregress(x, y)
            slope = float(lr.slope)
            tval = float(lr.slope / lr.stderr) if lr.stderr > 0 else None

    # ---------- 3. supporting check: timing part of the book ----------
    book_parts = []
    mkt_parts = []
    for coin, wins in bars.items():
        coin_daily = []
        per_win = []
        for w, df in wins.items():
            d = _prep(df)
            d["date"] = d["timestamp"].dt.floor("D")
            last_idx = d.groupby("date").tail(1).index.values
            if len(last_idx) < 2:
                continue
            vals = pd.to_numeric(d["postRebalance_total_value"], errors="coerce").values
            closes = d["close"].astype(float).values
            alloc = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce").values
            dates = d["date"].values
            for k in range(1, len(last_idx)):
                i0, i1 = last_idx[k - 1], last_idx[k]
                br = vals[i1] / vals[i0] - 1.0
                cr = closes[i1] / closes[i0] - 1.0
                pos = np.nanmean(alloc[i0:i1]) if i1 > i0 else np.nan
                if np.isfinite(cr):
                    coin_daily.append(cr)
                per_win.append((dates[i1], br, pos))
        if len(coin_daily) == 0:
            continue
        mu_d = float(np.mean(coin_daily))
        for dt, br, pos in per_win:
            if np.isfinite(br):
                book_parts.append((dt, coin, br))
            if np.isfinite(pos):
                mkt_parts.append((dt, coin, pos * mu_d))

    timing = None
    if book_parts and mkt_parts:
        b = pd.DataFrame(book_parts, columns=["date", "coin", "v"]).groupby("date")["v"].mean()
        m = pd.DataFrame(mkt_parts, columns=["date", "coin", "v"]).groupby("date")["v"].mean()
        timing = float(b.mean() - m.mean())
    timing_ok = None if timing is None else bool(timing > 0)

    # ---------- 4. decision ----------
    if n_pos < 100:
        status = "not observable"
        decided_by = f"Fewer than 100 grid cases in the regime with a forecast above 0 ({n_pos})."
    elif tval is None:
        status = "inconclusive"
        decided_by = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and timing_ok:
        status = "confirmed"
        decided_by = "The slope's t is 2 or more and the timing part of the book is positive."
    elif tval <= -2:
        status = "rejected"
        decided_by = "The slope's t is -2 or less."
    elif tval >= 2:
        status = "inconclusive"
        decided_by = "The slope's t is 2 or more but the timing part is not positive."
    else:
        status = "inconclusive"
        decided_by = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of 336-bar excess return on forecast, pooled, trending grid bars",
            "value": slope,
            "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
            "threshold": "confirm if t >= 2 (with positive timing part); reject if t <= -2",
        },
        "supporting_check": {"name": "timing part of book daily returns", "value": timing, "passed": timing_ok},
        "counts": {
            "grid cases in the regime": int(n_grid),
            "grid cases in the regime with a forecast above 0": int(n_pos),
        },
        "decided_by": decided_by,
        "reading": ("The regression uses all trending grid bars (forecast zero included) with an intercept, each coin's "
                    "mean 336-bar return is taken over the non-overlapping grids of all its windows, the regime is the "
                    "recorded 'regime' column, and the daily position held is the mean allocation over the bars spanning "
                    "each day's return."),
    }
