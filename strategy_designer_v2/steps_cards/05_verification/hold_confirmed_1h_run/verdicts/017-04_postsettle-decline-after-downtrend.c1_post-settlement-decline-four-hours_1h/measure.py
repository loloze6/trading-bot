import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.fall72.last_history_value"
    H = 4

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    # Per-coin data kept for the criterion
    coin_frames = {}
    for coin, wins in bars.items():
        coin_frames[coin] = []
        for w, df in wins.items():
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            fc = d[FC].astype(float)
            hour = d["timestamp"].dt.hour
            # the next bar starts 0..3 h after a settlement (00, 08, 16 UTC):
            # bars stamped 23,0,1,2 / 7,8,9,10 / 15,16,17,18
            in_window = ((hour + 1) % 8).isin([0, 1, 2, 3])
            # the 3-day (72-bar) price change: recorded raw value, else from prices
            raw_rec = d[RAW].astype(float) if RAW in d.columns else pd.Series(np.nan, index=d.index)
            raw_px = close / close.shift(72) - 1.0
            raw = raw_rec.where(raw_rec.notna(), raw_px)
            active = fc.notna() & (fc != 0)
            situ = in_window & (raw < 0) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
            coin_frames[coin].append(d)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("fewer than 90 % of the active bars are short bars in the 4 bars after a settlement "
                           "following a 72-bar fall" if n_active > 0 else "the record has no active bar"),
            "reading": "none",
        }

    # ---------- 2. Criterion ----------
    fcs, excess = [], []
    for coin, dlist in coin_frames.items():
        # coin's mean 4-bar return over all windows (non-overlapping grid 0,4,8,... per window)
        grid_rets = []
        for d in dlist:
            c = d["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    grid_rets.append(c[i + H] / c[i] - 1.0)
        if len(grid_rets) == 0:
            continue
        mu = float(np.mean(grid_rets))
        for d in dlist:
            ts = d["timestamp"]
            c = d["close"].astype(float).values
            f = d[FC].astype(float).values
            hr = ts.dt.hour.values
            mi = ts.dt.minute.values
            n = len(d)
            for i in range(n - H):
                if hr[i] not in (23, 7, 15) or mi[i] != 0:
                    continue
                if not np.isfinite(f[i]) or f[i] >= 0:
                    continue
                if ts.iloc[i + H] - ts.iloc[i] != pd.Timedelta(hours=H):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] == 0:
                    continue
                r = c[i + H] / c[i] - 1.0
                fcs.append(f[i])
                excess.append(r - mu)

    fcs = np.array(fcs, dtype=float)
    excess = np.array(excess, dtype=float)
    n_ep = int(len(fcs))
    counts = {"episodes with a negative forecast": n_ep}
    threshold = "confirm: mean product > 0 with t >= 2 and supporting check passes; reject: mean product < 0 with t <= -2; at least 300 episodes"
    reading = ("Entry bars are those stamped 23:00, 07:00 or 15:00 with forecast < 0 whose bar 4 rows later is exactly 4 h later in the same window; "
               "the coin's mean 4-bar return uses the non-overlapping grid of each window pooled over all windows; "
               "thirds are n//3 episodes by |forecast| pooled over coins and windows.")

    mean_prod, t = None, None
    if n_ep >= 2:
        prod = fcs / 10.0 * excess
        mean_prod = float(np.mean(prod))
        sd = float(np.std(prod, ddof=1))
        t = float(mean_prod / (sd / np.sqrt(n_ep))) if sd > 0 else 0.0

    sup_val, sup_pass = None, None
    k = n_ep // 3
    if k >= 1:
        order = np.argsort(np.abs(fcs), kind="mergesort")
        low = excess[order[:k]]
        high = excess[order[-k:]]
        sup_val = float(np.mean(high) - np.mean(low))
        sup_pass = bool(sup_val < 0)
    counts["episodes per third"] = int(k)

    main = {
        "name": "mean of (forecast/10) x excess 4-bar return after settlement",
        "value": mean_prod,
        "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
        "threshold": threshold,
    }
    sup = {"name": "excess 4-bar return, largest-|forecast| third minus smallest third",
           "value": sup_val, "passed": sup_pass}

    if n_ep < 300:
        status = "not observable"
        decided = f"only {n_ep} episodes with a negative forecast, below the plan's minimum of 300"
    elif mean_prod > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "the mean product is above 0 with t >= 2 and the top-minus-bottom third difference is below 0"
    elif mean_prod < 0 and t <= -2:
        status = "rejected"
        decided = "the mean product is below 0 with t <= -2"
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive"
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive"

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
