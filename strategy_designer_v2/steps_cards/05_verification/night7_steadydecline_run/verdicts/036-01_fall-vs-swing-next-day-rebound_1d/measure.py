import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.rel_fall.last_history_value"

    # ---------- collect per-bar data, window by window (never joining windows) ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        all_rets = []
        for wname, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = d["close"].astype(float)
            r1 = close.pct_change()                 # day's close-to-close return, inside the window
            nxt = close.shift(-1) / close - 1.0     # next-day return, inside the window
            all_rets.append(nxt.dropna().values)
            # recomputed raw component (period 1, vol_period 30) for bars where it is not recorded
            vol = r1.rolling(30, min_periods=30).std()
            recomputed = r1 / vol.replace(0, np.nan)
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            rows.append(pd.DataFrame({
                "coin": coin,
                "window": wname,
                "timestamp": d["timestamp"],
                "day": d["timestamp"].dt.floor("D"),
                "forecast": fc,
                "raw": raw,
                "next_ret": nxt,
            }))
        coin_rets[coin] = np.concatenate(all_rets) if all_rets else np.array([])

    if not rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": None, "supporting_check": None,
            "counts": {"cases": 0, "distinct days": 0},
            "decided_by": "No bars in the record.", "reading": "none",
        }
    data = pd.concat(rows, ignore_index=True)

    # ---------- 1. situation check ----------
    active = data[data["forecast"] != 0]
    n_active = len(active)
    if n_active > 0:
        in_sit = (active["raw"] <= -1.0) & (active["forecast"] > 0)
        agreement = float(in_sit.sum()) / n_active
    else:
        agreement = 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.9)

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars whose one-day "
                           "return is at least one 30-day standard deviation down (raw value <= -1)"
                           if n_active > 0 else "The forecast is never non-zero."),
            "reading": "Situation = raw VolatilityScaledReturn(1,30) <= -1 (recorded value, else recomputed from closes) with a long (positive) forecast.",
        }

    # ---------- 2. criterion ----------
    coin_mean = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_rets.items()}
    cases = data[(data["forecast"] > 0) & data["next_ret"].notna()].copy()
    cases["excess"] = cases["next_ret"] - cases["coin"].map(coin_mean)
    cases = cases[cases["excess"].notna()]
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    counts = {"cases": n_cases, "distinct days": n_days}
    threshold = "confirm: mean > 0 with t >= 2 (and supporting check); reject: mean < 0 with t <= -2"
    reading = ("Next-day return is close[t+1]/close[t]-1 within a window on every case bar (horizon 1 bar, so the grid "
               "is every bar); the coin's mean is over all its next-day returns in all windows; the day-clustered t "
               "uses deviations from the mean summed per UTC day with SE = sqrt(D/(D-1) * sum S_d^2)/n; the thirds "
               "are the first and last floor(n/3) cases sorted by forecast (ties by timestamp, then coin) and the "
               "check passes when the top-minus-bottom difference of means is > 0.")

    # main measure
    if n_cases > 0:
        m = float(cases["excess"].mean())
        dev = cases["excess"] - m
        S = dev.groupby(cases["day"]).sum().values
        D = len(S)
        if D > 1 and n_cases > 0:
            var = (D / (D - 1.0)) * float(np.sum(S ** 2)) / (n_cases ** 2)
            t = m / np.sqrt(var) if var > 0 else np.nan
        else:
            t = np.nan
    else:
        m, t = np.nan, np.nan

    # supporting check
    sup_val, sup_pass, welch_t = None, None, None
    k = n_cases // 3
    if k >= 2:
        srt = cases.sort_values(["forecast", "timestamp", "coin"], kind="mergesort")
        bottom = srt["excess"].values[:k]
        top = srt["excess"].values[-k:]
        sup_val = float(np.mean(top) - np.mean(bottom))
        wt = stats.ttest_ind(top, bottom, equal_var=False).statistic
        welch_t = float(wt) if np.isfinite(wt) else None
        sup_pass = bool(sup_val > 0)

    main = {
        "name": "mean next-day return minus coin's mean daily return, on bars with forecast > 0",
        "value": (float(m) if np.isfinite(m) else None),
        "statistic": ({"name": "t of the mean, cases clustered by day", "value": float(t)}
                      if np.isfinite(t) else None),
        "threshold": threshold,
    }
    supporting = {
        "name": "top third minus bottom third by forecast, mean next-day excess return"
                + (f" (Welch t {welch_t:.3f})" if welch_t is not None else ""),
        "value": sup_val,
        "passed": sup_pass,
    }

    # minimum counts first
    if n_cases < 300 or n_days < 200:
        miss = []
        if n_cases < 300:
            miss.append(f"{n_cases} cases < 300")
        if n_days < 200:
            miss.append(f"{n_days} distinct days < 200")
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": main,
            "supporting_check": supporting,
            "counts": counts,
            "decided_by": "The plan's minimum count is not reached: " + "; ".join(miss) + ".",
            "reading": reading,
        }

    if np.isfinite(m) and np.isfinite(t) and m > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Confirm rule met: mean excess next-day return above 0 with t >= 2, and top third above bottom third."
        else:
            status = "inconclusive"
            decided = "Inconclusive rule: the main measure confirms (mean > 0, t >= 2) but the supporting check fails."
    elif np.isfinite(m) and np.isfinite(t) and m < 0 and t <= -2:
        status = "rejected"
        decided = "Reject rule met: mean excess next-day return below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule: the t of the main measure lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
