import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    rows = []
    sit_flags = []
    reading_parts = []

    # ---------- collect per-coin rows, returns inside windows ----------
    coin_next_rets = {}
    per_coin_frames = {}
    for coin in sorted(bars.keys()):
        frames = []
        all_next = []
        for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            d["_prev_close"] = close.shift(1)
            d["_next_ret"] = close.shift(-1) / close - 1.0
            d["_close"] = close
            d["_coin"] = coin
            d["_win"] = str(w)
            all_next.append(d["_next_ret"])
            frames.append(d)
        if not frames:
            continue
        nr = pd.concat(all_next, ignore_index=True).dropna()
        coin_next_rets[coin] = float(nr.mean()) if len(nr) else np.nan
        per_coin_frames[coin] = frames

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, frames in per_coin_frames.items():
        for d in frames:
            f = pd.to_numeric(d[FC], errors="coerce")
            prev = d["_prev_close"]
            computable = prev.notna() & d["_close"].notna()
            active = f.notna() & (f != 0) & computable
            up = d["_close"] > prev
            n_active += int(active.sum())
            n_agree += int((active & up & (f < 0)).sum())
    if n_active > 0:
        agreement = n_agree / n_active
        passed = bool(agreement >= 0.9)
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are up days (close above the "
                           "previous close) with a negative (short) forecast, as the Fidelity requires."),
            "reading": ("The situation is computed from the closes inside each window; the first bar of a window, "
                        "whose previous close is not in the record, is left out of the agreement."),
        }

    # ---------- up-day cases ----------
    for coin, frames in per_coin_frames.items():
        mu = coin_next_rets.get(coin, np.nan)
        for d in frames:
            f = pd.to_numeric(d[FC], errors="coerce")
            reg = d["regime"].astype(str)
            mask = (reg == "mean_reversion") & f.notna() & d["_next_ret"].notna()
            if not mask.any():
                continue
            sub = d.loc[mask]
            ts = pd.to_datetime(sub["timestamp"], utc=True, errors="coerce")
            excess = sub["_next_ret"] - mu
            fs = f.loc[mask]
            rows.append(pd.DataFrame({
                "coin": coin,
                "win": sub["_win"].values,
                "ts": ts.values,
                "day": ts.dt.floor("D").values,
                "forecast": fs.values.astype(float),
                "excess": excess.values.astype(float),
                "gain": (fs.values.astype(float) / 10.0) * excess.values.astype(float),
            }))
    if rows:
        cases = pd.concat(rows, ignore_index=True)
        cases = cases.dropna(subset=["gain", "day"])
    else:
        cases = pd.DataFrame(columns=["coin", "win", "ts", "day", "forecast", "excess", "gain"])

    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    # ---------- main measure: mean gain, day-clustered t ----------
    mean_gain = None
    t_val = None
    if n_cases >= 2 and n_days >= 2:
        g = cases["gain"].values
        m = float(np.mean(g))
        dev = cases.assign(_dev=g - m).groupby("day")["_dev"].sum().values
        D = len(dev)
        var_mean = (D / (D - 1.0)) * float(np.sum(dev ** 2)) / (n_cases ** 2)
        se = np.sqrt(var_mean)
        mean_gain = m
        t_val = float(m / se) if se > 0 else None
    elif n_cases >= 1:
        mean_gain = float(cases["gain"].mean())

    # ---------- supporting check: deepest third minus shallowest third ----------
    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        srt = cases.sort_values(["forecast", "ts", "coin"], kind="mergesort").reset_index(drop=True)
        k = n_cases // 3
        deep = srt.iloc[:k]["excess"]
        shallow = srt.iloc[n_cases - k:]["excess"]
        sup_val = float(deep.mean() - shallow.mean())
        sup_pass = bool(sup_val < 0)

    counts = {"up-day cases": n_cases, "distinct days": n_days}

    # ---------- decision ----------
    if n_cases < 300 or n_days < 300:
        status = "not observable"
        decided_by = (f"The plan needs at least 300 up-day cases on at least 300 distinct days; the record has "
                      f"{n_cases} cases on {n_days} days.")
    elif t_val is None:
        status = "inconclusive"
        decided_by = "The t of the mean gain could not be computed (zero standard error), so neither rule is met."
    elif mean_gain > 0 and t_val >= 2 and sup_pass:
        status = "confirmed"
        decided_by = ("The mean gain is positive with t >= 2 and the deepest third's mean excess next-day return "
                      "minus the shallowest third's is below 0.")
    elif mean_gain < 0 and t_val <= -2:
        status = "rejected"
        decided_by = "The mean gain is negative with t <= -2."
    elif t_val >= 2:
        status = "inconclusive"
        decided_by = "The mean gain has t >= 2 but the supporting check (deepest minus shallowest third below 0) failed."
    else:
        status = "inconclusive"
        decided_by = "The t of the mean gain lies between -2 and 2."

    reading = ("Up-day cases are the bars whose regime is mean_reversion with a next-day close in the same window, "
               "the coin's mean daily return is over all its windows' next-day returns, the t clusters cases by UTC day "
               "(deviations summed per day, with a D/(D-1) correction), the thirds are n//3 cases each from sorting the "
               "forecast (lowest = deepest), the situation check leaves out each window's first bar, and the plan's "
               "'too few cases' rule is reported as not observable as the workflow requires.")

    return {
        "status": status,
        "situation_check": {"agreement": (float(agreement) if agreement is not None else None), "passed": bool(passed)},
        "main_measure": {
            "name": "mean of (forecast/10) x next-day excess return on up days",
            "value": (float(mean_gain) if mean_gain is not None else None),
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": float(t_val)}
                          if t_val is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "deepest third minus shallowest third mean excess next-day return < 0",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
