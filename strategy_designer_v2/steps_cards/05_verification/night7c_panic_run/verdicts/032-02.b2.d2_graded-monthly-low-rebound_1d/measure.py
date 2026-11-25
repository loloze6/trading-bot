import numpy as np
import pandas as pd


def _to_dt(s):
    if np.issubdtype(s.dtype, np.number):
        v = s.astype(float)
        unit = "ms" if v.abs().max() > 1e11 else "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    DEPTH = "debug_info.components.depth.last_history_value"
    PERIOD = 30

    # ---------- 1. situation check ----------
    n_active = 0
    n_evaluable = 0
    n_agree = 0
    frames = []
    coin_means = {}

    for coin in sorted(bars.keys()):
        rets_all = []
        for w in sorted(bars[coin].keys(), key=lambda x: int(str(x).lstrip("w")) if str(x).lstrip("w").isdigit() else str(x)):
            df = bars[coin][w].copy().reset_index(drop=True)
            if len(df) == 0:
                continue
            df["ts"] = _to_dt(df["timestamp"])
            df = df.sort_values("ts").reset_index(drop=True)
            close = df["close"].astype(float)
            low = df["low"].astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            # next-day return inside the window
            nxt = close.shift(-1) / close - 1.0
            df["ret1"] = nxt
            rets_all.append(nxt.dropna().values)

            # situation from the raw component value and the prices
            prior_low = low.shift(1).rolling(PERIOD, min_periods=PERIOD).min()
            break_px = close < prior_low
            break_px = break_px.where(prior_low.notna(), np.nan)
            if DEPTH in df.columns:
                depth_raw = pd.to_numeric(df[DEPTH], errors="coerce")
                brk = (depth_raw > 0).astype(float).where(depth_raw.notna(), break_px)
            else:
                brk = break_px
            ret30 = close / close.shift(PERIOD) - 1.0
            fall = (ret30 < 0).astype(float).where(ret30.notna(), np.nan)

            active = fc.fillna(0) != 0
            evaluable = active & brk.notna() & fall.notna()
            situation = (brk == 1) & (fall == 1)
            agree = evaluable & situation & (fc > 0)

            n_active += int(active.sum())
            n_evaluable += int(evaluable.sum())
            n_agree += int(agree.sum())

            df["coin"] = coin
            df["fc"] = fc
            frames.append(df[["coin", "ts", "fc", "ret1"]])
        allr = np.concatenate(rets_all) if rets_all else np.array([])
        coin_means[coin] = float(np.mean(allr)) if len(allr) else np.nan

    agreement = (n_agree / n_evaluable) if n_evaluable > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The situation is checked on active bars where it can be evaluated (break from the recorded raw depth > 0, "
               "or from prices if missing; 30-bar return from closes inside the window), bars without 30 prior bars in "
               "their window being left out of the share; the same-day pooled t sums each day's deviations from the mean "
               "(clustered standard error with a D/(D-1) correction); cases equal to the median forecast are in neither group.")

    main_name = "mean next-1-day return on forecast > 0 bars minus coin mean daily return"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 distinct days; reject: t <= -2 over >= 30 distinct days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "evaluable active bars": int(n_evaluable)},
            "decided_by": ("Fewer than 90% of the active bars are long bars where the close is below the prior 30-bar "
                           "low and the 30-bar return is negative, so the config does not do what the Fidelity says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    data = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["coin", "ts", "fc", "ret1"])
    cases = data[(data["fc"] > 0) & data["ret1"].notna()].copy()
    cases["excess"] = cases["ret1"] - cases["coin"].map(coin_means)
    cases = cases[cases["excess"].notna()]
    cases["day"] = cases["ts"].dt.floor("D")

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_ex = float(cases["excess"].mean()) if n_cases else None
    t_val = None
    if n_cases and n_days >= 2:
        dev = cases["excess"] - mean_ex
        s_d = dev.groupby(cases["day"]).sum().values
        var = (n_days / (n_days - 1)) * np.sum(s_d ** 2) / (n_cases ** 2)
        se = float(np.sqrt(var))
        t_val = float(mean_ex / se) if se > 0 else None

    sup_val = None
    if n_cases:
        med = cases["fc"].median()
        hi = cases.loc[cases["fc"] > med, "excess"]
        lo = cases.loc[cases["fc"] < med, "excess"]
        if len(hi) and len(lo):
            sup_val = float(hi.mean() - lo.mean())
    sup_pass = (sup_val is not None) and (sup_val > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"Fewer than 30 distinct days with cases ({n_days}), the plan's minimum count."
    elif t_val is not None and mean_ex > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess return > 0 with t >= 2 over at least 30 distinct days, and the above-minus-below-median check is > 0."
    elif t_val is not None and t_val <= -2:
        status = "rejected"
        decided = "Mean excess return has t <= -2 over at least 30 distinct days."
    elif t_val is not None and t_val >= 2 and not sup_pass:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check (above-median minus below-median excess return > 0) fails."
    else:
        status = "inconclusive"
        decided = "t is between -2 and 2 (or not computable), meeting neither the confirm nor the reject rule."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": {"name": "t of the mean, same-day cases pooled", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess return above median forecast minus below median",
            "value": sup_val,
            "passed": bool(sup_pass) if sup_val is not None else False,
        },
        "counts": {"distinct days with cases": n_days, "cases": n_cases},
        "decided_by": decided,
        "reading": reading,
    }
