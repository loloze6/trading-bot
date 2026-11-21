import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 26
    TEN, KIJ, SEN, DISP, LB = 9, 26, 52, 26, 26
    slope_col = "debug_info.components.slope.last_history_value"

    def fnum(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        return None if not np.isfinite(x) else x

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            hi = df["high"].astype(float)
            lo = df["low"].astype(float)
            cl = df["close"].astype(float)
            tenkan = (hi.rolling(TEN, min_periods=TEN).max() + lo.rolling(TEN, min_periods=TEN).min()) / 2
            kijun = (hi.rolling(KIJ, min_periods=KIJ).max() + lo.rolling(KIJ, min_periods=KIJ).min()) / 2
            span_a = (tenkan + kijun) / 2
            span_b = (hi.rolling(SEN, min_periods=SEN).max() + lo.rolling(SEN, min_periods=SEN).min()) / 2
            top = pd.concat([span_a, span_b], axis=1).max(axis=1, skipna=False).shift(DISP)
            mid = ((span_a + span_b) / 2).shift(DISP)
            pos_re = cl / top - 1.0
            slope_re = mid - mid.shift(LB)

            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            if slope_col in df.columns:
                slope_rec = pd.to_numeric(df[slope_col], errors="coerce")
            else:
                slope_rec = pd.Series([np.nan] * len(df))

            for i in range(len(df)):
                f = fc.iloc[i]
                if f == 0:
                    continue
                n_active += 1
                trending = regime.iloc[i] == "trending"
                # cloud slope > 0: recorded raw value, else recomputed, else detector's regime
                s = slope_rec.iloc[i]
                if not np.isfinite(s):
                    s = slope_re.iloc[i]
                slope_ok = (s > 0) if np.isfinite(s) else trending
                # close above cloud top: recomputed when history allows, else detector's regime
                p = pos_re.iloc[i]
                pos_ok = (p > 0) if np.isfinite(p) else trending
                if slope_ok and pos_ok and f > 0:
                    n_agree += 1

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    reading = ("Cloud position is recomputed from each window's prices (9/26/52, displaced 26, top edge) and the slope "
               "taken from the recorded raw slope component, falling back to the detector's 'trending' regime on bars "
               "where window history is too short to recompute; normal drift is each coin's mean 26-bar return over all "
               "grid bars of all its windows; the plan's minimum of 30 cases is applied as 'not observable' when not met.")

    main_name = "mean excess 26-bar forward return over coin drift, on grid bars with forecast > 0"
    main_thr = "confirm if mean > 0 with t >= 2 (and slope t >= 2); reject if mean < 0 with t <= -2 or slope t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "non-overlapping cases": 0},
            "decided_by": ("Fewer than 90% of active bars are long bars with the close above a rising cloud "
                           "(agreement %.3f), so the config does not do what the plan's situation says." % agreement),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []  # (coin, fwd, forecast)
    coin_all = {}
    for coin in sorted(bars):
        coin_all[coin] = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            cl = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            for i in range(0, len(df), H):
                j = i + H
                if j >= len(df):
                    break
                if not (np.isfinite(cl[i]) and np.isfinite(cl[j]) and cl[i] > 0):
                    continue
                r = cl[j] / cl[i] - 1.0
                coin_all[coin].append(r)
                if np.isfinite(fc[i]) and fc[i] > 0:
                    rows.append((coin, r, float(fc[i])))

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_all.items()}
    ex = np.array([r - drift[c] for c, r, f in rows], dtype=float)
    fv = np.array([f for c, r, f in rows], dtype=float)
    ok = np.isfinite(ex) & np.isfinite(fv)
    ex, fv = ex[ok], fv[ok]
    n = int(len(ex))

    mean_ex = float(np.mean(ex)) if n > 0 else None
    t_mean = None
    if n > 1:
        sd = np.std(ex, ddof=1)
        t_mean = fnum(np.mean(ex) / (sd / np.sqrt(n))) if sd > 0 else None

    slope_v, t_slope = None, None
    if n > 2 and np.std(fv) > 0:
        lr = stats.linregress(fv, ex)
        slope_v = fnum(lr.slope)
        if lr.stderr is not None and lr.stderr > 0:
            t_slope = fnum(lr.slope / lr.stderr)

    counts = {"non-overlapping cases": n, "active bars": int(n_active)}

    if n < 30:
        status = "not observable"
        decided = "Only %d non-overlapping cases, below the plan's minimum of 30." % n
        sup_pass = None if t_slope is None else bool(slope_v is not None and slope_v > 0 and t_slope >= 2)
    else:
        main_conf = t_mean is not None and mean_ex > 0 and t_mean >= 2
        main_rej = t_mean is not None and mean_ex < 0 and t_mean <= -2
        sup_pass = bool(t_slope is not None and slope_v > 0 and t_slope >= 2)
        sup_rej = t_slope is not None and slope_v < 0 and t_slope <= -2
        if main_rej or sup_rej:
            status = "rejected"
            decided = ("Reject rule met: mean excess return negative with t <= -2" if main_rej
                       else "Reject rule met: supporting slope negative with t <= -2") + "."
        elif main_conf and sup_pass:
            status = "confirmed"
            decided = "Confirm rule met: mean excess return positive with t >= 2 and supporting slope positive with t >= 2."
        elif main_conf:
            status = "inconclusive"
            decided = "Inconclusive rule: main measure confirms but the supporting slope check does not pass."
        else:
            status = "inconclusive"
            decided = "Inconclusive rule: mean excess return t between -2 and 2 and no reject condition met."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": fnum(mean_ex),
            "statistic": {"name": "t of the mean", "value": t_mean} if t_mean is not None else None,
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "OLS slope t of excess return on forecast",
            "value": t_slope,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
