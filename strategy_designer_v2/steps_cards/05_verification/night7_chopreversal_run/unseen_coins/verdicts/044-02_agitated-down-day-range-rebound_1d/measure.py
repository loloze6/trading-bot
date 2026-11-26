import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.range_mult.last_history_value"

    # ---------- gather per-coin data ----------
    rows = []
    coin_means = {}
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            close = d["close"].astype(float)
            d["prev_close"] = close.shift(1)
            d["next_ret"] = close.shift(-1) / close - 1.0
            all_rets.append(d["next_ret"].dropna().values)
            d["coin"] = coin
            d["window"] = w
            rows.append(d)
        r = np.concatenate(all_rets) if all_rets else np.array([])
        coin_means[coin] = float(np.mean(r)) if len(r) else np.nan
    if not rows:
        return {"status": "not observable", "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None, "counts": {"cases": 0, "distinct days": 0},
                "decided_by": "no bars in the record", "reading": "none"}
    data = pd.concat(rows, ignore_index=True)
    data["forecast"] = data["forecast"].astype(float)

    # ---------- situation check ----------
    active = data[(data["forecast"] != 0) & data["prev_close"].notna()]
    n_active = len(active)
    if n_active > 0:
        in_sit = (active["close"].astype(float) < active["prev_close"]) & (active["forecast"] > 0)
        agreement = float(in_sit.mean())
    else:
        agreement = 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    reading = ("Situation checked as close below the prior close within the window with a long forecast "
               "(the agitated profile is the code's added filter, not recomputable here; first bars of a window "
               "without a prior close left out); next-bar returns within windows; the coin's mean daily return is "
               "over all its windows' next-bar returns; the main t sums deviations per calendar day (clustered "
               "standard error); the range multiple is the recorded raw range_mult, the wider half being cases "
               "strictly above the coin's median and the narrower half at or below it; the plan's 'fewer cases -> "
               "inconclusive' is reported as 'not observable' per the workflow.")
    if not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agreement, "passed": False},
                "main_measure": None, "supporting_check": None,
                "counts": {"active bars": int(n_active)},
                "decided_by": ("Fewer than 90% of the active bars are down-close bars with a long forecast, "
                               "so the config does not do what the plan's situation (agitated down day, long) says."),
                "reading": reading}

    # ---------- cases ----------
    cases = data[(data["forecast"] > 0) & data["next_ret"].notna()].copy()
    cases["mu"] = cases["coin"].map(coin_means)
    cases["excess"] = cases["next_ret"] - cases["mu"]
    cases["val"] = cases["forecast"] / 10.0 * cases["excess"]
    cases["day"] = pd.to_datetime(cases["timestamp"], utc=True).dt.floor("D")
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique())
    counts = {"cases": n_cases, "distinct days": n_days}

    main_value = float(cases["val"].mean()) if n_cases else None
    main_t = None
    if n_cases > 1 and n_days > 1:
        dev = cases["val"] - cases["val"].mean()
        s = dev.groupby(cases["day"]).sum().values
        var = (s ** 2).sum() / n_cases ** 2 * n_days / (n_days - 1)
        se = np.sqrt(var)
        main_t = float(main_value / se) if se > 0 else None

    # ---------- supporting check ----------
    diff = None
    welch_t = None
    sup = cases[cases[RAW].notna()].copy() if RAW in cases.columns else cases.iloc[0:0]
    if len(sup):
        sup[RAW] = sup[RAW].astype(float)
        med = sup.groupby("coin")[RAW].transform("median")
        wide = sup.loc[sup[RAW] > med, "excess"]
        narrow = sup.loc[sup[RAW] <= med, "excess"]
        if len(wide) > 0 and len(narrow) > 0:
            diff = float(wide.mean() - narrow.mean())
        if len(wide) > 1 and len(narrow) > 1:
            t = stats.ttest_ind(wide.values, narrow.values, equal_var=False).statistic
            welch_t = float(t) if np.isfinite(t) else None
    sup_passed = None if diff is None else bool(diff > 0)

    main_measure = {"name": "mean of forecast/10 x next-bar excess return over cases",
                    "value": main_value,
                    "statistic": None if main_t is None else {"name": "t, cases of one day together", "value": main_t},
                    "threshold": "t >= 2 to confirm, t <= -2 to reject"}
    supporting = {"name": "wide-minus-narrow mean next-bar excess return (split at coin median range multiple)",
                  "value": diff, "passed": sup_passed,
                  "welch_t": welch_t}
    supporting = {k: v for k, v in supporting.items() if k != "welch_t"}
    if welch_t is not None:
        counts_extra = None  # keep counts only
    sit = {"agreement": agreement, "passed": True}

    # ---------- decision ----------
    if n_cases < 200 or n_days < 100:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 200) on {n_days} distinct days (need 100).")
    elif main_t is not None and main_t <= -2:
        status = "rejected"
        decided = f"Reject rule: the main measure's t ({main_t:.2f}) is -2 or less."
    elif welch_t is not None and welch_t <= -2:
        status = "rejected"
        decided = f"Reject rule: the wide-minus-narrow difference has a Welch t ({welch_t:.2f}) of -2 or less."
    elif main_t is not None and main_t >= 2 and diff is not None and diff > 0:
        status = "confirmed"
        decided = f"Confirm rule: main t ({main_t:.2f}) >= 2 and wide-minus-narrow difference ({diff:.5f}) > 0."
    else:
        status = "inconclusive"
        decided = ("Inconclusive rule: neither confirm nor reject met (main t "
                   f"{'n/a' if main_t is None else round(main_t, 2)}, difference "
                   f"{'n/a' if diff is None else round(diff, 6)}, Welch t "
                   f"{'n/a' if welch_t is None else round(welch_t, 2)}).")

    main_measure["threshold"] = ("confirm: t >= 2 with wide-minus-narrow > 0; reject: t <= -2 or difference "
                                 "Welch t <= -2" + ("" if welch_t is None else f" (difference Welch t = {welch_t:.3f})"))

    return {"status": status,
            "situation_check": sit,
            "main_measure": main_measure,
            "supporting_check": supporting,
            "counts": counts,
            "decided_by": decided,
            "reading": reading}
