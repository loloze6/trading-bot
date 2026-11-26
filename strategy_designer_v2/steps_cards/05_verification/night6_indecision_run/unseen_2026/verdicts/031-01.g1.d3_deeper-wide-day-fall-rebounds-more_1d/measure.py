import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    RANGE_MULT_MIN = 1.5
    CLOSE_LOC_MAX = 0.25
    RANGE_WIN = 20
    MIN_CASES = 30

    # ---------- coin mean daily return over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp") if "timestamp" in df.columns else df
            c = pd.to_numeric(d["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if allr.size else np.nan

    # ---------- situation check + case collection ----------
    n_active_eval = 0
    n_agree = 0
    case_rows = []  # (day, forecast, excess_ret, gain)

    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            d = df.copy()
            if "timestamp" in d.columns:
                d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
                d = d.sort_values("timestamp").reset_index(drop=True)
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
            pos = pd.to_numeric(d["postRebalance_current_allocation"], errors="coerce")

            rng = high - low
            mean_rng = rng.rolling(RANGE_WIN, min_periods=RANGE_WIN).mean()
            range_mult = rng / mean_rng.replace(0, np.nan)
            close_loc = (close - low) / rng.replace(0, np.nan)
            evaluable = range_mult.notna() & close_loc.notna()
            situation = (range_mult >= RANGE_MULT_MIN) & (close_loc <= CLOSE_LOC_MAX)

            active = fc != 0
            ev_active = active & evaluable
            n_active_eval += int(ev_active.sum())
            n_agree += int((ev_active & situation & (fc > 0)).sum())

            nxt = close.shift(-1) / close - 1.0
            sel = (fc > 0) & nxt.notna() & pos.notna()
            for i in np.where(sel.to_numpy())[0]:
                ex = float(nxt.iloc[i]) - mu
                gain = float(pos.iloc[i]) * ex
                day = d["timestamp"].iloc[i].floor("D") if "timestamp" in d.columns else i
                case_rows.append((day, float(fc.iloc[i]), ex, gain))

    agreement = (n_agree / n_active_eval) if n_active_eval > 0 else None
    passed = agreement is not None and agreement >= 0.90

    main_name = "mean of position x (next-day return - coin mean daily return) over forecast>0 bars, same-day cases summed"
    threshold = "confirm: mean > 0 with t >= 2 on >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 on >= 30 cases"
    reading = ("Range multiple uses the 20 recorded bars up to and including t within a window, so active bars without 20 "
               "prior bars are left out of the agreement share; the measure is position x (next-day return minus the coin's "
               "all-window mean daily return), the 30-case minimum counts (coin, bar) cases with forecast > 0, and the mean and "
               "t are taken over per-day sums of those cases.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(n_active_eval), "cases": len(case_rows)},
            "decided_by": ("Fewer than 90 % of the active bars are wide (range >= 1.5x 20-day mean range) low-close "
                           "(close location <= 0.25) days with a long forecast, as the plan's Fidelity requires."),
            "reading": reading,
        }

    n_cases = len(case_rows)
    if n_cases > 0:
        cdf = pd.DataFrame(case_rows, columns=["day", "fc", "ex", "gain"])
        daily = cdf.groupby("day")["gain"].sum().to_numpy(dtype=float)
        n_days = int(len(daily))
        mean_val = float(np.mean(cdf["gain"])) if n_days else None
        mean_daily = float(np.mean(daily))
        if n_days > 1:
            sd = float(np.std(daily, ddof=1))
            t = float(mean_daily / (sd / np.sqrt(n_days))) if sd > 0 else None
        else:
            t = None
        if n_cases > 2 and cdf["fc"].nunique() > 1 and cdf["ex"].nunique() > 1:
            rho = float(stats.spearmanr(cdf["fc"], cdf["ex"]).correlation)
        else:
            rho = None
    else:
        n_days, mean_daily, t, rho = 0, None, None, None

    counts = {"cases with a forecast above 0": int(n_cases), "days": int(n_days)}
    sup_passed = None if rho is None or not np.isfinite(rho) else bool(rho > 0)
    supporting = {"name": "Spearman(forecast, next-day excess return) > 0", "value": rho, "passed": sup_passed}

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} cases with a forecast above 0, fewer than the plan's minimum of 30."
    elif t is None or mean_daily is None or not np.isfinite(t):
        status = "inconclusive"
        decided = "The t of the main measure could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_daily > 0 and t >= 2:
        if sup_passed:
            status = "confirmed"
            decided = "Mean above 0 with t >= 2 on at least 30 cases and Spearman correlation above 0: the confirm rule."
        else:
            status = "inconclusive"
            decided = "A confirming t with a Spearman correlation at or below 0 is inconclusive by the plan."
    elif mean_daily < 0 and t <= -2:
        status = "rejected"
        decided = "Mean below 0 with t <= -2 on at least 30 cases: the reject rule."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or its sign disagrees with the mean): inconclusive by the plan."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_daily,
            "statistic": {"name": "t of the mean of per-day summed cases", "value": t} if t is not None else None,
            "threshold": threshold,
        },
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
