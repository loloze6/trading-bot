import numpy as np
import pandas as pd
from scipy import stats


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype("float64")
        mx = np.nanmax(np.abs(v.values)) if len(v) else 0
        if mx > 1e17:
            unit = "ns"
        elif mx > 1e14:
            unit = "us"
        elif mx > 1e11:
            unit = "ms"
        else:
            unit = "s"
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    RAW = "debug_info.components.ret72.last_history_value"
    H = 2

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin, wins in bars.items():
        prepared[coin] = {}
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            ts = _to_utc(d["timestamp"]).reset_index(drop=True)
            d["_hour"] = ts.dt.hour.values
            close = d["close"].astype(float)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            # raw 72-bar return: recorded value, else recomputed from prices inside the window
            ret72_px = close / close.shift(72) - 1.0
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw = raw.where(raw.notna(), ret72_px)
            else:
                raw = ret72_px
            d["_fc"] = fc
            d["_raw"] = raw
            prepared[coin][w] = d

            active = fc.notna() & (fc != 0)
            in_sit = d["_hour"].isin([15, 16])
            same_side = np.sign(fc) == np.sign(raw)
            n_active += int(active.sum())
            n_agree += int((active & in_sit & same_side & raw.notna()).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "OLS slope of 2-bar excess return (15:00 UTC bar) on recorded forecast, pooled"
    threshold = "slope t >= 2 confirms (with supporting mean > 0, >= 1000 cases); t <= -2 rejects"
    supp_name = "mean of sign(forecast) x excess 2-bar return"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars stamped 15:00/16:00 UTC "
                           "with the forecast's sign equal to the sign of the coin's 72-bar return, as the Fidelity's "
                           "situation and continuation side require."),
            "reading": "Situation bars are those stamped 15:00 and 16:00 UTC; expected side is the sign of the raw ret72 value (recomputed from prices where missing).",
        }

    # ---------- 2. criterion ----------
    xs, ys = [], []
    for coin, wins in prepared.items():
        # coin's mean 2-bar return over all windows, non-overlapping grid 0,2,4,... per window
        grid_rets = []
        for w, d in wins.items():
            c = d["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid_rets.append(r[np.isfinite(r)])
        if not grid_rets:
            continue
        allr = np.concatenate(grid_rets)
        if len(allr) == 0:
            continue
        coin_mean = float(np.mean(allr))

        for w, d in wins.items():
            c = d["close"].astype(float)
            fwd = c.shift(-H) / c - 1.0
            sel = (d["_hour"] == 15) & d["_fc"].notna() & fwd.notna() & np.isfinite(fwd)
            if sel.any():
                xs.append(d.loc[sel, "_fc"].values.astype(float))
                ys.append((fwd[sel] - coin_mean).values.astype(float))

    x = np.concatenate(xs) if xs else np.array([])
    y = np.concatenate(ys) if ys else np.array([])
    n = int(len(x))

    slope = None
    tstat = None
    if n >= 3 and np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0

    supp = float(np.mean(np.sign(x) * y)) if n > 0 else None
    supp_pass = None if supp is None else bool(supp > 0)

    if n < 1000:
        status = "not observable"
        decided = f"Only {n} cases (bars stamped 15:00 UTC with a 2-bar outcome), below the plan's minimum of 1000."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope could not be estimated (no variation in the forecast), so neither rule is met."
    elif tstat >= 2 and supp_pass:
        status = "confirmed"
        decided = "Slope t >= 2 and supporting mean > 0 from at least 1000 cases: the confirm rule."
    elif tstat <= -2:
        status = "rejected"
        decided = "Slope t <= -2: the reject rule (the post-settlement move runs against the 3-day return)."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "Slope t >= 2 but supporting mean <= 0: inconclusive by the plan's rule."
    else:
        status = "inconclusive"
        decided = "Slope t between -2 and 2: inconclusive by the plan's rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if tstat is None else {"name": "ordinary OLS slope t", "value": tstat},
            "threshold": threshold,
        },
        "supporting_check": {"name": supp_name, "value": supp, "passed": supp_pass},
        "counts": {"cases": n},
        "decided_by": decided,
        "reading": ("Cases are all bars stamped 15:00 UTC (including any with forecast 0) with close[t+2] taken two rows "
                    "later in the same window; the coin's mean 2-bar return is pooled over all its windows on the "
                    "non-overlapping grid 0,2,4,... of each window."),
    }
