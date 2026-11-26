import numpy as np
import pandas as pd


def measure(bars):
    fd_raw = "debug_info.components.fall_depth.last_history_value"

    # ---------- pass 1: per coin mean daily return over all windows; situation check ----------
    coin_mu = {}
    active_total = 0
    active_agree = 0
    prepared = {}  # coin -> list of per-window frames

    for coin, wins in bars.items():
        all_r = []
        frames = []
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            r_next = close.shift(-1) / close - 1.0          # inside this window only
            r_today = close / close.shift(1) - 1.0
            ret3_prev = close.shift(1) / close.shift(4) - 1.0  # 3-day return ending yesterday
            d["_r_next"] = r_next
            all_r.append(r_next.dropna().values)

            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            d["_fc"] = fc

            # prior fall: raw recorded value where present, else its sign from prices
            if fd_raw in d.columns:
                raw = pd.to_numeric(d[fd_raw], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            fall = pd.Series(np.where(raw.notna(), raw < 0,
                                      np.where(ret3_prev.notna(), ret3_prev < 0, np.nan)),
                             index=d.index)
            up = pd.Series(np.where(r_today.notna(), r_today > 0, np.nan), index=d.index)
            regime_mr = (d["regime"].astype(str) == "mean_reversion") if "regime" in d.columns \
                else pd.Series(False, index=d.index)

            situ = []
            for i in range(len(d)):
                u, f = up.iloc[i], fall.iloc[i]
                if pd.isna(u) or pd.isna(f):
                    situ.append(bool(regime_mr.iloc[i]))
                else:
                    situ.append(bool(u) and bool(f))
            situ = np.array(situ, dtype=bool)

            act = fc.values != 0
            active_total += int(act.sum())
            active_agree += int((act & situ & (fc.values < 0)).sum())
            frames.append(d)
        coin_mu[coin] = float(np.mean(np.concatenate(all_r))) if len(all_r) and \
            sum(len(a) for a in all_r) > 0 else np.nan
        prepared[coin] = frames

    agreement = (active_agree / active_total) if active_total > 0 else 0.0
    passed = bool(active_total > 0 and agreement >= 0.9)

    main_name = "mean unusual next-day fall after the bounce (sign flipped, coin mean removed)"
    thr = "t >= 2 confirms (with supporting check), t <= -2 rejects"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": None, "distinct days": None, "active bars": int(active_total)},
            "decided_by": ("Fewer than 90% of active bars are up days after a negative scaled 3-day "
                           "fall with a short forecast, so the config does not do what the Fidelity says."),
            "reading": "Up day and prior fall recomputed from prices or the recorded raw value; "
                       "where uncomputable (window start), the recorded regime was used.",
        }

    # ---------- cases ----------
    rows = []
    for coin, frames in prepared.items():
        mu = coin_mu[coin]
        for d in frames:
            m = (d["_fc"] < 0) & d["_r_next"].notna()
            for _, r in d[m].iterrows():
                dev = -(float(r["_r_next"]) - mu)
                rows.append((r["timestamp"].floor("D"), dev, abs(float(r["_fc"]))))
    cases = pd.DataFrame(rows, columns=["day", "dev", "absf"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    value = float(cases["dev"].mean()) if n_cases else None
    t = None
    if n_days >= 2:
        s = cases.groupby("day")["dev"].sum()
        sd = s.std(ddof=1)
        t = float(s.mean() / (sd / np.sqrt(len(s)))) if sd > 0 else None

    diff = None
    sup_pass = None
    if n_cases >= 2:
        med = cases["absf"].median()
        deep = cases.loc[cases["absf"] > med, "dev"]
        shal = cases.loc[cases["absf"] <= med, "dev"]
        if len(deep) and len(shal):
            diff = float(deep.mean() - shal.mean())
            sup_pass = bool(diff > 0)

    counts = {"cases": n_cases, "distinct days": n_days}
    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = "Fewer than 30 cases or fewer than 30 distinct days: the plan's minimum is not reached."
    elif t is not None and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "Main t is 2 or more and the deeper half falls more than the shallower half."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "Main t is -2 or less: the coin rises more than usual the day after these bounces."
    else:
        status = "inconclusive"
        decided = ("Main t of 2 or more but the supporting check fails." if (t is not None and t >= 2)
                   else "Main t lies between -2 and 2.")

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": value,
                         "statistic": ({"name": "t of the mean, cases summed per day", "value": t}
                                       if t is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "deeper minus shallower half mean unusual fall (split at median |forecast|)",
                             "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are bars with forecast < 0 and a next close in the same window; the t is that of the "
                    "per-day sums of deviations; the deeper half is |forecast| strictly above the median, ties going "
                    "to the shallower half; the up day and prior fall come from prices or the recorded raw value, "
                    "with the recorded regime used only where they cannot be computed (a window's first bars)."),
    }
