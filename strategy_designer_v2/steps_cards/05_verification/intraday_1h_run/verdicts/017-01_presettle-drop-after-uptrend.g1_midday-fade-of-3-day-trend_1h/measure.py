import numpy as np
import pandas as pd


def measure(bars):
    POS = "postRebalance_current_allocation"
    RAW = "debug_info.components.fade_3d.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    per_coin_frames = {}
    coin_mean_ret = {}

    for coin, wins in bars.items():
        rets_all = []
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float).reset_index(drop=True)
            d = d.reset_index(drop=True)
            # Return over the next bar, inside this window only
            r_next = close.shift(-1) / close - 1.0
            rets_all.append(r_next.dropna().values)
            # 72-bar return recomputed from prices, inside this window
            ret72_px = close / close.shift(72) - 1.0
            raw = d[RAW].astype(float) if RAW in d.columns else pd.Series(np.nan, index=d.index)
            raw = raw.where(raw.notna(), ret72_px)
            # Situation: the bar whose coming bar starts at 12:00 UTC (bar starting 11:00 UTC)
            next_start_hour = (ts + pd.Timedelta(hours=1)).dt.hour.reset_index(drop=True)
            situ = next_start_hour == 12
            fc = d["forecast"].astype(float).fillna(0.0)
            active = fc != 0
            expected_sign = -np.sign(raw)
            ok = active & situ & raw.notna() & (np.sign(fc) == expected_sign) & (expected_sign != 0)
            n_active += int(active.sum())
            n_agree += int(ok.sum())
            frames.append(pd.DataFrame({
                "regime": d["regime"].values,
                "pos": d[POS].astype(float).values if POS in d.columns else np.nan,
                "r_next": r_next.values,
            }))
        coin_mean_ret[coin] = float(np.mean(np.concatenate(rets_all))) if rets_all and sum(len(x) for x in rets_all) > 0 else np.nan
        per_coin_frames[coin] = frames

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled mean of position x (next 1-bar return - coin mean 1-bar return) on trending bars"
    threshold = "confirm: mean > 0 with t >= 2 and >= 4 of 6 coins positive; reject: mean < 0 with t <= -2"
    reading = ("Situation bars are those whose next bar starts at 12:00 UTC (bar timestamp 11:00 UTC); the main sample "
               "includes every 'trending' bar with a next bar in its window (zero positions included), the coin's mean "
               "1-bar return is over all bars of all its windows, the 500 minimum counts trending bars with a nonzero "
               "position, and the coin check needs at least 4 coins with a positive mean whatever the number of coins present.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on expected side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are bars whose next bar starts at 12:00 UTC "
                           "with a forecast opposite in sign to the 72-bar return, as the Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    pooled = []
    coin_means = {}
    n_nonzero = 0
    for coin, frames in per_coin_frames.items():
        vals = []
        m = coin_mean_ret.get(coin, np.nan)
        for f in frames:
            s = f[f["regime"] == "trending"]
            s = s[s["pos"].notna() & s["r_next"].notna()]
            if len(s) == 0 or not np.isfinite(m):
                continue
            g = s["pos"].values * (s["r_next"].values - m)
            vals.append(g)
            n_nonzero += int((s["pos"].values != 0).sum())
        if vals:
            v = np.concatenate(vals)
            if len(v) > 0:
                coin_means[coin] = float(np.mean(v))
                pooled.append(v)

    x = np.concatenate(pooled) if pooled else np.array([])
    n = int(len(x))
    mean = float(np.mean(x)) if n > 0 else None
    if n > 1:
        sd = float(np.std(x, ddof=1))
        t = float(mean / (sd / np.sqrt(n))) if sd > 0 else 0.0
    else:
        t = None

    n_pos_coins = int(sum(1 for v in coin_means.values() if v > 0))
    check_passed = n_pos_coins >= 4

    counts = {
        "hour-12 cases with a nonzero position": int(n_nonzero),
        "trending bars in sample": n,
        "coins with positive mean excess gain": n_pos_coins,
        "coins measured": int(len(coin_means)),
    }

    main = {"name": main_name, "value": mean,
            "statistic": {"name": "ordinary t of the mean", "value": t} if t is not None else None,
            "threshold": threshold}
    support = {"name": "coins with positive mean excess gain (need >= 4 of 6)",
               "value": n_pos_coins, "passed": bool(check_passed)}

    if n_nonzero < 500 or t is None:
        status = "not observable"
        decided = f"Only {n_nonzero} hour-12 cases with a nonzero position, below the plan's minimum of 500."
    elif mean > 0 and t >= 2 and check_passed:
        status = "confirmed"
        decided = "Pooled mean excess gain > 0 with t >= 2 and at least 4 of 6 coins positive."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "Pooled mean excess gain < 0 with t <= -2."
    elif t >= 2 and not check_passed:
        status = "inconclusive"
        decided = "t >= 2 but fewer than 4 of 6 coins have a positive mean excess gain."
    else:
        status = "inconclusive"
        decided = "The t of the pooled mean excess gain lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
