import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    DEPTH = "debug_info.components.depth.last_history_value"
    REG_ON = "mean_reversion"

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            if active.sum() == 0:
                continue
            reg = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)
            if DEPTH in df.columns:
                depth = pd.to_numeric(df[DEPTH], errors="coerce")
                below = depth.notna() & (depth < 0)
            else:
                below = pd.Series(False, index=df.index)
            sit = (reg == REG_ON) & below & (f > 0)
            n_active += int(active.sum())
            n_agree += int((active & sit).sum())

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "mean 10-bar excess forward return after forecast >= 10, pooled, non-overlapping"
    threshold = "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 30 non-overlapping cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars in the mean_reversion "
                           "(high-volatility) regime with the close below its 200-day SMA, so the config does not "
                           "do what the plan's situation states."
                           if n_active > 0 else "The record has no active bars to compare with the plan's situation."),
            "reading": "Situation taken as regime == mean_reversion and raw 200-day SMA distance < 0, expected side long.",
        }

    # ---------- 2. Criterion ----------
    rows = []  # (coin, ret, forecast, in_regime)
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            reg = (df["regime"].astype(str).to_numpy() if "regime" in df.columns
                   else np.array([""] * len(df)))
            n = len(df)
            for i in range(0, n - H, H):
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append((coin, c1 / c0 - 1.0, f[i], reg[i] == REG_ON))

    data = pd.DataFrame(rows, columns=["coin", "ret", "f", "inreg"])
    if len(data):
        coin_mean = data.groupby("coin")["ret"].mean()
        data["ex"] = data["ret"] - data["coin"].map(coin_mean)
    else:
        data["ex"] = []

    sel = data[data["f"].notna() & (data["f"] >= 10)]["ex"].dropna().to_numpy(dtype=float)
    n_cases = int(len(sel))
    mean_ex = float(np.mean(sel)) if n_cases > 0 else None
    t = None
    if n_cases >= 2:
        sd = float(np.std(sel, ddof=1))
        if sd > 0:
            t = float(mean_ex / (sd / np.sqrt(n_cases)))

    # supporting check: buckets within the high-vol regime
    reg_d = data[data["inreg"] & data["f"].notna()]
    b1 = reg_d[(reg_d["f"] >= 0) & (reg_d["f"] < 5)]["ex"].dropna()
    b2 = reg_d[(reg_d["f"] >= 5) & (reg_d["f"] < 10)]["ex"].dropna()
    b3 = reg_d[reg_d["f"] >= 10]["ex"].dropna()
    means = [float(b.mean()) if len(b) else None for b in (b1, b2, b3)]
    if all(m is not None for m in means):
        sup_passed = bool(means[0] < means[1] < means[2])
        sup_value = float(means[2] - means[0])
    else:
        sup_passed = None
        sup_value = None

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases with forecast >= 10, below the plan's minimum of 30."
    elif t is not None and mean_ex > 0 and t >= 2:
        status = "confirmed"
        decided = "The mean excess return is positive with t >= 2 on at least 30 non-overlapping cases."
    elif t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "The mean excess return is negative with t <= -2 on at least 30 non-overlapping cases."
    else:
        status = "inconclusive"
        decided = "The t-statistic lies between -2 and 2 with at least 30 cases, so it neither confirms nor rejects."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_ex,
            "statistic": None if t is None else {"name": "t of the mean", "value": t},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess rises across in-regime forecast buckets [0,5), [5,10), >=10 (value: top minus bottom bucket mean)",
            "value": sup_value,
            "passed": sup_passed,
        },
        "counts": {
            "non-overlapping cases with forecast >= 10": n_cases,
            "in-regime cases forecast 0 to 5": int(len(b1)),
            "in-regime cases forecast 5 to 10": int(len(b2)),
            "in-regime cases forecast 10 and above": int(len(b3)),
        },
        "decided_by": decided,
        "reading": ("Cases are the bars at positions 0, 10, 20, ... of each window, and the coin's mean 10-bar return "
                    "is taken over that same grid pooled across all its windows; the buckets are half-open [0,5), [5,10), "
                    ">=10 on mean_reversion-regime bars including zero forecasts; and the supporting check passes when "
                    "the three bucket means strictly increase and does not enter the decision."),
    }
