import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 24
    BAND = 2.0
    RAW = "debug_info.components.fall_x_rise.last_history_value"

    total_active = 0
    agree_active = 0
    case_rows = []  # (forecast, excess)

    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].to_numpy(dtype=float)
            n = len(c)
            for p in range(0, n - H, H):
                if c[p] > 0 and np.isfinite(c[p]) and np.isfinite(c[p + H]):
                    rets.append(c[p + H] / c[p] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if len(rets) else np.nan

    raw_cases = []  # (coin, forecast, ret)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            if n == 0:
                continue
            ts = pd.to_datetime(df["timestamp"], utc=True)
            close_hour = (ts + pd.Timedelta(hours=1)).dt.hour.to_numpy()
            settle = np.isin(close_hour, [0, 16])
            c = df["close"].to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(n, np.nan)

            # price-based fall and run-up, inside the window where computable
            fall = np.full(n, np.nan)
            rise = np.full(n, np.nan)
            if n > 2:
                fall[2:] = c[2:] / c[:-2] - 1.0
            if n > 168:
                rise[168:] = c[168:] / c[:-168] - 1.0
            fall_ok = np.where(np.isfinite(fall), fall < 0, True)
            rise_ok = np.where(np.isfinite(rise), rise > 0, True)
            raw_ok = np.isfinite(raw) & (raw > 0)
            situation = settle & raw_ok & fall_ok & rise_ok

            active = f != 0
            total_active += int(active.sum())
            agree_active += int((active & situation & (f > 0)).sum())

            # bets: rise of the forecast on its side of at least the band
            bet = np.zeros(n, dtype=bool)
            side = 0
            base = 0.0
            for i in range(n):
                fi = f[i]
                s = 1 if fi > 0 else (-1 if fi < 0 else 0)
                if s == 0:
                    side = 0
                    base = 0.0
                    continue
                if s != side:
                    side = s
                    base = 0.0
                mag = abs(fi)
                if mag - base >= BAND:
                    bet[i] = True
                    base = mag
                else:
                    base = min(base, mag)

            # one case per 24-bar grid cell: the first bet on a settlement bar
            for start in range(0, n, H):
                end = min(start + H, n)
                for i in range(start, end):
                    if bet[i] and settle[i]:
                        if i + H < n and np.isfinite(c[i]) and c[i] > 0 and np.isfinite(c[i + H]):
                            raw_cases.append((coin, f[i], c[i + H] / c[i] - 1.0))
                        break

    agreement = (agree_active / total_active) if total_active > 0 else 0.0
    passed = total_active > 0 and agreement >= 0.9

    main_name = "mean of (24-bar return minus coin mean 24-bar return) x forecast/10 on settlement-bar bets"
    threshold = "confirm t >= 2 with supporting check passing on >= 100 cases; reject t <= -2 on >= 100 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"cases": None, "active bars": int(total_active)},
            "decided_by": "Fewer than 90% of bars with a non-zero forecast are long bets on bars closing at 00:00 or 16:00 UTC after a 2-hour fall with a positive 7-day return, as the plan's Fidelity requires.",
            "reading": "Settlement bars are those whose close (start + 1 hour) is at 00:00 or 16:00 UTC; the situation is a positive raw fall_x_rise value with, where computable inside the window, a negative 2-bar return and a positive 168-bar return.",
        }

    fc = np.array([r[1] for r in raw_cases], dtype=float)
    ex = np.array([r[2] - coin_mean.get(r[0], np.nan) for r in raw_cases], dtype=float)
    ok = np.isfinite(fc) & np.isfinite(ex)
    fc, ex = fc[ok], ex[ok]
    n_cases = int(len(fc))
    prod = ex * fc / 10.0

    mean_prod = float(np.mean(prod)) if n_cases > 0 else None
    t_val = None
    if n_cases > 1:
        sd = float(np.std(prod, ddof=1))
        t_val = float(mean_prod / (sd / np.sqrt(n_cases))) if sd > 0 else 0.0

    sup_val = None
    sup_pass = None
    if n_cases > 1:
        med = float(np.median(fc))
        up = ex[fc > med]
        lo = ex[fc <= med]
        if len(up) > 0 and len(lo) > 0:
            sup_val = float(np.mean(up) - np.mean(lo))
            sup_pass = bool(sup_val > 0)
        else:
            sup_pass = False

    if n_cases < 100 or t_val is None:
        status = "not observable"
        decided = f"Only {n_cases} cases, below the plan's minimum of 100 cases."
    elif t_val >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main measure's t is 2 or more and the upper half minus lower half is above 0, on at least 100 cases."
    elif t_val <= -2:
        status = "rejected"
        decided = "The main measure's t is -2 or less, on at least 100 cases."
    elif t_val >= 2:
        status = "inconclusive"
        decided = "The main measure's t is 2 or more but the supporting check fails (upper half minus lower half not above 0)."
    else:
        status = "inconclusive"
        decided = "The main measure's t is between -2 and 2, on at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_prod,
            "statistic": {"name": "t of the mean", "value": t_val} if t_val is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 24-bar return, upper half minus lower half at the median forecast",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases},
        "decided_by": decided,
        "reading": "Settlement bars are those whose close (start + 1 hour) is at 00:00 or 16:00 UTC, a case is the first bet (forecast rise of at least 2) on a settlement bar in each 24-row grid cell of a window, the coin mean is over non-overlapping 24-bar returns at rows 0, 24, ... of all windows, and the upper half is forecasts strictly above the median, the lower half at or below it.",
    }
