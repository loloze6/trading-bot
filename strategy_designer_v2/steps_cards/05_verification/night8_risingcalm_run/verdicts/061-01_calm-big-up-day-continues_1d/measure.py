import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    RAW = "debug_info.components.day_move.last_history_value"
    PPV = "debug_info.components.day_move.post_pipeline_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            ret1 = np.full(len(df), np.nan)
            if len(df) > 1:
                ret1[1:] = close[1:] / close[:-1] - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").values
            else:
                raw = np.full(len(df), np.nan)
            day_sign = np.where(np.isnan(raw), np.sign(ret1), np.sign(raw))
            regime = df["regime"].astype(str).values
            calm = regime == "unknown"
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                s = day_sign[i]
                if calm[i] and not np.isnan(s) and s != 0 and np.sign(fc[i]) == s:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "pooled slope of 5-bar excess return on forecast, day-clustered t"
    threshold = "confirm if slope t >= 2 (100+ cases) and largest |forecast| third above smallest; reject if t <= -2 (100+ cases)"
    reading = ("Calm profile read as regime 'unknown' (no 'chop' veto) and the day's direction as the sign of the raw "
               "component (price return where missing); the slope t uses OLS with residual-score deviations summed per "
               "day (cluster-robust, G/(G-1) correction); the coin's mean 5-bar return is over all grid bars of all its "
               "windows; thirds are floor(n/3) cases at each end of |forecast|.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are calm-profile bars whose forecast sign follows the "
                           "day's return sign, as the Fidelity's situation and side require."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_rets = []
        cand = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ppv = pd.to_numeric(df[PPV], errors="coerce").values if PPV in df.columns else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                coin_rets.append(r)
                if fc[i] != 0 and np.isfinite(ppv[i]):
                    cand.append((ts.iloc[i].floor("D"), r, ppv[i], fc[i]))
        if not coin_rets:
            continue
        mu = float(np.mean(coin_rets))
        for d, r, x, f in cand:
            rows.append({"day": d, "y": r - mu, "x": x, "f": f})

    cases = pd.DataFrame(rows, columns=["day", "y", "x", "f"])
    n = int(len(cases))
    n_days = int(cases["day"].nunique()) if n else 0

    slope = None
    tval = None
    if n >= 3 and cases["x"].var() > 0:
        x = cases["x"].values.astype(float)
        y = cases["y"].values.astype(float)
        xc = x - x.mean()
        sxx = float(np.sum(xc ** 2))
        b = float(np.sum(xc * (y - y.mean())) / sxx)
        a = y.mean() - b * x.mean()
        e = y - a - b * x
        sc = pd.Series(xc * e).groupby(cases["day"].values).sum().values
        G = len(sc)
        if G > 1:
            var_b = (G / (G - 1)) * float(np.sum(sc ** 2)) / sxx ** 2
            if var_b > 0:
                slope = b
                tval = float(b / np.sqrt(var_b))
            else:
                slope = b

    sup_val = None
    sup_pass = None
    if n >= 3:
        k = n // 3
        c = cases.assign(a=cases["f"].abs(), d=cases["y"] * np.sign(cases["f"]))
        c = c.sort_values("a", kind="mergesort").reset_index(drop=True)
        low = float(c["d"].iloc[:k].mean())
        high = float(c["d"].iloc[n - k:].mean())
        sup_val = high - low
        sup_pass = bool(high > low)

    if n < 100:
        status = "not observable"
        decided = f"Only {n} non-overlapping calm-profile cases, below the plan's minimum of 100."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "Slope t >= 2 with at least 100 cases and the largest |forecast| third above the smallest third."
    elif tval <= -2:
        status = "rejected"
        decided = "Slope t <= -2 with at least 100 cases."
    elif tval >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but the size check failed (largest third not above smallest third)."
    else:
        status = "inconclusive"
        decided = "Slope t between -2 and 2 with at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": None if slope is None else float(slope),
            "statistic": None if tval is None else {"name": "slope t (day-clustered)", "value": float(tval)},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean directional excess 5-bar return, largest |forecast| third minus smallest third",
            "value": None if sup_val is None else float(sup_val),
            "passed": sup_pass,
        },
        "counts": {"non-overlapping cases inside the calm profile": n, "days": n_days},
        "decided_by": decided,
        "reading": reading,
    }
