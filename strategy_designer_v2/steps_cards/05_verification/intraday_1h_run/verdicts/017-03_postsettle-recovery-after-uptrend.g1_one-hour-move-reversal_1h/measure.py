import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fade.last_history_value"
    ALLOC = "postRebalance_current_allocation"

    def f(x):
        if x is None:
            return None
        x = float(x)
        return x if np.isfinite(x) else None

    # ---------- 1. Situation check: the forecast must fade the last-hour move ----------
    n_active = 0
    n_agree = 0
    prepared = {}  # coin -> list of per-window frames
    for coin, wins in bars.items():
        prepared[coin] = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True) if "timestamp" in df.columns else df.reset_index(drop=True)
            close = df["close"].astype(float)
            r1 = close / close.shift(1) - 1.0                      # last-hour return, inside the window
            vol20 = r1.rolling(20, min_periods=20).std()
            raw_recomp = r1 / vol20
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), raw_recomp)
            else:
                raw = raw_recomp
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: a last-hour move (raw != 0); expected side: opposite to the move (fade)
            agree = active & raw.notna() & (raw != 0) & (np.sign(fc) == -np.sign(raw))
            n_agree += int(agree.sum())

            nxt = close.shift(-1) / close - 1.0                    # next-bar return, inside the window
            vol720 = r1.rolling(720, min_periods=720).std()        # last 720 hourly returns, within window
            alloc = pd.to_numeric(df[ALLOC], errors="coerce") if ALLOC in df.columns else pd.Series(np.nan, index=df.index)
            prepared[coin].append(pd.DataFrame({"alloc": alloc, "nxt": nxt, "r1": r1, "vol720": vol720}))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = n_active > 0 and agreement >= 0.90

    main_name = "pooled mean per-bar excess gain: allocation x (next 1h return - coin's mean hourly return), before costs"
    main_threshold = "confirm if t >= 2 and the supporting check passes; reject if t <= -2; else inconclusive"
    sup_name = "Welch t of mean excess gain, bars above minus below the coin's median 720-bar volatility"

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of the active bars have a forecast opposite in sign to the last-hour vol-scaled move, so the config does not fade the move as the Fidelity states.",
            "reading": "Situation taken as any non-zero last-hour vol-scaled move (raw component value), expected side as the opposite sign of that move.",
        }

    # ---------- 2. Criterion ----------
    pooled_excess = []
    high_vals = []
    low_vals = []
    for coin, frames in prepared.items():
        if not frames:
            continue
        allr = pd.concat([fr["nxt"] for fr in frames])
        mu = allr.dropna().mean()  # coin's mean hourly return over all its windows
        coin_rows = []
        for fr in frames:
            ex = fr["alloc"] * fr["nxt"] - fr["alloc"] * mu
            d = pd.DataFrame({"ex": ex, "vol": fr["vol720"]})
            d = d[d["ex"].notna()]
            pooled_excess.append(d["ex"].values)
            coin_rows.append(d)
        cd = pd.concat(coin_rows) if coin_rows else pd.DataFrame({"ex": [], "vol": []})
        cv = cd[cd["vol"].notna()]
        if len(cv) > 0:
            med = cv["vol"].median()
            high_vals.append(cv.loc[cv["vol"] > med, "ex"].values)
            low_vals.append(cv.loc[cv["vol"] < med, "ex"].values)

    ex_all = np.concatenate(pooled_excess) if pooled_excess else np.array([])
    hi = np.concatenate(high_vals) if high_vals else np.array([])
    lo = np.concatenate(low_vals) if low_vals else np.array([])
    n_pool, n_hi, n_lo = int(len(ex_all)), int(len(hi)), int(len(lo))

    main_mean = f(ex_all.mean()) if n_pool > 0 else None
    main_t = None
    if n_pool > 1:
        sd = ex_all.std(ddof=1)
        main_t = f(ex_all.mean() / (sd / np.sqrt(n_pool))) if sd > 0 else None

    sup_t = None
    if n_hi > 1 and n_lo > 1:
        sup_t = f(stats.ttest_ind(hi, lo, equal_var=False).statistic)
    sup_pass = (sup_t is not None and sup_t >= 2.0) if sup_t is not None else None

    counts = {"bars pooled": n_pool, "high-volatility group bars": n_hi, "low-volatility group bars": n_lo}

    if n_pool < 10000:
        status, decided = "not observable", "Fewer than 10,000 bars pooled, the plan's minimum."
    elif n_hi < 2000 or n_lo < 2000:
        status, decided = "not observable", "A volatility group has fewer than 2,000 bars, the plan's minimum."
    elif main_t is None:
        status, decided = "inconclusive", "The main t could not be computed (zero variance), meeting neither confirm nor reject."
    elif main_t <= -2.0:
        status, decided = "rejected", "The main mean excess gain has t <= -2 (reject rule)."
    elif main_t >= 2.0 and sup_pass:
        status, decided = "confirmed", "The main mean excess gain has t >= 2 and the high-minus-low volatility Welch t is >= 2 (confirm rule)."
    elif main_t >= 2.0:
        status, decided = "inconclusive", "The main t is >= 2 but the supporting check's Welch t is below 2 (inconclusive rule)."
    else:
        status, decided = "inconclusive", "The main t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": main_mean,
            "statistic": {"name": "t of the mean", "value": main_t} if main_t is not None else None,
            "threshold": main_threshold,
        },
        "supporting_check": {"name": sup_name, "value": sup_t, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Every bar with a next in-window close counts (flat bars give zero excess), the coin mean is its pooled in-window hourly return, the 720-bar volatility uses the 720 in-window hourly returns up to the bar (sample std), the median is per coin over bars with that volatility, bars exactly at the median are left out of both groups, and the groups are pooled across coins for the Welch t and the 2,000 minimum.",
    }
