import numpy as np
import pandas as pd


def measure(bars):
    WIDTH_MIN = 2.0
    LOWCLOSE_MIN = 0.8
    EPS = 1e-9

    # ---------- 1. situation check ----------
    active_total = 0
    active_checkable = 0
    active_agree = 0
    coin_rets = {}
    frames = []

    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            high = d["high"].astype(float)
            low = d["low"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)

            r1 = close.pct_change()                      # inside the window only
            sd30 = r1.rolling(30, min_periods=30).std()  # last 30 daily returns, current bar included
            rng = high - low
            width = (rng / close) / sd30
            lowclose = np.where(rng > 0, (high - close) / rng.where(rng > 0), np.nan)
            lowclose = pd.Series(lowclose, index=d.index)

            act = fc != 0
            active_total += int(act.sum())
            checkable = act & width.notna() & lowclose.notna()
            situ = (width >= WIDTH_MIN - EPS) & (lowclose >= LOWCLOSE_MIN - EPS)
            agree = checkable & situ & (fc > 0)
            active_checkable += int(checkable.sum())
            active_agree += int(agree.sum())

            nxt = close.shift(-1) / close - 1.0
            rets_all.append(r1.dropna().values)
            frames.append(pd.DataFrame({
                "coin": coin,
                "day": pd.to_datetime(d["timestamp"], utc=True).dt.floor("D"),
                "forecast": fc.values,
                "next_ret": nxt.values,
            }))
        coin_rets[coin] = np.concatenate(rets_all) if rets_all else np.array([])

    agreement = (active_agree / active_checkable) if active_checkable > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading_base = ("Situation checked from prices as range/close over the ddof-1 std of the last 30 in-window daily "
                    "returns (current bar included) >= 2 and (high-close)/(high-low) >= 0.8 with a long forecast, on the "
                    "active bars where 30 prior returns exist in the window (the rising-calm profile, needing 60/365-bar "
                    "histories, is not recomputed); t groups cases per UTC day by summing their deviations; the "
                    "30-day minimum is reported as not observable; cases with the median forecast go to the lower group")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "active bars checkable": int(active_checkable)},
            "decided_by": ("Fewer than 90 % of the checkable active bars are wide (>= 2 return std) low-close "
                           "(bottom fifth) days with a long forecast, as the Fidelity's situation and side require."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    allf = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(
        columns=["coin", "day", "forecast", "next_ret"])
    cases = allf[(allf["forecast"] > 0) & allf["next_ret"].notna()].copy()
    cases["mean_ret"] = cases["coin"].map(
        lambda c: float(np.mean(coin_rets[c])) if len(coin_rets[c]) else np.nan)
    cases = cases[cases["mean_ret"].notna()]
    cases["excess"] = cases["next_ret"] - cases["mean_ret"]

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"distinct days with cases": n_days, "cases": n_cases}

    mean_ex = float(cases["excess"].mean()) if n_cases else None
    t = None
    if n_cases > 0 and n_days > 1:
        dev = cases["excess"] - mean_ex
        S = dev.groupby(cases["day"]).sum().values
        var_tot = (n_days / (n_days - 1.0)) * float(np.sum(S ** 2))
        se = np.sqrt(var_tot) / n_cases
        if se > 0:
            t = float(mean_ex / se)

    sup_val, sup_pass = None, None
    if n_cases > 0:
        med = float(cases["forecast"].median())
        hi = cases.loc[cases["forecast"] > med, "excess"]
        lo = cases.loc[cases["forecast"] <= med, "excess"]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {
        "name": "mean excess next-bar return of cases with forecast > 0 (vs coin's all-window mean daily return)",
        "value": mean_ex,
        "statistic": None if t is None else {"name": "t of the mean, cases grouped by day", "value": t},
        "threshold": "confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2",
    }
    sup = {"name": "mean excess above median forecast minus at/below median", "value": sup_val, "passed": sup_pass}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} distinct days with cases, fewer than the plan's minimum of 30."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean excess return could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean excess return is above 0 with t >= 2 and the supporting check passes."
        else:
            status = "inconclusive"
            decided = "The mean excess return is above 0 with t >= 2 but the supporting check fails."
    elif mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "The mean excess return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base + ".",
    }
