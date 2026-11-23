import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.volfall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            ret1 = close / close.shift(1) - 1.0
            vol20 = ret1.rolling(20, min_periods=20).std()
            recomputed = ret1 / vol20
            if RAW in df.columns:
                raw = df[RAW].astype(float)
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            fc = df["forecast"].astype(float)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: a day's fall in vol units (raw < 0); expected side: long
            agree = active & (raw < 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "forecast-weighted mean next-day excess return on bars with forecast > 0"
    threshold = "confirm: positive with t >= 2 and Spearman > 0; reject: negative with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"bars with forecast > 0": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are bars after a fall (negative volatility-scaled "
                           "return) with a long forecast, as the plan's situation and side require."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    xs, ws = [], []
    for coin, wins in bars.items():
        frames = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            nxt = close.shift(-1) / close - 1.0
            frames.append(pd.DataFrame({"fwd": nxt, "fc": df["forecast"].astype(float)}))
        if not frames:
            continue
        allc = pd.concat(frames, ignore_index=True)
        coin_mean = allc["fwd"].dropna().mean()
        sel = allc[(allc["fc"] > 0) & allc["fwd"].notna()]
        xs.append((sel["fwd"] - coin_mean).values)
        ws.append(sel["fc"].values)

    x = np.concatenate(xs) if xs else np.array([])
    wt = np.concatenate(ws) if ws else np.array([])
    n = int(len(x))

    m = None
    t = None
    rho = None
    if n >= 2 and wt.sum() > 0:
        W = wt.sum()
        m = float(np.sum(wt * x) / W)
        var_m = np.sum(wt ** 2 * (x - m) ** 2) / W ** 2 * n / (n - 1)
        t = float(m / np.sqrt(var_m)) if var_m > 0 else 0.0
        r = stats.spearmanr(wt, x).correlation
        rho = float(r) if r is not None and np.isfinite(r) else None

    sup_pass = None if rho is None else bool(rho > 0)

    if n < 200:
        status = "not observable"
        decided = "Fewer than 200 bars with forecast > 0 across all coins and windows (the plan's minimum count)."
    elif m is not None and m > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The weighted mean excess return is positive with t >= 2 and the Spearman correlation is above 0."
    elif m is not None and m < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        if m is not None and m > 0 and t is not None and t >= 2:
            decided = "The weighted mean is positive with t >= 2 but the Spearman check fails."
        else:
            decided = "The t of the weighted mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": m,
            "statistic": None if t is None else {"name": "t of the weighted mean", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "Spearman(forecast, next-day excess return) on forecast > 0 bars > 0",
            "value": rho,
            "passed": sup_pass,
        },
        "counts": {"bars with forecast > 0": n},
        "decided_by": decided,
        "reading": ("The t of the forecast-weighted mean uses the weighted standard error "
                    "sqrt(sum(w^2 (x-m)^2) / (sum w)^2 * n/(n-1)), every in-window bar with a next bar counts as a case, "
                    "the coin's mean daily return is over all its in-window daily returns, and the plan's 200-bar minimum "
                    "yields 'not observable' when unmet."),
    }
