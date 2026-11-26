import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    BAND = 2.0
    FD_RAW = "debug_info.components.fall_depth.last_history_value"

    # ---------------- 1. situation check ----------------
    n_active = 0
    n_determinable = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float)

            # 28-day return: recorded raw value where present, else recomputed from prices
            fall28 = close / close.shift(28) - 1.0
            if FD_RAW in df.columns:
                rec = pd.to_numeric(df[FD_RAW], errors="coerce")
                fall28 = rec.where(rec.notna(), fall28)
            day = close / close.shift(1) - 1.0

            rng = (high - low) / close
            short_rng = rng.rolling(28, min_periods=28).mean()
            long_rng = rng.rolling(120, min_periods=28).mean()
            range_ratio = short_rng / long_rng

            short_vol = vol.rolling(28, min_periods=28).mean()
            prior_vol = vol.shift(28).rolling(120, min_periods=20).mean()
            vol_ratio = short_vol / prior_vol

            active = fc.notna() & (fc != 0)
            determinable = fall28.notna() & day.notna() & range_ratio.notna() & vol_ratio.notna()
            situation = (fall28 < 0) & (day > 0) & (range_ratio <= 1.0) & (vol_ratio <= 1.0)
            agree = active & determinable & situation & (fc < 0)

            n_active += int(active.sum())
            n_determinable += int((active & determinable).sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_determinable) if n_determinable > 0 else None
    passed = agreement is not None and agreement >= 0.9
    reading_sc = ("situation recomputed per window from that window's own bars (28-day return from the recorded "
                  "fall_depth raw value or the closes, day return, range=(high-low)/close with 28 vs up-to-120-bar means, "
                  "volume 28-bar mean vs up-to-120 bars before them), agreement taken over the active bars where all four "
                  "conditions can be computed")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active, "active bars with situation computable": n_determinable,
                       "active bars in situation on the short side": n_agree},
            "decided_by": ("Fewer than 90% of the active bars are calm-decline up days on the short side: the plan's "
                           "situation asks the 28-day mean range to be at most its 120-day mean, while the config's "
                           "range_calm rule fires when it is at least 1 (gte), i.e. on wide-range days."),
            "reading": reading_sc + ".",
        }

    # ---------------- 2. criterion ----------------
    # normal 5-day drift per coin, non-overlapping grid over all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if c[i] > 0 and np.isfinite(c[i]) and np.isfinite(c[i + H]):
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, unusual, absforecast)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            f = df["forecast"].astype(float).fillna(0.0).to_numpy()
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            is_bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for i in range(n):
                fi = f[i]
                if fi < 0:
                    if not prev_short:
                        ref = 0.0
                    if ref - fi >= BAND:
                        is_bet[i] = True
                        ref = fi
                    else:
                        ref = max(ref, fi)
                    prev_short = True
                else:
                    prev_short = False
                    ref = 0.0
            for start in range(0, n, H):
                idx = [i for i in range(start, min(start + H, n)) if is_bet[i]]
                if not idx:
                    continue
                i = idx[0]
                if i + H >= n or not np.isfinite(drift[coin]):
                    continue
                r = c[i + H] / c[i] - 1.0
                if not np.isfinite(r):
                    continue
                u = -(r - drift[coin])
                cases.append((ts.iloc[i].normalize(), u, abs(f[i])))

    n_cases = len(cases)
    days = sorted(set(d for d, _, _ in cases))
    n_days = len(days)
    counts = {"distinct case days": n_days, "cases": n_cases}

    main_name = "mean unusual move, short side, 5 bars"
    thr = "positive with day-clustered t >= 2 to confirm; negative with t <= -2 to reject"
    sup_name = "OLS slope of unusual move on |forecast|"
    reading = (reading_sc + "; a case is the first short bet (forecast falling >= 2 points below its least-negative "
               "level since the last bet) in each 5-bar grid cell, the day-clustered t sums deviations per UTC day "
               "with a D/(D-1) correction, and the plan's 30-day minimum is treated as a minimum count (not observable).")

    if n_days < 30:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": "Fewer than the plan's 30 distinct case days.",
            "reading": reading,
        }

    d_arr = np.array([d for d, _, _ in cases])
    u = np.array([x for _, x, _ in cases], dtype=float)
    a = np.array([x for _, _, x in cases], dtype=float)
    m = float(u.mean())
    dev = pd.Series(u - m).groupby(pd.Series(d_arr)).sum().to_numpy()
    D = len(dev)
    var = (dev ** 2).sum() / (n_cases ** 2) * (D / (D - 1.0))
    t_main = float(m / np.sqrt(var)) if var > 0 else 0.0

    if np.std(a) > 0:
        lr = stats.linregress(a, u)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr > 0 else 0.0
    else:
        slope, t_slope = 0.0, 0.0

    if (m < 0 and t_main <= -2) or (slope < 0 and t_slope <= -2):
        status = "rejected"
        decided = ("Reject rule met: " + ("mean unusual move negative with t <= -2" if (m < 0 and t_main <= -2)
                                          else "supporting slope negative with t <= -2") + ".")
    elif m > 0 and t_main >= 2 and slope > 0:
        status = "confirmed"
        decided = "Confirm rule met: mean unusual move positive with t >= 2 and supporting slope above 0."
    else:
        status = "inconclusive"
        if -2 < t_main < 2:
            decided = "Inconclusive rule: the main t lies between -2 and 2."
        else:
            decided = "Inconclusive rule: main t >= 2 but the slope is at or below 0 with its t above -2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": m,
                         "statistic": {"name": "t of mean, cases of one day taken together", "value": t_main},
                         "threshold": thr},
        "supporting_check": {"name": sup_name, "value": slope, "passed": bool(slope > 0)},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
