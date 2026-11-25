import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"

    # ---------- gather per-bar data, window by window (never across windows) ----------
    rows = []
    drift_parts = {}
    for coin, wins in bars.items():
        coin_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").astype(float)
            prev_ret = close / close.shift(1) - 1.0          # bar t's own 1-bar return
            next_ret = close.shift(-1) / close - 1.0         # close[t+1]/close[t]-1, same window
            coin_rets.append(next_ret.dropna().values)
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce").astype(float)
            sub = pd.DataFrame({
                "coin": coin,
                "window": w,
                "day": ts.dt.floor("D"),
                "forecast": fc,
                "prev_ret": prev_ret,
                "next_ret": next_ret,
            })
            rows.append(sub)
        if coin_rets:
            allr = np.concatenate(coin_rets)
            drift_parts[coin] = float(np.mean(allr)) if allr.size else np.nan
        else:
            drift_parts[coin] = np.nan

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean unusual move, next day, short direction", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    data = pd.concat(rows, ignore_index=True)

    # ---------- situation check ----------
    active = data[(data["forecast"].notna()) & (data["forecast"] != 0)]
    # situation: bar t closed up (1-bar return > 0); expected side: short (forecast < 0)
    act_eval = active[active["prev_ret"].notna()]
    n_act = len(act_eval)
    if n_act > 0:
        good = ((act_eval["prev_ret"] > 0) & (act_eval["forecast"] < 0)).sum()
        agreement = float(good) / n_act
    else:
        agreement = 0.0
    passed = bool(n_act > 0 and agreement >= 0.90)

    reading = ("The up-close situation is computed as close[t]/close[t-1]-1 > 0 inside each window, so active bars "
               "on a window's first row (no previous close) are left out of the agreement; cases are bars with a "
               "negative forecast and a next close in the same window, the drift is each coin's mean 1-bar return "
               "pooled over all its windows, the t clusters deviations by UTC day, the thirds are equal-size splits "
               "of the cases sorted by abs(forecast), and the plan's minimum counts lead to 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean unusual move, next day, short direction", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_act)},
            "decided_by": ("Fewer than 90 % of the active bars are up-closing bars with a short forecast, "
                           "so the config does not do what the Fidelity's situation and side say."),
            "reading": reading,
        }

    # ---------- main measure ----------
    cases = data[(data["forecast"] < 0) & data["next_ret"].notna()].copy()
    cases["drift"] = cases["coin"].map(drift_parts)
    cases = cases[cases["drift"].notna() & cases["day"].notna()]
    cases["unusual"] = -(cases["next_ret"] - cases["drift"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    mean_u = float(cases["unusual"].mean()) if n_cases else None
    t_val = None
    if n_cases > 1 and n_days > 1:
        dev = cases["unusual"] - mean_u
        S = dev.groupby(cases["day"]).sum().values
        D = len(S)
        var = (D / (D - 1.0)) * np.sum(S ** 2) / (n_cases ** 2)
        se = np.sqrt(var)
        t_val = float(mean_u / se) if se > 0 else None

    # ---------- supporting check ----------
    diff = None
    sup_pass = None
    if n_cases >= 3:
        srt = cases.assign(absf=cases["forecast"].abs()).sort_values(
            ["absf", "coin", "day"], kind="mergesort")
        parts = np.array_split(np.arange(len(srt)), 3)
        bottom = srt["unusual"].values[parts[0]]
        top = srt["unusual"].values[parts[2]]
        if len(bottom) and len(top):
            diff = float(np.mean(top) - np.mean(bottom))
            sup_pass = bool(diff > 0)

    main = {
        "name": "mean unusual move, next day, short direction",
        "value": mean_u,
        "statistic": {"name": "t of the mean, cases of one day summed", "value": t_val} if t_val is not None else None,
        "threshold": "t >= 2 (with top third beating bottom third) confirms; t <= -2 rejects",
    }
    supporting = {"name": "top-third minus bottom-third mean unusual move by abs(forecast)",
                  "value": diff, "passed": sup_pass}

    # ---------- decision ----------
    if n_cases < 300 or n_days < 200:
        status = "not observable"
        decided_by = (f"The plan's minimum of 300 cases on 200 distinct days is not reached "
                      f"({n_cases} cases on {n_days} days).")
    elif t_val is None:
        status = "inconclusive"
        decided_by = "The t of the mean unusual move could not be computed (zero standard error)."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The mean unusual move has t >= 2 and the top third beats the bottom third."
    elif t_val <= -2:
        status = "rejected"
        decided_by = "The mean unusual move has t <= -2: the next day rises above drift after up days."
    elif t_val >= 2:
        status = "inconclusive"
        decided_by = "The t is >= 2 but the top third does not beat the bottom third."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean unusual move is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
