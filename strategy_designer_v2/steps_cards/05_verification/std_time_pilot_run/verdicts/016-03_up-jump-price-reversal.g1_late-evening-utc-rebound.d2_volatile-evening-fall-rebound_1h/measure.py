import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    FC = "forecast"
    RAW = "debug_info.components.fall_x_vol.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    n_unknown = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            dt = ts.diff().dropna()
            bar_dur = dt.median() if len(dt) else pd.Timedelta(hours=1)
            close_time = ts + bar_dur
            at_20 = (close_time.dt.hour == 20) & (close_time.dt.minute == 0)

            c = d["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(240, min_periods=240).std()
            vol_avg = vol.rolling(720, min_periods=720).mean()
            volr = vol / vol_avg
            vol_high = volr >= 1.0

            ret24 = c / c.shift(H) - 1
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            fall = pd.Series(np.where(ret24.notna(), ret24 < 0,
                                      np.where(raw.notna(), raw < 0, np.nan)),
                             index=d.index)

            f = pd.to_numeric(d[FC], errors="coerce")
            active = f.notna() & (f != 0)
            for i in np.where(active.values)[0]:
                if pd.isna(volr.iloc[i]) or pd.isna(fall.iloc[i]):
                    n_unknown += 1
                    continue
                n_active += 1
                ok = bool(at_20.iloc[i]) and bool(vol_high.iloc[i]) \
                    and bool(fall.iloc[i]) and f.iloc[i] > 0
                n_agree += int(ok)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The bar 'closing at 20:00 UTC' is the bar whose timestamp plus the bar length is 20:00 (timestamp is the "
               "start); high volatility is the 240-bar std of hourly returns at or above its 720-bar mean, recomputed "
               "from prices inside each window, and active bars where it cannot be computed (window warm-up) are left "
               "out of the agreement; the fall is the 24-bar price return below 0 (raw component sign where the return "
               "is not computable); the coin's mean 24-bar return uses the non-overlapping grid 0,24,48,... of every "
               "window pooled; one case per coin-day is the first qualifying bar of that UTC date.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": "t of mean forecast/10 x excess 24-bar return", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject, at least 100 cases"},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active), "active bars not checkable": int(n_unknown)},
            "decided_by": ("Fewer than 90% of the active (non-zero forecast) bars are long bars at the 20:00 UTC close "
                           "with high volatility after a 24-hour fall, as the plan's Fidelity requires."
                           if n_active > 0 else "No checkable active bars, so the forecast cannot be matched to the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. Criterion ----------
    # coin mean 24-bar return over all windows (non-overlapping grid)
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            c = df["close"].astype(float).values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    rets.append(c[p + H] / c[p] - 1)
        coin_mu[coin] = float(np.mean(rets)) if rets else np.nan

    vals, fcs, exc = [], [], []
    for coin, wins in bars.items():
        mu = coin_mu.get(coin, np.nan)
        if not np.isfinite(mu):
            continue
        seen_days = set()
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            c = d["close"].astype(float).values
            f = pd.to_numeric(d[FC], errors="coerce").values
            reg = d["regime"].astype(str).values
            n = len(d)
            for i in range(n):
                if reg[i] != "mean_reversion" or not np.isfinite(f[i]) or f[i] <= 0:
                    continue
                if i + H >= n:
                    continue
                day = ts.iloc[i].date()
                if day in seen_days:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0):
                    continue
                seen_days.add(day)
                e = c[i + H] / c[i] - 1 - mu
                exc.append(e)
                fcs.append(f[i])
                vals.append(f[i] / 10.0 * e)

    n_cases = len(vals)
    vals = np.asarray(vals, float)
    mean_v = float(np.mean(vals)) if n_cases > 0 else None
    t = None
    if n_cases > 1:
        sd = np.std(vals, ddof=1)
        t = float(mean_v / (sd / np.sqrt(n_cases))) if sd > 0 else None
    slope = None
    if n_cases > 2 and np.std(fcs) > 0:
        slope = float(stats.linregress(np.asarray(fcs, float), np.asarray(exc, float)).slope)
    slope_ok = None if slope is None else bool(slope > 0)

    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} cases, fewer than the plan's minimum of 100."
    elif t is not None and t >= 2 and slope_ok:
        status = "confirmed"
        decided = "Confirm rule met: t >= 2 with at least 100 cases and an OLS slope above 0."
    elif t is not None and t <= -2:
        status = "rejected"
        decided = "Reject rule met: t <= -2 with at least 100 cases."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule met: t >= 2 but the OLS slope is at or below 0."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule met: -2 < t < 2 with at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean of forecast/10 x excess 24-bar return",
                         "value": mean_v,
                         "statistic": None if t is None else {"name": "t of the mean", "value": t},
                         "threshold": "t >= 2 (confirm, with slope > 0) or t <= -2 (reject), with at least 100 cases"},
        "supporting_check": {"name": "OLS slope of excess 24-bar return on forecast", "value": slope,
                             "passed": slope_ok},
        "counts": {"cases": int(n_cases)},
        "decided_by": decided,
        "reading": reading,
    }
