import numpy as np
import pandas as pd


def measure(bars):
    raw_col = "debug_info.components.fall30.last_history_value"

    # ---------- collect rows; coin drift over all its windows (returns never cross windows) ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        coin_frames = []
        for w, df in wins.items():
            d = df.copy()
            d = d.sort_values("timestamp", kind="mergesort").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            d["next_ret"] = close.shift(-1) / close - 1.0  # inside this window only
            coin_rets.append(d["next_ret"].dropna().values)
            d["coin"] = coin
            d["window"] = w
            coin_frames.append(d)
        allr = np.concatenate(coin_rets) if coin_rets else np.array([])
        mu = float(np.mean(allr)) if allr.size else np.nan
        for d in coin_frames:
            d["mu"] = mu
            rows.append(d)

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"distinct days with a non-zero forecast": 0},
            "decided_by": "No bars in the record.", "reading": "none",
        }

    data = pd.concat(rows, ignore_index=True)
    data["forecast"] = pd.to_numeric(data["forecast"], errors="coerce")
    raw = pd.to_numeric(data[raw_col], errors="coerce") if raw_col in data.columns else pd.Series(np.nan, index=data.index)
    data["raw"] = raw
    data["ts"] = pd.to_datetime(data["timestamp"], utc=True)
    data["day"] = data["ts"].dt.floor("D")

    # ---------- situation check ----------
    active = data["forecast"].notna() & (data["forecast"] != 0)
    n_active = int(active.sum())
    in_profile = data["regime"].astype(str) == "unknown"   # the falling calm profile (no veto fired)
    fallen30 = data["raw"].notna() & (data["raw"] < 0)     # coin below its close of 30 bars ago
    short_side = data["forecast"] < 0
    agree = active & in_profile & fallen30 & short_side
    agreement = float(agree.sum() / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = "confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2"
    reading = ("The falling calm profile is read from the recorded regime 'unknown' (its detector components are not "
               "recorded and the 365-bar volatility percentile cannot be rebuilt inside ~120-bar windows), with the "
               "recorded 30-bar change below 0 and a negative forecast; the coin's drift is its mean next-bar return "
               "over all its windows; the reported mean and t are over per-day sums of the cases; terciles split the "
               "cases ranked by forecast (stable order) into three equal-count groups; the 100-day minimum counts "
               "distinct days with a non-zero forecast and a next-day return in the same window.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90 % of the non-zero forecasts fall on bars of the falling calm profile with the "
                           "coin down over 30 bars and a short forecast (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- cases ----------
    cases = data[active & data["next_ret"].notna() & data["mu"].notna()].copy()
    cases["excess"] = cases["next_ret"] - cases["mu"]
    cases["gain"] = (-cases["forecast"] / 10.0) * (-cases["excess"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique())
    counts = {"distinct days with a non-zero forecast": n_days, "cases (coin-days)": n_cases}

    # main measure: per-day sums
    daily = cases.groupby("day")["gain"].sum()
    if len(daily) >= 2:
        m = float(daily.mean())
        sd = float(daily.std(ddof=1))
        t = float(m / (sd / np.sqrt(len(daily)))) if sd > 0 else None
    elif len(daily) == 1:
        m, t = float(daily.mean()), None
    else:
        m, t = None, None

    # supporting check: deepest third minus shallowest third of next-day excess return
    sup_val = None
    sup_pass = None
    if n_cases >= 3:
        srt = cases.sort_values(["forecast", "coin", "ts"], kind="mergesort").reset_index(drop=True)
        k = n_cases // 3
        if k >= 1:
            deep = srt.iloc[:k]["excess"]
            shallow = srt.iloc[n_cases - k:]["excess"]
            sup_val = float(deep.mean() - shallow.mean())
            sup_pass = bool(sup_val < 0)

    main = {
        "name": "graded short gain vs drift, (-forecast/10) x -(next-day excess return), per-day sums",
        "value": m,
        "statistic": {"name": "t of the mean (per-day sums)", "value": t} if t is not None else None,
        "threshold": threshold_txt,
    }
    support = {
        "name": "deepest-third minus shallowest-third next-day excess return (< 0)",
        "value": sup_val,
        "passed": sup_pass,
    }

    if n_days < 100:
        status = "not observable"
        decided = "Fewer than the plan's minimum of 100 distinct days with a non-zero forecast (%d)." % n_days
    elif t is None or m is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed, so neither the confirm nor the reject rule is met."
    elif m > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The main measure's mean is positive with t >= 2 and the deepest-minus-shallowest check is below 0."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule (mean > 0, t >= 2) but the supporting check fails, which the plan calls inconclusive."
    elif m < 0 and t <= -2:
        status = "rejected"
        decided = "The main measure's mean is negative with t <= -2: larger falls are followed by rebounds against drift."
    else:
        status = "inconclusive"
        decided = "The main measure's t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
