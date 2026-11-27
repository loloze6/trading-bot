import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    REG = "regime"

    # ---------- collect per-bar data, window by window ----------
    rows = []
    all_rets = {}  # coin -> list of 1-bar returns over all windows
    for coin, wins in bars.items():
        coin_rets = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp", kind="mergesort").reset_index(drop=True)
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(d[FC], errors="coerce").to_numpy(dtype=float)
            reg = d[REG].astype(str).to_numpy() if REG in d.columns else np.array([""] * len(d))
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce") if "timestamp" in d.columns \
                else pd.Series([pd.NaT] * len(d))
            n = len(d)
            # next-bar return, inside the window only
            nxt = np.full(n, np.nan)
            if n > 1:
                nxt[:-1] = c[1:] / c[:-1] - 1.0
            coin_rets.extend([x for x in nxt if np.isfinite(x)])
            # up close, and the run of down closes before it (inside the window)
            # situation computable only if bars t-3..t exist (to know the run is >= 2) or run proved shorter
            for t in range(n):
                sit = np.nan
                if t >= 1 and np.isfinite(c[t]) and np.isfinite(c[t - 1]):
                    up = c[t] > c[t - 1]
                    if not up:
                        sit = 0.0
                    else:
                        # count down closes ending at t-1
                        run = 0
                        k = t - 1
                        known = False
                        while k >= 1:
                            if np.isfinite(c[k]) and np.isfinite(c[k - 1]) and c[k] < c[k - 1]:
                                run += 1
                                k -= 1
                                if run >= 2:
                                    known = True
                                    break
                            else:
                                known = True
                                break
                        if run >= 2:
                            sit = 1.0
                        elif known:
                            sit = 0.0
                        else:
                            sit = np.nan  # window start: run length unknown
                rows.append({
                    "coin": coin, "window": wname, "pos": t,
                    "day": ts.iloc[t].floor("D") if pd.notna(ts.iloc[t]) else pd.NaT,
                    "forecast": f[t], "regime": reg[t], "sit": sit, "ret1": nxt[t],
                })
        all_rets[coin] = coin_rets

    data = pd.DataFrame(rows)
    if len(data) == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean 1-day unusual move of cases, short direction", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None, "counts": {"days with cases": 0},
            "decided_by": "No bars in the record.", "reading": "none",
        }

    # ---------- situation check ----------
    active = data[np.isfinite(data["forecast"]) & (data["forecast"] != 0)]
    act_known = active[np.isfinite(active["sit"])]
    if len(act_known) > 0:
        ok = (act_known["sit"] == 1.0) & (act_known["forecast"] < 0) & \
             (act_known["regime"] == "mean_reversion")
        agreement = float(ok.mean())
    else:
        agreement = None
    passed = agreement is not None and agreement >= 0.9
    reading_sit = ("Situation = an up close (close above previous close) ending a run of 2+ down closes, "
                   "computed inside each window from prices, on the detector's mean_reversion regime "
                   "(which carries the falling-agitated profile veto, not recomputable from the record), "
                   "short side; active bars at a window start where the run length is unknown are left out")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean 1-day unusual move of cases, short direction", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars checked": int(len(act_known))},
            "decided_by": ("Fewer than 90% of active bars are short positions on run-breaking up closes "
                           "(2+ down closes) in the mean_reversion regime, as the Fidelity's situation requires."),
            "reading": reading_sit + ".",
        }

    # ---------- main measure ----------
    mu = {coin: (float(np.mean(v)) if len(v) else np.nan) for coin, v in all_rets.items()}
    cases = data[np.isfinite(data["forecast"]) & (data["forecast"] <= -2)].copy()
    cases = cases[np.isfinite(cases["ret1"]) & cases["day"].notna()].copy()
    cases["mu"] = cases["coin"].map(mu)
    cases = cases[np.isfinite(cases["mu"])]
    cases["u"] = -(cases["ret1"] - cases["mu"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        dev = cases["u"] - mean_u
        s_d = dev.groupby(cases["day"]).sum().to_numpy()
        var_mean = (n_days / (n_days - 1.0)) * float(np.sum(s_d ** 2)) / (n_cases ** 2)
        if var_mean > 0:
            t_val = float(mean_u / np.sqrt(var_mean))

    # ---------- supporting check ----------
    sup_val, sup_pass = None, None
    if n_cases >= 3:
        cs = cases.assign(size=cases["forecast"].abs()).sort_values(
            ["size", "day", "coin"], kind="mergesort").reset_index(drop=True)
        k = n_cases // 3
        bottom = cs.iloc[:k]["u"].mean()
        top = cs.iloc[n_cases - k:]["u"].mean()
        sup_val = float(top - bottom)
        sup_pass = bool(sup_val > 0)

    reading = (reading_sit + "; cases = bars with forecast <= -2 and a next close in the same window, the coin's "
               "mean daily return taken over all its windows, t from per-day summed deviations with a D/(D-1) "
               "correction, and thirds as the floor(n/3) smallest and largest |forecast| cases "
               "(ties ordered by day then coin); fewer than 30 days with cases is treated as not observable.")

    main = {"name": "mean 1-day unusual move of cases (forecast <= -2), short direction",
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day pooled", "value": t_val}
                          if t_val is not None else None),
            "threshold": "positive with t >= 2 confirms (with supporting check); negative with t <= -2 rejects"}
    sup = {"name": "mean unusual move top third minus bottom third of forecast size",
           "value": sup_val, "passed": sup_pass}
    counts = {"days with cases": n_days, "cases": n_cases}

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} days with cases, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move could not be computed."
    elif mean_u > 0 and t_val >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Mean unusual move positive with t >= 2 and the top-minus-bottom third check positive."
        else:
            status = "inconclusive"
            decided = "Mean unusual move positive with t >= 2 but the supporting check failed."
    elif mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move negative with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the mean unusual move lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
