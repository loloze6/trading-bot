import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.scaled_fall.last_history_value"
    CONFIRM_T = 2.0
    REJECT_T = -2.0
    MIN_CASES = 200
    MIN_DAYS = 100

    rows = []
    act_total = 0
    act_agree = 0

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        frames = []
        for w in sorted(wins.keys(), key=lambda k: (len(str(k)), str(k))):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
                d = d.assign(_ts=ts).sort_values("_ts", kind="mergesort").reset_index(drop=True)
            else:
                d = d.reset_index(drop=True)
                d["_ts"] = pd.NaT
            close = pd.to_numeric(d["close"], errors="coerce")
            # next-day return inside the window only
            d["_ret1"] = close.shift(-1) / close - 1.0
            d["_fc"] = pd.to_numeric(d["forecast"], errors="coerce")
            if RAW in d.columns:
                d["_raw"] = pd.to_numeric(d[RAW], errors="coerce")
            else:
                d["_raw"] = np.nan
            # agitated profile: the strategy's regime was active (not the 'chop' veto),
            # which is where the component is recorded
            reg = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            d["_profile"] = d["_raw"].notna() & (reg.str.lower() != "chop")
            frames.append(d)
        if not frames:
            continue

        # coin's mean daily return over all windows together
        all_ret = pd.concat([f["_ret1"] for f in frames]).dropna()
        coin_mean = float(all_ret.mean()) if len(all_ret) else np.nan

        for d in frames:
            # situation check
            active = d["_fc"].notna() & (d["_fc"] != 0)
            situ = d["_profile"] & (d["_raw"] < 0)
            agree = active & situ & (d["_fc"] > 0)
            act_total += int(active.sum())
            act_agree += int(agree.sum())

            sel = d["_profile"] & d["_fc"].notna() & d["_ret1"].notna()
            if np.isnan(coin_mean):
                continue
            sub = d.loc[sel]
            for ts, fc, r in zip(sub["_ts"], sub["_fc"], sub["_ret1"]):
                day = ts.floor("D") if pd.notna(ts) else None
                rows.append((coin, day, float(fc), float(r) - coin_mean))

    agreement = (act_agree / act_total) if act_total > 0 else 0.0
    passed = bool(act_total > 0 and agreement >= 0.9)

    main_name = "slope of next-day excess return on forecast, profile bars"
    threshold = "slope t >= 2 confirms (with supporting check), <= -2 rejects"
    reading = ("Profile bars are those where the strategy's regime was active (component recorded, regime not 'chop'); "
               "the coin's mean is the mean 1-day return over all its windows; the slope t uses day-clustered "
               "standard errors (CR1 correction); minimum counts are taken over profile bars with forecast above 0 "
               "and a next-day return inside the window.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(act_total), "active bars in situation on long side": int(act_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are agitated-profile down days "
                           "with a long forecast, so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    data = pd.DataFrame(rows, columns=["coin", "day", "fc", "ex"])
    pos = data[data["fc"] > 0]
    n_pos = int(len(pos))
    n_days = int(pos["day"].nunique()) if n_pos else 0
    counts = {
        "profile bars with forecast above 0": n_pos,
        "distinct days": n_days,
        "profile bars used": int(len(data)),
    }

    # supporting check
    sup_val = float(pos["ex"].mean()) if n_pos else None
    sup_pass = (sup_val is not None) and (sup_val > 0)

    # clustered OLS slope
    slope = None
    tval = None
    n = len(data)
    if n >= 3 and data["fc"].nunique() > 1:
        X = np.column_stack([np.ones(n), data["fc"].to_numpy()])
        y = data["ex"].to_numpy()
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ X.T @ y
        u = y - X @ beta
        keys = data["day"].astype(str).to_numpy()
        meat = np.zeros((2, 2))
        G = 0
        for g in pd.unique(keys):
            m = keys == g
            s = X[m].T @ u[m]
            meat += np.outer(s, s)
            G += 1
        if G >= 2:
            c = (G / (G - 1.0)) * ((n - 1.0) / (n - 2.0))
            V = c * XtX_inv @ meat @ XtX_inv
            se = float(np.sqrt(V[1, 1])) if V[1, 1] > 0 else np.nan
            slope = float(beta[1])
            tval = float(slope / se) if se and np.isfinite(se) and se > 0 else None

    main = {
        "name": main_name,
        "value": slope,
        "statistic": {"name": "slope t, day-clustered", "value": tval} if tval is not None else None,
        "threshold": threshold,
    }
    support = {"name": "mean excess next-day return, forecast > 0", "value": sup_val,
               "passed": bool(sup_pass) if sup_val is not None else None}

    if n_pos < MIN_CASES or n_days < MIN_DAYS:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_pos} profile bars with forecast above 0 (need 200) "
                   f"on {n_days} distinct days (need 100).")
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= CONFIRM_T and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess next-day return over forecast>0 bars is above 0."
    elif tval <= REJECT_T:
        status = "rejected"
        decided = "The slope's t is -2 or less: bigger scaled falls are followed by weaker next days."
    elif tval >= CONFIRM_T:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean excess next-day return is 0 or below."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
