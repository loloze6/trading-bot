import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.fall_in_swings.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ret1 = np.full(len(df), np.nan)
            if len(df) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # raw = 1-day return / 30-day std: its sign is the sign of the day's return
            sign_src = np.where(np.isnan(raw), ret1, raw)
            regime = df["regime"].astype(str).values
            for i in range(len(df)):
                if f[i] == 0 or np.isnan(f[i]):
                    continue
                n_active += 1
                fall = (not np.isnan(sign_src[i])) and sign_src[i] < 0
                calm = regime[i] != "chop"
                if fall and calm and f[i] < 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are calm-profile down days with a short forecast, as the Fidelity's situation (a one-day fall in a calm market, traded short) requires.",
            "reading": "The situation is a bar with a negative 1-day vol-scaled return (raw value, or the day's return from prices when not recorded) outside the 'chop' regime, with a negative forecast.",
        }

    # ---------- 2. criterion ----------
    # coin mean 5-bar return over all windows, on the non-overlapping grid
    coin_mu = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").values
            for t in range(0, len(close) - H, H):
                if np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0:
                    rs.append(close[t + H] / close[t] - 1.0)
        coin_mu[coin] = float(np.mean(rs)) if rs else np.nan

    rows = []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        if not np.isfinite(mu):
            continue
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for t in range(0, len(df) - H, H):
                if not (np.isfinite(f[t]) and f[t] < 0):
                    continue
                if not (np.isfinite(close[t]) and np.isfinite(close[t + H]) and close[t] > 0):
                    continue
                ex = close[t + H] / close[t] - 1.0 - mu
                rows.append({
                    "day": ts.iloc[t].strftime("%Y-%m-%d"),
                    "f": float(f[t]),
                    "gain": float(f[t] / 10.0 * ex),
                    "short_ex": float(-ex),
                })
    cases = pd.DataFrame(rows, columns=["day", "f", "gain", "short_ex"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    mean_gain = float(cases["gain"].mean()) if n_cases else None
    t_main = None
    if n_cases and n_days > 1:
        dev = cases["gain"] - mean_gain
        D = dev.groupby(cases["day"]).sum().values
        G = len(D)
        var = (G / (G - 1.0)) * np.sum(D ** 2) / (n_cases ** 2)
        t_main = float(mean_gain / np.sqrt(var)) if var > 0 else None

    sup_val, sup_t, sup_pass = None, None, None
    if n_cases >= 4:
        a = cases["f"].abs()
        med = a.median()
        up = cases.loc[a > med, "short_ex"].values
        lo = cases.loc[a <= med, "short_ex"].values
        if len(up) >= 2 and len(lo) >= 2:
            sup_val = float(np.mean(up) - np.mean(lo))
            tt = stats.ttest_ind(up, lo, equal_var=False).statistic
            sup_t = float(tt) if np.isfinite(tt) else None
            sup_pass = bool(sup_t is not None and sup_t >= 1.0)

    counts = {"cases": n_cases, "cases on distinct days": n_days}

    if n_days < 100:
        status = "not observable"
        decided = f"Fewer than 100 cases on distinct days ({n_days}), the plan's minimum."
    elif t_main is None:
        status = "inconclusive"
        decided = "The t of the mean excess gain could not be computed."
    elif mean_gain > 0 and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean excess gain is above 0 with t >= 2 and the supporting check passes (Welch t >= 1)."
    elif mean_gain < 0 and t_main <= -2:
        status = "rejected"
        decided = "The mean excess gain is below 0 with t <= -2."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess gain lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean excess gain of (forecast/10) x 5-bar excess return on grid cases",
            "value": mean_gain,
            "statistic": {"name": "t of the mean, same-day cases summed", "value": t_main} if t_main is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "upper minus lower |forecast| half, mean short-direction 5-bar excess return (Welch t >= 1)",
            "value": sup_t,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "The upper half is |forecast| strictly above the median and the lower half at or below it, the coin's mean 5-bar return is taken on the same non-overlapping grid of all its windows, the day-clustered t uses a G/(G-1) correction, and the supporting check's value is its Welch t (upper minus lower).",
    }
