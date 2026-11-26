import json
import numpy as np
import pandas as pd

H = 5
COMP = "thin_fall"
RAW_COL = "debug_info.components.%s.last_history_value" % COMP


def _raw_series(df):
    """Raw value of the thin_fall component on each bar (NaN where not recorded)."""
    if RAW_COL in df.columns:
        return pd.to_numeric(df[RAW_COL], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for v in df["debug_info.components"].values:
            val = np.nan
            try:
                d = v
                if isinstance(d, str):
                    d = json.loads(d)
                if isinstance(d, dict) and COMP in d:
                    c = d[COMP]
                    if isinstance(c, str):
                        c = json.loads(c)
                    if isinstance(c, dict) and c.get("last_history_value") is not None:
                        val = float(c["last_history_value"])
            except Exception:
                val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars):
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            close = pd.to_numeric(df["close"], errors="coerce").values
            regime = df["regime"].astype(str).values
            raw = _raw_series(df).values
            # 30-day return from prices within the window, as a fallback for the raw sign
            ret30 = np.full(len(df), np.nan)
            if len(df) > 30:
                ret30[30:] = close[30:] / close[:-30] - 1.0
            for i in range(len(df)):
                if f[i] == 0:
                    continue
                n_active += 1
                in_profile = regime[i] == "unknown"
                r = raw[i] if np.isfinite(raw[i]) else ret30[i]
                fell = np.isfinite(r) and r < 0
                if in_profile and fell and f[i] < 0:
                    n_agree += 1
    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = agreement is not None and agreement >= 0.9

    main_name = "|forecast|-weighted mean short-direction 5-bar excess return"
    threshold = "confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2"
    reading = ("Situation bars are bars with regime 'unknown' (the falling calm profile, the only regime with a "
               "strategy) and a negative thin_fall raw value (30-day return from prices where it is not recorded), "
               "on the short side; cases are grid bars 0,5,10,... of each window with forecast < 0 and a 5-bar "
               "return inside the window, the coin's mean is over all its grid cells in all windows, t is the "
               "|forecast|-weighted mean over a day-clustered standard error (weighted deviations summed per UTC "
               "day, G/(G-1) correction), and the supporting check splits at the median |forecast| into "
               "|forecast| > median versus <= median with unweighted half means.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in the situation on the short side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars inside the falling "
                           "calm profile with a negative 30-day thin-volume fall value"
                           if n_active > 0 else "No bar has a non-zero forecast, so the plan's short in falling "
                           "calm markets is never taken"),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin in sorted(bars):
        grid = []
        for w in sorted(bars[coin]):
            df = bars[coin][w].reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                grid.append((c1 / c0 - 1.0, f[i], ts.iloc[i].strftime("%Y-%m-%d")))
        if not grid:
            continue
        mean_r = float(np.mean([g[0] for g in grid]))
        for r, fc, day in grid:
            if np.isfinite(fc) and fc < 0:
                rows.append({"coin": coin, "day": day, "x": -(r - mean_r), "w": abs(fc)})

    cases = pd.DataFrame(rows, columns=["coin", "day", "x", "w"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"distinct days with cases": n_days, "cases": n_cases}

    m = None
    t = None
    if n_cases > 0 and cases["w"].sum() > 0:
        W = cases["w"].sum()
        m = float((cases["w"] * cases["x"]).sum() / W)
        dev = cases["w"] * (cases["x"] - m)
        D = dev.groupby(cases["day"]).sum().values
        G = len(D)
        if G > 1:
            var = (G / (G - 1.0)) * float(np.sum(D ** 2)) / (W ** 2)
            se = np.sqrt(var)
            t = float(m / se) if se > 0 else None

    sup_val = None
    sup_pass = None
    if n_cases > 0:
        med = cases["w"].median()
        big = cases.loc[cases["w"] > med, "x"]
        small = cases.loc[cases["w"] <= med, "x"]
        if len(big) > 0 and len(small) > 0:
            sup_val = float(big.mean() - small.mean())
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    main = {"name": main_name, "value": m,
            "statistic": None if t is None else {"name": "t of the weighted mean, cases of one day pooled",
                                                 "value": t},
            "threshold": threshold}
    supp = {"name": "mean excess of larger-|forecast| half minus smaller half", "value": sup_val,
            "passed": sup_pass}
    sc = {"agreement": float(agreement), "passed": True}

    if n_days < 30:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": supp, "counts": counts,
                "decided_by": "Fewer than the plan's minimum of 30 distinct days with cases (%d)." % n_days,
                "reading": reading}

    if m is not None and t is not None and m > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The weighted mean short-direction excess return is above 0 with t >= 2 and the supporting check is positive."
    elif m is not None and t is not None and m < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean short-direction excess return is below 0 with t <= -2."
    elif t is not None and t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check is at or below 0, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive."

    return {"status": status, "situation_check": sc, "main_measure": main, "supporting_check": supp,
            "counts": counts, "decided_by": decided, "reading": reading}
