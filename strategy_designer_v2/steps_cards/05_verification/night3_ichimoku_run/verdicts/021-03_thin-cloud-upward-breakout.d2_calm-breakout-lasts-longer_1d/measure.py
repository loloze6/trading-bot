import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 40
    BAND = 2.0
    FC = "forecast"

    def cloud_state(df):
        # Ichimoku 9/26/52, displacement 26, from the window's own prices only
        hi = df["high"].astype(float)
        lo = df["low"].astype(float)
        cl = df["close"].astype(float)
        tenkan = (hi.rolling(9).max() + lo.rolling(9).min()) / 2.0
        kijun = (hi.rolling(26).max() + lo.rolling(26).min()) / 2.0
        span_a = ((tenkan + kijun) / 2.0).shift(26)
        span_b = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2.0).shift(26)
        top = np.maximum(span_a, span_b)
        bot = np.minimum(span_a, span_b)
        st = np.full(len(df), np.nan)
        valid = (top.notna() & bot.notna() & cl.notna()).values
        c, t, b = cl.values, top.values, bot.values
        for i in range(len(df)):
            if valid[i]:
                st[i] = 1.0 if c[i] > t[i] else (-1.0 if c[i] < b[i] else 0.0)
        return st

    def cross_flags(st):
        # 1 = first close above after last outside side was below, 0 = not, nan = unknown
        out = np.full(len(st), np.nan)
        for i in range(len(st)):
            if np.isnan(st[i]):
                continue
            if st[i] != 1.0:
                out[i] = 0.0
                continue
            res = np.nan
            j = i - 1
            while j >= 0:
                if np.isnan(st[j]):
                    res = np.nan
                    break
                if st[j] == 1.0:
                    res = 0.0
                    break
                if st[j] == -1.0:
                    res = 1.0
                    break
                j -= 1
            out[i] = res
        return out

    # ---------- situation check ----------
    n_active = 0
    n_checkable = 0
    n_agree_checkable = 0
    n_agree_regime = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            cr = cross_flags(cloud_state(df))
            reg = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            for i in range(len(df)):
                if f[i] == 0:
                    continue
                n_active += 1
                if reg[i] == "trending" and f[i] > 0:
                    n_agree_regime += 1
                if not np.isnan(cr[i]):
                    n_checkable += 1
                    if cr[i] == 1.0 and f[i] > 0:
                        n_agree_checkable += 1

    if n_active == 0:
        agreement = None
    elif n_checkable > 0:
        agreement = n_agree_checkable / n_checkable
    else:
        agreement = n_agree_regime / n_active
    sit_passed = bool(agreement is not None and agreement >= 0.9)

    reading = ("Situation agreement is measured on the active bars where the cloud and the last outside side can be "
               "recomputed from the window's own prices (falling back to regime 'trending' with a long forecast only if "
               "none can); cases are long bets (forecast rise of >= 2 points from its low on the long side) read once "
               "per 40-bar grid cell from each window's first row with close[t+40] in the window; drift and usual move "
               "are the mean and std of each coin's non-overlapping 40-bar returns over all its windows; the weighted "
               "mean's t uses the forecast-weighted variance with effective n = (sum w)^2 / sum w^2; the median split "
               "drops cases equal to the median and compares unscaled drift-adjusted returns.")

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "forecast-weighted mean of drift-adjusted 40-bar return / usual 40-bar move",
                             "value": None, "statistic": None, "threshold": "> 0 with t >= 2 (reject t <= -2)"},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": "No active bar in the record: fewer than 30 cases in total.",
            "reading": reading,
        }

    if not sit_passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "forecast-weighted mean of drift-adjusted 40-bar return / usual 40-bar move",
                             "value": None, "statistic": None, "threshold": "> 0 with t >= 2 (reject t <= -2)"},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": ("Fewer than 90 % of the active bars are long bets on the first close above the Ichimoku "
                           "cloud after the last outside side was below, as the plan's Fidelity states."),
            "reading": reading,
        }

    # ---------- coin drift and usual move ----------
    coin_stats = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for p in range(0, len(c) - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] > 0:
                    rets.append(c[p + H] / c[p] - 1.0)
        rets = np.array(rets)
        if len(rets) >= 2:
            coin_stats[coin] = (float(np.mean(rets)), float(np.std(rets, ddof=1)))
        else:
            coin_stats[coin] = (np.nan, np.nan)

    # ---------- cases ----------
    vals, adj, fcs = [], [], []
    for coin, wins in bars.items():
        drift, usual = coin_stats[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df[FC], errors="coerce").values
            c = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            side_long = False
            low = 0.0
            used_cells = set()
            for i in range(n):
                fi = f[i]
                if not np.isfinite(fi):
                    continue
                if fi > 0:
                    if not side_long:
                        side_long = True
                        low = 0.0
                    low = min(low, fi)
                    if fi - low >= BAND:
                        low = fi
                        cell = i // H
                        if cell in used_cells:
                            continue
                        used_cells.add(cell)
                        if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0 \
                                and np.isfinite(drift) and np.isfinite(usual) and usual > 0:
                            r = c[i + H] / c[i] - 1.0
                            adj.append(r - drift)
                            vals.append((r - drift) / usual)
                            fcs.append(fi)
                else:
                    side_long = False
                    low = 0.0

    vals = np.array(vals, dtype=float)
    adj = np.array(adj, dtype=float)
    fcs = np.array(fcs, dtype=float)
    n_cases = int(len(vals))

    main_name = "forecast-weighted mean of drift-adjusted 40-bar return / usual 40-bar move"
    main_thr = "confirm: > 0 with t >= 2; reject: t <= -2"
    sup_name = "calm minus violent half (median forecast split), mean drift-adjusted 40-bar return"

    wmean, wt = None, None
    if n_cases >= 2 and fcs.sum() > 0:
        wsum = fcs.sum()
        wmean = float(np.sum(vals * fcs) / wsum)
        wvar = float(np.sum(fcs * (vals - wmean) ** 2) / wsum) * n_cases / (n_cases - 1)
        n_eff = wsum ** 2 / np.sum(fcs ** 2)
        se = np.sqrt(wvar / n_eff) if wvar > 0 else 0.0
        wt = float(wmean / se) if se > 0 else None
    elif n_cases == 1:
        wmean = float(vals[0])

    diff, welch = None, None
    n_high, n_low = 0, 0
    if n_cases > 0:
        med = float(np.median(fcs))
        hi = adj[fcs > med]
        lo = adj[fcs < med]
        n_high, n_low = int(len(hi)), int(len(lo))
        if n_high > 0 and n_low > 0:
            diff = float(np.mean(hi) - np.mean(lo))
        if n_high >= 2 and n_low >= 2:
            tt = stats.ttest_ind(hi, lo, equal_var=False)
            if np.isfinite(tt.statistic):
                welch = float(tt.statistic)

    counts = {"cases": n_cases, "high-forecast half": n_high, "low-forecast half": n_low}

    sup_passed = None
    if diff is not None and welch is not None:
        sup_passed = bool(diff > 0 and welch >= 2)

    result = {
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": wmean,
                         "statistic": ({"name": "t of the forecast-weighted mean", "value": wt} if wt is not None else None),
                         "threshold": main_thr},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_passed,
                             "welch_t": welch},
        "counts": counts,
        "reading": reading,
    }

    if n_cases < 30:
        result["status"] = "not observable"
        result["decided_by"] = "Fewer than 30 cases in total over the coins and windows (minimum count not reached)."
        return result

    main_reject = wt is not None and wt <= -2
    sup_reject = welch is not None and welch <= -2
    if main_reject or sup_reject:
        result["status"] = "rejected"
        result["decided_by"] = ("Reject rule met: the weighted mean has t <= -2" if main_reject else
                                "Reject rule met: the calm-minus-violent difference has Welch t <= -2") + "."
        return result

    main_conf = wmean is not None and wt is not None and wmean > 0 and wt >= 2
    if main_conf and sup_passed:
        result["status"] = "confirmed"
        result["decided_by"] = ("Confirm rule met: the weighted mean is above 0 with t >= 2 and the calm-minus-violent "
                                "difference is above 0 with Welch t >= 2.")
        return result

    result["status"] = "inconclusive"
    if main_conf:
        result["decided_by"] = ("The weighted mean meets the confirm rule but the calm-minus-violent difference does "
                                "not reach > 0 with Welch t >= 2, so the result is inconclusive.")
    else:
        result["decided_by"] = "Neither the confirm nor the reject rule is met: inconclusive (any other result)."
    return result
