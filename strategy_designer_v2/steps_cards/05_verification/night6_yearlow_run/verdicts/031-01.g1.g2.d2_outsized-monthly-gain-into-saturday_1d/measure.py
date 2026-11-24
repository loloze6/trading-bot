import numpy as np
import pandas as pd


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype("float64")
        mx = np.nanmax(np.abs(v.values)) if len(v) else 0
        unit = "ns" if mx > 1e17 else ("us" if mx > 1e14 else ("ms" if mx > 1e11 else "s"))
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def _day_clustered_t(values, days):
    values = np.asarray(values, dtype=float)
    n = len(values)
    if n < 2:
        return None
    m = values.mean()
    dev = pd.Series(values - m).groupby(np.asarray(days)).sum()
    D = len(dev)
    if D < 2:
        return None
    var_sum = float((dev.values ** 2).sum()) * D / (D - 1)
    if var_sum <= 0:
        return None
    se = np.sqrt(var_sum) / n
    return float(m / se)


def measure(bars):
    LH = "debug_info.components.gain20.last_history_value"
    FRI = 4  # Python weekday: Monday 0 ... Friday 4, Saturday 5

    # ---------- per coin: coin's mean daily return over all its windows, and Friday cases ----------
    case_rows = []
    n_active = 0
    n_agree = 0

    for coin, wins in bars.items():
        all_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True).copy()
            d["_ts"] = _to_utc(d["timestamp"]).values
            d["_ts"] = pd.to_datetime(d["_ts"], utc=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            lh = pd.to_numeric(d[LH], errors="coerce") if LH in d.columns else pd.Series(np.nan, index=d.index)

            nxt_close = close.shift(-1)
            nxt_ts = d["_ts"].shift(-1)
            ret = nxt_close / close - 1.0  # inside this window only
            all_rets.append(ret.dropna().values)

            wd = d["_ts"].dt.weekday

            # ---------- situation check ----------
            active = fc != 0
            situation = (wd == FRI) & (lh > 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            # ---------- cases: Friday bar, forecast > 0, next row is Saturday ----------
            nxt_is_sat = nxt_ts.dt.weekday == 5
            sel = (wd == FRI) & (fc > 0) & ret.notna() & nxt_is_sat.fillna(False)
            for i in np.where(sel.values)[0]:
                coin_rows.append({
                    "coin": coin,
                    "day": d["_ts"].iloc[i].strftime("%Y-%m-%d"),
                    "forecast": float(fc.iloc[i]),
                    "ret": float(ret.iloc[i]),
                })
        allr = np.concatenate(all_rets) if all_rets else np.array([])
        coin_mean = float(np.mean(allr)) if len(allr) else np.nan
        for r in coin_rows:
            r["excess"] = r["ret"] - coin_mean
            case_rows.append(r)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else bool(agreement >= 0.9)

    main_name = "mean of forecast x excess Saturday return over Friday cases"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2"
    reading = ("A case is a Friday-start (UTC) bar with forecast > 0 whose next row in the same window is the Saturday bar; "
               "the coin's mean daily return is over all next-row returns of all its windows; the day-clustered t sums "
               "deviations per Friday with a D/(D-1) correction; the top fifth per coin is the ceil(20%) highest forecasts "
               "(stable order on ties); fewer than the plan's minimum counts gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are Friday bars with a positive 20-day "
                           "scaled gain and a long forecast, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "forecast", "ret", "excess"])
    cases = cases.dropna(subset=["forecast", "excess"])
    n_cases = int(len(cases))
    n_fridays = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct Fridays": n_fridays}

    value = None
    tstat = None
    if n_cases > 0:
        prod = (cases["forecast"] * cases["excess"]).values
        value = float(prod.mean())
        tstat = _day_clustered_t(prod, cases["day"].values)

    # ---------- supporting check ----------
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        is_top = pd.Series(False, index=cases.index)
        for coin, g in cases.groupby("coin", sort=True):
            k = int(np.ceil(len(g) * 0.2))
            if k <= 0:
                continue
            order = g.sort_values("forecast", ascending=False, kind="mergesort")
            is_top.loc[order.index[:k]] = True
        top = cases.loc[is_top, "excess"]
        rest = cases.loc[~is_top, "excess"]
        if len(top) > 0 and len(rest) > 0:
            sup_val = float(top.mean() - rest.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    sit = {"agreement": (float(agreement) if agreement is not None else None), "passed": bool(passed)}
    mm = {"name": main_name, "value": value,
          "statistic": ({"name": "t of the mean, cases of the same Friday summed", "value": float(tstat)}
                        if tstat is not None else None),
          "threshold": threshold}
    sc = {"name": "top fifth minus rest of positive cases, excess Saturday return", "value": sup_val,
          "passed": sup_pass}

    if n_cases < 100 or n_fridays < 50:
        status = "not observable"
        decided = (f"The plan's minimum of 100 cases over 50 distinct Fridays is not reached "
                   f"({n_cases} cases, {n_fridays} Fridays).")
    elif tstat is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif value > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule: the mean product is above 0 with t >= 2 and the top fifth beats the rest."
    elif value < 0 and tstat <= -2:
        status = "rejected"
        decided = "Reject rule: the mean product is below 0 with t <= -2."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule: t >= 2 but the supporting check (top fifth minus rest above 0) failed."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": mm,
        "supporting_check": sc,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
