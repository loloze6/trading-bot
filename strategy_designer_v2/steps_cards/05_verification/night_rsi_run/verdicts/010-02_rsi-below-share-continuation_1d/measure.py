import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 14
    RAW = "debug_info.components.rsi_below_share.last_history_value"

    # ---------- 1. Situation check ----------
    # Fidelity: situation = share of last 30 days with RSI(14) below 50, kept.
    # The idea expects a lower return the larger that share, so the expected
    # side is short when share > 0.5 (raw > 0), long when share < 0.5 (raw < 0).
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[RAW], errors="coerce") if RAW in df.columns else pd.Series(np.nan, index=df.index)
            active = f.notna() & (f != 0) & raw.notna()
            n_active += int(active.sum())
            agree = active & (np.sign(f) == -np.sign(raw)) & (raw != 0)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars have a forecast sign opposite to the sign of "
                          "(share of last 30 days with RSI below 50 minus 0.5), so the config does not go short "
                          "when RSI spent more time below 50 and long when less, as the Fidelity states.",
            "reading": "Active bars are those with a non-zero forecast and a recorded raw share; the expected "
                       "side is the opposite sign of the raw value (share minus 0.5).",
        }

    # ---------- 2. Grid samples ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            raw = (pd.to_numeric(d[RAW], errors="coerce").values if RAW in d.columns
                   else np.full(len(d), np.nan))
            n = len(d)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({"coin": coin, "window": w, "ret": c1 / c0 - 1.0,
                             "forecast": fc[t], "raw": raw[t]})
    g = pd.DataFrame(rows, columns=["coin", "window", "ret", "forecast", "raw"])

    if len(g) > 0:
        coin_mean = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(coin_mean)
    else:
        g["excess"] = []

    m = g.dropna(subset=["forecast", "excess"])
    prod = (m["forecast"] / 10.0) * m["excess"]
    n_cases = int(len(prod))

    mean_val = float(prod.mean()) if n_cases > 0 else None
    if n_cases > 1:
        sd = float(prod.std(ddof=1))
        t_val = float(mean_val / (sd / np.sqrt(n_cases))) if sd > 0 else None
    else:
        t_val = None

    # ---------- supporting check ----------
    per_coin_rho = {}
    n_negative = 0
    for coin, gc in g.dropna(subset=["raw", "excess"]).groupby("coin"):
        if len(gc) >= 3 and gc["raw"].nunique() > 1 and gc["excess"].nunique() > 1:
            rho = stats.spearmanr(gc["raw"], gc["excess"]).correlation
            rho = float(rho) if np.isfinite(rho) else None
        else:
            rho = None
        per_coin_rho[str(coin)] = rho
        if rho is not None and rho < 0:
            n_negative += 1
    support_passed = bool(n_negative >= 2)

    counts = {"independent grid cases in total": n_cases}
    for coin, gc in m.groupby("coin"):
        counts["grid cases " + str(coin)] = int(len(gc))
    counts["coins with negative Spearman"] = int(n_negative)

    # ---------- decision ----------
    if n_cases < 300:
        status = "not observable"
        decided_by = f"Only {n_cases} independent grid cases, below the plan's minimum of 300."
    elif t_val is None:
        status = "inconclusive"
        decided_by = "The t-statistic could not be computed (zero dispersion), so neither rule is met."
    elif mean_val > 0 and t_val >= 2.0 and support_passed:
        status = "confirmed"
        decided_by = "Mean signed excess return above 0 with t >= 2.0 and Spearman negative in at least 2 coins."
    elif mean_val < 0 and t_val <= -2.0:
        status = "rejected"
        decided_by = "Mean signed excess return below 0 with t <= -2.0: returns run with the RSI side."
    elif t_val >= 2.0 and not support_passed:
        status = "inconclusive"
        decided_by = "t >= 2.0 but the supporting check fails (Spearman negative in fewer than 2 coins)."
    else:
        status = "inconclusive"
        decided_by = "t lies between -2.0 and 2.0, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": "mean of forecast/10 x coin excess 14-bar return on the non-overlapping grid",
            "value": mean_val,
            "statistic": ({"name": "t of the mean", "value": t_val} if t_val is not None else None),
            "threshold": "confirm if mean > 0 with t >= 2.0 (and support passes); reject if mean < 0 with t <= -2.0",
        },
        "supporting_check": {
            "name": "Spearman(raw share below, excess 14-bar return) negative in at least 2 coins; per coin: "
                    + ", ".join(f"{k}={v}" for k, v in per_coin_rho.items()),
            "value": float(n_negative),
            "passed": support_passed,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": "Grid bars are positions 0, 14, 28, ... of each window with t+14 inside the window; the coin's "
                   "mean 14-bar return is the mean of its grid returns over all its windows; the supporting check "
                   "keeps the plan's literal 'at least 2 coins negative' even though only the coins present in "
                   "the record are tested.",
    }
