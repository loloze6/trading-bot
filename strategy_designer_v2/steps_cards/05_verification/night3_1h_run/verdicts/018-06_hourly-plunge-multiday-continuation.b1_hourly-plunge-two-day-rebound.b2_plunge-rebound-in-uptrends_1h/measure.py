import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 96
    BAND = 2.0
    RAW = "debug_info.components.plunge_in_uptrend.last_history_value"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            fc = df["forecast"].astype(float)
            # situation from prices: a 24-hour fall while the 30-day return is positive
            r24 = close / close.shift(24) - 1.0
            r720 = close / close.shift(720) - 1.0
            sit_price = (r24 < 0) & (r720 > 0)
            price_known = r24.notna() & r720.notna()
            # situation from the component's raw value: the fall-times-rise product is positive
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            raw_known = raw.notna()
            sit = pd.Series(False, index=df.index)
            sit[raw_known] = raw[raw_known] > 0
            fb = (~raw_known) & price_known
            sit[fb] = sit_price[fb]
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # expected side: long (the outcome is a rise)
            n_agree += int((active & sit & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean unusual 96-bar move of the cases (return minus the coin's normal 96-bar drift)"
    main_thr = "confirm: mean > 0 with t >= 2 on >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 on >= 30 cases"
    sup_name = "mean unusual move of cases above the median entry forecast minus that of cases below it"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("fewer than 90% of the bars with a non-zero forecast are long bars of the plan's "
                           "situation (a 24-hour fall while the 30-day return is positive)"),
            "reading": "the situation is taken as a positive raw fall-times-rise value (any 24-hour fall with a positive 30-day return, the graded threshold), recomputed from prices where the raw value is missing",
        }

    # ---------- 2. Criterion ----------
    # normal 96-bar drift per coin: non-overlapping grid of all windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = df.sort_values("timestamp")["close"].astype(float).to_numpy()
            idx = np.arange(0, len(close) - H, H)
            if len(idx):
                r = close[idx + H] / close[idx] - 1.0
                rets.extend(r[np.isfinite(r)].tolist())
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    unusual = []
    entry_fc = []
    for coin, wins in bars.items():
        if not np.isfinite(drift.get(coin, np.nan)):
            continue
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).to_numpy()
            fc = df["forecast"].astype(float).fillna(0.0).to_numpy()
            n = len(fc)
            # bets: a rise of the long forecast of at least the band from its lowest level since the last bet
            low = 0.0
            bet = np.zeros(n, dtype=bool)
            for i in range(n):
                f = fc[i]
                if f <= 0:
                    low = 0.0
                    continue
                if f - low >= BAND:
                    bet[i] = True
                    low = f
                else:
                    low = min(low, f)
            seen = set()
            for i in np.where(bet)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                unusual.append(r - drift[coin])
                entry_fc.append(fc[i])

    u = np.array(unusual, dtype=float)
    e = np.array(entry_fc, dtype=float)
    ncases = int(len(u))
    mean_u = float(np.mean(u)) if ncases else None
    t = None
    if ncases >= 2:
        sd = float(np.std(u, ddof=1))
        t = float(mean_u / (sd / np.sqrt(ncases))) if sd > 0 else None

    sup_val = None
    if ncases >= 2:
        med = float(np.median(e))
        hi = u[e > med]
        lo = u[e < med]
        if len(hi) and len(lo):
            sup_val = float(np.mean(hi) - np.mean(lo))
    sup_pass = (sup_val > 0) if sup_val is not None else None

    if ncases < 30:
        status = "not observable"
        decided = f"fewer than the plan's minimum of 30 cases across all coins and windows ({ncases})."
    elif t is None:
        status = "inconclusive"
        decided = "the t of the mean could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_u > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "mean unusual move above 0 with t >= 2 on at least 30 cases, and the supporting check above 0."
    elif mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "mean unusual move below 0 with t <= -2 on at least 30 cases."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check is not above 0."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_val,
                             "passed": (bool(sup_pass) if sup_pass is not None else None)},
        "counts": {"cases": ncases},
        "decided_by": decided,
        "reading": ("the situation is a positive raw fall-times-rise value (prices used where the raw value is missing); "
                    "a case is the first bet (forecast rise >= 2 from its lowest level since the last bet, reset at 0) in each "
                    "96-bar grid cell from a window's first row, cases without 96 bars left in their window are dropped, and the "
                    "supporting split uses cases strictly above versus strictly below the median entry forecast."),
    }
