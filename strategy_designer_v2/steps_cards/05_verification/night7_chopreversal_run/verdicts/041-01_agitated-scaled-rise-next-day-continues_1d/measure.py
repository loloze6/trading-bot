import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.scaled_rise.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    frames = []
    coin_mu = {}

    for coin, wins in bars.items():
        coin_rets = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d = d.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            reg = d["regime"].astype(str).str.strip().str.lower()
            if LHV in d.columns:
                raw = pd.to_numeric(d[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)

            # Agitated profile: the detector did not veto the bar to "chop"
            # (vol percentile > 0.5); scaled rise: raw component > 0.
            agitated = (reg != "chop") & reg.notna()
            situation = agitated & (raw > 0)

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

            # Next-bar return, inside the window only.
            nxt = close.shift(-1) / close - 1.0
            coin_rets.append(nxt.dropna().values)

            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            frames.append(pd.DataFrame({
                "coin": coin,
                "day": ts.dt.floor("D"),
                "f": fc,
                "r": nxt,
            }))
        if coin_rets:
            allr = np.concatenate(coin_rets)
            coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.9
    else:
        agreement = None
        passed = True

    main_name = "forecast-weighted mean next-day excess return (over coin mean daily return) on forecast > 0"
    threshold = "confirm: positive with t >= 2 and supporting check passes; reject: negative with t <= -2"
    reading = ("The agitated profile is read from the recorded regime (not 'chop', i.e. the vol-percentile veto did not fire) since "
               "the detector's component is not recorded; the 1-bar horizon uses every bar; the day-clustered t is the ratio-estimator "
               "t with per-day summed residuals f*(excess - mean); thirds are the lowest and highest floor(n/3) cases ranked by forecast "
               "pooled across coins; the 100-day minimum counts distinct UTC days of forecast > 0 cases with a next-day return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are agitated (non-chop) bars with a positive "
                           "scaled rise and a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    if frames:
        allc = pd.concat(frames, ignore_index=True)
    else:
        allc = pd.DataFrame(columns=["coin", "day", "f", "r"])
    allc["mu"] = allc["coin"].map(coin_mu)
    cases = allc[(allc["f"] > 0) & allc["r"].notna() & allc["mu"].notna() & allc["day"].notna()].copy()
    cases["ex"] = cases["r"] - cases["mu"]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    value = None
    tstat = None
    if n_cases > 0:
        W = cases["f"].values.astype(float)
        X = cases["ex"].values.astype(float)
        m = float(np.sum(W * X) / np.sum(W))
        value = m
        cases["e"] = W * (X - m)
        e_d = cases.groupby("day")["e"].sum().values
        G = len(e_d)
        if G > 1:
            var = G / (G - 1) * np.sum(e_d ** 2) / (np.sum(W) ** 2)
            se = float(np.sqrt(var))
            tstat = float(m / se) if se > 0 else None

    # Supporting check
    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        srt = cases.sort_values("f", kind="mergesort").reset_index(drop=True)
        k = n_cases // 3
        bottom = srt.iloc[:k]["ex"].mean()
        top = srt.iloc[n_cases - k:]["ex"].mean()
        sup_val = float(top - bottom)
        sup_pass = bool(sup_val > 0)

    counts = {"distinct days with forecast > 0": n_days, "cases with forecast > 0": n_cases}

    if n_days < 100:
        status = "not observable"
        decided_by = f"Fewer than 100 distinct days with forecast > 0 ({n_days}), the plan's minimum."
    elif tstat is None:
        status = "inconclusive"
        decided_by = "The main measure's t could not be computed, so neither the confirm nor the reject rule is met."
    elif value > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided_by = "The main measure is positive with t >= 2 and the top-minus-bottom-third check is above 0."
    elif value < 0 and tstat <= -2:
        status = "rejected"
        decided_by = "The main measure is negative with t <= -2: scaled rises are given back beyond drift."
    elif value > 0 and tstat >= 2:
        status = "inconclusive"
        decided_by = "Main t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided_by = "The main measure's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": value,
            "statistic": None if tstat is None else {"name": "t of the weighted mean, cases of one day clustered", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean next-day excess return, top third minus bottom third by forecast",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
