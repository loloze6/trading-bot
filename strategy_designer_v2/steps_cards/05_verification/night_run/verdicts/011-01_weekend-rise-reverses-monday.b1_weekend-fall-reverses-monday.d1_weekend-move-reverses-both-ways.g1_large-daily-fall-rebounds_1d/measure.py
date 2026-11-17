import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.vs_fall.last_history_value"
    POS = "postRebalance_current_allocation"

    # ---------- gather per-bar data, window by window (never across windows) ----------
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            next_ret = close.shift(-1) / close - 1.0          # inside the window only
            prev_ret = close / close.shift(1) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            # where the component is not recorded, the sign of the vol-scaled return
            # is the sign of the 1-day return, recomputed from prices
            raw_sign_src = raw.where(raw.notna(), prev_ret)
            frames.append(pd.DataFrame({
                "coin": coin,
                "window": w,
                "forecast": pd.to_numeric(d["forecast"], errors="coerce"),
                "pos": pd.to_numeric(d[POS], errors="coerce") if POS in d.columns else np.nan,
                "raw": raw_sign_src,
                "next_ret": next_ret,
            }))

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None, "counts": {},
            "decided_by": "No bars in the record.", "reading": "none",
        }

    allb = pd.concat(frames, ignore_index=True)

    # ---------- situation check ----------
    active = allb[allb["forecast"].fillna(0) != 0]
    n_active = int(len(active))
    if n_active > 0:
        in_sit = (active["raw"] < 0) & (active["forecast"] > 0)
        agreement = float(in_sit.mean())
    else:
        agreement = 0.0
    passed_sit = n_active > 0 and agreement >= 0.90

    reading = ("Situation bars are bars whose volatility-scaled 1-day return (recorded raw value, or the 1-day price "
               "return where missing) is below zero, with a long forecast expected; the coin's mean daily return is "
               "pooled over all its windows; the main t uses every bar with a next-bar return (horizon 1, so every bar "
               "is its own non-overlapping case); the top-10% group is the pooled positive-forecast bars at or above "
               "the 90th percentile of positive forecasts across all coins; a minimum count not reached gives "
               "'not observable'.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars after a daily fall "
                           "(negative volatility-scaled return), as the plan's situation requires."),
            "reading": reading,
        }

    # ---------- excess returns ----------
    coin_mean = allb.dropna(subset=["next_ret"]).groupby("coin")["next_ret"].mean()
    allb["excess"] = allb["next_ret"] - allb["coin"].map(coin_mean)

    # ---------- main measure ----------
    m = allb.dropna(subset=["pos", "excess"])
    prod = (m["pos"] * m["excess"]).to_numpy(dtype=float)
    n_main = int(len(prod))
    mean_prod = float(np.mean(prod)) if n_main > 0 else None
    if n_main > 1:
        sd = float(np.std(prod, ddof=1))
        t_main = float(mean_prod / (sd / np.sqrt(n_main))) if sd > 0 else 0.0
    else:
        t_main = None
    n_nonzero = int((m["pos"] != 0).sum())

    # ---------- supporting check ----------
    posf = allb[(allb["forecast"] > 0)].dropna(subset=["excess"])
    if len(posf) > 0:
        thr = float(np.quantile(posf["forecast"].to_numpy(dtype=float), 0.90))
        top = posf[posf["forecast"] >= thr]
    else:
        thr = None
        top = posf
    n_top = int(len(top))
    top_mean = float(top["excess"].mean()) if n_top > 0 else None
    sup_passed = (top_mean is not None) and (top_mean > 0)

    counts = {
        "bars with a non-zero position": n_nonzero,
        "bars in the top-10% group": n_top,
        "bars in the main measure": n_main,
    }

    main = {
        "name": "t of mean of position x next-bar excess return, pooled, before costs",
        "value": mean_prod,
        "statistic": {"name": "t of the mean", "value": t_main} if t_main is not None else None,
        "threshold": "confirm if t >= 2 with supporting check passed; reject if t <= -2; otherwise inconclusive",
    }
    support = {
        "name": "mean next-bar excess return on top 10% of positive forecasts > 0",
        "value": top_mean,
        "passed": bool(sup_passed) if top_mean is not None else None,
    }

    # ---------- decision ----------
    if n_nonzero < 300 or n_top < 30 or t_main is None:
        missing = []
        if n_nonzero < 300:
            missing.append(f"bars with a non-zero position {n_nonzero} < 300")
        if n_top < 30:
            missing.append(f"bars in the top-10% group {n_top} < 30")
        if t_main is None:
            missing.append("too few bars to compute the t")
        status = "not observable"
        decided = "Minimum count not reached: " + "; ".join(missing) + "."
    elif t_main >= 2 and sup_passed:
        status = "confirmed"
        decided = "Main t >= 2 and the top-10% group's mean next-bar excess return is above 0."
    elif t_main <= -2:
        status = "rejected"
        decided = "Main t <= -2."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "Main t >= 2 but the supporting check failed (top-10% mean excess return not above 0)."
    else:
        status = "inconclusive"
        decided = "Main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
