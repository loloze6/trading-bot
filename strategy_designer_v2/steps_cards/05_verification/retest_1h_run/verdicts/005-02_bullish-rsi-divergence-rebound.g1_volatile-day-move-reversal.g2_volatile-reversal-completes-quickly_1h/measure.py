import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 72
    RAW = "debug_info.components.day_move_fade.last_history_value"
    VOL_P, VOL_L = 480, 2400

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)
            # detector's volatility ratio, recomputed from the prices inside the window
            r1 = close.pct_change()
            vol = r1.rolling(VOL_P, min_periods=VOL_P).std()
            volmean = vol.rolling(VOL_L, min_periods=VOL_L).mean()
            ratio = vol / volmean
            vol_ok = ratio >= 1.0
            # where the window is too short to recompute, the detector's own decision stands
            reg_ok = df["regime"].astype(str) == "mean_reversion"
            vol_cond = pd.Series(np.where(ratio.notna(), vol_ok, reg_ok), index=df.index).astype(bool)
            # the day's move: recorded raw value, else recomputed 24-bar return
            if RAW in df.columns:
                raw = df[RAW].astype(float)
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), close / close.shift(24) - 1)
            active = fc.notna() & (fc != 0)
            side_ok = np.sign(fc) == -np.sign(raw)
            agree = active & vol_cond & side_ok & raw.notna() & (raw != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of active bars are bars of a high 480-bar volatility regime "
                           "(ratio to its 2400-bar mean >= 1) with the forecast opposite the 24-bar move."),
            "reading": ("Volatility ratio recomputed from prices inside each window, with the recorded regime "
                        "used where the window lacks the history; side taken as opposite the 24-bar move."),
        }

    # ---------- 2. criterion ----------
    grid = {}
    coin_mean = {}
    for coin, wins in bars.items():
        rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            for p in range(0, n, H):
                if p + H >= n:
                    break
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({
                    "ret": c1 / c0 - 1.0,
                    "fc": float(df["forecast"].iloc[p]) if pd.notna(df["forecast"].iloc[p]) else np.nan,
                    "regime": str(df["regime"].iloc[p]),
                })
        g = pd.DataFrame(rows, columns=["ret", "fc", "regime"])
        grid[coin] = g
        coin_mean[coin] = float(g["ret"].mean()) if len(g) else np.nan

    main_vals = []
    per_coin = {}
    sup_x, sup_y = [], []
    for coin, g in grid.items():
        if len(g) == 0:
            per_coin[coin] = 0
            continue
        g = g[(g["regime"] == "mean_reversion") & g["fc"].notna()].copy()
        g["sx"] = np.sign(g["fc"]) * (g["ret"] - coin_mean[coin])
        m = g[g["fc"].abs() >= 10]
        per_coin[coin] = int(len(m))
        main_vals.extend(m["sx"].tolist())
        s = g[g["fc"] != 0]
        sup_x.extend(s["fc"].abs().tolist())
        sup_y.extend(s["sx"].tolist())

    main_vals = np.array(main_vals, dtype=float)
    n_main = int(len(main_vals))
    mean_v = float(main_vals.mean()) if n_main > 0 else None
    t_v = None
    if n_main > 1:
        sd = main_vals.std(ddof=1)
        if sd > 0:
            t_v = float(mean_v / (sd / np.sqrt(n_main)))

    slope = None
    sup_x = np.array(sup_x, dtype=float)
    sup_y = np.array(sup_y, dtype=float)
    if len(sup_x) >= 3 and np.ptp(sup_x) > 0:
        slope = float(stats.linregress(sup_x, sup_y).slope)
    sup_pass = (slope > 0) if slope is not None else None

    counts = {"independent cases pooled": n_main}
    for coin, c in per_coin.items():
        counts[f"cases on {coin}"] = c
    counts["grid bars in regime with forecast != 0 (supporting)"] = int(len(sup_x))

    coins_short = [c for c, k in per_coin.items() if 0 < k < 10]
    if n_main < 30 or coins_short:
        status = "not observable"
        if n_main < 30:
            decided = f"Fewer than 30 independent cases pooled ({n_main})."
        else:
            decided = f"Fewer than 10 cases on a coin with cases ({', '.join(coins_short)})."
    elif t_v is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed (no spread in the cases), so neither rule is met."
    elif t_v >= 2 and mean_v > 0:
        if sup_pass:
            status = "confirmed"
            decided = "Mean signed excess return is positive with t >= 2 and the supporting slope is positive."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting slope is <= 0 (or not computable), which the plan calls inconclusive."
    elif t_v <= -2 and mean_v < 0:
        status = "rejected"
        decided = "Mean signed excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean signed 72-bar excess return on grid bars with |forecast| >= 10 in mean_reversion",
            "value": mean_v,
            "statistic": {"name": "ordinary t", "value": t_v} if t_v is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "slope of signed excess return on |forecast|, grid bars in regime with forecast != 0",
            "value": slope,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("The coin's mean 72-bar return is the mean over all its non-overlapping grid returns across all "
                    "windows, grid bars without a bar t+72 in the same window are dropped, and the plan's minimum "
                    "counts are applied as 'not observable' per the workflow."),
    }
