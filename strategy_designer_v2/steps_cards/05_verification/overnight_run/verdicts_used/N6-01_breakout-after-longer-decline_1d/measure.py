import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.range_top.last_history_value"

    def fwd_ret(close, h):
        c = close.to_numpy(dtype=float)
        out = np.full(len(c), np.nan)
        if len(c) > h:
            out[:-h] = c[h:] / c[:-h] - 1.0
        return out

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if not active.any():
                continue
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                top = raw > 0
            else:
                top = pd.Series(False, index=df.index)
            sit = (reg == "trending") & top & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & sit).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.90
    else:
        agreement = None
        passed = True

    reading = ("Situation bars are those with regime 'trending' (the detector's close-below-close-60-bars-ago rule) "
               "and range_top raw value > 0 (upper half of the 21-close range, the graded 'top of range'), on the long side; "
               "the coin's mean 10-bar return is over all its bars with a 10-bar forward return in all windows (overlapping); "
               "qualifying bars (forecast >= 10) are chained into one case while each is within 10 bars of the previous "
               "qualifying bar in the same window, and each case takes the excess return of its first bar; "
               "the t is the ordinary t of the mean; the supporting correlation is Pearson on trending bars at grid positions 0,10,20,... of each window.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean forward 10-bar excess return after forecast >= 10",
                             "value": None, "statistic": None,
                             "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"independent cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars in the 'trending' regime "
                           "(close below its close 60 bars earlier) with the close in the upper part of its 21-close range."),
            "reading": reading,
        }

    # ---------- 2. coin mean 10-bar return, pooled over windows ----------
    coin_mean = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            r = fwd_ret(pd.to_numeric(df["close"], errors="coerce"), H)
            allr.append(r[np.isfinite(r)])
        allr = np.concatenate(allr) if allr else np.array([])
        coin_mean[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- 3. main measure ----------
    cases = []
    sup_f, sup_x = [], []
    for coin, wins in bars.items():
        m = coin_mean.get(coin, np.nan)
        if not np.isfinite(m):
            continue
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            r = fwd_ret(pd.to_numeric(df["close"], errors="coerce"), H)
            ex = r - m
            # declustered qualifying bars
            q = np.where((fc >= 10) & np.isfinite(ex))[0]
            last = None
            for i in q:
                if last is None or i - last > H:
                    cases.append(float(ex[i]))
                last = i
            # supporting check grid
            reg = df["regime"].astype(str).to_numpy() if "regime" in df.columns else np.array([""] * len(df))
            for i in range(0, len(df), H):
                if reg[i] == "trending" and np.isfinite(fc[i]) and np.isfinite(ex[i]):
                    sup_f.append(fc[i])
                    sup_x.append(ex[i])

    cases = np.array(cases, dtype=float)
    n_cases = int(len(cases))
    mean_ex = float(np.mean(cases)) if n_cases > 0 else None
    t = None
    if n_cases >= 2:
        sd = float(np.std(cases, ddof=1))
        if sd > 0:
            t = float(mean_ex / (sd / np.sqrt(n_cases)))

    sup_f = np.array(sup_f)
    sup_x = np.array(sup_x)
    corr = None
    if len(sup_f) >= 3 and np.std(sup_f) > 0 and np.std(sup_x) > 0:
        corr = float(stats.pearsonr(sup_f, sup_x)[0])
    sup_passed = None if corr is None else bool(corr > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 independent cases ({n_cases}), the plan's minimum count, so the data cannot show the idea."
    elif t is not None and mean_ex > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean excess return is greater than 0 with t >= 2 over the independent cases."
    elif t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "The mean excess return is below 0 with t <= -2 over the independent cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2, which neither confirms nor rejects."

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": True},
        "main_measure": {"name": "mean forward 10-bar excess return after forecast >= 10",
                         "value": mean_ex,
                         "statistic": None if t is None else {"name": "t of the mean", "value": t},
                         "threshold": "mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects"},
        "supporting_check": {"name": "correlation of forecast with forward 10-bar excess return, trending bars, non-overlapping",
                             "value": corr, "passed": sup_passed},
        "counts": {"independent cases": n_cases, "supporting samples": int(len(sup_f))},
        "decided_by": decided,
        "reading": reading,
    }
