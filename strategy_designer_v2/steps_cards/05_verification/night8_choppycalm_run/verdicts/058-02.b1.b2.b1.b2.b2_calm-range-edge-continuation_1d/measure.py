import numpy as np
import pandas as pd


RAW = "debug_info.components.range_pos.last_history_value"
H = 5


def _price_side(df):
    # Sign of the close's place in its 20-day high-low range (current bar included), from the prices.
    hi = df["high"].astype(float).rolling(20, min_periods=20).max()
    lo = df["low"].astype(float).rolling(20, min_periods=20).min()
    mid = (hi + lo) / 2.0
    return np.sign(df["close"].astype(float) - mid)


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = f != 0
            if not active.any():
                continue
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            side = np.sign(raw)
            fallback = _price_side(df)
            side = side.where(raw.notna(), fallback)
            calm = df["regime"].astype(str) != "chop"
            ok = active & calm & (side != 0) & (np.sign(f) == side)
            n_active += int(active.sum())
            n_agree += int(ok[active].sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "|forecast|-weighted mean of sign(forecast) x (5-bar return minus coin's mean 5-bar return)"
    threshold = "confirm: > 0 with t >= 2 and convexity check passes; reject: < 0 with t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "Fewer than 90% of the active bars are calm (non-chop) bars whose forecast sign matches "
                          "the sign of the close's place around the 20-day range middle.",
            "reading": "Calm is a bar whose regime is not 'chop'; the expected side is the sign of the raw range "
                       "position (prices' 20-day high-low midpoint when the raw value is missing).",
        }

    # ---------- 2. criterion ----------
    rows = []
    coin_grid_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            raw = (pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns
                   else np.full(len(df), np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df) - H, H):
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                r = c[i + H] / c[i] - 1.0
                allr.append(r)
                if f[i] != 0:
                    rows.append({"coin": coin, "day": ts.iloc[i].strftime("%Y-%m-%d"),
                                 "f": float(f[i]), "r": r, "raw": float(raw[i])})
        coin_grid_rets[coin] = float(np.mean(allr)) if allr else np.nan

    cases = pd.DataFrame(rows, columns=["coin", "day", "f", "r", "raw"])
    if len(cases):
        cases["mu"] = cases["coin"].map(coin_grid_rets)
        cases = cases.dropna(subset=["mu"])
        cases["y"] = np.sign(cases["f"]) * (cases["r"] - cases["mu"])
        cases["w"] = cases["f"].abs()
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}

    value = None
    tstat = None
    if n_cases > 0 and cases["w"].sum() > 0:
        W = cases["w"].sum()
        m = float((cases["w"] * cases["y"]).sum() / W)
        value = m
        dev = cases["w"] * (cases["y"] - m)
        per_day = dev.groupby(cases["day"]).sum()
        G = len(per_day)
        if G > 1:
            se = np.sqrt((per_day ** 2).sum() * G / (G - 1)) / W
            tstat = float(m / se) if se > 0 else None

    # supporting check
    sup_val = None
    sup_pass = None
    sc = cases.dropna(subset=["raw"]) if n_cases else cases
    if len(sc) >= 2:
        a = sc["raw"].abs()
        med = a.median()
        up = sc[a > med]
        lo = sc[a <= med]
        if len(up) and len(lo) and up["raw"].abs().mean() > 0 and lo["raw"].abs().mean() > 0:
            u = up["y"].mean() / up["raw"].abs().mean()
            l = lo["y"].mean() / lo["raw"].abs().mean()
            sup_val = float(u - l)
            sup_pass = bool(u > l)

    main = {"name": main_name, "value": value,
            "statistic": ({"name": "t of weighted mean, cases of one day pooled", "value": tstat}
                          if tstat is not None else None),
            "threshold": threshold}
    support = {"name": "upper-minus-lower half mean signed excess return per unit |raw position|",
               "value": sup_val, "passed": sup_pass}
    reading = ("Grid at positions 0,5,10,... of each window with cases where forecast != 0; coin mean 5-bar return "
               "taken over that same grid on all its windows; t is cluster-robust by calendar day; halves split at "
               "the median |raw| (ties to the lower half) and 'per unit' is the half's mean signed excess return "
               "(unweighted) divided by its mean |raw|; calm is regime not 'chop'.")

    if n_cases < 100 or n_days < 60:
        status = "not observable"
        decided = (f"The plan's minimum of 100 grid cases on 60 distinct days is not reached "
                   f"({n_cases} cases, {n_days} days).")
    elif value is None or tstat is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif value > 0 and tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Weighted mean signed excess return is above 0 with t >= 2 and the convexity check passes."
        else:
            status = "inconclusive"
            decided = "A confirming main measure whose convexity check fails is inconclusive."
    elif value < 0 and tstat <= -2:
        status = "rejected"
        decided = "Weighted mean signed excess return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2 (or sign and t disagree), which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": support,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
