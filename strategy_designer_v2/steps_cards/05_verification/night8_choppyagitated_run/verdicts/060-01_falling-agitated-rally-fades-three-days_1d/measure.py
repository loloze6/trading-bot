import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    BAND = 2.0
    RAW = "debug_info.components.scaled_rise.last_history_value"
    MIN_DAYS = 30

    def _num(s):
        return pd.to_numeric(s, errors="coerce")

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = _num(df["forecast"]).fillna(0.0).values
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            if RAW in df.columns:
                raw = _num(df[RAW]).values
            else:
                raw = np.full(len(df), np.nan)
            active = f != 0
            # falling agitated = the detector's non-vetoed regime "unknown"; a one-day rise = raw scaled return > 0
            situ = (reg == "unknown") & np.isfinite(raw) & (np.nan_to_num(raw, nan=0.0) > 0)
            agree = active & situ & (f < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean short-signed unusual 3-bar move of the cases (vs coin's normal 3-bar drift)"
    main_thr = "day-clustered t >= 2 to confirm (with slope t >= 2); t <= -2 or slope t <= -2 to reject"
    sup_name = "OLS slope of short-signed unusual move on |forecast|"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bets on up days in the "
                           "falling agitated regime, so the config does not do what the plan's situation says."),
            "reading": "The falling agitated situation is read from the regime column (the detector's only "
                       "non-chop regime 'unknown'), and the rise from the recorded raw scaled return being > 0.",
        }

    # ---------- 2. normal drift per coin ----------
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = _num(df["close"]).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. cases ----------
    xs, fa, days = [], [], []
    for coin, wins in bars.items():
        d0 = drift.get(coin, np.nan)
        if not np.isfinite(d0):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            f = _num(df["forecast"]).fillna(0.0).values
            c = _num(df["close"]).values
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            side, ref = 0, 0.0
            taken = set()
            n = len(df)
            for t in range(n):
                ft = f[t]
                s = int(np.sign(ft))
                bet = False
                if s == 0:
                    side, ref = 0, 0.0
                else:
                    if s != side:
                        side, ref = s, 0.0
                    mag = abs(ft)
                    if mag - ref >= BAND - 1e-12:
                        bet = True
                        ref = mag
                    else:
                        ref = min(ref, mag)
                if not bet or s >= 0:
                    continue
                cell = t // H
                if cell in taken:
                    continue
                taken.add(cell)
                if t + H >= n:
                    continue
                if not (np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] > 0):
                    continue
                r = c[t + H] / c[t] - 1.0
                xs.append(-(r - d0))
                fa.append(abs(ft))
                tt = ts.iloc[t]
                days.append(str(tt.date()) if pd.notna(tt) else f"na_{coin}_{w}_{t}")

    xs = np.asarray(xs, dtype=float)
    fa = np.asarray(fa, dtype=float)
    n_cases = int(len(xs))
    n_days = int(len(set(days)))
    counts = {"distinct case days": n_days, "cases": n_cases}

    mean = float(np.mean(xs)) if n_cases > 0 else None
    t_main = None
    if n_cases > 1:
        dev = pd.Series(xs - mean).groupby(pd.Series(days)).sum().values
        se = np.sqrt(np.sum(dev ** 2)) / n_cases
        t_main = float(mean / se) if se > 0 else None

    slope, t_slope = None, None
    if n_cases > 2 and np.std(fa) > 0:
        lr = stats.linregress(fa, xs)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    reading = ("A case is the first short bet (rise of |forecast| >= 2 from its lowest level since the last bet) in "
               "each 3-bar cell counted from each window's first row; the day-clustered t sums deviations per UTC day "
               "with no small-sample correction; the slope t is the ordinary OLS t; the plan's 30-day minimum is "
               "applied as 'not observable'; the situation is read from the regime 'unknown' and raw value > 0.")

    main = {"name": main_name, "value": mean,
            "statistic": {"name": "day-clustered t", "value": t_main} if t_main is not None else None,
            "threshold": main_thr}
    sup_pass = None if t_slope is None else bool(t_slope >= 2)
    sup = {"name": sup_name, "value": slope, "passed": sup_pass}
    sc = {"agreement": agreement, "passed": True}

    if n_days < MIN_DAYS:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": sup, "counts": counts,
                "decided_by": f"Only {n_days} distinct case days, below the plan's minimum of 30.",
                "reading": reading}

    if (t_main is not None and t_main <= -2) or (t_slope is not None and t_slope <= -2):
        status = "rejected"
        decided = "Reject rule met: the main t is <= -2 or the slope's t is <= -2."
    elif t_main is not None and t_main >= 2 and t_slope is not None and t_slope >= 2:
        status = "confirmed"
        decided = "Confirm rule met: the main t is >= 2 and the slope's t is >= 2, before costs."
    else:
        status = "inconclusive"
        decided = ("Neither rule met: the main t is between -2 and 2, or it is >= 2 with a slope t below 2 "
                   "(or a statistic could not be computed).")

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": sup, "counts": counts, "decided_by": decided, "reading": reading}
