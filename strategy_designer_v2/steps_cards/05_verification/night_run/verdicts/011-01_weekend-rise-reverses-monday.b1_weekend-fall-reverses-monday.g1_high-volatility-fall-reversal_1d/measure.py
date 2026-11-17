import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    reading = ("The plan's situation (a down day in the high-volatility regime) is taken as regime == "
               "'mean_reversion' (the volatility-percentile regime, which is not recorded and cannot be rebuilt "
               "inside ~120-bar windows) and a negative close-to-close return from the prices, falling back to the "
               "sign of fall_vol's raw value on a window's first bar; the expected side is long; the coin's mean "
               "daily return is the mean of all its next-day returns over all windows; the 'fewer than 100 bars "
               "with forecast > 0' rule is applied as a minimum count, counting only bars that have a next-day return.")

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            ret = close / close.shift(1) - 1.0
            col = "debug_info.components.fall_vol.last_history_value"
            if col in df.columns:
                raw = pd.to_numeric(df[col], errors="coerce")
                ret = ret.where(ret.notna(), raw)
            down = ret < 0
            reg = df["regime"].astype(str) == "mean_reversion"
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & down & reg & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars on a down day in the "
                           "high-volatility regime, so the config does not do what the plan's Fidelity says."
                           if n_active > 0 else "No bar has a non-zero forecast, so the situation cannot be checked."),
            "reading": reading,
        }

    # ---------- coin mean daily return over all windows ----------
    coin_mean = {}
    per_coin_frames = {}
    for coin, wins in bars.items():
        all_r = []
        frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fwd = close.shift(-1) / close - 1.0
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            all_r.append(fwd.dropna().values)
            frames.append(pd.DataFrame({"fc": fc.values, "fwd": fwd.values}))
        rr = np.concatenate(all_r) if all_r else np.array([])
        coin_mean[coin] = float(np.mean(rr)) if len(rr) else np.nan
        per_coin_frames[coin] = frames

    fcs, exs = [], []
    for coin, frames in per_coin_frames.items():
        mu = coin_mean[coin]
        if not np.isfinite(mu):
            continue
        for f in frames:
            sel = f[(f["fc"] > 0) & f["fwd"].notna() & f["fc"].notna()]
            fcs.append(sel["fc"].values)
            exs.append(sel["fwd"].values - mu)
    fc_arr = np.concatenate(fcs) if fcs else np.array([])
    ex_arr = np.concatenate(exs) if exs else np.array([])
    n = int(len(fc_arr))

    threshold = "confirm if t >= 2 with Spearman rho > 0; reject if t <= -2; else inconclusive; at least 100 bars with forecast > 0"
    mm_name = "mean of (forecast/10) x next-day excess return on bars with forecast > 0, pooled"
    counts = {"bars with forecast > 0": n}

    if n < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": mm_name, "value": float(np.mean((fc_arr / 10.0) * ex_arr)) if n else None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": f"Only {n} bars with forecast > 0, fewer than the plan's minimum of 100.",
            "reading": reading,
        }

    vals = (fc_arr / 10.0) * ex_arr
    mean = float(np.mean(vals))
    sd = float(np.std(vals, ddof=1))
    t = float(mean / (sd / np.sqrt(n))) if sd > 0 else float("nan")

    rho = stats.spearmanr(fc_arr, ex_arr).correlation
    rho = float(rho) if rho is not None and np.isfinite(rho) else None
    rho_pass = (rho is not None) and (rho > 0)

    if np.isfinite(t) and t >= 2 and rho_pass:
        status = "confirmed"
        decided = f"t = {t:.2f} >= 2 and the rank correlation {rho:.3f} > 0: the confirm rule."
    elif np.isfinite(t) and t <= -2:
        status = "rejected"
        decided = f"t = {t:.2f} <= -2: the reject rule."
    elif np.isfinite(t) and t >= 2:
        status = "inconclusive"
        decided = f"t = {t:.2f} >= 2 but the rank correlation ({rho}) is not above 0: inconclusive by the plan's rule."
    else:
        status = "inconclusive"
        decided = f"t = {t:.2f} lies between -2 and 2: inconclusive by the plan's rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": mm_name, "value": mean,
                         "statistic": {"name": "t of the mean", "value": t if np.isfinite(t) else None},
                         "threshold": threshold},
        "supporting_check": {"name": "Spearman rho of forecast vs next-day excess return > 0",
                             "value": rho, "passed": bool(rho_pass) if rho is not None else None},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
