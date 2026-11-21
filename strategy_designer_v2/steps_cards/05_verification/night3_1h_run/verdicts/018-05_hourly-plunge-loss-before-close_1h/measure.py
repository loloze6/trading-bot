import numpy as np
import pandas as pd


def measure(bars):
    RAW = "debug_info.components.drop24.last_history_value"

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        return d

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = prep(df)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            ret24 = (d["close"] / d["close"].shift(24) - 1.0) * 100.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").where(lambda s: s.notna(), ret24)
            else:
                raw = ret24
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & (raw < 0) & (fc < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"cases": None, "active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars on which the "
                           "24-hour return is negative, as the plan's situation (a graded short held while "
                           "the 24-hour fall lasts) requires."),
            "reading": "The situation is read as the raw 24-hour return being below zero, with a short forecast.",
        }

    # ---------- 2. criterion ----------
    case_ex = []
    case_fc = []
    for coin, wins in bars.items():
        # Coin's mean hourly return over all windows pooled
        hr = []
        prepared = {}
        for w, df in wins.items():
            d = prep(df)
            prepared[w] = d
            r = (d["close"].shift(-1) / d["close"] - 1.0).dropna()
            hr.append(r.values)
        allr = np.concatenate(hr) if hr else np.array([])
        if allr.size == 0:
            continue
        mu = float(np.mean(allr))

        for w, d in prepared.items():
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            prev = fc.shift(1)
            cross = (fc <= -2) & (prev > -2)
            day = d["timestamp"].dt.floor("D")
            # last bar of each UTC day within this window
            last_idx = d.groupby(day).apply(lambda g: g.index.max())
            seen = set()
            for i in np.where(cross.values)[0]:
                dd = day.iloc[i]
                if dd in seen:
                    continue
                seen.add(dd)
                j = int(last_idx.loc[dd])
                c0 = d["close"].iloc[i]
                c1 = d["close"].iloc[j]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                hours = (d["timestamp"].iloc[j] - d["timestamp"].iloc[i]).total_seconds() / 3600.0
                ret = c1 / c0 - 1.0
                excess_short = -(ret - mu * hours)
                case_ex.append(float(excess_short))
                case_fc.append(float(fc.iloc[i]))

    ex = np.array(case_ex, dtype=float)
    fcs = np.array(case_fc, dtype=float)
    n = int(ex.size)

    mean_ex = float(np.mean(ex)) if n > 0 else None
    t = None
    if n >= 2:
        sd = float(np.std(ex, ddof=1))
        t = float(mean_ex / (sd / np.sqrt(n))) if sd > 0 else None

    big = ex[fcs <= -10]
    small = ex[(fcs > -10) & (fcs <= -2)]
    diff = float(np.mean(big) - np.mean(small)) if (big.size > 0 and small.size > 0) else None
    sup_pass = (diff > 0) if diff is not None else None

    counts = {"cases": n, "cases forecast <= -10": int(big.size),
              "cases forecast between -10 and -2": int(small.size)}

    if n < 30:
        status = "not observable"
        decided = f"Fewer than the plan's minimum of 30 cases in total ({n})."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the mean excess short return could not be computed (zero dispersion)."
    elif t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The mean excess short return has t >= 2 over at least 30 cases and the supporting difference is above 0."
    elif t >= 2:
        status = "inconclusive"
        decided = "A confirming t >= 2 with a supporting difference at or below 0 (or not computable) is inconclusive."
    elif t <= -2:
        status = "rejected"
        decided = "The mean excess short return has t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess short return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean excess short return from the first -2 crossing to the same UTC day's close",
            "value": mean_ex,
            "statistic": {"name": "one-group t of the mean", "value": t} if t is not None else None,
            "threshold": "confirm t >= 2 with supporting difference > 0, reject t <= -2, over at least 30 cases",
        },
        "supporting_check": {
            "name": "mean excess (forecast <= -10) minus mean excess (-10 < forecast <= -2)",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first bar of each coin-window-UTC-day whose forecast is <= -2 while the previous "
                    "bar's forecast in the same window was > -2 (a window's first row cannot cross), its end is the "
                    "last recorded bar of that UTC day in the window (a signal on that last bar counts with a zero "
                    "return), the hours remaining are the clock hours between the two bars, the coin's mean hourly "
                    "return pools all its windows, and the one-case-per-coin-day cases stand in for the 24-bar grid."),
    }
