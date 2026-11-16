import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    COMP = "range20"
    REGIME = "trending"

    def _component_raw(df, comp_id):
        col = f"debug_info.components.{comp_id}.last_history_value"
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"]:
                val = np.nan
                if isinstance(v, dict):
                    c = v.get(comp_id)
                    if isinstance(c, dict):
                        val = c.get("last_history_value", np.nan)
                try:
                    val = float(val)
                except (TypeError, ValueError):
                    val = np.nan
                out.append(val)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    def _range_pos_from_prices(close):
        # Position of the close in its last 20 closes (current included), centred: -0.5 low .. +0.5 high.
        lo = close.rolling(20, min_periods=20).min()
        hi = close.rolling(20, min_periods=20).max()
        rng = hi - lo
        pos = (close - lo) / rng.replace(0, np.nan) - 0.5
        return pos

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            raw = _component_raw(df, COMP)
            fallback = _range_pos_from_prices(close)
            raw = raw.where(raw.notna(), fallback)
            regime = df["regime"].astype(str)
            active = fc.notna() & (fc != 0)
            in_regime = regime == REGIME
            side_ok = np.sign(fc) == np.sign(raw)
            agree = active & in_regime & side_ok & raw.notna()
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "t-statistic of the pooled OLS slope of excess 10-bar forward return on forecast (trending, 10-bar grid)"
    threshold = "confirm: slope > 0 with t >= 2 and top-minus-bottom-third > 0; reject: slope < 0 with t <= -2; at least 100 grid cases"
    sup_name = "mean excess 10-bar return, top third of forecasts minus bottom third"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on its side": int(n_agree)},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are in regime `trending` (close at or above SMA200) with the forecast's sign matching the side of the close's position in its 20-close range.",
            "reading": "The plan's side was read from its graded comparison (higher in the range long, lower short), checked against the sign of the recorded range20 raw value (recomputed from 20 closes where missing), with the SMA200 condition read from the `regime` column.",
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            regime = df["regime"].astype(str).values
            n = len(df)
            for t in range(0, n - H, H):
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                all_rets.append(r)
                rows.append((coin, r, fc[t], regime[t]))
        # coin mean stored after loop
        mean_r = float(np.mean(all_rets)) if all_rets else np.nan
        rows = [(c, r, f, g, mean_r) if (c == coin and len(x) == 4) else x
                for x in rows for (c, r, f, g) in [x[:4]]]

    data = pd.DataFrame(rows, columns=["coin", "ret", "forecast", "regime", "coin_mean"])
    data = data[(data["regime"] == REGIME)]
    data = data.dropna(subset=["ret", "forecast", "coin_mean"])
    data["excess"] = data["ret"] - data["coin_mean"]
    n_cases = int(len(data))

    counts = {"independent grid cases in regime trending": n_cases}

    if n_cases < 100:
        return {
            "status": "not observable",
            "situation_check": {"agreement": agreement, "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} independent 10-bar grid cases in regime `trending`, below the plan's minimum of 100.",
            "reading": "Coin mean 10-bar return taken over all grid samples of all its windows (all regimes); thirds cut by sorted forecast rank as n//3 lowest and n//3 highest cases.",
        }

    x = data["forecast"].values.astype(float)
    y = data["excess"].values.astype(float)
    if np.std(x) == 0:
        slope, tstat = 0.0, 0.0
    else:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        tstat = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else 0.0

    order = np.argsort(x, kind="mergesort")
    k = n_cases // 3
    bottom = y[order[:k]]
    top = y[order[-k:]]
    diff = float(np.mean(top) - np.mean(bottom)) if k > 0 else None
    sup_pass = bool(diff is not None and diff > 0)

    if slope > 0 and tstat >= 2 and sup_pass:
        status = "confirmed"
        decided = f"Slope positive with t = {tstat:.2f} >= 2 and top-minus-bottom-third difference {diff:.4f} > 0: confirm rule met."
    elif slope < 0 and tstat <= -2:
        status = "rejected"
        decided = f"Slope negative with t = {tstat:.2f} <= -2: reject rule met."
    elif tstat >= 2:
        status = "inconclusive"
        decided = f"t = {tstat:.2f} >= 2 but top-minus-bottom-third difference is at or below 0: inconclusive by the plan's rule."
    else:
        status = "inconclusive"
        decided = f"Slope t = {tstat:.2f} lies between -2 and 2: inconclusive by the plan's rule."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": main_name, "value": tstat,
                         "statistic": {"name": "OLS slope t", "value": tstat},
                         "threshold": threshold},
        "supporting_check": {"name": sup_name, "value": diff, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": "Coin mean 10-bar return taken over all grid samples of all its windows (all regimes), cases are grid bars whose `regime` is trending, and thirds are the n//3 lowest and n//3 highest forecasts by sorted rank.",
    }
