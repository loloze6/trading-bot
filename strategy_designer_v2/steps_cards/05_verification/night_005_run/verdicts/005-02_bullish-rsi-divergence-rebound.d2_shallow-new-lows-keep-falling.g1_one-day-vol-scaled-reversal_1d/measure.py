import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    FL = "debug_info.components.fall_low.last_history_value"
    RS = "debug_info.components.rise.last_history_value"

    # ---------- coin mean daily return over all windows ----------
    coin_mu = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            if len(c) > 1:
                r = c[1:] / c[:-1] - 1.0
                rets.append(r[np.isfinite(r)])
        allr = np.concatenate(rets) if rets else np.array([])
        coin_mu[coin] = float(np.mean(allr)) if len(allr) else np.nan

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    prod_vals = []
    ex_pos = []
    ex_neg = []
    for coin, wins in bars.items():
        mu = coin_mu[coin]
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            fl = (pd.to_numeric(df[FL], errors="coerce").to_numpy(dtype=float)
                  if FL in df.columns else np.full(n, np.nan))
            rs = (pd.to_numeric(df[RS], errors="coerce").to_numpy(dtype=float)
                  if RS in df.columns else np.full(n, np.nan))
            prev_ret = np.full(n, np.nan)
            if n > 1:
                prev_ret[1:] = close[1:] / close[:-1] - 1.0

            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                n_active += 1
                # day direction: sign of the raw vol-scaled 1-day return, else the price return
                d = rs[i] if np.isfinite(rs[i]) else prev_ret[i]
                if not np.isfinite(d) or d == 0:
                    continue
                if d < 0:
                    # vol-scaled fall with close near the low -> long
                    in_sit = np.isfinite(fl[i]) and fl[i] != 0
                    expected = 1.0
                else:
                    # vol-scaled rise -> short
                    in_sit = True
                    expected = -1.0
                if in_sit and np.sign(f) == expected:
                    n_agree += 1

            # ---------- main measure inputs (1-bar, non-overlapping) ----------
            for i in range(n - 1):
                f = fc[i]
                if not (np.isfinite(f) and np.isfinite(close[i]) and np.isfinite(close[i + 1])
                        and np.isfinite(mu)):
                    continue
                ex = close[i + 1] / close[i] - 1.0 - mu
                if not np.isfinite(ex):
                    continue
                prod_vals.append(f * ex)
                if f > 0:
                    ex_pos.append(ex)
                elif f < 0:
                    ex_neg.append(ex)

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "mean of forecast[t] x next-day excess return over coin mean, pooled"
    threshold = "confirm t >= 2 with positive check; reject t <= -2"
    reading = ("Down/up day is taken from the sign of the raw vol-scaled 1-day return (price return if missing), "
               "the long situation also requires a non-zero raw fall_low value; the main mean includes every bar "
               "with a next bar in its window (zero forecasts included), and the minimum counts are the bars with a "
               "non-zero forecast and a next-day return, by forecast sign.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the non-zero-forecast bars are long on vol-scaled falls with "
                           "the close near the low or short on vol-scaled rises, below the 90% required."),
            "reading": reading,
        }

    x = np.asarray(prod_vals, dtype=float)
    n_all = len(x)
    if n_all > 1:
        m = float(np.mean(x))
        sd = float(np.std(x, ddof=1))
        t = float(m / (sd / np.sqrt(n_all))) if sd > 0 else 0.0
    else:
        m, t = (float(x[0]) if n_all == 1 else None), None

    n_pos, n_neg = len(ex_pos), len(ex_neg)
    n_nonzero = n_pos + n_neg
    if n_pos > 0 and n_neg > 0:
        check_val = float(np.mean(ex_pos) - np.mean(ex_neg))
        check_pass = bool(check_val > 0)
    else:
        check_val, check_pass = None, None

    counts = {
        "bars_measured": int(n_all),
        "bars_nonzero_forecast": int(n_nonzero),
        "bars_forecast_positive": int(n_pos),
        "bars_forecast_negative": int(n_neg),
    }

    if n_nonzero < 1000 or n_pos < 300 or n_neg < 300 or t is None:
        status = "not observable"
        decided_by = (f"Minimum counts not reached: {n_nonzero} non-zero-forecast bars (need 1000), "
                      f"{n_pos} long and {n_neg} short (need 300 each).")
    elif t >= 2 and check_pass:
        status = "confirmed"
        decided_by = "The main measure has t >= 2 and the supporting check is positive."
    elif t <= -2:
        status = "rejected"
        decided_by = "The main measure has t <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided_by = "The main measure has t >= 2 but the supporting check is not positive."
    else:
        status = "inconclusive"
        decided_by = "The main measure's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": m,
            "statistic": ({"name": "t of the mean", "value": t} if t is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean next-day excess return, forecast>0 minus forecast<0",
            "value": check_val,
            "passed": check_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
