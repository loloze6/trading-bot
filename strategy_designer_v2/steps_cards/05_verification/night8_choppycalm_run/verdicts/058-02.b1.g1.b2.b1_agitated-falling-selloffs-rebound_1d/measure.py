import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    case_rows = []  # (day, coin, forecast, excess_next_return)

    coin_means = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_means[coin] = float(np.mean(allr)) if allr.size else np.nan

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").astype(float)
            # raw value, recomputed from prices where not recorded
            ret1 = close / close.shift(1) - 1.0
            sd20 = ret1.rolling(20, min_periods=20).std(ddof=1)
            recomputed = ret1 / sd20
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").astype(float)
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: a down day (scaled return < 0), expected side long
            situ = raw.notna() & (raw < 0)
            n_agree += int((active & situ & (fc > 0)).sum())

            # cases for the criterion
            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(df["timestamp"], utc=True)
            mu = coin_means.get(coin, np.nan)
            mask = (fc > 0) & nxt.notna() & np.isfinite(nxt)
            for i in np.where(mask.to_numpy())[0]:
                case_rows.append((ts.iloc[i].strftime("%Y-%m-%d"), coin,
                                  float(fc.iloc[i]), float(nxt.iloc[i] - mu)))

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "forecast-weighted mean excess next-day return"
    threshold = "confirm: positive with t >= 2 (and top-minus-bottom third > 0); reject: negative with t <= -2"
    reading = ("Situation bars are bars where the recorded scaled return (recomputed from prices if missing) is below 0, "
               "on the long side; the t is a day-clustered t of the weighted mean (per-day sums of w*(x-mean), "
               "with G/(G-1) correction); thirds are split by sorted forecast with np.array_split and compared "
               "on unweighted mean excess returns; the plan's minimum of 100 cases on 60 days is applied as "
               "'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": len(case_rows), "distinct days": len(set(r[0] for r in case_rows))},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bets on down days "
                           "(scaled one-day return below 0), the plan's situation and side."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["day", "coin", "w", "x"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    # ---------- main measure ----------
    m = None
    t = None
    if n_cases > 0 and cases["w"].sum() > 0:
        W = cases["w"].sum()
        m = float((cases["w"] * cases["x"]).sum() / W)
        dev = cases["w"] * (cases["x"] - m)
        D = dev.groupby(cases["day"]).sum().to_numpy()
        G = len(D)
        if G > 1:
            se = np.sqrt(np.sum(D ** 2) * G / (G - 1)) / W
            t = float(m / se) if se > 0 else None

    # ---------- supporting check ----------
    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        order = cases.sort_values("w", kind="mergesort").reset_index(drop=True)
        parts = np.array_split(np.arange(len(order)), 3)
        bottom = order.loc[parts[0], "x"].mean()
        top = order.loc[parts[2], "x"].mean()
        sup_val = float(top - bottom)
        sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": m,
            "statistic": {"name": "day-clustered t of the weighted mean", "value": t} if t is not None else None,
            "threshold": threshold}
    support = {"name": "top third minus bottom third mean excess next-day return",
               "value": sup_val, "passed": sup_pass}

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = f"The plan's minimum of 100 cases on 60 distinct days is not reached ({n_cases} cases, {n_days} days)."
    elif t is None or m is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The weighted mean excess return is positive with t >= 2 and the top third beats the bottom third."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (positive, t >= 2) but the supporting check fails (top minus bottom <= 0)."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean excess return is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
