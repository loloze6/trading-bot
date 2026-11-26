import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    GB = "debug_info.components.giveback.last_history_value"
    BAND = 2.0

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    drift = {}
    case_rows = []

    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            regime = df["regime"].astype(str).values
            gb = (pd.to_numeric(df[GB], errors="coerce").values
                  if GB in df.columns else np.full(len(df), np.nan))
            n = len(df)

            # next-day returns inside the window
            nxt = np.full(n, np.nan)
            if n > 1:
                nxt[:-1] = close[1:] / close[:-1] - 1.0
            all_rets.append(nxt[~np.isnan(nxt)])

            # up day from prices; first row of a window has no prior close in the record,
            # there the detector's ret1 > 0 rule (regime 'trending') stands in
            up = np.zeros(n, dtype=bool)
            if n > 1:
                up[1:] = close[1:] > close[:-1]
            up[0] = regime[0] == "trending"
            # falling agitated profile: the detector's profile_trend / profile_swing are not recorded
            # and need 365 bars of history, so the profile is read from regime 'trending'
            profile = regime == "trending"
            gb_ok = np.where(np.isnan(gb), True, gb <= 0)
            situation = up & profile & gb_ok

            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # ---------- cases: short bets (rise of the short forecast of at least the band) ----------
            ts = pd.to_datetime(df["timestamp"], utc=True).dt.floor("D").values
            side = 0
            ref = 0.0
            for i in range(n):
                f = fc[i]
                s = int(np.sign(f))
                if s == 0:
                    side = 0
                    ref = 0.0
                    continue
                if s != side:
                    side = s
                    ref = 0.0
                mag = abs(f)
                if mag - ref >= BAND:
                    ref = mag
                    if s < 0 and not np.isnan(nxt[i]):
                        case_rows.append((coin, ts[i], nxt[i], mag))
                else:
                    ref = min(ref, mag)
        r = np.concatenate(all_rets) if all_rets else np.array([])
        drift[coin] = float(np.mean(r)) if len(r) else np.nan

    agreement = n_agree / n_active if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    reading = ("Cases are the short bets of the workflow's case definition (a rise of the short forecast of at "
               "least 2 points, every bar on the 1-bar grid); the profile part of the situation is read from the "
               "recorded regime 'trending' since its 365-bar components are not recorded, the up day from closes; "
               "the supporting check splits cases at the median |forecast| (top: above, bottom: at or below); "
               "the day-clustered t uses a G/(G-1) correction; fewer than 100 case days gives 'not observable'.")

    main_name = "mean unusual move over the next bar, short direction"
    thr = "confirm t >= 2 with supporting check > 0; reject t <= -2; at least 100 distinct case days"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short up days inside the "
                           "falling agitated profile (agreement %.3f)." % agreement),
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "ret", "absf"])
    if len(cases):
        cases["u"] = -(cases["ret"] - cases["coin"].map(drift))
        cases = cases.dropna(subset=["u"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_u = float(cases["u"].mean()) if n_cases else None
    t_val = None
    if n_cases and n_days > 1:
        dev = cases["u"] - mean_u
        g = dev.groupby(cases["day"]).sum().values
        G = len(g)
        var = (G / (G - 1)) * np.sum(g ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_u / se) if se > 0 else None

    supp_val = None
    if n_cases >= 2:
        med = cases["absf"].median()
        top = cases.loc[cases["absf"] > med, "u"]
        bot = cases.loc[cases["absf"] <= med, "u"]
        if len(top) and len(bot):
            supp_val = float(top.mean() - bot.mean())
    supp_pass = None if supp_val is None else bool(supp_val > 0)

    counts = {"distinct case days": n_days, "cases": n_cases}

    if n_days < 100:
        status = "not observable"
        decided = "Fewer than 100 distinct case days (%d), the plan's minimum." % n_days
    elif t_val is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and supp_pass:
        status = "confirmed"
        decided = "The main measure has t >= 2 and the supporting check is positive."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main measure has t <= -2: up days are followed by further rises beyond the coin's drift."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main t is >= 2 but the supporting check is <= 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": mean_u,
                         "statistic": ({"name": "t of the mean, clustered by day", "value": t_val}
                                       if t_val is not None else None),
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move, top half |forecast| minus bottom half",
                             "value": supp_val, "passed": supp_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
