import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.volfall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            vol = df["volume"].astype(float).values
            fc = df["forecast"].astype(float).values
            raw = df[RAW].astype(float).values if RAW in df.columns else np.full(len(df), np.nan)
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            for t in range(len(df)):
                f = fc[t]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                # 20-day return in percent, from prices inside the window
                if t >= 20 and close[t - 20] > 0:
                    in_sit = (close[t] / close[t - 20] - 1.0) * 100.0 < -10.0
                else:
                    in_sit = reg[t] == "trending"
                # expected side: sign of the 30-day volume change
                side = 0.0
                if t >= 59:
                    m_new = np.nanmean(vol[t - 29:t + 1])
                    m_old = np.nanmean(vol[t - 59:t - 29])
                    if m_new > 0 and m_old > 0:
                        side = np.sign(np.log(m_new / m_old))
                elif np.isfinite(raw[t]):
                    side = np.sign(raw[t])
                if in_sit and side != 0 and np.sign(f) == side:
                    n_agree += 1

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "|forecast|-weighted mean signed 5-day excess return"
    threshold = "confirm if > 0 with t >= 2; reject if < 0 with t <= -2; at least 30 independent days"
    reading = ("The 20-day return is computed from closes inside the window when 20 prior bars exist (else the recorded "
               "regime 'trending' is taken), the expected side is the sign of ln(30-day mean volume / prior 30-day mean) "
               "from volumes when 60 bars exist (else the sign of the raw volfall value); the coin's mean 5-day return is "
               "over the non-overlapping grid of all its windows, the t is a ratio-estimator t with weighted deviations "
               "summed per UTC day, and fewer than 30 independent days is reported as 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "independent days": None},
            "decided_by": ("Fewer than 90 % of the active bars are bars with a 20-day return below -10 % with the forecast's "
                           "sign equal to the sign of the 30-day volume change, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for t in range(0, len(df) - H, H):
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                r = close[t + H] / close[t] - 1.0
                grid_rets.append(r)
                f = fc[t]
                if np.isfinite(f) and f != 0:
                    coin_cases.append((ts.iloc[t].floor("D"), r, f))
        if not grid_rets:
            continue
        mu = float(np.mean(grid_rets))
        for d, r, f in coin_cases:
            rows.append((d, (r - mu) * np.sign(f), abs(f)))

    n_cases = len(rows)
    if n_cases == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"independent days": 0, "cases": 0},
            "decided_by": "No case on the 5-bar grid: fewer than 30 independent days with a case.",
            "reading": reading,
        }

    cdf = pd.DataFrame(rows, columns=["day", "x", "w"])
    cdf["wx"] = cdf["x"] * cdf["w"]
    g = cdf.groupby("day").agg(W=("w", "sum"), S=("wx", "sum"))
    n_days = int(len(g))
    sumW = float(g["W"].sum())
    m = float(g["S"].sum() / sumW) if sumW > 0 else float("nan")

    tval = None
    if n_days >= 2 and sumW > 0:
        e = g["S"].values - m * g["W"].values
        se = np.sqrt(n_days / (n_days - 1.0) * np.sum(e ** 2)) / sumW
        tval = float(m / se) if se > 0 else (float(np.sign(m) * np.inf) if m != 0 else 0.0)

    counts = {"independent days": n_days, "cases": int(n_cases)}
    stat = {"name": "t of the weighted mean, cases of one day summed", "value": tval} if tval is not None else None

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} independent days with a case, below the plan's minimum of 30."
    elif m > 0 and tval is not None and tval >= 2:
        status = "confirmed"
        decided = "Confirm: the weighted mean signed excess return is above 0 with t >= 2 over at least 30 independent days."
    elif m < 0 and tval is not None and tval <= -2:
        status = "rejected"
        decided = "Reject: the weighted mean signed excess return is below 0 with t <= -2 over at least 30 independent days."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the t lies between -2 and 2 with at least 30 independent days."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": m, "statistic": stat, "threshold": threshold},
        "supporting_check": None,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
