import numpy as np
import pandas as pd
from scipy import stats


def _to_utc(ts):
    s = pd.Series(ts)
    if pd.api.types.is_numeric_dtype(s):
        v = s.astype(float)
        med = np.nanmedian(np.abs(v.values)) if len(v) else 0
        unit = "ns" if med > 1e17 else ("us" if med > 1e14 else ("ms" if med > 1e11 else "s"))
        return pd.to_datetime(v, unit=unit, utc=True)
    return pd.to_datetime(s, utc=True)


def measure(bars):
    H = 24
    RAW = "debug_info.components.fall24.last_history_value"

    n_active = 0
    n_agree = 0
    coin_rows = {}      # coin -> list of DataFrames of regime-bar cases
    coin_grid = {}      # coin -> list of non-overlapping 24-bar returns (holding the coin)

    for coin, windows in bars.items():
        coin_rows[coin] = []
        coin_grid[coin] = []
        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            ts = _to_utc(df["timestamp"]).reset_index(drop=True)
            # bar closes one hour after its start time
            close_hour = (ts + pd.Timedelta(hours=1)).dt.hour

            # raw 24-bar return: recorded value where present, recomputed from prices elsewhere
            recomputed = close / close.shift(H) - 1.0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed

            # --- situation check ---
            active = fc.notna() & (fc != 0)
            situation = (close_hour == 20) & (raw < 0)
            agree = active & situation & (fc > 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

            # --- forward 24-bar return, inside the window ---
            fwd = close.shift(-H) / close - 1.0

            # holding the coin: non-overlapping grid 0, 24, 48, ... of each window
            pos = np.arange(0, len(df), H)
            g = fwd.iloc[pos].dropna()
            coin_grid[coin].extend(g.tolist())

            # regime bars
            if "regime" in df.columns:
                reg = df["regime"].astype(str) == "mean_reversion"
            else:
                reg = close_hour == 20
            sub = pd.DataFrame({"fwd": fwd[reg], "forecast": fc[reg]}).dropna()
            if len(sub):
                coin_rows[coin].append(sub)

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "OLS slope of excess 24-bar return on forecast (regime bars, pooled)"
    threshold = "confirm: t >= 2 and mean excess on forecast>0 bars > 0; reject: t <= -2"
    reading = ("Situation bars are those whose close (timestamp + 1h) is at 20:00 UTC with a negative 24-bar return "
               "(recorded raw value, else recomputed from closes), expected side long; regime bars are those with "
               "regime == 'mean_reversion'; forward returns use row offsets inside each window; the coin's mean 24-bar "
               "return uses the non-overlapping grid 0, 24, 48, ... of each window pooled over all windows; t is the "
               "OLS slope over its standard error; the plan's minimum counts lead to 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on long side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the active bars are 20:00-UTC-close bars after a 24-hour fall with a "
                           "positive (long) forecast, so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    parts = []
    for coin, lst in coin_rows.items():
        if not lst:
            continue
        d = pd.concat(lst, ignore_index=True)
        g = coin_grid.get(coin, [])
        if len(g) == 0:
            continue
        d["excess"] = d["fwd"] - float(np.mean(g))
        parts.append(d)
    data = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=["fwd", "forecast", "excess"])

    n_regime = int(len(data))
    pos_mask = data["forecast"] > 0 if n_regime else pd.Series([], dtype=bool)
    n_pos = int(pos_mask.sum()) if n_regime else 0
    counts = {"regime bars with a full 24-bar forward return": n_regime,
              "regime bars with forecast > 0": n_pos}

    slope = None
    tstat = None
    if n_regime >= 3 and data["forecast"].nunique() > 1:
        lr = stats.linregress(data["forecast"].astype(float).values, data["excess"].astype(float).values)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    mean_pos = float(data.loc[pos_mask, "excess"].mean()) if n_pos > 0 else None
    sup_pass = (mean_pos > 0) if mean_pos is not None else None

    main = {"name": main_name, "value": slope,
            "statistic": ({"name": "OLS slope t", "value": tstat} if tstat is not None else None),
            "threshold": threshold}
    sup = {"name": "mean excess 24-bar return on forecast > 0 bars", "value": mean_pos, "passed": sup_pass}
    sc = {"agreement": (float(agreement) if agreement is not None else None), "passed": passed}

    if n_regime < 2000:
        status = "not observable"
        decided = f"Only {n_regime} regime bars with a full 24-bar forward return, below the plan's minimum of 2000."
    elif n_pos < 500:
        status = "not observable"
        decided = f"Only {n_pos} regime bars with forecast > 0, below the plan's minimum of 500."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, which meets neither the confirm nor the reject rule."
    elif tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return on forecast > 0 bars is above 0."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less."
    elif tstat >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but the mean excess return on forecast > 0 bars is not above 0."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": sc,
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
