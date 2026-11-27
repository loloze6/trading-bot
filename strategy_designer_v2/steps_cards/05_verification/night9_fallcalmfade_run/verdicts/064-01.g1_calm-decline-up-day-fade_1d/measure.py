import numpy as np
import pandas as pd
from scipy import stats

RAW = "debug_info.components.scaled_rise_fade.last_history_value"


def measure(bars):
    H = 3

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            # profile: the regime detector's vetoes send bars outside falling-calm to "chop";
            # bars inside the profile keep the default regime "unknown"
            in_profile = df["regime"].astype(str).str.lower() == "unknown"
            # up day: raw volatility-scaled 1-day return > 0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            c = pd.to_numeric(df["close"], errors="coerce")
            r1 = c / c.shift(1) - 1
            sd20 = r1.rolling(20, min_periods=20).std()
            raw_px = r1 / sd20
            raw = raw.where(raw.notna(), raw_px)
            up_day = raw > 0
            active = fc != 0
            agree = active & in_profile & up_day & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "agreeing bars": n_agree},
            "decided_by": ("No active bars in the record." if n_active == 0 else
                           "Fewer than 90% of the bars with a non-zero forecast are short forecasts on up days "
                           "inside the falling-calm profile (regime 'unknown'), as the Fidelity's situation requires."),
            "reading": "Profile membership read from the recorded regime (vetoes give 'chop' outside the profile); "
                       "up day read from the raw scaled return being above 0.",
        }

    # ---------- 2. criterion ----------
    # coin's mean 3-bar return over all windows, on the non-overlapping grid
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            n = len(c)
            for i in range(0, n - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rets.append(c[i + H] / c[i] - 1)
        coin_mu[coin] = float(np.mean(rets)) if rets else np.nan

    rows = []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n - H, H):
                f = fc[i]
                if not np.isfinite(f) or f >= 0:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                r3 = c[i + H] / c[i] - 1
                unusual = r3 - mu
                rows.append({
                    "day": ts.iloc[i].floor("D"),
                    "size": abs(f),
                    "fade": -unusual,
                    "value": (-f / 10.0) * (-unusual),
                })

    cases = pd.DataFrame(rows)
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"independent cases (distinct days)": n_days, "cases": n_cases}

    main_name = "t of mean position-weighted 3-bar fade beyond drift (cases summed per day)"
    main_thr = "confirm t >= 2 (with slope > 0); reject t <= -2"
    sup_name = "OLS slope of -(unusual 3-bar return) on forecast size"
    reading = ("Profile membership read from the recorded regime; cases are grid bars (0,3,6,... of each window) "
               "with forecast < 0 and a close 3 bars later in the same window; the main value is the mean per case "
               "and its t is the ordinary t of the per-day sums; the slope is on |forecast|, with its t from OLS; "
               "fewer than 30 distinct days is treated as not observable.")

    if n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": float(cases["value"].mean()) if n_cases else None,
                             "statistic": None, "threshold": main_thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than 30 independent cases (distinct days) across coins and windows.",
            "reading": reading,
        }

    daily = cases.groupby("day")["value"].sum().to_numpy()
    mean_val = float(cases["value"].mean())
    sd = float(np.std(daily, ddof=1)) if len(daily) > 1 else np.nan
    t_main = float(np.mean(daily) / (sd / np.sqrt(len(daily)))) if sd and np.isfinite(sd) and sd > 0 else np.nan

    x = cases["size"].to_numpy(dtype=float)
    y = cases["fade"].to_numpy(dtype=float)
    if np.ptp(x) > 0 and len(x) > 2:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else np.nan
    else:
        slope, t_slope = np.nan, np.nan

    slope_pass = bool(np.isfinite(slope) and slope > 0) if np.isfinite(slope) else None

    if np.isfinite(t_main) and t_main <= -2:
        status = "rejected"
        decided = "Reject: the main measure's t is -2 or less (scaled up days followed by rises beyond drift)."
    elif np.isfinite(t_slope) and t_slope <= -2:
        status = "rejected"
        decided = "Reject: the supporting slope's t is -2 or less (the fade shrinks as the rise grows)."
    elif np.isfinite(t_main) and t_main >= 2 and slope_pass:
        status = "confirmed"
        decided = "Confirm: the main measure's t is 2 or more and the supporting slope is above 0."
    else:
        status = "inconclusive"
        if np.isfinite(t_main) and t_main >= 2:
            decided = "Inconclusive: main t is 2 or more but the slope is at or below 0 with a t above -2."
        else:
            decided = "Inconclusive: the main t is between -2 and 2 and no reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": mean_val,
                         "statistic": {"name": "t of the mean (per-day sums)",
                                       "value": t_main if np.isfinite(t_main) else None},
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": slope if np.isfinite(slope) else None,
                             "passed": slope_pass,
                             "t": t_slope if np.isfinite(t_slope) else None},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
