import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    NH_RAW = "debug_info.components.near_high.last_history_value"
    NH_POST = "debug_info.components.near_high.post_pipeline_value"
    OF_RAW = "debug_info.components.offset.last_history_value"
    OF_POST = "debug_info.components.offset.post_pipeline_value"
    H = 10
    STD_WIN, STD_MINP = 60, 20

    def standardise(raw):
        # value(t) * 10 / mean(|last `window` raw values|, t left out), capped; 0 until min_periods; 0 if mean is 0
        vals = raw.to_numpy(dtype=float)
        out = np.full(len(vals), np.nan)
        past = []
        for i, v in enumerate(vals):
            if np.isnan(v):
                continue
            if len(past) >= STD_MINP:
                m = np.mean(np.abs(past[-STD_WIN:]))
                out[i] = 0.0 if m == 0 else float(np.clip(v * 10.0 / m, -20, 20))
            past.append(v)
        return out, len(past)

    def in_profile(df):
        rec = df[NH_RAW].notna() if NH_RAW in df.columns else pd.Series(False, index=df.index)
        reg = df["regime"].astype(str) == "unknown" if "regime" in df.columns else pd.Series(True, index=df.index)
        return (rec & reg).to_numpy()

    # ---------- 1. situation check ----------
    n_active, n_agree = 0, 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            active = np.nan_to_num(fc) != 0
            if not active.any():
                continue
            prof = in_profile(df)
            expected = np.full(len(df), np.nan)
            if NH_RAW in df.columns:
                raw_nh = pd.to_numeric(df[NH_RAW], errors="coerce")
                raw_of = pd.to_numeric(df[OF_RAW], errors="coerce") if OF_RAW in df.columns else pd.Series(np.nan, index=df.index)
                s_nh, _ = standardise(raw_nh)
                s_of, _ = standardise(raw_of)
                # history counts: rebuilt value only trustworthy once a full window of recorded raw values exists
                cnt = raw_nh.notna().cumsum().shift(1).fillna(0).to_numpy()
                post_nh = pd.to_numeric(df[NH_POST], errors="coerce").to_numpy(dtype=float) if NH_POST in df.columns else np.full(len(df), np.nan)
                post_of = pd.to_numeric(df[OF_POST], errors="coerce").to_numpy(dtype=float) if OF_POST in df.columns else np.full(len(df), np.nan)
                rebuilt = np.clip((s_nh + s_of) / 2.0, -20, 20)
                fallback = np.clip((post_nh + post_of) / 2.0, -20, 20)
                expected = np.where(cnt >= STD_WIN, rebuilt, fallback)
                expected = np.where(np.isnan(expected), fallback, expected)
            ok = active & prof & ~np.isnan(expected) & (np.sign(expected) == np.sign(fc))
            n_active += int(active.sum())
            n_agree += int(ok.sum())
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "pooled slope of excess 10-bar return on forecast, profile bars, non-overlapping grid"
    thr = "slope t >= 2 (with top-minus-bottom > 0) confirms; t <= -2 rejects; at least 300 grid cases and 100 distinct grid days"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars are inside the rising profile with the sign of the rebuilt nearness-to-high forecast (nearer than usual long, further short)." if n_active > 0 else "No active bars: the config never takes the position the plan's situation calls for.",
            "reading": "The expected side on each bar is the sign of the forecast rebuilt from the components' raw values (post-pipeline values where the window lacks a full standardise history), and the profile is bars with regime 'unknown' where near_high is recorded.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            prof = in_profile(df)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                rows.append((coin, w, ts.iloc[i].normalize(), r, fc[i], bool(prof[i])))
    g = pd.DataFrame(rows, columns=["coin", "window", "day", "ret", "fc", "prof"])
    if len(g):
        coin_mean = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(coin_mean)
        cases = g[g["prof"] & g["fc"].notna()].copy()
    else:
        cases = pd.DataFrame(columns=["coin", "window", "day", "ret", "fc", "prof", "excess"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    slope, t, diff = None, None, None
    if n_cases >= 3 and cases["fc"].nunique() > 1:
        lr = stats.linregress(cases["fc"].astype(float), cases["excess"].astype(float))
        slope = float(lr.slope)
        t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None
        srt = cases.sort_values("fc", kind="mergesort")
        k = n_cases // 3
        if k > 0:
            diff = float(srt["excess"].iloc[-k:].mean() - srt["excess"].iloc[:k].mean())
    check_pass = None if diff is None else bool(diff > 0)

    if n_cases < 300 or n_days < 100:
        status = "not observable"
        decided = f"Minimum count not reached: {n_cases} grid cases inside the profile (300 needed) and {n_days} distinct grid days (100 needed)."
    elif t is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so it meets neither the confirm nor the reject rule."
    elif t <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: reject, whatever the check shows."
    elif t >= 2 and check_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the top-minus-bottom difference is positive: confirm."
    elif t >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the top-minus-bottom difference is 0 or less: inconclusive."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t is None else {"name": "OLS slope t", "value": t},
            "threshold": thr,
        },
        "supporting_check": {"name": "mean excess return, top third minus bottom third by forecast", "value": diff, "passed": check_pass},
        "counts": {"grid cases inside the profile": n_cases, "distinct grid days": n_days},
        "decided_by": decided,
        "reading": "The coin's mean 10-bar return is the mean over all its non-overlapping grid cases in all windows (profile or not), the profile is bars with regime 'unknown' where near_high is recorded, the thirds are the n//3 lowest and highest grid cases by forecast (stable sort), and the expected side is the sign of the forecast rebuilt from raw component values (post-pipeline values where a window lacks a full standardise history).",
    }
