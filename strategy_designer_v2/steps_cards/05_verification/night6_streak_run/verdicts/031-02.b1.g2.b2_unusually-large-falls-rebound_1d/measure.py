import numpy as np
import pandas as pd

RAW = "debug_info.components.scaled_fall.last_history_value"
H = 2


def _to_day(ts):
    s = pd.Series(ts)
    if np.issubdtype(s.dtype, np.number):
        mx = float(np.nanmax(s.values)) if len(s) else 0.0
        unit = "ns" if mx > 1e17 else ("us" if mx > 1e14 else ("ms" if mx > 1e11 else "s"))
        dt = pd.to_datetime(s, unit=unit, utc=True)
    else:
        dt = pd.to_datetime(s, utc=True)
    return dt.dt.floor("D").dt.strftime("%Y-%m-%d").values


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                # where the raw value is not recorded, its sign is the sign of the one-bar return
                raw = raw.where(raw.notna(), ret1)
            else:
                raw = ret1
            active = fc.notna() & (fc != 0)
            situ = raw < 0  # a fall on the latest day
            agree = active & situ & (fc > 0)  # expected side: long
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars after a down day "
                           "(negative volatility-scaled one-bar return), as the Fidelity's situation and side require."
                           if n_active > 0 else "The forecast is never non-zero, so the plan's long-after-a-fall situation is never traded."),
            "reading": "Situation read as a negative raw component value (or negative one-bar return where not recorded), side long.",
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
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            days = _to_day(df["timestamp"].values)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append({"coin": coin, "day": days[i], "f": fc[i], "r": c1 / c0 - 1.0})
        if coin_rows:
            cdf = pd.DataFrame(coin_rows)
            drift = cdf["r"].mean()  # coin's mean 2-day return over all its windows
            cdf["y"] = cdf["r"] - drift
            rows.append(cdf)

    if not rows:
        data = pd.DataFrame(columns=["coin", "day", "f", "r", "y"])
    else:
        data = pd.concat(rows, ignore_index=True)
    data = data[np.isfinite(data["f"].astype(float)) & np.isfinite(data["y"].astype(float))]

    pos = data[data["f"] > 0]
    n_pos = int(len(pos))
    n_pos_days = int(pos["day"].nunique()) if n_pos else 0
    counts = {
        "grid bars with a positive forecast": n_pos,
        "distinct days of those grid bars": n_pos_days,
        "grid bars (all)": int(len(data)),
        "distinct days (all grid bars)": int(data["day"].nunique()) if len(data) else 0,
    }

    # slope and its day-clustered t
    slope = None
    t = None
    if len(data) >= 3 and data["f"].astype(float).var() > 0:
        x = data["f"].astype(float).values
        y = data["y"].astype(float).values
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        b = float(np.sum(xc * (y - y.mean())) / sxx)
        a = y.mean() - b * x.mean()
        e = y - a - b * x
        score = pd.Series(xc * e).groupby(data["day"].values).sum().values
        G = len(score)
        if G > 1:
            var_b = (G / (G - 1.0)) * float(np.sum(score ** 2)) / sxx ** 2
            if var_b > 0:
                t = float(b / np.sqrt(var_b))
        slope = b

    # supporting check: top fifth of positive forecasts
    sup_val = None
    sup_pass = None
    if n_pos > 0:
        cut = float(np.quantile(pos["f"].astype(float).values, 0.8))
        top = pos[pos["f"].astype(float) >= cut]
        if len(top):
            sup_val = float(top["y"].mean())
            sup_pass = bool(sup_val > 0)

    main = {
        "name": "slope of 2-day return minus normal drift on the forecast (pooled, non-overlapping grid)",
        "value": slope,
        "statistic": {"name": "slope t, cases summed per day (day-clustered)", "value": t} if t is not None else None,
        "threshold": "t >= 2 with the supporting check passing confirms; t <= -2 rejects; otherwise inconclusive",
    }
    support = {
        "name": "mean 2-day return minus normal drift on grid bars in the top fifth of positive forecasts, above 0",
        "value": sup_val,
        "passed": sup_pass,
    }
    reading = ("Grid at positions 0,2,4,... of each window with all grid bars (forecast 0 included) in the regression; "
               "normal drift is the coin's mean 2-day grid return over all its windows; the slope's t uses day-summed "
               "score contributions (cluster-robust, G/(G-1) correction); the top fifth is forecasts at or above the 80th "
               "percentile of positive grid forecasts pooled over coins; the minimum counts count positive-forecast grid bars "
               "with a valid 2-day return, and failing them gives 'not observable'.")

    if n_pos < 200 or n_pos_days < 100:
        status = "not observable"
        decided = (f"Minimum not reached: {n_pos} grid bars with a positive forecast (need 200) over "
                   f"{n_pos_days} distinct days (need 100).")
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-fifth mean excess 2-day return is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger falls are followed by larger further falls than usual."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
