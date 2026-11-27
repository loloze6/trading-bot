import numpy as np
import pandas as pd


def _component_series(df, comp_id, field="last_history_value"):
    """Read a recorded component value, flattened column or dict column; NaN where missing."""
    col = f"debug_info.components.{comp_id}.{field}"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        def get(v):
            try:
                if isinstance(v, str):
                    import json
                    v = json.loads(v)
                if isinstance(v, dict):
                    c = v.get(comp_id)
                    if isinstance(c, dict):
                        x = c.get(field)
                        return float(x) if x is not None else np.nan
            except Exception:
                return np.nan
            return np.nan
        return df["debug_info.components"].apply(get).astype(float)
    return pd.Series(np.nan, index=df.index)


def measure(bars):
    situ_ok = 0
    situ_total = 0
    case_rows = []      # (coin, date, forecast, raw next return)
    coin_means = {}

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        all_rets = []
        per_window = []
        for w in sorted(wins.keys(), key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = wins[w].copy().reset_index(drop=True)
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce")
            high = pd.to_numeric(df["high"], errors="coerce")
            low = pd.to_numeric(df["low"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)

            # --- situation from prices (inside the window only)
            up = close / close.shift(1) - 1.0
            rng = high - low
            loc = (close - low) / rng.replace(0, np.nan)
            mean_rng = rng.rolling(20, min_periods=20).mean()
            wide_px = 1.0 - rng / mean_rng.replace(0, np.nan)
            wide_rec = _component_series(df, "width_short", "last_history_value")
            wide = wide_rec.where(wide_rec.notna(), wide_px)

            computable = up.notna() & loc.notna() & wide.notna()
            situ = (up > 0) & (loc > 0.5) & (wide < 0)
            active = fc != 0
            sel = active & computable
            situ_total += int(sel.sum())
            situ_ok += int((sel & situ & (fc < 0)).sum())

            # --- next-day return, inside the window
            nxt = close.shift(-1) / close - 1.0
            all_rets.append(nxt.dropna().values)
            ts = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            per_window.append((df, fc, nxt, ts))

        if all_rets:
            r = np.concatenate(all_rets)
            mu = float(np.mean(r)) if len(r) else np.nan
        else:
            mu = np.nan
        coin_means[coin] = mu
        for df, fc, nxt, ts in per_window:
            m = (fc < 0) & nxt.notna() & ts.notna()
            for i in np.where(m.values)[0]:
                case_rows.append((coin, ts.iloc[i].floor("D"), float(fc.iloc[i]), float(nxt.iloc[i]) - mu))

    agreement = (situ_ok / situ_total) if situ_total > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)
    reading = ("Agreement counts active bars whose situation can be computed inside the window (up day, close above "
               "mid-range, recorded or price-rebuilt compression below 0) and short; the 30 independent case days "
               "minimum is applied as 'not observable'; the t clusters deviations by UTC day with a D/(D-1) correction; "
               "the supporting correlation is Pearson between the forecast and the raw (unsigned) next-day excess return.")
    threshold = "mean > 0 with t >= 2 (and correlation > 0) confirms; t <= -2 rejects"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "mean short-side next-day excess return", "value": None,
                             "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(situ_total)},
            "decided_by": "Fewer than 90% of active bars are short bars of the plan's situation (up day, close in upper "
                          "half, range above its 20-day mean).",
            "reading": reading,
        }

    cases = pd.DataFrame(case_rows, columns=["coin", "day", "fc", "ex"])
    n = len(cases)
    n_days = int(cases["day"].nunique()) if n else 0

    mean_v, t_v, corr = None, None, None
    if n > 0:
        x = -cases["ex"].values
        mean_v = float(np.mean(x))
        dev = pd.Series(x - mean_v).groupby(cases["day"].values).sum().values
        D = len(dev)
        if D > 1:
            var = (D / (D - 1)) * np.sum(dev ** 2) / (n ** 2)
            se = np.sqrt(var)
            t_v = float(mean_v / se) if se > 0 else None
        if n > 2 and np.std(cases["fc"].values) > 0 and np.std(cases["ex"].values) > 0:
            corr = float(np.corrcoef(cases["fc"].values, cases["ex"].values)[0, 1])

    corr_pass = None if corr is None else bool(corr > 0)

    if n_days < 30:
        status = "not observable"
        decided = f"Only {n_days} independent case days, below the plan's minimum of 30."
    elif t_v is None:
        status = "inconclusive"
        decided = "The t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_v > 0 and t_v >= 2 and corr_pass:
        status = "confirmed"
        decided = "Mean short-side excess return above 0 with t >= 2 and a positive forecast/excess-return correlation."
    elif mean_v > 0 and t_v >= 2:
        status = "inconclusive"
        decided = "Confirm-strength mean, but the correlation is not above 0."
    elif t_v <= -2:
        status = "rejected"
        decided = "Mean short-side excess return has t <= -2: these days rise more than usual the next day."
    else:
        status = "inconclusive"
        decided = "The t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "mean short-side next-day excess return",
                         "value": mean_v,
                         "statistic": None if t_v is None else {"name": "t of the mean, cases clustered by day",
                                                                 "value": t_v},
                         "threshold": threshold},
        "supporting_check": {"name": "correlation forecast vs next-day excess return",
                             "value": corr, "passed": corr_pass},
        "counts": {"cases": int(n), "independent case days": n_days},
        "decided_by": decided,
        "reading": reading,
    }
