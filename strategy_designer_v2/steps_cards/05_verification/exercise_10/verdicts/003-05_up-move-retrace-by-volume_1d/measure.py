import numpy as np
import pandas as pd


def measure(bars):
    H_COL = "debug_info.components.heavy_up.last_history_value"
    T_COL = "debug_info.components.thin_up.last_history_value"

    def wstats(x, w):
        x = np.asarray(x, float)
        w = np.asarray(w, float)
        sw = w.sum()
        if len(x) == 0 or sw <= 0:
            return None, None, 0.0
        m = float(np.sum(w * x) / sw)
        sw2 = float(np.sum(w ** 2))
        denom = sw - sw2 / sw
        if denom <= 0:
            return m, None, (sw ** 2) / sw2 if sw2 > 0 else 0.0
        var = float(np.sum(w * (x - m) ** 2) / denom)
        neff = (sw ** 2) / sw2
        return m, var, neff

    total_active = 0
    agree = 0
    heavy_r, heavy_w, thin_r, thin_w = [], [], [], []
    all_next = []

    for coin in bars:
        for win in bars[coin]:
            df = bars[coin][win].reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float)

            # Raw move from the config's component (one-bar percent change).
            move = pd.Series(np.nan, index=df.index)
            if H_COL in df.columns:
                move = df[H_COL].astype(float)
            if T_COL in df.columns:
                move = move.fillna(df[T_COL].astype(float))
            move = move.fillna(close.pct_change())

            vmean = vol.rolling(20, min_periods=20).mean()
            nxt = close.shift(-1) / close - 1.0  # inside this window only
            all_next.extend(nxt.dropna().tolist())

            # Situation check
            active = fc.notna() & (fc != 0)
            checkable = active & move.notna() & vmean.notna() & vol.notna()
            heavy_sit = (move > 0) & (vol >= vmean)
            thin_sit = (move > 0) & (vol < vmean)
            ok = (heavy_sit & (fc > 0)) | (thin_sit & (fc < 0))
            total_active += int(checkable.sum())
            agree += int((checkable & ok).sum())

            # Main measure: forecast-bearing up bars, grouped by forecast side
            up = active & (move > 0) & nxt.notna()
            h = up & (fc > 0)
            t = up & (fc < 0)
            heavy_r.extend(nxt[h].tolist())
            heavy_w.extend(fc[h].abs().tolist())
            thin_r.extend(nxt[t].tolist())
            thin_w.extend(fc[t].abs().tolist())

    agreement = float(agree / total_active) if total_active > 0 else 0.0
    passed = total_active > 0 and agreement >= 0.9

    reading = ("Heavy/thin up bars are taken as forecast-bearing bars with a positive one-bar move "
               "and a positive/negative forecast (the strategy's own volume classification), the volume "
               "check uses a 20-bar rolling mean including the current bar (bars without 20 bars of "
               "history left out of the agreement), the Welch t uses weighted means, unbiased weighted "
               "variances and effective sizes (sum w)^2/sum w^2, the plan's under-30 rule is reported "
               "as not observable, and the unconditional mean is the pooled mean of all next-bar returns "
               "inside the windows.")

    name = "weighted mean next-bar return after heavy up bars minus after thin up bars"
    thr = "confirm if difference > 0 with t >= 2; reject if difference < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars checked": int(total_active)},
            "decided_by": ("Fewer than 90% of active bars are up bars with long on volume at/above its "
                           "20-bar mean or short on volume below it, so the config does not do what the "
                           "Fidelity's situation and sides say."),
            "reading": reading,
        }

    n_h, n_t = len(heavy_r), len(thin_r)
    counts = {"heavy forecast-bearing up bars": int(n_h),
              "thin forecast-bearing up bars": int(n_t)}

    mh, vh, neh = wstats(heavy_r, heavy_w)
    mt, vt, net = wstats(thin_r, thin_w)
    diff = (mh - mt) if (mh is not None and mt is not None) else None
    tstat = None
    if diff is not None and vh is not None and vt is not None and neh > 0 and net > 0:
        se = np.sqrt(vh / neh + vt / net)
        if se > 0:
            tstat = float(diff / se)

    uncond = float(np.mean(all_next)) if len(all_next) else None
    sup_val = (mt - uncond) if (mt is not None and uncond is not None) else None
    supporting = {
        "name": "weighted mean next-bar return after thin up bars minus unconditional mean daily return",
        "value": None if sup_val is None else float(sup_val),
        "passed": None if sup_val is None else bool(sup_val < 0),
    }

    main = {"name": name,
            "value": None if diff is None else float(diff),
            "statistic": None if tstat is None else {"name": "weighted Welch t", "value": tstat},
            "threshold": thr}

    if n_h < 30 or n_t < 30:
        status = "not observable"
        decided = "Fewer than 30 forecast-bearing up bars fall in at least one group across all windows."
    elif tstat is None:
        status = "inconclusive"
        decided = "The t-statistic could not be computed, so neither the confirm nor the reject rule is met."
    elif diff > 0 and tstat >= 2:
        status = "confirmed"
        decided = "The heavy-minus-thin difference is positive with t >= 2 (confirm rule)."
    elif diff < 0 and tstat <= -2:
        status = "rejected"
        decided = "The heavy-minus-thin difference is negative with t <= -2 (reject rule)."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
