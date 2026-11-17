import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.weekend_ret.last_history_value"

    def to_ts(s):
        if pd.api.types.is_numeric_dtype(s):
            v = pd.to_numeric(s, errors="coerce")
            mx = np.nanmax(v.values) if len(v) else 0
            unit = "ms" if mx > 1e11 else "s"
            return pd.to_datetime(v, unit=unit, utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")

    active_total = 0
    active_agree = 0
    case_rows = []      # (coin, forecast, r2)
    coin_means = {}

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        grid_rets = []
        for w in sorted(wins.keys()):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            n = len(df)
            # coin mean of non-overlapping 2-bar returns (grid 0,2,4,... per window)
            for i in range(0, n - 2, 2):
                if np.isfinite(close[i]) and np.isfinite(close[i + 2]) and close[i] != 0:
                    grid_rets.append(close[i + 2] / close[i] - 1.0)

            ts = to_ts(df["timestamp"])
            dow = ts.dt.dayofweek.values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values.astype(float)
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * n)

            # raw 1-bar return in percent: recorded value, else recomputed from prices
            raw_price = np.full(n, np.nan)
            raw_price[1:] = (close[1:] / close[:-1] - 1.0) * 100.0
            if LHV in df.columns:
                rec = pd.to_numeric(df[LHV], errors="coerce").values.astype(float)
                raw = np.where(np.isfinite(rec), rec, raw_price)
            else:
                raw = raw_price

            # situation check
            sunday = dow == 6  # bar starting Sunday: its next bar is Monday
            for i in range(n):
                if np.isfinite(fc[i]) and fc[i] != 0:
                    active_total += 1
                    if sunday[i] and np.isfinite(raw[i]) and raw[i] > 0 and fc[i] < 0:
                        active_agree += 1

            # cases
            for i in range(n):
                if sunday[i] and regime[i] == "mean_reversion" and np.isfinite(fc[i]) and fc[i] < 0:
                    if i + 2 < n and np.isfinite(close[i]) and np.isfinite(close[i + 2]) and close[i] != 0:
                        case_rows.append((coin, fc[i], close[i + 2] / close[i] - 1.0))
        coin_means[coin] = float(np.mean(grid_rets)) if grid_rets else np.nan

    agreement = (active_agree / active_total) if active_total > 0 else None
    passed = True if agreement is None else bool(agreement >= 0.9)

    main_name = "t of mean of x = (-forecast/10) * -(r2 - coin mean 2-bar return), Sunday short cases"
    threshold = "confirm t >= 2 with check < 0; reject t <= -2; at least 100 cases"
    reading = ("Sunday bar = bar whose UTC start is a Sunday (next bar Monday); 'rose' read as raw 1-bar return > 0; "
               "cases need t+2 inside the window; thirds by |forecast| from a stable ascending sort split with "
               "np.array_split; fewer than 100 cases reported as not observable per the minimum-count rule.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None},
            "decided_by": "Fewer than 90% of active bars are Sunday bars after a weekend rise with a short forecast, "
                          "so the config does not trade the plan's situation on its side.",
            "reading": reading,
        }

    cases = [(c, f, r) for (c, f, r) in case_rows if np.isfinite(coin_means.get(c, np.nan))]
    ncases = len(cases)
    fcs = np.array([f for _, f, _ in cases], dtype=float)
    dev = np.array([r - coin_means[c] for c, _, r in cases], dtype=float)
    x = (-fcs / 10.0) * (-dev)

    mean_x = float(np.mean(x)) if ncases > 0 else None
    t = None
    if ncases > 1:
        sd = float(np.std(x, ddof=1))
        t = float(mean_x / (sd / np.sqrt(ncases))) if sd > 0 else None

    check_val = None
    if ncases >= 3:
        order = np.argsort(np.abs(fcs), kind="mergesort")
        parts = np.array_split(order, 3)
        check_val = float(np.mean(dev[parts[2]]) - np.mean(dev[parts[0]]))
    check_pass = None if check_val is None else bool(check_val < 0)

    sit = {"agreement": None if agreement is None else float(agreement), "passed": passed}
    mm = {"name": main_name, "value": mean_x,
          "statistic": None if t is None else {"name": "ordinary t of the mean", "value": t},
          "threshold": threshold}
    sc = {"name": "mean(r2 - m) top third minus bottom third by |forecast|", "value": check_val,
          "passed": check_pass}
    counts = {"cases": ncases}

    if ncases < 100:
        status = "not observable"
        decided = f"Only {ncases} cases, below the plan's minimum of 100 cases."
    elif t is None:
        status = "inconclusive"
        decided = "The t of the main measure could not be computed (zero dispersion)."
    elif t >= 2 and check_pass:
        status = "confirmed"
        decided = "The main measure has t >= 2 and the top-minus-bottom third check is below 0."
    elif t <= -2:
        status = "rejected"
        decided = "The main measure has t <= -2: weekend rises are followed by above-average Monday-Tuesday returns."
    elif t >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the supporting check is at or above 0, which the plan rules inconclusive."
    else:
        status = "inconclusive"
        decided = "t lies strictly between -2 and 2."

    return {
        "status": status,
        "situation_check": sit,
        "main_measure": mm,
        "supporting_check": sc,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
