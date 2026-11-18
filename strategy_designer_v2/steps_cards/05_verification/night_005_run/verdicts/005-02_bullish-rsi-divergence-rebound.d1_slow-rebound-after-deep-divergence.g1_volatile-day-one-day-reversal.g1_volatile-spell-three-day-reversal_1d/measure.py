import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    FADE = "debug_info.components.fade.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            r = close.pct_change()
            # 20-day volatility over its 60-day mean, recomputed from prices inside the window
            s20 = r.rolling(20, min_periods=20).std()
            ratio = s20 / s20.rolling(60, min_periods=60).mean()
            reg_mr = (df["regime"] == "mean_reversion").to_numpy()
            ratio_v = ratio.to_numpy()
            situation = np.where(np.isfinite(ratio_v), ratio_v >= 1.0, reg_mr)
            # day's return: the fade component's raw value where recorded, else from prices
            if FADE in df.columns:
                day_ret = pd.to_numeric(df[FADE], errors="coerce")
                day_ret = day_ret.where(day_ret.notna(), r)
            else:
                day_ret = r
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            dr = day_ret.to_numpy()
            active = np.isfinite(fc) & (fc != 0)
            expected_side = np.where(np.isfinite(dr), -np.sign(dr), np.nan)
            ok = active & situation.astype(bool) & (np.sign(fc) == expected_side)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "grid cases pooled": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the 20-day volatility "
                           "is at or above its 60-day mean with the forecast's sign against the day's move."),
            "reading": ("The volatility ratio is recomputed from closes (20-bar std of daily returns over its 60-bar "
                        "mean) where the window allows, else the recorded regime is used; the side is minus the sign of "
                        "the day's return."),
        }

    # ---------- 2. criterion ----------
    products = []
    absf = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            n = len(df)
            idx = np.arange(0, n, H)
            idx = idx[idx + H < n]
            if len(idx) == 0:
                continue
            fwd = close[idx + H] / close[idx] - 1.0
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()[idx]
            reg = df["regime"].to_numpy()[idx]
            coin_rows.append(pd.DataFrame({"fwd": fwd, "fc": fc, "reg": reg}))
        if not coin_rows:
            continue
        cd = pd.concat(coin_rows, ignore_index=True)
        cd = cd[np.isfinite(cd["fwd"])]
        coin_mean = cd["fwd"].mean()  # coin's mean 3-bar return over all its windows (grid bars)
        kept = cd[(cd["reg"] == "mean_reversion") & np.isfinite(cd["fc"])]
        p = (kept["fc"] / 10.0) * (kept["fwd"] - coin_mean)
        products.extend(p.tolist())
        absf.extend(kept["fc"].abs().tolist())

    products = np.asarray(products, dtype=float)
    absf = np.asarray(absf, dtype=float)
    N = int(len(products))

    mean_p = float(products.mean()) if N > 0 else None
    t = None
    if N > 1:
        sd = products.std(ddof=1)
        t = float(mean_p / (sd / np.sqrt(N))) if sd > 0 else None

    supp_val = None
    supp_pass = None
    k = N // 3
    if k >= 1:
        order = np.argsort(absf, kind="mergesort")
        bottom = products[order[:k]]
        top = products[order[N - k:]]
        supp_val = float(top.mean() - bottom.mean())
        supp_pass = bool(supp_val > 0)

    if N < 100:
        status = "not observable"
        decided = f"Only {N} grid cases pooled, below the plan's minimum of 100."
    elif t is not None and t >= 2 and supp_pass:
        status = "confirmed"
        decided = "The main measure's t is at least +2 and the top-minus-bottom third check is above 0."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "The main measure's t is at most -2."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "The main measure's t is at least +2 but the supporting check failed."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean of forecast/10 x (3-bar forward return minus coin mean), mean_reversion grid bars",
            "value": mean_p,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "t >= +2 confirms (with supporting check), t <= -2 rejects",
        },
        "supporting_check": {
            "name": "mean product top third of |forecast| minus bottom third",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": {"grid cases pooled": N, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": ("The coin's mean 3-bar return is taken over all grid bars of all its windows, the grid bars whose "
                    "3-bar forward return leaves the window are dropped, the thirds are the N//3 smallest and N//3 "
                    "largest |forecast| cases after a stable sort, and the 100-case minimum is applied as "
                    "'not observable'."),
    }
