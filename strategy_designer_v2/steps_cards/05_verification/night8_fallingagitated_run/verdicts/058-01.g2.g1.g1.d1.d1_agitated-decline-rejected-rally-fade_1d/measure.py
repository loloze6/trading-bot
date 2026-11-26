import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"

    # ---------- collect per-bar data (within windows only) ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce")
            nxt = close.shift(-1)
            r1 = nxt / close - 1.0
            rets_all.append(r1.dropna().values)
            prev1 = close.shift(1)
            prev2 = close.shift(2)
            # up-close streak of exactly 1: today up, yesterday not up (flat counts as not up)
            streak_known = prev1.notna() & prev2.notna() & close.notna()
            streak1 = (close > prev1) & (prev1 <= prev2)
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D")
            out = pd.DataFrame({
                "coin": coin,
                "window": w,
                "day": day,
                "forecast": fc,
                "regime": d["regime"].astype(str),
                "r1": r1,
                "streak_known": streak_known,
                "streak1": streak1,
            })
            rows.append(out)
        coin_rets[coin] = np.concatenate(rets_all) if rets_all else np.array([])

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean drift-removed next-day short-side move on case bars",
                             "value": None, "statistic": None,
                             "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2"},
            "supporting_check": None,
            "counts": {"case-days": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    allb = pd.concat(rows, ignore_index=True)
    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_rets.items()}

    # ---------- situation check ----------
    active = allb[allb["forecast"].notna() & (allb["forecast"] != 0)]
    active_known = active[active["streak_known"]]
    n_active = len(active_known)
    if n_active > 0:
        in_sit = (
            active_known["streak1"]
            & (active_known["regime"] == "mean_reversion")
            & (active_known["forecast"] < 0)
        )
        agreement = float(in_sit.mean())
    else:
        agreement = None
    passed = (agreement is not None) and (agreement >= 0.9)

    reading = (
        "The falling-agitated profile is read from the recorded regime (mean_reversion is only reached when neither "
        "profile veto fires) since the detector's components are not recorded, the up streak of exactly 1 is recomputed "
        "from closes inside each window (first two bars of a window left out of the agreement), and the plan's "
        "'fewer than 30 case-days' is counted as case bars (coin-days) across all coins and windows, treated as a "
        "minimum count giving 'not observable'; the day-clustered t sums deviations per UTC day with an "
        "n_days/(n_days-1) correction."
    )

    main_name = "mean drift-removed next-day short-side move on case bars"
    main_thr = "confirm: mean > 0 with t >= 2 (and supporting difference > 0); reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are first up days after a non-up day inside the "
                           "mean_reversion (falling agitated) regime with a short forecast, so the config does "
                           "not do what the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- main measure ----------
    cases = allb[(allb["regime"] == "mean_reversion") & (allb["forecast"] < 0)].copy()
    cases = cases[cases["r1"].notna()]
    cases["drift"] = cases["coin"].map(drift)
    cases = cases[cases["drift"].notna()]
    cases["move"] = -(cases["r1"] - cases["drift"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"case-days": n_cases, "distinct days with cases": n_days}

    mean_move = float(cases["move"].mean()) if n_cases else None
    t_val = None
    if n_cases > 1 and n_days > 1:
        dev = cases["move"] - mean_move
        D = dev.groupby(cases["day"]).sum().values
        var_mean = (n_days / (n_days - 1.0)) * float(np.sum(D ** 2)) / (n_cases ** 2)
        if var_mean > 0:
            t_val = float(mean_move / np.sqrt(var_mean))

    # ---------- supporting check ----------
    sup_val = None
    sup_pass = None
    if n_cases > 0:
        a = cases["forecast"].abs()
        med = float(a.median())
        hi = cases.loc[a > med, "move"]
        lo = cases.loc[a <= med, "move"]
        if len(hi) > 0 and len(lo) > 0:
            sup_val = float(hi.mean() - lo.mean())
            sup_pass = bool(sup_val > 0)

    main = {
        "name": main_name,
        "value": mean_move,
        "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t_val}
                      if t_val is not None else None),
        "threshold": main_thr,
    }
    supporting = {
        "name": "mean move |forecast| above median minus at or below median",
        "value": sup_val,
        "passed": sup_pass,
    }

    # ---------- decision ----------
    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} case-days across all coins and windows, below the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed (no spread across days)."
    elif mean_move > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = ("Mean drift-removed short-side move is above 0 with t >= 2 and the supporting "
                       "difference is above 0.")
        else:
            status = "inconclusive"
            decided = ("The main measure meets the confirm rule (mean > 0, t >= 2) but the supporting "
                       "difference is not above 0.")
    elif mean_move < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean drift-removed short-side move is below 0 with t <= -2: these days are followed by further rises."
    else:
        status = "inconclusive"
        decided = "The t of the main measure lies strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
