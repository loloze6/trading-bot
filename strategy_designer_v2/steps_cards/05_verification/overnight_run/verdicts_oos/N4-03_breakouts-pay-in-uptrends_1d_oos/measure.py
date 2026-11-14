import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    FC = "forecast"
    UP = "debug_info.components.high_up.last_history_value"
    DN = "debug_info.components.high_down.last_history_value"

    def tstat(x):
        x = np.asarray(x, dtype=float)
        n = len(x)
        if n < 2:
            return None
        sd = x.std(ddof=1)
        if not np.isfinite(sd) or sd == 0:
            return None
        return float(x.mean() / (sd / np.sqrt(n)))

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if FC not in df.columns:
                continue
            f = pd.to_numeric(df[FC], errors="coerce")
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            up = pd.to_numeric(df[UP], errors="coerce") if UP in df.columns else pd.Series(np.nan, index=df.index)
            dn = pd.to_numeric(df[DN], errors="coerce") if DN in df.columns else pd.Series(np.nan, index=df.index)
            # fallback: raw 20-day Donchian position of the close, computed from in-window closes
            c = pd.to_numeric(df["close"], errors="coerce")
            hi = c.rolling(20, min_periods=20).max()
            lo = c.rolling(20, min_periods=20).min()
            rng = (hi - lo).replace(0, np.nan)
            don = 40.0 * (c - lo) / rng - 20.0
            raw = pd.Series(np.where(reg == "trending", up,
                                     np.where(reg == "mean_reversion", dn, np.nan)), index=df.index)
            raw = raw.fillna(don)
            active = f.notna() & (f != 0)
            exp_side = pd.Series(np.where(reg == "trending", 1.0,
                                          np.where(reg == "mean_reversion", -1.0, 0.0)), index=df.index)
            situ = (raw > 0) & (exp_side != 0)
            ok = active & situ & (np.sign(f) == exp_side)
            n_active += int(active.sum())
            n_agree += int(ok.sum())

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "pooled mean signed 10-bar excess return, |forecast|>=10",
                             "value": None, "statistic": None,
                             "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2"},
            "supporting_check": None,
            "counts": {"non-overlapping cases": 0, "trending cases": 0, "mean_reversion cases": 0},
            "decided_by": "No bar has a non-zero forecast, so neither the situation nor the criterion can be observed.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    passed = agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "pooled mean signed 10-bar excess return, |forecast|>=10",
                             "value": None, "statistic": None,
                             "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2"},
            "supporting_check": None,
            "counts": None,
            "decided_by": "Fewer than 90% of active bars are upper-half 20-day range closes positioned long in `trending` "
                          "(close >= SMA200) and short in `mean_reversion` (close < SMA200), as the Fidelity requires.",
            "reading": "Situation = raw Donchian position > 0 (upper half of the 20-day range) with side from the `regime` column.",
        }

    # ---------- 2. criterion ----------
    signed_all, signed_tr, signed_mr = [], [], []
    for coin, wins in bars.items():
        # holding: coin's mean 10-bar return over all bars of all windows pooled
        all_fwd = []
        frames = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce")
            fwd = c.shift(-H) / c - 1.0
            all_fwd.append(fwd.dropna().values)
            frames.append((df, fwd))
        all_fwd = np.concatenate(all_fwd) if all_fwd else np.array([])
        if len(all_fwd) == 0:
            continue
        holding = float(np.mean(all_fwd))
        for df, fwd in frames:
            if FC not in df.columns:
                continue
            f = pd.to_numeric(df[FC], errors="coerce")
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series([""] * len(df))
            for i in range(0, len(df), H):
                fi = f.iloc[i]
                ri = fwd.iloc[i]
                if pd.isna(fi) or pd.isna(ri) or abs(fi) < 10:
                    continue
                ex = float(ri) - holding
                s = float(np.sign(fi)) * ex
                signed_all.append(s)
                if reg.iloc[i] == "trending":
                    signed_tr.append(ex)
                elif reg.iloc[i] == "mean_reversion":
                    signed_mr.append(-ex)

    n_all, n_tr, n_mr = len(signed_all), len(signed_tr), len(signed_mr)
    mean_all = float(np.mean(signed_all)) if n_all else None
    t_all = tstat(signed_all)
    mean_tr = float(np.mean(signed_tr)) if n_tr else None
    mean_mr = float(np.mean(signed_mr)) if n_mr else None
    t_tr = tstat(signed_tr)
    t_mr = tstat(signed_mr)

    sup_passed = None
    if mean_tr is not None and mean_mr is not None:
        sup_passed = bool(mean_tr > 0 and mean_mr > 0)

    counts = {"non-overlapping cases": n_all, "trending cases": n_tr, "mean_reversion cases": n_mr}

    if n_all < 30:
        status = "not observable"
        decided = f"The pool has {n_all} non-overlapping cases, fewer than the plan's minimum of 30."
    elif n_tr < 10 or n_mr < 10:
        status = "not observable"
        decided = (f"A regime has fewer than 10 non-overlapping cases (trending {n_tr}, mean_reversion {n_mr}), "
                   "below the plan's minimum.")
    elif t_all is None:
        status = "inconclusive"
        decided = "The t-statistic cannot be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean_all > 0 and t_all >= 2:
        status = "confirmed"
        decided = "Confirm: the pooled mean signed excess return is > 0 with t >= 2 on non-overlapping cases."
    elif mean_all < 0 and t_all <= -2:
        status = "rejected"
        decided = "Reject: the pooled mean signed excess return is < 0 with t <= -2 on non-overlapping cases."
    else:
        status = "inconclusive"
        decided = "Inconclusive: the pooled t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "pooled mean signed 10-bar excess return over holding, |forecast|>=10",
            "value": mean_all,
            "statistic": {"name": "t of the mean", "value": t_all} if t_all is not None else None,
            "threshold": "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "per-regime mean: trending excess, mean_reversion negative excess",
            "value": mean_tr,
            "passed": sup_passed,
            "trending": {"mean": mean_tr, "sign": (float(np.sign(mean_tr)) if mean_tr is not None else None),
                         "t": t_tr, "n": n_tr},
            "mean_reversion": {"mean": mean_mr, "sign": (float(np.sign(mean_mr)) if mean_mr is not None else None),
                               "t": t_mr, "n": n_mr},
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are grid bars 0,10,20,... of each window with |forecast|>=10 and a full in-window 10-bar return; "
                    "holding is the coin's mean of all in-window 10-bar returns (every bar) pooled over its windows; "
                    "regimes are split on the `regime` column, the situation is a raw Donchian position > 0, and the "
                    "supporting check passes when both regime means are positive."),
    }
