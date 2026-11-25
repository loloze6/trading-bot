import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    COL_POS = "postRebalance_current_allocation"
    TOL = 1e-12

    # ---------- per-coin mean daily return over all windows (inside windows only) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check and case collection ----------
    n_active = 0
    n_agree = 0
    n_active_uncomputable = 0
    cases = []  # (day, excess, |forecast|)

    for coin, wins in bars.items():
        mu = coin_mean[coin]
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)

            # raw regime-detector components, recomputed from prices inside the window
            diff_abs = close.diff().abs()
            path = diff_abs.rolling(30, min_periods=30).sum()
            net = (close - close.shift(30)).abs()
            er = net / path
            er = er.where(path > 0)
            r30 = close / close.shift(30) - 1.0
            r7 = close / close.shift(7) - 1.0

            computable = er.notna() & r30.notna() & r7.notna()
            situ = computable & (er <= 0.3 + TOL) & (
                ((r30 > 0) & (r7 > 0)) | ((r30 < 0) & (r7 < 0))
            )
            exp_side = np.sign(r7)

            active = fc.notna() & (fc != 0)
            act_comp = active & computable
            n_active_uncomputable += int((active & ~computable).sum())
            n_active += int(act_comp.sum())
            agree = act_comp & situ & (np.sign(fc) == exp_side)
            n_agree += int(agree.sum())

            # cases: regime active and a position held, next-day return inside the window
            pos = df[COL_POS].astype(float) if COL_POS in df.columns else pd.Series(np.nan, index=df.index)
            nxt = close.shift(-1) / close - 1.0
            reg = df["regime"].astype(str) == "trending"
            m = reg & pos.notna() & (pos != 0) & nxt.notna() & fc.notna()
            if m.any() and np.isfinite(mu):
                ts = pd.to_datetime(df.loc[m, "timestamp"], utc=True).dt.floor("D")
                exc = np.sign(pos[m].values) * (nxt[m].values - mu)
                for d, e, a in zip(ts.values, exc, np.abs(fc[m].values)):
                    cases.append((d, float(e), float(a)))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading_base = (
        "Situation recomputed per window from closes (ER = |close[t]-close[t-30]| / sum of 30 absolute daily changes, "
        "30- and 7-day close-to-close returns, side = sign of the 7-day return) and agreement taken over active bars "
        "where it is computable (first 30 bars of each window left out); cases are bars with regime 'trending' and a "
        "non-zero position, the coin mean is the mean of all its within-window daily returns, the main t is clustered "
        "by calendar day (deviations summed per day), and the top half is |forecast| above its median among the cases, "
        "the bottom half at or below it."
    )

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": n_active,
                       "active bars not computable": n_active_uncomputable},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are bars where the 30-day efficiency "
                           "ratio is at or below 0.3 with the 30- and 7-day returns sharing a sign and the forecast "
                           "on the 7-day move's side."),
            "reading": reading_base,
        }

    # ---------- main measure ----------
    cdf = pd.DataFrame(cases, columns=["day", "exc", "absf"])
    n = len(cdf)
    n_days = int(cdf["day"].nunique()) if n else 0

    mean = float(cdf["exc"].mean()) if n else None
    t = None
    if n >= 2 and n_days >= 2:
        dev = cdf["exc"] - mean
        S = dev.groupby(cdf["day"]).sum().values
        var_mean = (n_days / (n_days - 1)) * np.sum(S ** 2) / (n ** 2)
        se = np.sqrt(var_mean)
        t = float(mean / se) if se > 0 else None

    # ---------- supporting check ----------
    diff = None
    welch_t = None
    sup_pass = None
    if n >= 4:
        med = cdf["absf"].median()
        top = cdf.loc[cdf["absf"] > med, "exc"].values
        bot = cdf.loc[cdf["absf"] <= med, "exc"].values
        if len(top) >= 2 and len(bot) >= 2:
            diff = float(np.mean(top) - np.mean(bot))
            wt = stats.ttest_ind(top, bot, equal_var=False).statistic
            welch_t = float(wt) if np.isfinite(wt) else None
            sup_pass = bool(diff > 0)

    counts = {"in-regime position-days": int(n), "distinct days": n_days}

    main = {
        "name": "mean of sign(position) x (next-day return - coin mean daily return) on in-regime position bars",
        "value": mean,
        "statistic": {"name": "t of the mean, clustered by day", "value": t} if t is not None else None,
        "threshold": "confirm: mean > 0 with t >= 2 (and top-minus-bottom difference > 0); reject: mean < 0 with t <= -2",
    }
    sup = {
        "name": "mean excess, top half minus bottom half of |forecast| (Welch t %s)" %
                ("%.3f" % welch_t if welch_t is not None else "n/a"),
        "value": diff,
        "passed": sup_pass,
    }

    if n < 200 or n_days < 100:
        status = "not observable"
        decided = ("Fewer than 200 in-regime position-days or fewer than 100 distinct days "
                   "(%d cases on %d days)." % (n, n_days))
    elif t is None or mean is None:
        status = "inconclusive"
        decided = "The main t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main mean is above 0 with t >= 2 and the top-half minus bottom-half difference is above 0."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the top-half minus bottom-half difference is not above 0."
    elif mean < 0 and t <= -2:
        status = "rejected"
        decided = "The main mean is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2 (or its sign disagrees with the mean's), meeting neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
