import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    RAW = "debug_info.components.near_high.last_history_value"

    # ---------- 1. Situation check ----------
    # Situation (Fidelity): trending regime (above 200-SMA and positive 60-day return,
    # i.e. the detector's rule, read from `regime`) and the close in the upper part of
    # its 20-day range (raw range position > 0). Expected side: long.
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if active.sum() == 0:
                continue
            reg = df["regime"].astype(str) == "trending"
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                upper = raw.notna() & (raw > 0)
            else:
                upper = pd.Series(False, index=df.index)
            situ = reg & upper & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situ).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    threshold_txt = ("mean excess 10-bar return > 0 with t >= 2 to confirm, < 0 with t <= -2 to reject, "
                     "at least 30 non-overlapping cases with forecast >= 10")
    main_name = "mean forward 10-bar return minus coin mean, forecast >= 10"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None,
                             "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars in the trending "
                           "regime with the close in the upper half of its 20-day range, as the Fidelity's "
                           "situation requires."),
            "reading": ("The situation is checked as regime == 'trending' with raw Donchian range position > 0 "
                        "and forecast > 0; bars with no recorded range position count as outside the situation."),
        }

    # ---------- 2. Forward returns and coin means ----------
    frames = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = pd.DataFrame({
                "close": pd.to_numeric(df["close"], errors="coerce").values,
                "forecast": pd.to_numeric(df["forecast"], errors="coerce").values,
                "regime": df["regime"].astype(str).values,
            })
            d["fwd"] = d["close"].shift(-H) / d["close"] - 1.0
            d["pos"] = np.arange(len(d))
            d["grid"] = (d["pos"] % H) == 0
            d["coin"] = coin
            d["window"] = w
            frames.append(d)
    all_df = pd.concat(frames, ignore_index=True)
    all_df = all_df[np.isfinite(all_df["fwd"])]
    coin_mean = all_df.groupby("coin")["fwd"].mean()
    all_df["excess"] = all_df["fwd"] - all_df["coin"].map(coin_mean)

    sel = all_df[all_df["forecast"].notna() & (all_df["forecast"] >= 10)]
    value = float(sel["excess"].mean()) if len(sel) > 0 else None
    non_ov = sel[sel["grid"]]["excess"].values
    n_nonov = int(len(non_ov))
    if n_nonov >= 2 and np.std(non_ov, ddof=1) > 0:
        t = float(np.mean(non_ov) / (np.std(non_ov, ddof=1) / np.sqrt(n_nonov)))
    else:
        t = None

    # ---------- Supporting check ----------
    tr = all_df[(all_df["regime"] == "trending") & all_df["forecast"].notna() & np.isfinite(all_df["excess"])]
    rho = None
    if len(tr) >= 3 and tr["forecast"].nunique() > 1 and tr["excess"].nunique() > 1:
        r = stats.spearmanr(tr["forecast"].values, tr["excess"].values).correlation
        rho = float(r) if np.isfinite(r) else None
    sup_passed = None if rho is None else bool(rho > 0)

    # ---------- Decision ----------
    if n_nonov < 30:
        status = "not observable"
        decided = (f"Only {n_nonov} non-overlapping cases with forecast >= 10, below the plan's minimum of 30.")
    elif value is not None and t is not None and value > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean excess 10-bar return after forecasts >= 10 is above 0 with t >= 2 on at least 30 non-overlapping cases."
    elif value is not None and t is not None and value < 0 and t <= -2:
        status = "rejected"
        decided = "The mean excess 10-bar return after forecasts >= 10 is below 0 with t <= -2 on at least 30 non-overlapping cases."
    else:
        status = "inconclusive"
        decided = "With at least 30 non-overlapping cases, t lies between -2 and 2 (or sign and t disagree), meeting neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": value,
                         "statistic": None if t is None else {"name": "t of the mean (non-overlapping samples)", "value": t},
                         "threshold": threshold_txt},
        "supporting_check": {"name": "Spearman rank correlation forecast vs forward 10-bar excess return, trending bars",
                             "value": rho, "passed": sup_passed},
        "counts": {"non-overlapping cases with forecast >= 10": n_nonov,
                   "bars with forecast >= 10": int(len(sel)),
                   "trending bars": int(len(tr))},
        "decided_by": decided,
        "reading": ("The situation is checked as regime == 'trending' with raw range position > 0 and a long forecast; "
                    "the coin's mean is its mean forward 10-bar return over all bars of all its windows; the reported "
                    "value is the mean over all bars with forecast >= 10, while the t-statistic and the case count use "
                    "the non-overlapping grid (positions 0, 10, 20, ... of each window)."),
    }
