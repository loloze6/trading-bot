import numpy as np
import pandas as pd


def measure(bars):
    H = 24
    RAW = "debug_info.components.run24.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # fallback sign of the 24-bar run from prices (vol scaling keeps the sign)
            run_sign_px = np.sign(close / close.shift(H) - 1.0)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw_sign = np.sign(raw).where(raw.notna(), run_sign_px)
            else:
                raw_sign = run_sign_px
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            # situation: the vol-scaled 24h run is non-zero; expected side: opposite to it
            agree = active & raw_sign.notna() & (raw_sign != 0) & (np.sign(f) == -raw_sign)
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.9)

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of active bars have a forecast opposite in sign to the volatility-scaled 24-bar run, "
                          "so the config does not bet against the run as the plan's Fidelity says.",
            "reading": "The situation is taken as a non-zero volatility-scaled 24-bar run (the cubic dead zone is graded, not a gate), "
                       "and the expected side is opposite to the run's sign.",
        }

    # ---------- 2. criterion ----------
    # grid samples per coin
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                rows.append((coin, w, f[i], r))
    g = pd.DataFrame(rows, columns=["coin", "window", "forecast", "ret"])

    if len(g):
        drift = g.groupby("coin")["ret"].mean()
        g["adj"] = np.sign(g["forecast"]) * (g["ret"] - g["coin"].map(drift))
        g = g[g["forecast"].notna()]
    else:
        g["adj"] = []

    ext = g[g["forecast"].abs() >= 10]["adj"].dropna().to_numpy(dtype=float)
    rest = g[(g["forecast"] != 0) & (g["forecast"].abs() < 10)]["adj"].dropna().to_numpy(dtype=float)
    n_ext = int(len(ext))
    n_rest = int(len(rest))

    mean_ext = float(np.mean(ext)) if n_ext > 0 else None
    if n_ext > 1:
        sd = float(np.std(ext, ddof=1))
        t_ext = float(mean_ext / (sd / np.sqrt(n_ext))) if sd > 0 else None
    else:
        t_ext = None

    if n_ext > 0 and n_rest > 0:
        diff = float(np.mean(ext) - np.mean(rest))
        sup_pass = bool(diff > 0)
    else:
        diff = None
        sup_pass = None

    if n_ext < 30:
        status = "not observable"
        decided = f"Only {n_ext} extreme grid cases (abs(forecast) >= 10), below the plan's minimum of 30."
    elif t_ext is None:
        status = "inconclusive"
        decided = "The t of the mean could not be computed (zero dispersion), so neither confirm nor reject is met."
    elif mean_ext > 0 and t_ext >= 2:
        if sup_pass is True:
            status = "confirmed"
            decided = "Main mean above 0 with t >= 2 over at least 30 cases and supporting difference (extreme minus rest) above 0."
        else:
            status = "inconclusive"
            decided = "Main mean above 0 with t >= 2, but the supporting difference (extreme minus rest) is not above 0."
    elif mean_ext < 0 and t_ext <= -2:
        status = "rejected"
        decided = "Main mean below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed_sit},
        "main_measure": {
            "name": "mean forecast-signed drift-adjusted 24-bar forward return on extreme grid bars",
            "value": mean_ext,
            "statistic": ({"name": "t of the mean", "value": t_ext} if t_ext is not None else None),
            "threshold": "confirm: mean > 0 with t >= 2 over >= 30 cases (and supporting difference > 0); reject: mean < 0 with t <= -2 over >= 30 cases",
        },
        "supporting_check": {
            "name": "extreme minus other non-zero grid bars, mean signed drift-adjusted 24-bar return",
            "value": diff,
            "passed": sup_pass,
        },
        "counts": {"extreme grid cases": n_ext, "other non-zero grid cases": n_rest},
        "decided_by": decided,
        "reading": "The grid is positions 0, 24, 48, ... of each window with a full 24-bar forward return inside the window, "
                   "the coin's mean 24-bar return is the mean of these grid returns over all its windows, and the situation "
                   "check takes every non-zero volatility-scaled run as the situation with the expected side opposite to its sign.",
    }
