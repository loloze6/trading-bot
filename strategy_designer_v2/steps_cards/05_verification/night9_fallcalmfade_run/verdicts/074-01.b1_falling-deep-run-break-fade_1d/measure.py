import numpy as np
import pandas as pd


def measure(bars):
    RD_RAW = "debug_info.components.run_depth.last_history_value"
    PERIOD = 60          # PriceEvolutionComponent period (falling profile veto)
    VETO = -10.0         # veto: evolution >= -10 -> chop; falling means evolution < -10
    MIN_CASES = 100

    # ---------- pass 1: coin drift (mean daily return over all windows) ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp")
            c = d["close"].astype(float).values
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- pass 2: situation check and cases ----------
    n_active = 0
    n_agree = 0
    case_rows = []  # (day, weight, gain, drift-adjusted return, |forecast|)

    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float)
            f = pd.to_numeric(d["forecast"], errors="coerce")
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series([""] * len(d))
            rd = pd.to_numeric(d[RD_RAW], errors="coerce") if RD_RAW in d.columns else pd.Series(np.nan, index=d.index)

            prev1 = c.shift(1)
            prev2 = c.shift(2)
            up = c > prev1
            prior_down = prev1 < prev2
            bounce_px = up & prior_down
            # fallback where price lookback is missing (window start): run_depth raw > 0
            no_lb = prev2.isna()
            bounce = bounce_px.copy()
            bounce[no_lb] = (rd[no_lb] > 0).fillna(False)

            evo = (c / c.shift(PERIOD) - 1.0) * 100.0
            falling = evo < VETO
            # fallback where the 60-bar lookback is not in the window: detector did not veto
            no_evo = evo.isna()
            falling = falling.copy()
            falling[no_evo] = (regime[no_evo] != "chop") & (regime[no_evo] != "nan")

            situation = bounce & falling
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (f < 0)).sum())

            nxt = c.shift(-1)
            r1 = nxt / c - 1.0
            day = pd.to_datetime(d["timestamp"], utc=True).dt.floor("D")
            for i in np.where((f < 0).values & np.isfinite(r1.values))[0]:
                adj = float(r1.iloc[i]) - mu
                wt = abs(float(f.iloc[i]))
                case_rows.append((day.iloc[i], wt, -adj, adj, wt))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if n_active == 0 else bool(agreement >= 0.9)

    main_name = "|forecast|-weighted mean drift-adjusted 1-bar short gain on forecast<0 bars"
    threshold = "t >= 2 confirm, t <= -2 reject, over at least 100 cases"
    reading = ("Situation from prices: up close after a down close, falling = 60-bar close change "
               "(percent) below -10, with run_depth raw > 0 and a non-chop regime used only where the "
               "window lacks the price lookback; t is the weighted mean over a day-clustered standard error "
               "(weighted deviations summed per day); halves split at the median |forecast| "
               "(deeper strictly above), compared by unweighted mean drift-adjusted next-day return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": len(case_rows), "active bars": n_active},
            "decided_by": ("Fewer than 90% of non-zero-forecast bars are short bars on the first up close "
                           "after a down run in a falling (60-bar change < -10%) market."),
            "reading": reading,
        }

    n = len(case_rows)
    m = None
    t = None
    n_days = 0
    if n > 0:
        cr = pd.DataFrame(case_rows, columns=["day", "w", "g", "adj", "af"])
        W = cr["w"].sum()
        n_days = int(cr["day"].nunique())
        if W > 0:
            m = float((cr["w"] * cr["g"]).sum() / W)
            dev = cr["w"] * (cr["g"] - m)
            D = dev.groupby(cr["day"]).sum().values
            if n_days > 1:
                var = (n_days / (n_days - 1.0)) * float(np.sum(D ** 2)) / (W ** 2)
                se = np.sqrt(var)
                t = float(m / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n > 0:
        med = cr["af"].median()
        deep = cr.loc[cr["af"] > med, "adj"]
        shal = cr.loc[cr["af"] <= med, "adj"]
        if len(deep) > 0 and len(shal) > 0:
            sup_val = float(deep.mean() - shal.mean())
            sup_pass = bool(sup_val <= 0)

    counts = {"cases": n, "days": n_days}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, below the plan's minimum of 100."
    elif t is not None and t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Weighted mean gain t >= 2 over at least 100 cases and the deeper half's drift-adjusted return is not above the shallower half's."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "Weighted mean gain t <= -2 over at least 100 cases: bounce days are followed by rises beyond the drift."
    else:
        status = "inconclusive"
        if t is not None and t >= 2:
            decided = "t >= 2 but the supporting check fails (deeper half not weaker), so inconclusive."
        else:
            decided = "t between -2 and 2 over at least 100 cases: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": m,
            "statistic": ({"name": "t of weighted mean, day-clustered", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "deeper-half minus shallower-half drift-adjusted next-day return <= 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
