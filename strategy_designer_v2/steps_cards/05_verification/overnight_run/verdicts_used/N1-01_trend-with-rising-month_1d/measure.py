import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    MIN_CASES = 30

    def get_raw(df, cid):
        col = f"debug_info.components.{cid}.last_history_value"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            def ext(x):
                try:
                    if isinstance(x, dict):
                        v = x.get(cid, {})
                        if isinstance(v, dict):
                            return v.get("last_history_value", np.nan)
                except Exception:
                    pass
                return np.nan
            return pd.to_numeric(df["debug_info.components"].map(ext), errors="coerce")
        return pd.Series(np.nan, index=df.index)

    n_active = 0
    n_agree = 0
    coin_frames = {}

    for coin, wins in bars.items():
        coin_frames[coin] = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            dist = get_raw(df, "dist")
            mom = get_raw(df, "mom")
            regime = df["regime"].astype(str) if "regime" in df.columns else pd.Series("", index=df.index)

            have_raw = dist.notna() & mom.notna()
            sit_raw = (dist >= 0) & (mom >= 0)
            sit = np.where(have_raw, sit_raw, regime == "trending")
            sit = pd.Series(sit, index=df.index).astype(bool)

            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            n_agree += int((active & sit & (fc > 0)).sum())

            fwd = close.shift(-H) / close - 1.0
            coin_frames[coin].append(pd.DataFrame({
                "fwd": fwd.values,
                "fc": fc.values,
                "grid": (np.arange(len(df)) % H == 0),
            }))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean excess forward 20-bar return after forecast > 0 (non-overlapping, pooled)"
    threshold = "confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive"
    reading = ("Situation taken as raw dist >= 0 and mom >= 0 from the strategy components' last_history_value "
               "(falling back to regime == 'trending' where those values are missing), side long (forecast > 0); "
               "the coin's mean 20-bar return uses every bar's forward 20-bar return in all its windows, cases are "
               "the window-grid bars 0, 20, 40, ... with forecast > 0 and a full forward return, the t is the "
               "ordinary one-sample t, and the plan's 'fewer than 30 cases' minimum is treated as not observable.")

    if n_active > 0 and not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of active bars are long bars with close above its 200-day SMA "
                           "and a non-negative 20-bar return, below the required 90%."),
            "reading": reading,
        }

    ex_list, fc_list = [], []
    for coin, frames in coin_frames.items():
        if not frames:
            continue
        allc = pd.concat(frames, ignore_index=True)
        coin_mean = allc["fwd"].dropna().mean()
        if not np.isfinite(coin_mean):
            continue
        sel = allc[allc["grid"] & (allc["fc"] > 0) & allc["fwd"].notna()]
        ex_list.extend((sel["fwd"] - coin_mean).tolist())
        fc_list.extend(sel["fc"].tolist())

    ex = np.array(ex_list, dtype=float)
    fcs = np.array(fc_list, dtype=float)
    n = int(len(ex))
    counts = {"non-overlapping active 20-bar cases pooled": n}

    mean_ex = float(ex.mean()) if n > 0 else None
    t = None
    if n >= 2:
        sd = ex.std(ddof=1)
        if sd > 0:
            t = float(mean_ex / (sd / np.sqrt(n)))

    slope = None
    sup_pass = None
    if n >= 3 and np.nanstd(fcs) > 0:
        slope = float(stats.linregress(fcs, ex).slope)
        sup_pass = bool(slope > 0)
    supporting = {"name": "slope of excess forward 20-bar return on forecast (active, non-overlapping)",
                  "value": slope, "passed": sup_pass}

    main = {"name": main_name, "value": mean_ex,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": threshold}
    sc = {"agreement": (float(agreement) if agreement is not None else None), "passed": passed}

    if n < MIN_CASES:
        return {"status": "not observable", "situation_check": sc, "main_measure": main,
                "supporting_check": supporting, "counts": counts,
                "decided_by": f"Only {n} non-overlapping active 20-bar cases pooled, fewer than the plan's minimum of 30.",
                "reading": reading}

    if t is not None and mean_ex > 0 and t >= 2:
        status = "confirmed"
        dec = "Confirm rule met: mean excess forward 20-bar return is above 0 with t >= 2."
    elif t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        dec = "Reject rule met: mean excess forward 20-bar return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        dec = "Inconclusive rule met: the t-stat lies between -2 and 2."

    return {"status": status, "situation_check": sc, "main_measure": main,
            "supporting_check": supporting, "counts": counts,
            "decided_by": dec, "reading": reading}
