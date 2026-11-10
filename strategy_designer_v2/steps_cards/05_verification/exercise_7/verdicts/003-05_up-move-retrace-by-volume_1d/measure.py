import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    HB = "debug_info.components.heavy_move.last_history_value"
    TB = "debug_info.components.thin_move.last_history_value"

    sit_total = 0
    sit_agree = 0
    thin_shares, heavy_shares = [], []
    part_excess = {"heavy": [], "thin": []}

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            # raw one-bar move: close-to-close within the window, falling back to the component's raw value
            move = close / close.shift(1) - 1
            comp = pd.Series(np.nan, index=df.index)
            for col in (HB, TB):
                if col in df.columns:
                    comp = comp.fillna(pd.to_numeric(df[col], errors="coerce"))
            move = move.fillna(comp)
            nxt = close.shift(-1) / close - 1

            # situation: move ranks at or above the 0.90 percentile of its own (in-window) history
            vals = move.values
            pct = np.full(len(vals), np.nan)
            for i in range(len(vals)):
                hist = vals[: i + 1]
                hist = hist[~np.isnan(hist)]
                if len(hist) >= 20 and not np.isnan(vals[i]):
                    pct[i] = np.mean(hist <= vals[i])
            vol = df["volume"].astype(float)
            vmean = vol.rolling(20, min_periods=20).mean()
            fc = pd.to_numeric(df["forecast"], errors="coerce")

            for i in range(len(df)):
                f = fc.iloc[i]
                if pd.isna(f) or f == 0:
                    continue
                if np.isnan(pct[i]) or pd.isna(vmean.iloc[i]) or pd.isna(vol.iloc[i]):
                    continue
                sit_total += 1
                if pct[i] >= 0.9:
                    heavy = vol.iloc[i] >= vmean.iloc[i]
                    if (heavy and f > 0) or ((not heavy) and f < 0):
                        sit_agree += 1

            # main measure and supporting check, groups taken from the record's regime labels
            reg = df["regime"].astype(str)
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce")
            for i in range(len(df)):
                r = reg.iloc[i]
                grp = "heavy" if r == "trending" else ("thin" if r == "mean_reversion" else None)
                if grp is None:
                    continue
                m, n = move.iloc[i], nxt.iloc[i]
                if pd.notna(m) and pd.notna(n) and m != 0:
                    (heavy_shares if grp == "heavy" else thin_shares).append(n / m)
                f = fc.iloc[i]
                if pd.notna(f) and f != 0 and pd.notna(alloc.iloc[i]) and pd.notna(n):
                    part_excess[grp].append(alloc.iloc[i] * n - n)

    agreement = sit_agree / sit_total if sit_total > 0 else 0.0
    passed = agreement >= 0.9
    sit = {"agreement": float(agreement), "passed": bool(passed)}

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": sit,
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars checked": int(sit_total)},
            "decided_by": "Fewer than 90% of active bars are top-decile one-bar up moves with long on volume at/above its 20-bar mean and short below it, so the config does not do what the Fidelity says.",
            "reading": "Percentile ranks and 20-bar volume means are computed from in-window history only (bars without 20 bars of history are skipped).",
        }

    n_thin, n_heavy = len(thin_shares), len(heavy_shares)
    thin_mean = float(np.mean(thin_shares)) if n_thin else None
    heavy_mean = float(np.mean(heavy_shares)) if n_heavy else None
    t = None
    if n_thin >= 2 and n_heavy >= 2:
        t = float(stats.ttest_ind(thin_shares, heavy_shares, equal_var=False).statistic)
    diff = thin_mean - heavy_mean if (thin_mean is not None and heavy_mean is not None) else None

    ex_h = float(np.mean(part_excess["heavy"])) if part_excess["heavy"] else None
    ex_t = float(np.mean(part_excess["thin"])) if part_excess["thin"] else None
    sup_pass = None
    sup_val = None
    if ex_h is not None and ex_t is not None:
        sup_pass = bool(ex_h > 0 and ex_t > 0)
        sup_val = float(min(ex_h, ex_t))

    if n_thin < 15 or n_heavy < 15 or diff is None:
        status = "inconclusive"
        decided = "Fewer than 15 thin cases or fewer than 15 heavy cases across the 6 windows."
    elif thin_mean >= heavy_mean:
        status = "rejected"
        decided = "The thin mean share is at or above the heavy mean share."
    elif t is not None and t <= -2.0 and thin_mean < 0:
        status = "confirmed"
        decided = "Thin mean share is below heavy with Welch t magnitude at least 2.0, and the thin mean share is below 0."
    elif t is None or t > -2.0:
        status = "inconclusive"
        decided = "Thin is below heavy but the Welch t-stat is under 2.0 in magnitude."
    else:
        status = "inconclusive"
        decided = "Thin is below heavy with |t| >= 2.0 but the thin mean share is not below 0; no confirm or reject rule is met."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": {
            "name": "mean next-bar return / move return, thin minus heavy",
            "value": diff,
            "statistic": {"name": "Welch t (thin minus heavy)", "value": t} if t is not None else None,
            "threshold": "thin mean below heavy mean with Welch t of at least 2.0 in magnitude, and thin mean below 0",
        },
        "supporting_check": {
            "name": "mean per-bar strategy gain minus BTC return on active bars, worse of heavy-only and thin-only parts",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"thin cases": int(n_thin), "heavy cases": int(n_heavy)},
        "decided_by": decided,
        "reading": "Sharp-move bars are the record's regime labels (trending = heavy, mean_reversion = thin), the move is the bar's in-window close-to-close return, a t-stat 'of at least 2.0' is read as thin-minus-heavy t <= -2.0, and the supporting check compares the mean per-bar position gain with the mean BTC next-bar return over the same active bars in each part.",
    }
