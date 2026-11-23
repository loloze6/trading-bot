import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    RAW = "debug_info.components.fade.last_history_value"

    def raw_from_prices(close):
        r = close.pct_change()
        vol = r.rolling(24, min_periods=24).std(ddof=1)
        return r / vol

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw = raw.where(raw.notna(), raw_from_prices(close))
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            fa = f[active]
            ra = raw[active]
            ok = ra.notna() & (ra.abs() < 3.0) & (ra != 0) & (np.sign(fa) == -np.sign(ra))
            n_agree += int(ok.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a nonzero forecast are bars with a moderate "
                          "(|scaled shock| < 3) hourly shock faded on the opposite side, as the Fidelity requires.",
            "reading": "The situation is |last_history_value| < 3 with the forecast's sign opposite to the shock's; "
                       "missing raw values are recomputed from closes (1h return / 24-bar std).",
        }

    # ---------- 2. criterion ----------
    # coin's mean 24-bar return over all windows (non-overlapping grid)
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            n = len(close)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
                    rets.append(c1 / c0 - 1.0)
        coin_mu[coin] = float(np.mean(rets)) if rets else np.nan

    fs, xs, dirr = [], [], []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(close)
            for t in range(0, n - H, H):
                ft = f[t]
                if not np.isfinite(ft) or ft == 0:
                    continue
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1) and c0 > 0):
                    continue
                dr = c1 / c0 - 1.0 - mu
                fs.append(ft)
                xs.append(ft / 10.0 * dr)
                dirr.append(np.sign(ft) * dr)

    fs = np.array(fs, dtype=float)
    xs = np.array(xs, dtype=float)
    dirr = np.array(dirr, dtype=float)
    n_cases = int(len(xs))

    mean_x = float(np.mean(xs)) if n_cases > 0 else None
    if n_cases > 1 and np.std(xs, ddof=1) > 0:
        t_main = float(np.mean(xs) / (np.std(xs, ddof=1) / np.sqrt(n_cases)))
    else:
        t_main = None

    top_mean = bot_mean = diff = None
    sup_passed = None
    if n_cases >= 3:
        order = np.argsort(np.abs(fs), kind="mergesort")
        thirds = np.array_split(order, 3)
        bot_mean = float(np.mean(dirr[thirds[0]]))
        top_mean = float(np.mean(dirr[thirds[2]]))
        diff = top_mean - bot_mean
        sup_passed = bool(top_mean > bot_mean)

    main = {
        "name": "t of mean of forecast/10 x drift-removed 24-bar return",
        "value": mean_x,
        "statistic": {"name": "t of the mean", "value": t_main} if t_main is not None else None,
        "threshold": "confirm if t >= 2 (with top third beating bottom third); reject if t <= -2",
    }
    support = {
        "name": "top-third minus bottom-third mean drift-removed return in forecast direction",
        "value": diff,
        "passed": sup_passed,
    }
    counts = {"cases with a nonzero forecast": n_cases}
    reading = ("Cases are grid bars 0,24,48,... of each window with a nonzero forecast and a close 24 bars later "
               "in the same window; the coin's mean is over its non-overlapping 24-bar grid returns of all windows; "
               "thirds are pooled over all cases by |forecast| (stable sort, numpy array_split); the plan's "
               "'fewer than 500 cases' is treated as the minimum count giving 'not observable'.")

    if n_cases < 500 or t_main is None:
        status = "not observable"
        decided = "Fewer than 500 cases with a nonzero forecast (minimum count not reached)."
    elif t_main >= 2 and sup_passed:
        status = "confirmed"
        decided = "The main t is 2 or more and the top third beats the bottom third."
    elif t_main <= -2:
        status = "rejected"
        decided = "The main t is -2 or less."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more but the top third does not beat the bottom third."
    else:
        status = "inconclusive"
        decided = "The main t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
