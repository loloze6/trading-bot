import numpy as np
import pandas as pd


def measure(bars):
    FC = "forecast"
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        all_r = []
        for w, df in wins.items():
            d = df.copy()
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce")
            ret1 = close / close.shift(1) - 1.0           # same-day return, inside the window
            nxt = close.shift(-1) / close - 1.0           # next-bar return, inside the window
            up = ret1 > 0
            # first bar of a window: previous close not in the record -> fall back on the detector's regime
            first = ret1.isna()
            if "regime" in d.columns:
                up = up.where(~first, d["regime"].astype(str) == "mean_reversion")
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            day = ts.dt.floor("D")
            all_r.append(nxt.dropna().values)
            rows.append(pd.DataFrame({
                "coin": coin, "window": w, "day": day, "fc": fc,
                "up": up.astype(bool), "nxt": nxt,
            }))
        coin_rets[coin] = np.concatenate(all_r) if all_r else np.array([])

    if not rows:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None,
                "counts": {"days with a case": 0},
                "decided_by": "no bars in the record", "reading": "none"}

    data = pd.concat(rows, ignore_index=True)
    reading = ("The up day is the close-to-close return above 0 inside the window (on a window's first bar, where the "
               "previous close is not recorded, the recorded regime 'mean_reversion' stands for it); the per-day pooled t "
               "is the mean over its day-clustered standard error (deviations summed per day, G/(G-1) correction); "
               "'up days with forecast 0' are up days by that same rule.")

    # ---- situation check ----
    active = data[data["fc"].notna() & (data["fc"] != 0)]
    n_active = len(active)
    if n_active == 0:
        agreement = None
        passed = False
    else:
        ok = active["up"] & (active["fc"] < 0)
        agreement = float(ok.mean())
        passed = agreement >= 0.90

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("fewer than 90 % of the bars with a non-zero forecast are up days (1-day return above 0) "
                           "with a short (negative) forecast, as the Fidelity's situation and side require"
                           if n_active > 0 else "no bar has a non-zero forecast"),
            "reading": reading,
        }

    # ---- excess next-day returns ----
    mu = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in coin_rets.items()}
    data["mu"] = data["coin"].map(mu)
    data["exc"] = data["nxt"] - data["mu"]

    cases = data[(data["fc"] < 0) & data["exc"].notna() & data["day"].notna()].copy()
    cases["x"] = cases["exc"] * (-cases["fc"] / 10.0)
    n_cases = len(cases)
    n_days = int(cases["day"].nunique())

    mean_x = float(cases["x"].mean()) if n_cases else None
    t_x = None
    if n_cases > 1 and n_days > 1:
        dev = cases["x"] - mean_x
        s = dev.groupby(cases["day"]).sum().values
        G = len(s)
        var = (G / (G - 1)) * np.sum(s ** 2) / (n_cases ** 2)
        if var > 0:
            t_x = float(mean_x / np.sqrt(var))

    # ---- supporting check ----
    deep = data[(data["fc"] <= -10) & data["exc"].notna()]["exc"]
    nonshort = data[(data["fc"] == 0) & data["up"] & data["exc"].notna()]["exc"]
    if len(deep) and len(nonshort):
        diff = float(deep.mean() - nonshort.mean())
        supp_pass = bool(diff < 0)
    else:
        diff = None
        supp_pass = None

    counts = {"days with a case": n_days, "cases": int(n_cases),
              "deep cases (forecast <= -10)": int(len(deep)),
              "up days with forecast 0": int(len(nonshort))}

    main = {"name": "mean next-day excess return x (-forecast/10) on short cases",
            "value": mean_x,
            "statistic": ({"name": "t of the mean, cases pooled per day", "value": t_x} if t_x is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 and supporting difference < 0; reject: mean < 0 with t <= -2"}
    supp = {"name": "mean next-day excess return, forecast <= -10 minus up days with forecast 0",
            "value": diff, "passed": supp_pass}

    if n_days < 200 or t_x is None:
        status = "not observable"
        decided = f"only {n_days} days with a case, below the plan's minimum of 200 days."
    elif mean_x > 0 and t_x >= 2 and supp_pass is True:
        status = "confirmed"
        decided = "The main measure's mean is above 0 with t >= 2 and the supporting difference is below 0."
    elif mean_x < 0 and t_x <= -2:
        status = "rejected"
        decided = "The main measure's mean is below 0 with t <= -2."
    elif mean_x > 0 and t_x >= 2:
        status = "inconclusive"
        decided = "A confirming t with a supporting difference at or above 0 (or not measurable) is inconclusive."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supp,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
