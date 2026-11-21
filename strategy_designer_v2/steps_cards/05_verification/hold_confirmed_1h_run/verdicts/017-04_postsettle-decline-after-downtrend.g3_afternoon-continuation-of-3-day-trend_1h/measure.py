import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.trend3d.last_history_value"
    H = 2

    def to_ts(s):
        if np.issubdtype(s.dtype, np.number):
            mx = float(np.nanmax(s.values)) if len(s) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(s, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True)

    def wkey(w):
        try:
            return int(str(w).lstrip("w"))
        except Exception:
            return str(w)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin in sorted(bars.keys()):
        prepared[coin] = {}
        for w in sorted(bars[coin].keys(), key=wkey):
            df = bars[coin][w].copy().reset_index(drop=True)
            df["ts"] = to_ts(df["timestamp"])
            df["close"] = pd.to_numeric(df["close"], errors="coerce")
            df["forecast"] = pd.to_numeric(df["forecast"], errors="coerce")
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            recomputed = (df["close"] / df["close"].shift(72) - 1.0) * 100.0
            raw = raw.where(raw.notna(), recomputed)
            df["raw3d"] = raw
            prepared[coin][w] = df

            coming_hour = (df["ts"] + pd.Timedelta(hours=1)).dt.hour
            in_slot = coming_hour.isin([16, 17])
            fc = df["forecast"]
            active = fc.notna() & (fc != 0)
            side_ok = np.sign(fc) == np.sign(df["raw3d"])
            agree = active & in_slot & side_ok & df["raw3d"].notna() & (df["raw3d"] != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled mean of forecast/10 x excess 2-bar return from the 16:00 slot open"
    main_thr = "confirm: mean > 0 with ordinary t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2"
    sup_name = "signed excess 2-bar return, top third minus bottom third of |forecast| (Welch t >= 1)"

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"independent cases": 0, "active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars are bars whose coming bar starts at 16:00 or 17:00 UTC "
                          "with the forecast's sign equal to the 72-bar return's sign.",
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    vals, fcs = [], []
    for coin in prepared:
        # coin's mean 2-bar return over all its windows, non-overlapping grid per window
        grid_rets = []
        for w, df in prepared[coin].items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.append(r[np.isfinite(r)])
        if not grid_rets:
            continue
        allr = np.concatenate(grid_rets)
        if len(allr) == 0:
            continue
        coin_mean = float(np.mean(allr))

        for w in sorted(prepared[coin].keys(), key=wkey):
            df = prepared[coin][w]
            c = df["close"].values
            n = len(df)
            pos = np.where(df["ts"].dt.hour.values == 15)[0]
            pos = pos[pos + H < n]
            for p in pos:
                f = df["forecast"].iloc[p]
                r = c[p + H] / c[p] - 1.0
                if not (np.isfinite(f) and np.isfinite(r)):
                    continue
                ex = r - coin_mean
                vals.append(f / 10.0 * ex)
                fcs.append((f, ex))

    n_cases = len(vals)
    counts = {"independent cases": int(n_cases)}
    vals = np.asarray(vals, dtype=float)

    main_mean = float(np.mean(vals)) if n_cases > 0 else None
    main_t = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        main_t = float(main_mean / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    # supporting check
    sup_val, sup_t, sup_pass = None, None, None
    if n_cases >= 6:
        f_arr = np.array([x[0] for x in fcs], dtype=float)
        ex_arr = np.array([x[1] for x in fcs], dtype=float)
        signed = np.sign(f_arr) * ex_arr
        order = np.argsort(np.abs(f_arr), kind="mergesort")
        k = n_cases // 3
        bottom = signed[order[:k]]
        top = signed[order[-k:]]
        sup_val = float(np.mean(top) - np.mean(bottom))
        tt = stats.ttest_ind(top, bottom, equal_var=False)
        sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else 0.0
        sup_pass = bool(sup_val > 0 and sup_t >= 1.0)

    reading = ("Cases are the rows stamped 15:00 UTC with close[t+2] taken two rows later in the same window; "
               "cases with forecast 0 are kept; the coin's mean 2-bar return is the mean over the non-overlapping "
               "grid (positions 0, 2, 4, ...) of all its windows pooled; thirds are n//3 cases by |forecast| (stable sort); "
               "the 300 minimum is checked on the number of cases.")

    if n_cases < 300 or main_t is None:
        status = "not observable"
        decided = f"The plan's minimum of 300 independent cases is not reached ({n_cases})."
    elif main_mean > 0 and main_t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main mean is above 0 with t >= 2 and the supporting check passes (Welch t >= 1, top third larger)."
    elif main_mean < 0 and main_t <= -2:
        status = "rejected"
        decided = "The main mean is below 0 with t <= -2."
    elif main_t >= 2:
        status = "inconclusive"
        decided = "The main t is >= 2 while the supporting check fails."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": main_mean,
            "statistic": ({"name": "ordinary t of the mean", "value": main_t} if main_t is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": sup_name,
            "value": sup_val,
            "passed": sup_pass,
            "welch_t": sup_t,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
