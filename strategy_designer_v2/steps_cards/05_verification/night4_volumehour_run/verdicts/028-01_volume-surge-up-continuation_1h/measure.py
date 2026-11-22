import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 6
    BAND = 2.0
    VOL_LOOKBACK = 720
    RAW = "debug_info.components.vol_move.last_history_value"

    # ---------- 1. Situation check: active bars must be up-hours (raw product > 0), long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ret1 = np.full(len(df), np.nan)
            if len(df) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            # situation sign: raw component value (return x volume ratio); fall back to the hour's price return
            sit_val = np.where(np.isnan(raw), ret1, raw)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & (sit_val > 0) & (fc > 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean excess 6-bar return over long-bet cases", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects, with at least 100 cases"},
            "supporting_check": None,
            "counts": {"cases": 0, "active bars": n_active},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are up-hours (positive return x volume ratio) with a long forecast, as the plan's situation and side require.",
            "reading": "none",
        }

    # ---------- 2. Coin's mean 6-bar return over all windows (non-overlapping grid) ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            close = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(close) - H, H):
                r = close[i + H] / close[i] - 1.0
                if np.isfinite(r):
                    rets.append(r)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    # ---------- 3. Cases: long bets (forecast rise >= 2 from its lowest since last bet), once per 6-bar cell ----------
    excess_all = []
    sup_x, sup_y = [], []
    for coin, wins in bars.items():
        cm = coin_mean[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            vol = pd.to_numeric(df["volume"], errors="coerce").values
            n = len(df)
            bet = np.zeros(n, dtype=bool)
            trough = 0.0
            for t in range(n):
                f = fc[t]
                if f <= 0:
                    trough = 0.0
                    continue
                if f - trough >= BAND:
                    bet[t] = True
                    trough = f
                else:
                    trough = min(trough, f)
            for start in range(0, n, H):
                idx = np.where(bet[start:start + H])[0]
                if len(idx) == 0:
                    continue
                t = start + int(idx[0])
                if t + H >= n:
                    continue
                r = close[t + H] / close[t] - 1.0
                if not np.isfinite(r) or not np.isfinite(cm):
                    continue
                ex = r - cm
                excess_all.append(ex)
                if t >= VOL_LOOKBACK:
                    prior = vol[t - VOL_LOOKBACK:t]
                    m = np.nanmean(prior)
                    if np.isfinite(m) and m > 0 and np.isfinite(vol[t]):
                        sup_x.append(vol[t] / m)
                        sup_y.append(ex)

    n_cases = len(excess_all)
    n_sup = len(sup_x)
    ex = np.array(excess_all, dtype=float)
    mean_ex = float(ex.mean()) if n_cases > 0 else None
    t_main = None
    if n_cases > 1:
        sd = ex.std(ddof=1)
        t_main = float(mean_ex / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    slope = slope_t = None
    if n_sup >= 3 and np.std(sup_x) > 0:
        lr = stats.linregress(np.array(sup_x), np.array(sup_y))
        slope = float(lr.slope)
        slope_t = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0
    sup_pass = (slope > 0) if slope is not None else None

    # ---------- 4. Decision ----------
    if n_cases < 100:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 100 cases."
    elif (t_main is not None and t_main <= -2) or (slope_t is not None and slope_t <= -2):
        status = "rejected"
        if t_main is not None and t_main <= -2:
            decided = "Reject rule: the mean excess 6-bar return has t <= -2 with at least 100 cases."
        else:
            decided = "Reject rule: the slope of excess return on volume ratio has t <= -2."
    elif t_main is not None and t_main >= 2 and sup_pass:
        status = "confirmed"
        decided = "Confirm rule: mean excess 6-bar return has t >= 2 with at least 100 cases and the supporting slope is above 0."
    else:
        status = "inconclusive"
        if t_main is not None and t_main >= 2:
            decided = "Inconclusive rule: confirming main measure but the supporting slope is at or below 0 (or not computable) with t above -2."
        else:
            decided = "Inconclusive rule: the main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean excess 6-bar return over long-bet cases",
                         "value": mean_ex,
                         "statistic": {"name": "t of the mean", "value": t_main} if t_main is not None else None,
                         "threshold": "t >= 2 confirms, t <= -2 rejects, with at least 100 cases"},
        "supporting_check": {"name": "OLS slope of excess return on volume ratio (cases at bar >= 720)",
                             "value": slope, "passed": sup_pass},
        "counts": {"cases": n_cases, "cases at or after bar 720": n_sup},
        "decided_by": decided,
        "reading": "A bet is a forecast rise of at least 2 from its lowest positive level since the last bet (reset to 0 when flat), each 6-bar grid cell counts once at its first bet, the reject rule is checked before the confirm rule, and fewer than 100 cases is reported as not observable per the workflow's minimum-count rule.",
    }
