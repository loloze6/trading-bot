import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.rise.last_history_value"
    EPS = 1e-9

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if FC not in df.columns or len(df) == 0:
                continue
            fc = pd.to_numeric(df[FC], errors="coerce")
            vol = pd.to_numeric(df["volume"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # volume / 30-bar average (current bar included), inside the window only
            vr = vol / vol.rolling(30, min_periods=30).mean()
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            thin_from_regime = regime.isin(["mean_reversion", "chop"])
            thin = np.where(vr.notna(), vr <= 0.75 + EPS, thin_from_regime)
            # rise: the component's raw vol-scaled return > 0, else the bar's own return > 0
            ret1 = close / close.shift(1) - 1
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            rise = np.where(raw.notna(), raw > 0, ret1 > 0)
            active = fc.notna() & (fc != 0)
            situ = pd.Series(thin, index=df.index).astype(bool) & pd.Series(rise, index=df.index).astype(bool) & (fc < 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean 5-bar excess return after thin-volume rise events (forecast <= -2)"
    threshold = "confirm: mean <= 0 with t <= -2 on >= 30 events and check passes; reject: mean >= 0 with t >= +2 on >= 30 events"
    reading = ("Thin volume is recomputed as volume over its 30-bar mean including the current bar (the regime column where "
               "30 bars are not yet available in the window), a rise is the recorded raw vol-scaled return > 0 (else the "
               "bar's return); events are de-overlapped before dropping those without a 5-bar return inside the window; "
               "the larger half is |forecast| strictly above the median and the smaller half at or below it, and an empty "
               "half fails the check.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active, "non-overlapping events": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short forecasts on thin-volume "
                           "(ratio <= 0.75) rise days, so the config does not do what the plan's situation says."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    # coin mean 5-bar return over all windows, non-overlapping grid
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            for p in range(0, len(close) - H, H):
                a, b = close[p], close[p + H]
                if np.isfinite(a) and np.isfinite(b) and a != 0:
                    rets.append(b / a - 1)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    ex, absf = [], []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df[FC], errors="coerce").to_numpy()
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            last_kept = None
            for t in range(len(df)):
                if not (np.isfinite(fc[t]) and fc[t] <= -2):
                    continue
                if last_kept is not None and t - last_kept < H:
                    continue
                last_kept = t
                if t + H >= len(df):
                    continue
                a, b = close[t], close[t + H]
                if not (np.isfinite(a) and np.isfinite(b) and a != 0) or not np.isfinite(coin_mean[coin]):
                    continue
                ex.append(b / a - 1 - coin_mean[coin])
                absf.append(abs(fc[t]))

    ex = np.array(ex, dtype=float)
    absf = np.array(absf, dtype=float)
    n = len(ex)

    mean_ex = float(ex.mean()) if n > 0 else None
    t_stat = None
    if n > 1:
        sd = ex.std(ddof=1)
        if sd > 0:
            t_stat = float(mean_ex / (sd / np.sqrt(n)))

    sup_val, sup_pass = None, None
    if n > 0:
        med = np.median(absf)
        big = ex[absf > med]
        small = ex[absf <= med]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val <= 0)
        else:
            sup_pass = False

    if n < 30:
        status = "not observable"
        decided = f"Only {n} non-overlapping events, below the plan's minimum of 30."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_ex <= 0 and t_stat <= -2 and sup_pass:
        status = "confirmed"
        decided = "Mean excess return <= 0 with t <= -2 on at least 30 events, and the larger-|forecast| half gives back at least as much."
    elif mean_ex >= 0 and t_stat >= 2:
        status = "rejected"
        decided = "Mean excess return >= 0 with t >= +2 on at least 30 events."
    elif t_stat <= -2:
        status = "inconclusive"
        decided = "t <= -2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and +2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t_stat} if t_stat is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess return, larger-|forecast| half minus smaller half (must be <= 0)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"non-overlapping events": int(n), "active bars": int(n_active)},
        "decided_by": decided,
        "reading": reading,
    }
