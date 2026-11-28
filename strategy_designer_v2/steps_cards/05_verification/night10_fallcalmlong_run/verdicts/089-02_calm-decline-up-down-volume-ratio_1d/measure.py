import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.updown_vol.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            # falling calm profile = no veto fired = regime "unknown" (the only regime with a strategy)
            in_profile = regime == "unknown"
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # lean: log up/down volume ratio > 0 (standardise keeps the sign; clip at 0 keeps positives)
            lean_up = raw.notna() & (raw > 0)
            situation_long = in_profile & lean_up & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situation_long).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.90
    else:
        agreement = None
        passed = True

    reading = ("The falling calm profile is read from the recorded regime ('unknown' = neither veto fired, "
               "since the 365-bar volatility percentile cannot be rebuilt from the windows' bars) and the lean "
               "from the raw log ratio being above 0 with a long forecast; the coin's mean 5-bar return is the mean "
               "over all its non-overlapping grid returns of all its windows; the clustered t uses the weighted-mean "
               "deviations summed per UTC day with a G/(G-1) correction; the plan's minimum counts lead to "
               "'not observable' as the workflow requires.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation on the long side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are falling calm bars (regime "
                           "'unknown') with a positive up/down volume lean and a long forecast, as the Fidelity states."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                coin_rows.append({
                    "coin": coin,
                    "ret": c1 / c0 - 1.0,
                    "f": fc[i],
                    "day": ts.iloc[i].normalize(),
                })
        if coin_rows:
            cdf = pd.DataFrame(coin_rows)
            cdf["excess"] = cdf["ret"] - cdf["ret"].mean()
            rows.append(cdf)

    if rows:
        allc = pd.concat(rows, ignore_index=True)
        cases = allc[allc["f"].notna() & (allc["f"] > 0) & allc["excess"].notna()].copy()
    else:
        cases = pd.DataFrame(columns=["coin", "ret", "f", "day", "excess"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases with forecast > 0": n_cases, "distinct days": n_days}

    m = None
    t = None
    rho = None
    if n_cases > 0:
        f = cases["f"].values.astype(float)
        x = cases["excess"].values.astype(float)
        sf = f.sum()
        m = float((f * x).sum() / sf)
        if n_days >= 2:
            e = f * (x - m) / sf
            g = pd.Series(e).groupby(cases["day"].values).sum().values
            G = len(g)
            var = (g ** 2).sum() * G / (G - 1)
            if var > 0:
                t = float(m / np.sqrt(var))
        if n_cases >= 3 and np.std(f) > 0 and np.std(x) > 0:
            r = stats.spearmanr(f, x).correlation
            rho = float(r) if np.isfinite(r) else None

    main = {
        "name": "forecast-weighted mean 5-bar excess return (forecast > 0, non-overlapping grid)",
        "value": m,
        "statistic": {"name": "t of the weighted mean, clustered by day", "value": t} if t is not None else None,
        "threshold": "confirm: above 0 with t >= 2 (and Spearman > 0); reject: below 0 with t <= -2",
    }
    sup_passed = None if rho is None else bool(rho > 0)
    support = {"name": "Spearman correlation forecast vs 5-bar excess return", "value": rho, "passed": sup_passed}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases with forecast > 0 (need 30) "
                   f"on {n_days} distinct days (need 20).")
    elif m is None or t is None:
        status = "inconclusive"
        decided = "The clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "The weighted mean excess return is above 0 with t >= 2 and the Spearman correlation is above 0."
        else:
            status = "inconclusive"
            decided = "A confirming t (>= 2, mean above 0) whose Spearman correlation is 0 or below is inconclusive."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean excess return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": bool(passed)},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
