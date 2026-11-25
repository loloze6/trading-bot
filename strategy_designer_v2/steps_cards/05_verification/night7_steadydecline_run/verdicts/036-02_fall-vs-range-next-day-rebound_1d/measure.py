import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RAW = "debug_info.components.fall.last_history_value"
    MIN_CASE_DAYS = 100

    def ratio_from_prices(df):
        # max(0, close[t-1]-close[t]) / mean(high-low over the 30 bars before t), inside the window only
        close = df["close"].astype(float)
        rng = (df["high"].astype(float) - df["low"].astype(float))
        base = rng.shift(1).rolling(30, min_periods=30).mean()
        fall = (close.shift(1) - close).clip(lower=0)
        r = fall / base
        r[(base <= 0) | base.isna()] = np.nan
        return r

    # ---------- coin mean daily return over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            df = df.sort_values("timestamp")
            c = df["close"].astype(float).values
            if len(c) > 1:
                rets.append(c[1:] / c[:-1] - 1.0)
        allr = np.concatenate(rets) if rets else np.array([])
        allr = allr[np.isfinite(allr)]
        coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check and cases ----------
    n_active = 0
    n_agree = 0
    case_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            ratio = raw.copy()
            pr = ratio_from_prices(df)
            ratio = ratio.where(ratio.notna(), pr)

            active = fc != 0
            n_active += int(active.sum())
            agree = active & (ratio >= 1.0) & (fc > 0)
            n_agree += int(agree.sum())

            close = df["close"].astype(float)
            nxt = close.shift(-1) / close - 1.0
            ts = pd.to_datetime(df["timestamp"], utc=True)
            is_case = (df["regime"].astype(str) == "mean_reversion") & (fc > 0)
            for i in np.where(is_case.values)[0]:
                r = nxt.iloc[i]
                if not np.isfinite(r):
                    continue
                case_rows.append({
                    "coin": coin,
                    "day": ts.iloc[i].floor("D"),
                    "excess": float(r - coin_mu[coin]),
                    "ratio": float(ratio.iloc[i]) if np.isfinite(ratio.iloc[i]) else np.nan,
                })

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean next-day excess return (close[t+1]/close[t]-1 minus coin's mean daily return) on case bars, same-day cases summed"
    thr = "confirm: mean > 0 with t >= 2 and Spearman > 0; reject: t <= -2"
    sup_name = "Spearman correlation of raw ratio (fall.last_history_value) vs next-day excess return across cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "case days": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are long bars where the one-day fall is at least the 30-day mean high-low range, as the Fidelity's situation requires.",
            "reading": "Situation taken as fall ratio >= 1 (recorded raw value, recomputed from prices where missing) with a positive forecast.",
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "excess", "ratio"])
    n_cases = int(len(cases))
    if n_cases > 0:
        day_sums = cases.groupby("day")["excess"].sum()
    else:
        day_sums = pd.Series(dtype=float)
    n_days = int(len(day_sums))

    mean_v = float(day_sums.mean()) if n_days > 0 else None
    t_v = None
    if n_days > 1:
        sd = float(day_sums.std(ddof=1))
        if sd > 0:
            t_v = float(mean_v / (sd / np.sqrt(n_days)))

    sc = cases.dropna(subset=["ratio", "excess"])
    rho = None
    if len(sc) >= 3 and sc["ratio"].nunique() > 1 and sc["excess"].nunique() > 1:
        rho = float(stats.spearmanr(sc["ratio"], sc["excess"]).correlation)
    rho_pass = None if rho is None or not np.isfinite(rho) else bool(rho > 0)

    counts = {"case days": n_days, "case bars": n_cases, "active bars": int(n_active)}

    if n_days < MIN_CASE_DAYS:
        status = "not observable"
        decided = f"Only {n_days} case days across all coins and windows, fewer than the plan's minimum of 100."
    elif t_v is None:
        status = "inconclusive"
        decided = "The t of the mean next-day excess return could not be computed, so neither the confirm nor the reject rule is met."
    elif t_v <= -2:
        status = "rejected"
        decided = "Reject rule met: the mean next-day excess return has t <= -2."
    elif t_v >= 2 and mean_v > 0 and rho_pass:
        status = "confirmed"
        decided = "Confirm rule met: the mean next-day excess return is positive with t >= 2 and the Spearman correlation is above 0."
    elif t_v >= 2:
        status = "inconclusive"
        decided = "Inconclusive rule met: t >= 2 but the Spearman correlation is at or below 0 (or not computable)."
    else:
        status = "inconclusive"
        decided = "Inconclusive rule met: the t of the mean next-day excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_v,
            "statistic": None if t_v is None else {"name": "t of the mean (over per-day summed cases)", "value": t_v},
            "threshold": thr,
        },
        "supporting_check": {"name": sup_name, "value": rho, "passed": rho_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases on the same UTC day are summed into one value and the mean and ordinary t are taken over these day sums, the Spearman correlation is taken over individual case bars, the coin's mean daily return is the mean of all its 1-bar returns inside all windows, and the plan's 'fewer than 100 case days' is reported as not observable.",
    }
