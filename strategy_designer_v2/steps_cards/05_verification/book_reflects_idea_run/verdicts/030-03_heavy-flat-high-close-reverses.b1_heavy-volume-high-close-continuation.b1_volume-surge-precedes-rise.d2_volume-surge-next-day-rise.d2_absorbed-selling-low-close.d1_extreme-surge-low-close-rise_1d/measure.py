import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    COMP = "debug_info.components.absorb_low.last_history_value"
    BAND = 2.0

    def raw_from_prices(df):
        vol = df["volume"].astype(float)
        base = vol.shift(1).rolling(20, min_periods=20).mean()
        ratio = vol / base
        rng = (df["high"] - df["low"]).astype(float)
        loc = (df["high"] - df["close"]).astype(float) / rng.replace(0.0, np.nan)
        return ratio * loc

    # ---------- situation check ----------
    n_active = 0
    n_agree = 0
    # ---------- case collection ----------
    case_rows = []  # (coin, forecast, next_ret)
    coin_rets = {}

    for coin, wins in bars.items():
        all_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float)
            nxt = close.shift(-1) / close - 1.0  # inside the window only
            all_rets.append(nxt.dropna().values)

            fc = pd.to_numeric(df["forecast"], errors="coerce")
            recomputed = raw_from_prices(df)
            if COMP in df.columns:
                raw = pd.to_numeric(df[COMP], errors="coerce")
                raw = raw.where(raw.notna(), recomputed)
            else:
                raw = recomputed

            # situation check on active bars
            active = fc.notna() & (fc != 0)
            n_active += int(active.sum())
            agree = active & (raw > 0) & (fc > 0)
            n_agree += int(agree.sum())

            # bets: rise of the forecast on the long side of at least the band,
            # from its lowest level on that side since the last bet (from 0 after flat/side change)
            ref = 0.0
            fvals = fc.values
            for i in range(len(df)):
                f = fvals[i]
                if not np.isfinite(f):
                    continue
                if f <= 0:
                    ref = 0.0
                    continue
                ref = min(ref, f)
                if f - ref >= BAND:
                    ref = f
                    r = nxt.iloc[i]
                    if np.isfinite(r):
                        case_rows.append((coin, float(f), float(r)))
        coin_rets[coin] = np.concatenate(all_rets) if all_rets else np.array([])

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed_sit = bool(n_active > 0 and agreement >= 0.90)

    main_name = "mean excess next-day return over bet bars (vs coin's mean daily return)"
    main_thr = "confirm: mean > 0 with t >= 2 over >= 100 cases; reject: mean < 0 with t <= -2 over >= 100 cases"
    sup_name = "top fifth by forecast minus other four fifths, mean excess return (Welch t > 0)"
    reading = ("Situation taken as the raw surge-times-low-close product being above 0 on a long (positive) forecast bar; "
               "cases are long bets (forecast rise >= 2 points from its lowest level since the last bet, from 0 after flat) with a next-day return inside the window; "
               "the top fifth is the floor(n/5) cases with the largest forecast (stable sort), the rest are the other four fifths.")

    if not passed_sit:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars where the surge-times-low-close "
                           "product is positive, so the config does not do what the plan's Fidelity says."),
            "reading": reading,
        }

    coin_mean = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in coin_rets.items()}
    fcs = []
    exc = []
    for coin, f, r in case_rows:
        m = coin_mean.get(coin, np.nan)
        if np.isfinite(m):
            fcs.append(f)
            exc.append(r - m)
    fcs = np.array(fcs, dtype=float)
    exc = np.array(exc, dtype=float)
    n = len(exc)

    mean_exc = float(np.mean(exc)) if n > 0 else None
    t_main = None
    if n >= 2:
        sd = float(np.std(exc, ddof=1))
        t_main = float(mean_exc / (sd / np.sqrt(n))) if sd > 0 else 0.0

    # supporting check
    sup_val = None
    sup_t = None
    sup_pass = None
    n_top = n // 5
    if n_top >= 2 and n - n_top >= 2:
        order = np.argsort(-fcs, kind="mergesort")
        top = exc[order[:n_top]]
        rest = exc[order[n_top:]]
        sup_val = float(np.mean(top) - np.mean(rest))
        tt = stats.ttest_ind(top, rest, equal_var=False)
        sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else 0.0
        sup_pass = bool(sup_t > 0)

    counts = {"cases": int(n), "top fifth cases": int(n_top), "other cases": int(n - n_top)}

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases (bets) were found, fewer than the plan's minimum of 100."
    elif mean_exc is not None and t_main is not None and mean_exc > 0 and t_main >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean excess next-day return is above 0 with t >= 2 over at least 100 cases, and the top fifth beats the other four fifths (Welch t > 0)."
        else:
            status = "inconclusive"
            decided = "The mean excess next-day return is above 0 with t >= 2, but the supporting check (top fifth vs other four fifths, Welch t > 0) fails."
    elif mean_exc is not None and t_main is not None and mean_exc < 0 and t_main <= -2:
        status = "rejected"
        decided = "The mean excess next-day return is below 0 with t <= -2 over at least 100 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean excess next-day return lies between -2 and 2 over at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_exc,
            "statistic": ({"name": "ordinary t of the mean", "value": t_main} if t_main is not None else None),
            "threshold": main_thr,
        },
        "supporting_check": {"name": sup_name, "value": sup_t, "passed": sup_pass,
                             "difference": sup_val},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
