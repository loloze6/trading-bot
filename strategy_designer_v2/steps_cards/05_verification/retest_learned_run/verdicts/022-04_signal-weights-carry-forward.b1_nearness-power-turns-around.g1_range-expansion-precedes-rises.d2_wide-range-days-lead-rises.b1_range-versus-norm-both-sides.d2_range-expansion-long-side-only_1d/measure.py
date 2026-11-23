import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    MIN_CASES = 100
    RAW = "debug_info.components.range_excess.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            rng = pd.to_numeric(df["high"], errors="coerce") - pd.to_numeric(df["low"], errors="coerce")
            recomputed = 1.0 - rng / rng.rolling(30, min_periods=30).mean()
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            # situation: today's range above its 30-day mean range (raw < 0), long side (forecast > 0)
            agree = active & raw.notna() & (raw < 0) & (fc > 0)
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (
                "Fewer than 90% of the bars with a non-zero forecast are long bars on days whose high-low range "
                "exceeds the 30-day mean range (raw compression value below 0), as the Fidelity's situation and "
                "long side require." if n_active > 0 else
                "No bar has a non-zero forecast, so the config never takes the plan's long position on wide-range days."
            ),
            "reading": "Situation taken as last_history_value < 0 (range above its 30-day mean, recomputed from prices where missing) with forecast > 0.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, close[i + H] / c0 - 1.0, fc[i]))
    g = pd.DataFrame(rows, columns=["coin", "ret", "fc"])

    if len(g) > 0:
        coin_mean = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(coin_mean)
        sel = g[(g["fc"] > 0) & g["fc"].notna() & g["excess"].notna()]
    else:
        sel = pd.DataFrame(columns=["coin", "ret", "fc", "excess"])

    n_cases = int(len(sel))
    value = None
    t = None
    if n_cases > 0:
        f = sel["fc"].astype(float).values
        e = sel["excess"].astype(float).values
        value = float(np.sum(f * e) / np.sum(f))
        prod = f * e
        if n_cases > 1:
            sd = np.std(prod, ddof=1)
            t = float(np.mean(prod) / (sd / np.sqrt(n_cases))) if sd > 0 else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided_by = f"Only {n_cases} independent grid cases with forecast > 0, below the plan's minimum of 100."
    elif value is not None and t is not None and value > 0 and t >= 2:
        status = "confirmed"
        decided_by = "Confirm: the forecast-weighted mean excess 3-bar return is above 0 with t >= 2 over at least 100 grid cases."
    elif value is not None and t is not None and value < 0 and t <= -2:
        status = "rejected"
        decided_by = "Reject: the forecast-weighted mean excess 3-bar return is below 0 with t <= -2 over at least 100 grid cases."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: the t of the products forecast x excess is between -2 and 2 (or not defined)."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "forecast-weighted mean excess 3-bar return",
            "value": value,
            "statistic": {"name": "t of per-bar forecast x excess", "value": t} if t is not None else None,
            "threshold": "above 0 with t >= 2 confirms; below 0 with t <= -2 rejects; at least 100 grid cases",
        },
        "supporting_check": None,
        "counts": {"independent grid cases with forecast > 0": n_cases},
        "decided_by": decided_by,
        "reading": (
            "The coin's mean 3-bar return is taken over all its non-overlapping grid bars (positions 0, 3, 6, ... "
            "of every window, forward return inside the window), and the plan's 'fewer than 100 cases' is reported "
            "as not observable per the minimum-count rule."
        ),
    }
