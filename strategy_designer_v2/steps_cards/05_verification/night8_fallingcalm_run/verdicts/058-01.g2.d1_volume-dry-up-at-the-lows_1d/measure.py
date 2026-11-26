import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    VOL_COL = "debug_info.components.vol_shrink.last_history_value"
    LOW_COL = "debug_info.components.near_low.last_history_value"

    def recompute_vol_shrink(df):
        v = pd.to_numeric(df["volume"], errors="coerce")
        last = v.rolling(30, min_periods=30).mean()
        prior = v.shift(30).rolling(30, min_periods=30).mean()
        with np.errstate(divide="ignore", invalid="ignore"):
            out = np.log(last / prior)
        return out.replace([np.inf, -np.inf], np.nan)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = f != 0
            if not active.any():
                continue
            if VOL_COL in df.columns:
                vs = pd.to_numeric(df[VOL_COL], errors="coerce")
            else:
                vs = pd.Series(np.nan, index=df.index)
            vs = vs.where(vs.notna(), recompute_vol_shrink(df))
            regime = df["regime"].astype(str)
            # falling calm profile = the strategy's regime ("unknown"), not vetoed to chop
            profile = regime == "unknown"
            shrunk = vs < 0
            situation = profile & shrunk & (f < 0)
            n_active += int(active.sum())
            n_agree += int((situation & active).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("The falling calm profile is read as regime 'unknown' (the regime holding the strategy, "
               "the vetoes sending other bars to chop), 'volume shrunk' as a raw vol_shrink log ratio below 0, "
               "and nearness to the low as graded (no cut-off) as the Fidelity says it is damped; "
               "the top/bottom halves are the largest and smallest floor(n/2) cases by |forecast| "
               "(the middle case dropped when n is odd); the day-clustered t of the weighted mean uses the "
               "per-day sums of w*(x-mean) with a G/(G-1) correction; and fewer than 30 cases or 20 days "
               "is reported as not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are short bars in the falling calm profile with "
                           "volume shrunk (raw log ratio < 0): the config shorts also where the plan's situation "
                           "(volume shrunk near the low) does not hold."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                rets_all.append(r)
                if np.isfinite(f[i]) and f[i] < 0:
                    rows.append({"coin": coin, "r": r, "w": abs(f[i]),
                                 "day": ts.iloc[i].strftime("%Y-%m-%d")})
        coin_rets[coin] = float(np.mean(rets_all)) if rets_all else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "r", "w", "day"])
    if len(cases):
        cases["mu"] = cases["coin"].map(coin_rets)
        cases = cases.dropna(subset=["r", "w", "mu"])
        cases["x"] = -cases["r"] + cases["mu"]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"cases": n_cases, "distinct days": n_days}

    main_name = "|forecast|-weighted mean excess 5-bar fall of short cases"
    thr = "t >= 2 confirms (with top-minus-bottom > 0), t <= -2 rejects"

    wmean = None
    tval = None
    if n_cases > 0 and cases["w"].sum() > 0:
        W = float(cases["w"].sum())
        wmean = float((cases["w"] * cases["x"]).sum() / W)
        dev = cases["w"] * (cases["x"] - wmean)
        per_day = dev.groupby(cases["day"]).sum()
        G = len(per_day)
        if G > 1:
            var = float((per_day ** 2).sum()) / W ** 2 * G / (G - 1)
            se = np.sqrt(var)
            tval = float(wmean / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases >= 2:
        srt = cases.sort_values("w", kind="mergesort").reset_index(drop=True)
        k = n_cases // 2
        bottom = srt.iloc[:k]
        top = srt.iloc[n_cases - k:]
        sup_val = float(top["x"].mean() - bottom["x"].mean())
        sup_pass = bool(sup_val > 0)

    main = {"name": main_name, "value": wmean,
            "statistic": {"name": "t of weighted mean, cases of one day summed", "value": tval} if tval is not None else None,
            "threshold": thr}
    supporting = {"name": "mean excess fall, top half minus bottom half of |forecast|",
                  "value": sup_val, "passed": sup_pass}

    if n_cases < 30 or n_days < 20:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases (need 30) and {n_days} distinct days (need 20).")
    elif tval is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The weighted mean excess fall has t >= 2 and the top-minus-bottom difference is above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The weighted mean excess fall has t <= -2: the coin rises more than usual after the signals."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting top-minus-bottom check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
