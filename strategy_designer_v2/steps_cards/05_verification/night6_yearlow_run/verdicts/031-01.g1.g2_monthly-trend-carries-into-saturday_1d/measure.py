import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    COL_RAW = "debug_info.components.ret20.last_history_value"
    rows = []
    situation_hits = 0
    active_total = 0
    all_next_returns = {}

    for coin, windows in bars.items():
        coin_rets = []
        for w, df in windows.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy().reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            # Next bar's return, inside the window only.
            nxt = close.shift(-1) / close - 1.0
            coin_rets.append(nxt.dropna().values)

            # The 20-day return: recorded raw value, else recomputed from the prices.
            ret20_px = close / close.shift(20) - 1.0
            if COL_RAW in d.columns:
                raw = pd.to_numeric(d[COL_RAW], errors="coerce")
                raw = raw.where(raw.notna(), ret20_px)
            else:
                raw = ret20_px

            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            # A bar whose coming bar is Saturday is a Friday bar (daily bars, start time UTC).
            is_friday = (ts.dt.weekday == 4).values

            active = (fc != 0).values
            active_total += int(active.sum())
            ok = active & is_friday & (np.sign(fc.values) == np.sign(raw.values)) & raw.notna().values
            situation_hits += int(ok.sum())

            regime = d["regime"].astype(str).values
            for i in range(len(d)):
                if regime[i] == "trending" and is_friday[i] and not np.isnan(nxt.iloc[i]):
                    rows.append({
                        "coin": coin,
                        "day": ts.iloc[i].date().isoformat(),
                        "forecast": float(fc.iloc[i]),
                        "ret": float(nxt.iloc[i]),
                    })
        all_next_returns[coin] = np.concatenate(coin_rets) if coin_rets else np.array([])

    agreement = situation_hits / active_total if active_total > 0 else 0.0
    passed = agreement >= 0.90
    threshold = "t of 2 or more confirms (with top-minus-bottom above 0); t of -2 or less rejects; at least 200 distinct Friday days"
    main_name = "t of the daily-summed forecast/10 x excess next-bar return on Friday-close trending cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(active_total), "active bars in situation on expected side": int(situation_hits)},
            "decided_by": "Fewer than 90% of the active bars are Friday-close bars whose forecast sign follows the 20-day return's sign, as the Fidelity's situation and comparison require.",
            "reading": "The situation is read as bars whose start timestamp is a Friday (UTC), so the coming bar is Saturday, with the expected side equal to the sign of the raw 20-day return.",
        }

    cases = pd.DataFrame(rows, columns=["coin", "day", "forecast", "ret"])
    mu = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in all_next_returns.items()}
    if len(cases):
        cases["excess"] = cases["ret"] - cases["coin"].map(mu)
        cases["gain"] = cases["forecast"] / 10.0 * cases["excess"]
        cases = cases.dropna(subset=["excess", "gain"])

    n_cases = int(len(cases))
    daily = cases.groupby("day")["gain"].sum() if n_cases else pd.Series(dtype=float)
    n_days = int(len(daily))

    mean_val = None
    t_val = None
    if n_days >= 2:
        sd = float(daily.std(ddof=1))
        mean_val = float(daily.mean())
        t_val = float(mean_val / (sd / np.sqrt(n_days))) if sd > 0 else None

    # Supporting check: top third minus bottom third of the forecast, Saturday excess return, Welch t.
    diff = None
    welch_t = None
    n_third = n_cases // 3
    if n_third >= 2:
        order = cases.reset_index(drop=True)
        idx = np.argsort(order["forecast"].values, kind="mergesort")
        bottom = order["excess"].values[idx[:n_third]]
        top = order["excess"].values[idx[-n_third:]]
        diff = float(np.mean(top) - np.mean(bottom))
        tt = stats.ttest_ind(top, bottom, equal_var=False)
        welch_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
    check_passed = (diff is not None and diff > 0)

    counts = {"distinct Friday days with cases": n_days, "coin-cases": n_cases, "cases per third": int(n_third)}

    if n_days < 200:
        status = "not observable"
        decided = f"The plan's minimum of 200 distinct Friday days with cases is not reached ({n_days})."
    elif t_val is None:
        status = "inconclusive"
        decided = "The main measure's t could not be computed (zero dispersion), so neither the confirm nor the reject rule is met."
    elif t_val >= 2 and check_passed:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the top-minus-bottom difference is above 0."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main measure's t is 2 or more but the top-minus-bottom difference is at or below 0."
    else:
        status = "inconclusive"
        decided = "The main measure's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_val,
            "statistic": ({"name": "t of the mean across days", "value": t_val} if t_val is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "Saturday excess return, top third minus bottom third of forecast (Welch t "
                    + (f"{welch_t:.3f}" if welch_t is not None else "n/a") + ")",
            "value": diff,
            "passed": (bool(check_passed) if diff is not None else None),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Cases are all Friday-start bars with regime 'trending' and a next bar in the same window (forecast 0 included), the coin's mean is its mean next-bar return over all windows, the thirds are the lowest and highest floor(n/3) cases pooled across coins by forecast (stable sort), and only the 200-day minimum is applied as a hard count since the 2,000 coin-cases is stated as 'about'.",
    }
