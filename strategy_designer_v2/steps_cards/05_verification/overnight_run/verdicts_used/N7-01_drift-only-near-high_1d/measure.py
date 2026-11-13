import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    REC = "debug_info.components.recency.last_history_value"

    def prep(df):
        df = df.reset_index(drop=True).copy()
        c = df["close"].astype(float)
        sma = c.rolling(20, min_periods=20).mean()
        rmax = c.rolling(20, min_periods=20).max()
        is_high = (c >= rmax) & rmax.notna()
        idx = pd.Series(np.where(is_high, np.arange(len(c)), np.nan))
        last_high = idx.ffill()
        bars_since = np.arange(len(c)) - last_high
        recent_px = (bars_since < 20) & last_high.notna()
        if REC in df.columns:
            rec = pd.to_numeric(df[REC], errors="coerce")
            recent = pd.Series(np.where(rec.notna(), rec > 0, recent_px), index=df.index).astype(bool)
        else:
            recent = recent_px.astype(bool)
        regime_tr = df["regime"].astype(str).str.lower().eq("trending") if "regime" in df.columns else pd.Series(False, index=df.index)
        above = pd.Series(np.where(sma.notna(), c > sma, regime_tr), index=df.index).astype(bool)
        below = (sma.notna() & (c < sma)).astype(bool)
        fwd = c.shift(-H) / c - 1.0
        df["_sit"] = above & recent
        df["_flat_below"] = recent_px.astype(bool) & below
        df["_fwd"] = fwd
        df["_grid"] = (np.arange(len(df)) % H) == 0
        df["_fc"] = pd.to_numeric(df["forecast"], errors="coerce")
        return df

    data = {coin: {w: prep(df) for w, df in wins.items()} for coin, wins in bars.items()}

    # --- situation check ---
    n_active, n_ok = 0, 0
    for coin, wins in data.items():
        for w, df in wins.items():
            act = df["_fc"].notna() & (df["_fc"] != 0)
            n_active += int(act.sum())
            n_ok += int((act & df["_sit"] & (df["_fc"] > 0)).sum())
    agreement = float(n_ok / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars are long bars with close above SMA20 and a new 20-day closing high within 20 bars, as the plan's situation requires.",
            "reading": "Situation recomputed from in-window prices (SMA20 of close, new 20-bar closing high within the last 20 bars), using the recency component's raw value when recorded and the regime label where SMA20 is not yet computable.",
        }

    # --- criterion ---
    xs, ws, sup = [], [], []
    for coin, wins in data.items():
        allf = pd.concat([df["_fwd"] for df in wins.values()]).dropna()
        if len(allf) == 0:
            continue
        mu = float(allf.mean())
        for w, df in wins.items():
            g = df[df["_grid"] & df["_fwd"].notna()]
            a = g[g["_fc"].notna() & (g["_fc"] > 0)]
            xs.extend((a["_fwd"] - mu).tolist())
            ws.extend(a["_fc"].tolist())
            f = g[g["_fc"].notna() & (g["_fc"] == 0) & g["_flat_below"]]
            sup.extend((f["_fwd"] - mu).tolist())

    x = np.asarray(xs, float)
    wt = np.asarray(ws, float)
    n = int(len(x))
    m, t = None, None
    if n >= 2 and wt.sum() > 0:
        m = float(np.sum(wt * x) / np.sum(wt))
        se = np.sqrt(np.sum(wt ** 2 * (x - m) ** 2)) / np.sum(wt) * np.sqrt(n / (n - 1))
        t = float(m / se) if se > 0 else (float(np.sign(m) * np.inf) if m != 0 else 0.0)
    elif n == 1:
        m = float(x[0])

    sup_val = float(np.mean(sup)) if len(sup) > 0 else None
    sup_pass = (sup_val <= 0) if sup_val is not None else None

    if n < 100:
        status = "not observable"
        decided = f"Only {n} non-overlapping active 5-bar blocks across all coins and windows, below the plan's minimum of 100."
    elif m is not None and t is not None and m > 0 and t >= 2:
        status = "confirmed"
        decided = "The forecast-weighted mean excess return is positive with t >= 2."
    elif m is not None and t is not None and m < 0 and t <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "forecast-weighted mean forward 5-bar excess return over coin mean",
            "value": m,
            "statistic": {"name": "t of weighted mean (weighted sandwich SE)", "value": t} if t is not None else None,
            "threshold": "confirm if positive with t >= 2; reject if negative with t <= -2",
        },
        "supporting_check": {
            "name": "mean forward 5-bar excess return on flat bars with recent high and close below SMA20",
            "value": sup_val,
            "passed": None if sup_pass is None else bool(sup_pass),
        },
        "counts": {
            "non-overlapping active 5-bar blocks": n,
            "supporting flat blocks": int(len(sup)),
        },
        "decided_by": decided,
        "reading": "Active blocks are grid bars 0,5,10,... of each window with forecast > 0; the coin's mean 5-bar return is over all bars of all its windows; excess on supporting bars is the coin's forward return minus that mean; the weighted t uses SE = sqrt(sum w^2 (x-m)^2)/sum w x sqrt(n/(n-1)); 'new high within 20 bars' means a 20-bar closing high 0-19 bars ago; and fewer than 100 blocks gives 'not observable'.",
    }
