import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FC = "forecast"
    RAW = "debug_info.components.mon_thu.last_history_value"
    DAY = pd.Timedelta(days=1)

    # ---------- collect per-coin data ----------
    coin_mu = {}
    active_total = 0
    active_agree = 0
    cases = []  # dicts: coin, date, fc, sat_ret, fri_ret

    for coin, wins in bars.items():
        # coin's mean daily return over all its windows (returns inside each window only)
        all_rets = []
        prepared = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("ts").reset_index(drop=True)
            close = d["close"].astype(float).values
            nxt = np.full(len(d), np.nan)
            if len(d) > 1:
                nxt[:-1] = close[1:] / close[:-1] - 1.0
            d["next_ret"] = nxt
            all_rets.append(pd.Series(nxt).dropna())
            prepared.append(d)
        if all_rets:
            r = pd.concat(all_rets)
            mu = float(r.mean()) if len(r) else np.nan
        else:
            mu = np.nan
        coin_mu[coin] = mu

        for d in prepared:
            n = len(d)
            ts = d["ts"]
            close = d["close"].astype(float).values
            fc = pd.to_numeric(d[FC], errors="coerce").values
            raw = (pd.to_numeric(d[RAW], errors="coerce").values
                   if RAW in d.columns else np.full(n, np.nan))
            ts_list = list(ts)
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                active_total += 1
                t_i = ts_list[i]
                is_friday = t_i.weekday() == 4  # bar whose next bar is Saturday
                # side: Monday-close to Thursday-close return, from prices; raw value as fallback
                side = np.nan
                if i >= 4 and ts_list[i - 1] == t_i - DAY and ts_list[i - 4] == t_i - 4 * DAY:
                    mt = close[i - 1] / close[i - 4] - 1.0
                    if np.isfinite(mt):
                        side = np.sign(mt)
                if not np.isfinite(side) and np.isfinite(raw[i]):
                    side = np.sign(raw[i])
                if is_friday and np.isfinite(side) and side != 0 and np.sign(f) == side:
                    active_agree += 1

                # cases for the criterion: Friday bars with a non-zero forecast
                if not is_friday:
                    continue
                if i + 1 >= n:
                    continue
                sat = d["next_ret"].iloc[i]
                if not np.isfinite(sat):
                    continue
                fri = np.nan
                if i >= 1:
                    fri = close[i] / close[i - 1] - 1.0
                cases.append({
                    "coin": coin,
                    "date": t_i.normalize(),
                    "fc": float(f),
                    "sat_ret": float(sat),
                    "fri_ret": float(fri) if np.isfinite(fri) else np.nan,
                })

    threshold_txt = ("confirm: mean > 0 with date-clustered t >= 2 and positive forecast coefficient; "
                     "reject: mean < 0 with t <= -2; at least 100 distinct Fridays with cases")
    main_name = "mean of forecast/10 x (Saturday return - coin mean daily return) over Friday cases"
    reading = ("Friday is the bar whose UTC start timestamp is a Friday and the Monday-to-Thursday side is taken from "
               "close[t-1]/close[t-4]-1 (falling back on the sign of the raw mon_thu value when those bars are missing); "
               "the date-summed t is the cluster-robust t of the mean (deviations summed per date, G/(G-1) correction); "
               "the regression uses OLS with an intercept on cases with Friday's return available; and the plan's "
               "minimum of 100 distinct Fridays is applied as 'not observable' when unmet.")

    if active_total == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"distinct Fridays with cases": 0, "cases": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 100 distinct Fridays with cases is not reached.",
            "reading": reading,
        }

    agreement = active_agree / active_total
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Friday bars whose forecast sign "
                           "matches the sign of the Monday-to-Thursday return, as the Fidelity requires."),
            "reading": reading,
        }

    cdf = pd.DataFrame(cases)
    if len(cdf):
        cdf["mu"] = cdf["coin"].map(coin_mu)
        cdf["excess"] = cdf["sat_ret"] - cdf["mu"]
        cdf["val"] = cdf["fc"] / 10.0 * cdf["excess"]
        cdf = cdf[np.isfinite(cdf["val"])]
    n_cases = int(len(cdf))
    n_fridays = int(cdf["date"].nunique()) if n_cases else 0

    mean_val = float(cdf["val"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2:
        dev = cdf["val"] - mean_val
        S = dev.groupby(cdf["date"]).sum().values
        G = len(S)
        if G >= 2:
            var = (G / (G - 1.0)) * float(np.sum(S ** 2)) / (n_cases ** 2)
            if var > 0:
                t_val = float(mean_val / np.sqrt(var))

    # supporting regression
    coef = None
    sub = cdf.dropna(subset=["excess", "fc", "fri_ret"]) if n_cases else cdf
    if n_cases and len(sub) >= 4:
        X = np.column_stack([np.ones(len(sub)), sub["fc"].values, sub["fri_ret"].values])
        y = sub["excess"].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        coef = float(beta[1])
    sup_passed = None
    if coef is not None and mean_val is not None:
        sup_passed = bool(np.sign(coef) == np.sign(mean_val) and mean_val != 0)

    counts = {"distinct Fridays with cases": n_fridays, "cases": n_cases,
              "regression cases": int(len(sub)) if n_cases else 0}

    if n_fridays < 100:
        status = "not observable"
        decided = f"Only {n_fridays} distinct Fridays with cases, below the plan's minimum of 100."
    elif t_val is None:
        status = "inconclusive"
        decided = "The date-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_val > 0 and t_val >= 2:
        if coef is not None and coef > 0:
            status = "confirmed"
            decided = "The main measure is positive with t >= 2 and the forecast's regression coefficient is positive."
        else:
            status = "inconclusive"
            decided = "t >= 2 but the supporting forecast coefficient is not positive, which the plan calls inconclusive."
    elif mean_val < 0 and t_val <= -2:
        status = "rejected"
        decided = "The main measure is negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean, cases of one date summed", "value": t_val}
                          if t_val is not None else None),
            "threshold": threshold_txt,
        },
        "supporting_check": {
            "name": "forecast coefficient in OLS of Saturday excess return on forecast and Friday return",
            "value": coef,
            "passed": sup_passed,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
