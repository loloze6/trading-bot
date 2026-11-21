import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    FC = "forecast"
    RAW = "debug_info.components.fall_x_vol.last_history_value"

    def _ts(df):
        return pd.to_datetime(df["timestamp"], utc=True)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    n_active_computable = 0
    n_agree_computable = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = _ts(df)
            close_time = ts + pd.Timedelta(hours=1)  # timestamp is bar start; the bar closes 1h later
            at_20 = (close_time.dt.hour == 20) & (close_time.dt.minute == 0)
            close = df["close"].astype(float)
            r1 = close.pct_change()
            vol = r1.rolling(240, min_periods=240).std()
            vol_avg = vol.rolling(720, min_periods=720).mean()
            volr = vol / vol_avg
            vol_known = volr.notna()
            vol_high = volr >= 1.0
            raw = df[RAW].astype(float) if RAW in df.columns else pd.Series(np.nan, index=df.index)
            ret24_past = close / close.shift(H) - 1.0
            fall = raw < 0
            fall = fall.where(raw.notna(), ret24_past < 0)
            fc = df[FC].astype(float).fillna(0.0)
            active = fc != 0
            long_side = fc > 0
            agree_all = active & at_20 & fall & long_side & (vol_high | ~vol_known)
            n_active += int(active.sum())
            n_agree += int(agree_all.sum())
            act_c = active & vol_known
            n_active_computable += int(act_c.sum())
            n_agree_computable += int((act_c & at_20 & fall & long_side & vol_high).sum())

    if n_active_computable > 0:
        agreement = n_agree_computable / n_active_computable
    elif n_active > 0:
        agreement = n_agree / n_active
    else:
        agreement = None

    sit_passed = agreement is not None and agreement >= 0.9

    main_name = "t of mean of forecast/10 x excess 24-bar return, one case per coin-day"
    thr = "confirm t >= 2 with >= 100 cases and slope > 0; reject t <= -2 with >= 100 cases"
    reading_sit = ("The 20:00 UTC close is the bar whose timestamp (start) is 19:00 UTC; volatility high is the "
                   "240-bar std of hourly simple returns at or above its 720-bar mean, recomputed inside each window, "
                   "with the agreement taken over active bars where that ratio is computable; a fall is a negative "
                   "raw fall_x_vol value")

    if not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars closing at 20:00 UTC "
                           "after a 24h fall with 10-day volatility at or above its 30-day average"
                           if agreement is not None else "No bar has a non-zero forecast."),
            "reading": reading_sit + ".",
        }

    # ---------- 2. criterion ----------
    # coin mean 24-bar return over all windows, non-overlapping grid
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            c = df["close"].astype(float).to_numpy()
            idx = np.arange(0, len(c) - H, H)
            r = c[idx + H] / c[idx] - 1.0
            rets.append(r[np.isfinite(r)])
        coin_mu[coin] = float(np.mean(np.concatenate(rets))) if rets and sum(len(x) for x in rets) else np.nan

    vals, fcs, exs = [], [], []
    for coin, wins in bars.items():
        mu = coin_mu.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = _ts(df)
            close = df["close"].astype(float)
            fwd = close.shift(-H) / close - 1.0
            fc = df[FC].astype(float)
            sel = (df["regime"] == "mean_reversion") & (fc > 0) & fwd.notna() & fc.notna()
            if not sel.any():
                continue
            sub = pd.DataFrame({"day": ts[sel].dt.date, "f": fc[sel], "r": fwd[sel]})
            sub = sub.groupby("day", sort=True).first()
            for f, r in zip(sub["f"].to_numpy(), sub["r"].to_numpy()):
                ex = r - mu
                vals.append(f / 10.0 * ex)
                fcs.append(f)
                exs.append(ex)

    n = len(vals)
    vals = np.asarray(vals, float)
    mean_v = float(np.mean(vals)) if n else None
    t = None
    if n >= 2:
        sd = float(np.std(vals, ddof=1))
        t = float(mean_v / (sd / np.sqrt(n))) if sd > 0 else None
    slope = None
    if n >= 3 and np.std(fcs) > 0:
        slope = float(stats.linregress(np.asarray(fcs, float), np.asarray(exs, float)).slope)
    slope_pass = None if slope is None else bool(slope > 0)

    if n < 100:
        status = "not observable"
        decided = f"The plan's minimum of 100 cases is not reached ({n} cases)."
    elif t is not None and t >= 2 and slope_pass:
        status = "confirmed"
        decided = "Confirm: t >= 2 with at least 100 cases, and the slope is above 0."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "Reject: t <= -2 with at least 100 cases."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "Inconclusive: t >= 2 with a slope at or below 0."
    else:
        status = "inconclusive"
        decided = "Inconclusive: -2 < t < 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_v,
            "statistic": None if t is None else {"name": "t of the mean", "value": t},
            "threshold": thr,
        },
        "supporting_check": {"name": "OLS slope of excess 24-bar return on forecast", "value": slope,
                             "passed": slope_pass},
        "counts": {"cases": int(n)},
        "decided_by": decided,
        "reading": reading_sit + "; one case per coin-day is the first qualifying bar of that UTC date within a "
                   "window, cases without a bar 24 rows later in the same window are dropped, and the coin's mean "
                   "24-bar return uses the non-overlapping grid of all its windows.",
    }
