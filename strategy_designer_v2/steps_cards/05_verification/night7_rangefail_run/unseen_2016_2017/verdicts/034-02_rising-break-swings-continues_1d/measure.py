import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    PERIOD = 20
    LHV = "debug_info.components.brk_dist.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            lhv = df[LHV].astype(float).values if LHV in df.columns else np.full(len(df), np.nan)
            prior_max = pd.Series(close).shift(1).rolling(PERIOD, min_periods=PERIOD).max().values
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                if np.isfinite(lhv[i]):
                    in_sit = lhv[i] > 0
                elif np.isfinite(prior_max[i]):
                    in_sit = close[i] > prior_max[i]
                else:
                    in_sit = False
                if in_sit and fc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "forecast-weighted mean excess 5-bar return"
    main_thr = "confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2"
    sup_name = "Spearman correlation of forecast with 5-bar excess return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars with the close above the "
                          "highest close of the prior 20 bars, the plan's breakout situation on its long side.",
            "reading": "The situation is the breakout (recorded distance > 0, or recomputed from closes); the rising-profile "
                       "veto is code-added and only removes bars, so it is not required of active bars.",
        }

    # ---------- 2. coin mean 5-bar return over all windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df.sort_values("timestamp")["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases: bets of the forecast, once per grid cell ----------
    cases = []  # (day, forecast, excess)
    for coin, wins in bars.items():
        cm = coin_mean[coin]
        if not np.isfinite(cm):
            continue
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            fc = df["forecast"].astype(float).fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            side = 0
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                s = int(np.sign(f))
                if s == 0:
                    side = 0
                    low = 0.0
                    continue
                if s != side:
                    side = s
                    low = 0.0
                mag = abs(f)
                if mag - low >= BAND:
                    bet[i] = True
                    low = mag
                else:
                    low = min(low, mag)
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n or not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] <= 0:
                    continue
                r = c[i + H] / c[i] - 1.0
                cases.append((ts.iloc[i].strftime("%Y-%m-%d"), float(fc[i]), r - cm))

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct days": int(n_days)}
    reading = ("A case is a holding-period bet of the forecast (a rise of at least 2 points from its lowest level on its "
               "side since the last bet), the first one in each 5-bar grid cell of a window; the t of the weighted mean "
               "sums the weighted deviations per day; the plan's 'fewer than 30 cases/days' is reported as not observable.")

    if n_cases < 30 or n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "The plan's minimum of 30 cases on 30 distinct days is not reached.",
            "reading": reading,
        }

    d = pd.DataFrame(cases, columns=["day", "w", "x"])
    sw = d["w"].sum()
    m = float((d["w"] * d["x"]).sum() / sw)
    dev = d["w"] * (d["x"] - m)
    D = dev.groupby(d["day"]).sum().values
    G = len(D)
    var_m = (G / (G - 1.0)) * np.sum(D ** 2) / (sw ** 2)
    se = float(np.sqrt(var_m))
    t = float(m / se) if se > 0 else 0.0

    rho = stats.spearmanr(d["w"].values, d["x"].values).correlation
    rho = float(rho) if np.isfinite(rho) else None
    sup_pass = bool(rho is not None and rho > 0)

    if m > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The forecast-weighted mean excess 5-bar return is above 0 with t >= 2 and the Spearman correlation is above 0."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The forecast-weighted mean excess 5-bar return is below 0 with t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the Spearman correlation is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": m,
                         "statistic": {"name": "t of the weighted mean, cases of one day together", "value": t},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": rho, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
