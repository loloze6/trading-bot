import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    RAW = "debug_info.components.vol_scaled_mom.last_history_value"
    PPV = "debug_info.components.vol_scaled_mom.post_pipeline_value"

    # ---------- 1. situation check ----------
    # Fidelity: the situation is the 30-bar return over 60-bar volatility; the outcome is
    # a rise, so the expected side is long, and the forecast is flat when the ratio is not
    # positive. So an active bar must have a raw ratio > 0 and a forecast > 0.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            raw = (pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns
                   else pd.Series(np.nan, index=df.index))
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            ok = active & raw.notna() & (raw > 0) & (fc > 0)
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "slope of 10-bar excess return on post_pipeline_value (non-overlapping grid, before costs)"
    threshold = "confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive"
    reading = ("The coin's mean 10-bar return is the mean of its non-overlapping grid returns over all its windows; "
               "'pooling cases of the same day' is read as a day-clustered standard error for the OLS slope "
               "(each day's sum of x-deviation times residual taken as one piece of evidence); grid cases need "
               "a forward return inside the window and a recorded post_pipeline_value.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("The plan's situation (a positive 30-bar volatility-scaled return, held long) holds on only "
                           f"{agreement:.1%} of the bars where the forecast is not zero, below 90%."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            x = (pd.to_numeric(df[PPV], errors="coerce").values if PPV in df.columns
                 else np.full(len(df), np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for t in range(0, len(df), H):
                if t + H >= len(df):
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                coin_rows.append({
                    "coin": coin,
                    "day": ts.iloc[t].floor("D"),
                    "ret": c1 / c0 - 1.0,
                    "x": x[t],
                })
        if coin_rows:
            cdf = pd.DataFrame(coin_rows)
            drift = cdf["ret"].mean()
            cdf["excess"] = cdf["ret"] - drift
            rows.append(cdf)

    if rows:
        data = pd.concat(rows, ignore_index=True)
        data = data[np.isfinite(data["x"].astype(float)) & np.isfinite(data["excess"].astype(float))]
    else:
        data = pd.DataFrame(columns=["coin", "day", "ret", "x", "excess"])

    n_total = int(len(data))
    n_pos = int((data["x"] > 0).sum()) if n_total else 0
    n_days = int(data["day"].nunique()) if n_total else 0
    counts = {"grid cases in total": n_total, "grid cases with forecast > 0": n_pos, "days": n_days}

    slope = None
    tstat = None
    if n_total >= 3:
        x = data["x"].astype(float).values
        y = data["excess"].astype(float).values
        xm = x - x.mean()
        sxx = float(np.sum(xm ** 2))
        if sxx > 0:
            b = float(np.sum(xm * (y - y.mean())) / sxx)
            a = float(y.mean() - b * x.mean())
            e = y - a - b * x
            sc = pd.Series(xm * e).groupby(data["day"].values).sum().values
            G = len(sc)
            meat = float(np.sum(sc ** 2))
            if G > 1:
                meat *= G / (G - 1)
            se = np.sqrt(meat) / sxx
            slope = b
            tstat = float(b / se) if se > 0 else None

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t, day-clustered", "value": tstat} if tstat is not None else None),
            "threshold": threshold}

    if n_pos < 200 or n_total < 1000:
        miss = []
        if n_pos < 200:
            miss.append(f"{n_pos} grid cases with forecast > 0 (fewer than 200)")
        if n_total < 1000:
            miss.append(f"{n_total} grid cases in total (fewer than 1000)")
        status = "not observable"
        decided = "The plan's minimum count is not reached: " + "; ".join(miss) + "."
    elif slope is None or tstat is None:
        status = "inconclusive"
        decided = "The slope or its t could not be computed (no variation in the forecast), so neither rule is met."
    elif slope > 0 and tstat >= 2:
        status = "confirmed"
        decided = f"The slope is positive with t = {tstat:.2f} >= 2 (plan's confirm rule; no supporting check)."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = f"The slope is negative with t = {tstat:.2f} <= -2 (plan's reject rule)."
    else:
        status = "inconclusive"
        decided = f"The slope has |t| = {abs(tstat):.2f} < 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
