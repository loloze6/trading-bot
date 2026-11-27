import numpy as np
import pandas as pd

H = 7
MIN_INDEPENDENT = 30
RAW_COL = "debug_info.components.month_fall.last_history_value"
PROFILE_REGIME = "unknown"  # the only regime with a strategy: the choppy agitated profile


def _window_frame(df):
    d = df.reset_index(drop=True).copy()
    d["close"] = pd.to_numeric(d["close"], errors="coerce")
    d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
    if RAW_COL in d.columns:
        raw = pd.to_numeric(d[RAW_COL], errors="coerce")
    else:
        raw = pd.Series(np.nan, index=d.index)
    # recompute the 30-bar percent return from prices where the component is not recorded
    recomputed = (d["close"] / d["close"].shift(30) - 1.0) * 100.0
    d["raw"] = raw.where(raw.notna(), recomputed)
    d["ts"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
    return d


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    frames = {}
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            d = _window_frame(df)
            frames[(coin, w)] = d
            active = d["forecast"] != 0
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("", index=d.index)
            situation = (d["raw"] < 0) & (regime == PROFILE_REGIME)
            agree = active & situation & (d["forecast"] < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    reading_base = ("The situation is the 30-bar return (month_fall raw value, recomputed from closes where missing) below 0 "
                    "on bars whose regime is the profile's regime 'unknown', short side; independent cases are the distinct "
                    "UTC days the grid cases fall on; the coin's mean 7-bar return is over all grid bars of all its windows; "
                    "the halves are the n//2 largest and n//2 smallest |forecast| cases (the median case left out when n is odd) "
                    "compared on unweighted mean unsigned excess return; a count below 30 is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "agreeing bars": n_agree},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars with the close below its close "
                           "30 bars earlier inside the choppy agitated profile, as the plan's Fidelity requires."
                           if n_active > 0 else "The record has no active bar, so the forecast cannot be matched to the plan's situation."),
            "reading": reading_base,
        }

    # ---------- 2. criterion ----------
    # coin drift: mean of non-overlapping 7-bar returns over all windows
    coin_rets = {}
    cases = []
    for (coin, w), d in frames.items():
        c = d["close"].values
        n = len(d)
        for i in range(0, n - H, H):
            if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                continue
            r = c[i + H] / c[i] - 1.0
            coin_rets.setdefault(coin, []).append(r)
            f = d["forecast"].iloc[i]
            if f < 0:
                cases.append((coin, d["ts"].iloc[i], float(f), r))

    rows = []
    for coin, ts, f, r in cases:
        mu = float(np.mean(coin_rets[coin]))
        ex = r - mu
        day = ts.floor("D") if pd.notna(ts) else None
        rows.append({"coin": coin, "day": day, "w": abs(f), "excess": ex, "short_excess": -ex})
    cdf = pd.DataFrame(rows, columns=["coin", "day", "w", "excess", "short_excess"])
    cdf = cdf.dropna(subset=["day", "w", "excess"])
    n_cases = int(len(cdf))
    n_days = int(cdf["day"].nunique()) if n_cases else 0

    wmean = None
    tval = None
    if n_cases > 0 and cdf["w"].sum() > 0:
        W = float(cdf["w"].sum())
        wmean = float((cdf["w"] * cdf["short_excess"]).sum() / W)
        dev = cdf["w"] * (cdf["short_excess"] - wmean)
        s_day = dev.groupby(cdf["day"]).sum().values
        D = len(s_day)
        if D > 1:
            var = (D / (D - 1.0)) * float(np.sum(s_day ** 2)) / (W ** 2)
            se = np.sqrt(var)
            tval = float(wmean / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        s = cdf.sort_values(["w", "day", "coin"], kind="mergesort").reset_index(drop=True)
        k = n_cases // 2
        shallow = s.iloc[:k]["excess"]
        deep = s.iloc[n_cases - k:]["excess"]
        sup_val = float(deep.mean() - shallow.mean())
        sup_pass = bool(sup_val < 0)

    counts = {"independent cases (days)": n_days, "cases": n_cases}

    if n_days < MIN_INDEPENDENT:
        status = "not observable"
        decided = f"Fewer than {MIN_INDEPENDENT} independent cases ({n_days} days), so the data cannot show the idea."
    elif wmean is None or tval is None:
        status = "inconclusive"
        decided = "The t of the weighted mean cannot be computed, so neither the confirm nor the reject rule is met."
    elif wmean > 0 and tval >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The weighted mean short-side excess return is above 0 with t >= 2 and the deeper half falls more than the shallower half."
        else:
            status = "inconclusive"
            decided = "The main measure confirms (mean > 0, t >= 2) but the supporting check fails, which the plan calls inconclusive."
    elif wmean < 0 and tval <= -2:
        status = "rejected"
        decided = "The weighted mean short-side excess return is below 0 with t <= -2: after the fall, the coin beats its drift."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "|forecast|-weighted mean short-side 7-bar excess return",
            "value": wmean,
            "statistic": {"name": "t of the weighted mean, cases of one day taken together", "value": tval} if tval is not None else None,
            "threshold": "above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject",
        },
        "supporting_check": {
            "name": "deeper half minus shallower half excess 7-bar return (below 0)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
