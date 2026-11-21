import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.fall24.last_history_value"
    H = 2

    n_active = 0
    n_agree = 0
    case_rows = []      # (coin, forecast, ret2)
    coin_grid_rets = {}  # coin -> list of non-overlapping 2-bar returns

    for coin in sorted(bars.keys()):
        grid_list = []
        for window in sorted(bars[coin].keys(), key=lambda w: (len(str(w)), str(w))):
            df = bars[coin][window]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close = pd.to_numeric(df["close"], errors="coerce").astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).astype(float)

            # --- situation check ---
            # Bar closing at 20:00 UTC: its coming bar starts at 20:00.
            next_hour = (ts + pd.Timedelta(hours=1)).dt.hour
            is_hour = (next_hour == 20).values
            # 24-bar fall: raw PriceEvolution(24) < 0; recompute from prices where missing
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce").astype(float)
            else:
                raw = pd.Series(np.nan, index=df.index)
            recomputed = close / close.shift(24) - 1.0
            raw = raw.where(raw.notna(), recomputed)
            is_fall = (raw < 0).fillna(False).values
            situation = is_hour & is_fall

            active = (fc != 0).values
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0).values).sum())

            # --- 2-bar forward returns inside the window ---
            ret2 = (close.shift(-H) / close - 1.0).values

            # non-overlapping grid for the coin's mean 2-bar return
            idx = np.arange(0, len(df), H)
            g = ret2[idx]
            g = g[np.isfinite(g)]
            grid_list.extend(g.tolist())

            # --- cases: regime mean_reversion with forecast > 0, one per day ---
            regime = df["regime"].astype(str).values
            mask = (regime == "mean_reversion") & (fc > 0).values
            if mask.any():
                sub = pd.DataFrame({
                    "day": ts[mask].dt.floor("D").values,
                    "fc": fc[mask].values,
                    "r": ret2[mask],
                })
                sub = sub.groupby("day", sort=True).first().reset_index()
                for _, row in sub.iterrows():
                    case_rows.append((coin, float(row["fc"]), float(row["r"])))
        coin_grid_rets[coin] = grid_list

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    threshold_txt = "slope t >= 2 confirms (with check), t <= -2 rejects, otherwise inconclusive; at least 500 cases"
    main_name = "t of OLS slope of excess 2-bar return on forecast (pooled)"
    check_name = "mean excess 2-bar return, top third minus bottom third of forecasts"
    reading = ("Decision bars are those whose timestamp + 1h has hour 20 with a negative 24-bar raw change; "
               "one case per coin per UTC day (first such bar), cases without a full 2-bar return inside the window dropped; "
               "the coin mean uses non-overlapping 2-bar returns on each window's grid from its first row; "
               "thirds are the n//3 lowest and n//3 highest forecasts after a stable sort.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of active (nonzero-forecast) bars are long on bars closing at 20:00 UTC "
                           "after a 24-hour fall, so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    coin_mean = {c: (float(np.mean(v)) if len(v) > 0 else np.nan) for c, v in coin_grid_rets.items()}
    cases = pd.DataFrame(case_rows, columns=["coin", "fc", "r"])
    if len(cases):
        cases["mu"] = cases["coin"].map(coin_mean)
        cases["ex"] = cases["r"] - cases["mu"]
        cases = cases[np.isfinite(cases["ex"]) & np.isfinite(cases["fc"])].reset_index(drop=True)
    n_cases = int(len(cases))
    counts = {"cases": n_cases}

    if n_cases < 500:
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold_txt},
            "supporting_check": {"name": check_name, "value": None, "passed": None},
            "counts": counts,
            "decided_by": f"Only {n_cases} cases, fewer than the 500 the plan requires.",
            "reading": reading,
        }

    x = cases["fc"].values.astype(float)
    y = cases["ex"].values.astype(float)
    if np.std(x) > 0:
        lr = stats.linregress(x, y)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else float("nan")
    else:
        slope, t_slope = float("nan"), float("nan")

    order = np.argsort(x, kind="mergesort")
    k = n_cases // 3
    bottom = y[order[:k]]
    top = y[order[n_cases - k:]]
    diff = float(np.mean(top) - np.mean(bottom)) if k > 0 else float("nan")
    check_pass = bool(np.isfinite(diff) and diff > 0)
    counts["top third"] = int(k)
    counts["bottom third"] = int(k)

    if np.isfinite(t_slope) and t_slope >= 2 and check_pass:
        status = "confirmed"
        decided = f"Slope t = {t_slope:.2f} >= 2 and top-minus-bottom third excess return {diff:.5f} > 0."
    elif np.isfinite(t_slope) and t_slope <= -2:
        status = "rejected"
        decided = f"Slope t = {t_slope:.2f} <= -2."
    elif np.isfinite(t_slope) and t_slope >= 2:
        status = "inconclusive"
        decided = f"Slope t = {t_slope:.2f} >= 2 but the supporting check fails (difference {diff:.5f} <= 0)."
    else:
        status = "inconclusive"
        decided = f"Slope t = {t_slope:.2f} lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope if np.isfinite(slope) else None,
            "statistic": {"name": "OLS slope t", "value": t_slope if np.isfinite(t_slope) else None},
            "threshold": threshold_txt,
        },
        "supporting_check": {"name": check_name, "value": diff if np.isfinite(diff) else None,
                             "passed": check_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
