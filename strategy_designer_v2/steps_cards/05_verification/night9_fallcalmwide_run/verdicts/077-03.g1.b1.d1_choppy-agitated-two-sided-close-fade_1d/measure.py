import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.close_off_mid.last_history_value"
    PROFILE_REGIME = "unknown"  # the config's only strategy regime: inside the choppy-agitated profile
    MIN_CASES = 100
    MIN_DAYS = 50

    # ---------- coin drift: mean daily return over all windows of the coin ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) < 2:
                continue
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            r = c[1:] / c[:-1] - 1.0
            rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- collect bars ----------
    n_active = 0
    n_agree = 0
    case_rows = []  # (day, forecast, drift-adjusted next return)
    for coin, wins in bars.items():
        mu = coin_mu.get(coin, np.nan)
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            high = pd.to_numeric(df["high"], errors="coerce").to_numpy(dtype=float)
            low = pd.to_numeric(df["low"], errors="coerce").to_numpy(dtype=float)
            regime = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            # off-middle sign: from the raw value, or from prices where the raw value is missing
            price_off = 2.0 * (close - (high + low) / 2.0) / close
            off = np.where(np.isfinite(raw), raw, price_off)
            expected = -np.sign(off)  # fade: short above mid, long below

            in_profile = regime == PROFILE_REGIME
            situation = in_profile & np.isfinite(off) & (off != 0)

            active = np.isfinite(f) & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (np.sign(f) == expected)).sum())

            # next-day returns inside the window
            nxt = np.full(len(df), np.nan)
            if len(df) >= 2:
                nxt[:-1] = close[1:] / close[:-1] - 1.0
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D")
            for i in np.where(active & np.isfinite(nxt))[0]:
                if not np.isfinite(mu):
                    continue
                case_rows.append((ts.iloc[i], f[i], nxt[i] - mu))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90
    situation_check = {"agreement": float(agreement), "passed": bool(passed)}

    main_name = "t of the daily mean of forecast/10-weighted drift-adjusted next-day returns"
    main_thr = "confirm if t >= 2 with supporting check passing; reject if t <= -2"
    sup_name = "top-third minus bottom-third |forecast| mean drift-adjusted next-day return in forecast direction"
    reading = ("Profile bars are those whose recorded regime is the config's strategy regime 'unknown' (not 'chop'), "
               "the expected side is the opposite sign of the close's off-mid distance (raw value, prices where missing), "
               "cases are all active bars with a next bar in the window, days are UTC calendar days, and thirds are "
               "the lowest and highest n//3 cases ranked by |forecast| with unweighted means.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": situation_check,
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are choppy-agitated profile bars "
                           "faded against the close's side of mid-range (agreement %.3f)." % agreement),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["day", "f", "ra"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    # main measure
    t_val = None
    mean_daily = None
    if n_cases:
        cases["w"] = cases["f"] / 10.0 * cases["ra"]
        daily = cases.groupby("day")["w"].sum().to_numpy(dtype=float)
        if daily.size >= 2:
            sd = float(np.std(daily, ddof=1))
            mean_daily = float(np.mean(daily))
            t_val = float(mean_daily / (sd / np.sqrt(daily.size))) if sd > 0 else 0.0
        elif daily.size == 1:
            mean_daily = float(daily[0])

    # supporting check
    sup_val = None
    if n_cases >= 3:
        k = n_cases // 3
        order = np.argsort(np.abs(cases["f"].to_numpy()), kind="mergesort")
        dir_ret = (np.sign(cases["f"].to_numpy()) * cases["ra"].to_numpy())
        bottom = dir_ret[order[:k]]
        top = dir_ret[order[-k:]]
        sup_val = float(np.mean(top) - np.mean(bottom))
    sup_pass = (sup_val is not None) and (sup_val > 0)

    main_measure = {
        "name": main_name,
        "value": mean_daily,
        "statistic": {"name": "t of the mean over days", "value": t_val} if t_val is not None else None,
        "threshold": main_thr,
    }
    supporting = {"name": sup_name, "value": sup_val, "passed": bool(sup_pass) if sup_val is not None else None}

    if n_cases < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = ("The plan's minimum of %d cases on %d distinct days is not reached (%d cases, %d days)."
                   % (MIN_CASES, MIN_DAYS, n_cases, n_days))
    elif t_val is None:
        status = "not observable"
        decided = "The main t could not be computed."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main t is 2 or more and the top-third minus bottom-third difference is above 0."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more but the supporting check fails (difference not above 0)."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main t is -2 or less: the next day continues the close's direction, net of drift."
    else:
        status = "inconclusive"
        decided = "The main t is between -2 and 2."

    return {
        "status": status,
        "situation_check": situation_check,
        "main_measure": main_measure,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
