import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    MIN_DAYS = 30
    MR_POST = "debug_info.components.month_return.post_pipeline_value"
    SO_POST = "debug_info.components.short_offset.post_pipeline_value"
    MR_RAW = "debug_info.components.month_return.last_history_value"
    SO_RAW = "debug_info.components.short_offset.last_history_value"

    def standardise(raw, window=60, min_periods=20):
        # value(t) * 10 / mean(|last `window` raw values|, bar t left out), capped at -20..20
        raw = pd.Series(raw, dtype=float).reset_index(drop=True)
        absprev = raw.abs().shift(1)
        denom = absprev.rolling(window, min_periods=min_periods).mean()
        out = raw * 10.0 / denom
        out[(denom == 0) | denom.isna()] = 0.0
        return out.clip(-20, 20).values

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            regime = df["regime"].astype(str)
            # values after transforms; rebuild from raw values where the post value is missing
            mr = pd.to_numeric(df[MR_POST], errors="coerce") if MR_POST in df else pd.Series(np.nan, index=df.index)
            so = pd.to_numeric(df[SO_POST], errors="coerce") if SO_POST in df else pd.Series(np.nan, index=df.index)
            if MR_RAW in df and mr.isna().any():
                raw = pd.to_numeric(df[MR_RAW], errors="coerce")
                rb = np.minimum(standardise(raw.fillna(0.0)), 10.0)
                rb = pd.Series(rb, index=df.index).where(raw.notna())
                mr = mr.fillna(rb)
            if SO_RAW in df and so.isna().any():
                raw = pd.to_numeric(df[SO_RAW], errors="coerce")
                rb = -pd.Series(standardise(raw.fillna(0.0)), index=df.index).where(raw.notna())
                so = so.fillna(rb)
            rebuilt = (mr + so) / 2.0
            in_profile = regime.str.lower() == "unknown"  # the only regime with a strategy = choppy agitated
            situation_short = in_profile & mr.notna() & so.notna() & (rebuilt < 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & situation_short & (fc < 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active bars are short bars inside the choppy agitated profile "
                           "(regime 'unknown') with a negative rebuilt forecast (month_return clipped at +10 plus the -10 offset), "
                           "so the config does not do what the Fidelity says."),
            "reading": "The profile is read from the recorded regime ('unknown' is the only regime with a strategy); "
                       "the expected side is short wherever the rebuilt forecast is below 0.",
        }

    # ---------------- 2. criterion ----------------
    # coin mean 7-bar return over all windows (non-overlapping grid)
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    vals, wts, days = [], [], []
    for coin, wins in bars.items():
        mu = coin_mean.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    continue
                f = fc[i]
                if not (np.isfinite(f) and f < 0):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                vals.append(-(r - mu))
                wts.append(abs(f))
                days.append(ts.iloc[i].floor("D"))

    vals = np.array(vals, dtype=float)
    wts = np.array(wts, dtype=float)
    n_cases = int(len(vals))
    n_days = int(len(set(days)))

    wmean, tval, supp_val, supp_pass = None, None, None, None
    if n_cases > 0 and wts.sum() > 0:
        wmean = float(np.sum(vals * wts) / np.sum(wts))
        contrib = wts * (vals - wmean) / np.sum(wts)
        per_day = pd.Series(contrib).groupby(pd.Series(days)).sum().values
        G = len(per_day)
        if G > 1:
            var = np.sum(per_day ** 2) * G / (G - 1)
            se = np.sqrt(var)
            tval = float(wmean / se) if se > 0 else None
        order = np.argsort(-wts, kind="mergesort")
        k = n_cases // 2
        if k >= 1 and n_cases - k >= 1:
            big = vals[order[:k]]
            small = vals[order[k:]]
            supp_val = float(np.mean(big) - np.mean(small))
            supp_pass = bool(supp_val > 0)

    if n_days < MIN_DAYS:
        status = "not observable"
        decided = f"Fewer than {MIN_DAYS} independent days with a short grid case ({n_days}): the minimum is not reached."
    elif wmean is None or tval is None:
        status = "inconclusive"
        decided = "The weighted mean or its day-clustered t could not be computed."
    elif wmean > 0 and tval >= 2 and supp_pass is True:
        status = "confirmed"
        decided = "Weighted mean directional excess return above 0 with t >= 2 over at least 30 days, and the larger-|forecast| half beats the smaller half."
    elif tval <= -2:
        status = "rejected"
        decided = "Weighted mean directional excess return has t <= -2 over at least 30 days: the coin rose against the shorts."
    elif tval >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails (or the mean is not above 0), so the result is inconclusive."
    else:
        status = "inconclusive"
        decided = "|t| < 2 over at least 30 days: the result is inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "|forecast|-weighted mean 7-bar directional excess return (short), short grid bars",
            "value": wmean,
            "statistic": {"name": "day-clustered t", "value": tval} if tval is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 over >= 30 days and supporting check passes; reject: t <= -2 over >= 30 days",
        },
        "supporting_check": {
            "name": "mean excess of larger-|forecast| half minus smaller half",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": {"independent days with a short grid case": n_days, "short grid cases": n_cases},
        "decided_by": decided,
        "reading": ("Days are UTC calendar days of the grid bar; the day-clustered t sums each day's weighted deviations; "
                    "the larger half is the top floor(n/2) cases by |forecast| (ties in record order) with unweighted half means; "
                    "'near zero' is read as covered by the |t| < 2 rule, with no extra threshold."),
    }
