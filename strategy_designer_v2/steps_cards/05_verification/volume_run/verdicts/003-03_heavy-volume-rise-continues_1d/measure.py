import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.vol_rise.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation (adapted): the day's rise in usual moves times its volume ratio.
    # The bar is in the situation when that graded value is positive. Expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0  # inside the window only
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # Raw is (return / std) x volume ratio, so its sign is the sign of the day's return.
            # Where raw is not recorded, use the day's return from the prices.
            in_sit = np.where(raw.notna(), raw > 0, ret1 > 0)
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & pd.Series(in_sit, index=df.index) & (fc > 0)).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "mean 5-bar excess return over coin mean on grid bars with forecast >= 2"
    threshold = "confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars "
                           "after a positive volume-weighted scaled one-day rise, the plan's "
                           "situation and side." if n_active > 0 else
                           "No bar has a non-zero forecast, so the config never takes the "
                           "plan's situation."),
            "reading": ("A bar is in the situation when the raw component value is above 0 "
                        "(from the day's price return where it is not recorded), and the "
                        "expected side is long."),
        }

    # ---------- 2. Criterion ----------
    sig_fc = []
    sig_ex = []
    for coin, wins in bars.items():
        rows = []
        all_rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy()
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy()
            n = len(df)
            for p in range(0, n - H, H):
                c0, c1 = close[p], close[p + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                rows.append((fc[p], r))
        if not all_rets:
            continue
        coin_mean = float(np.mean(all_rets))
        for f, r in rows:
            if np.isfinite(f) and f >= 2:
                sig_fc.append(float(f))
                sig_ex.append(r - coin_mean)

    n_sig = len(sig_ex)
    counts = {"signal grid bars": n_sig}
    reading = ("A bar is in the situation when the raw component value is above 0 (long side); "
               "grid bars are positions 0,5,10,... of each window with close[t+5] inside the window, "
               "and the coin's mean 5-bar return is taken over all its windows' grid bars together.")

    mean_ex = float(np.mean(sig_ex)) if n_sig > 0 else None
    t_val = None
    if n_sig >= 2:
        sd = float(np.std(sig_ex, ddof=1))
        if sd > 0:
            t_val = mean_ex / (sd / np.sqrt(n_sig))
    rho = None
    if n_sig >= 3:
        rr = stats.spearmanr(sig_fc, sig_ex).correlation
        if rr is not None and np.isfinite(rr):
            rho = float(rr)

    main = {"name": main_name, "value": mean_ex,
            "statistic": ({"name": "ordinary t of the mean", "value": float(t_val)}
                          if t_val is not None else None),
            "threshold": threshold}
    sup_passed = (rho > 0) if rho is not None else None
    supporting = {"name": "Spearman(forecast, excess return) on signal bars",
                  "value": rho, "passed": sup_passed}

    if n_sig < 30:
        status = "not observable"
        decided = f"Only {n_sig} signal grid bars, fewer than the plan's minimum of 30."
    elif t_val is None:
        status = "inconclusive"
        decided = "The t of the mean cannot be computed (zero spread), so neither rule is met."
    elif mean_ex > 0 and t_val >= 2 and sup_passed:
        status = "confirmed"
        decided = "Mean excess return above 0 with t >= 2 and Spearman correlation above 0 (confirm rule)."
    elif mean_ex < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean excess return below 0 with t <= -2 (reject rule)."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the Spearman correlation is 0 or below (inconclusive rule)."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (inconclusive rule)."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
