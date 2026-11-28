import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.heavy_up.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            if FC not in df.columns or len(df) == 0:
                continue
            fc = pd.to_numeric(df[FC], errors="coerce").fillna(0.0).values
            vol = pd.to_numeric(df["volume"], errors="coerce")
            close = pd.to_numeric(df["close"], errors="coerce")
            # mean volume of the last 3 bars vs mean of the 20 bars before them
            short_m = vol.rolling(3, min_periods=3).mean()
            prior_m = vol.shift(3).rolling(20, min_periods=20).mean()
            vratio = (short_m / prior_m).values
            ret3 = (close / close.shift(3) - 1.0).values
            regime = df["regime"].astype(str).values if "regime" in df.columns else np.array([""] * len(df))
            raw = pd.to_numeric(df[RAW], errors="coerce").values if RAW in df.columns else np.full(len(df), np.nan)
            for i in range(len(df)):
                if fc[i] == 0:
                    continue
                n_active += 1
                in_trend = regime[i] == "trending"
                # heavy recent volume: from prices, else the recorded regime
                if np.isfinite(vratio[i]):
                    heavy = vratio[i] > 1.0
                else:
                    heavy = in_trend
                # the 3 days rose: from prices, else the recorded raw component
                if np.isfinite(ret3[i]):
                    rose = ret3[i] > 0
                elif np.isfinite(raw[i]):
                    rose = raw[i] > 0
                else:
                    rose = False
                # falling-calm profile: only the regime (not vetoed to chop) can show it
                profile_ok = in_trend
                if heavy and rose and profile_ok and fc[i] > 0:
                    n_agree += 1
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    reading = ("Heavy volume is the mean of bars t-2..t over the mean of bars t-22..t-3 recomputed from the "
               "window's volumes (the recorded regime where fewer bars exist), the rise is close[t]/close[t-3]-1>0, "
               "and the falling-calm profile (60-bar fall, 365-bar volatility percentile) is read from the regime "
               "being 'trending' since it cannot be rebuilt from the recorded bars; the median split puts cases "
               "above the median forecast in the upper half and the rest in the lower half, halves compared "
               "unweighted; the t is the forecast-weighted mean over its day-clustered standard error.")

    main_name = "forecast-weighted mean excess 5-day return of forecast>0 grid bars"
    thr = "confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2; fewer than 30 cases inconclusive"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": 0},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are long bars inside heavy 3-day "
                           "volume after a 3-day rise in the falling-calm profile (agreement %.3f)." % agreement),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = pd.to_numeric(df["close"], errors="coerce").values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    cases = []  # (day, forecast, excess)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            for i in range(0, len(df), H):
                if i + H >= len(df):
                    break
                if not (np.isfinite(fc[i]) and fc[i] > 0):
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0):
                    continue
                if not np.isfinite(coin_mean[coin]):
                    continue
                r = c[i + H] / c[i] - 1.0
                cases.append((ts.iloc[i].floor("D"), float(fc[i]), r - coin_mean[coin]))

    n = len(cases)
    days = sorted(set(x[0] for x in cases))
    n_days = len(days)
    counts = {"cases": int(n), "days": int(n_days), "active bars": int(n_active)}

    mean_w = None
    t = None
    supp_val = None
    supp_pass = None
    if n > 0:
        wts = np.array([x[1] for x in cases])
        ex = np.array([x[2] for x in cases])
        mean_w = float(np.sum(wts * ex) / np.sum(wts))
        dev = pd.Series(wts * (ex - mean_w), index=[x[0] for x in cases]).groupby(level=0).sum().values
        J = len(dev)
        if J > 1:
            se = np.sqrt(np.sum(dev ** 2) * J / (J - 1)) / np.sum(wts)
            t = float(mean_w / se) if se > 0 else None
        med = float(np.median(wts))
        up = ex[wts > med]
        lo = ex[wts <= med]
        if len(up) > 0 and len(lo) > 0:
            supp_val = float(np.mean(up) - np.mean(lo))
            supp_pass = bool(supp_val > 0)
        else:
            supp_pass = False

    if n < 30:
        status = "not observable"
        decided = "The plan's minimum of 30 cases is not reached (%d cases)." % n
    elif t is None:
        status = "inconclusive"
        decided = "The t of the weighted mean excess return cannot be computed, so it does not meet the confirm or reject rule."
    elif mean_w > 0 and t >= 2:
        if supp_pass:
            status = "confirmed"
            decided = "The weighted mean excess return is above 0 with t >= 2 and the upper-minus-lower median split is above 0."
        else:
            status = "inconclusive"
            decided = "The weighted mean excess return is above 0 with t >= 2 but the supporting check fails: a confirming t with a failed check is inconclusive."
    elif mean_w < 0 and t <= -2:
        status = "rejected"
        decided = "The weighted mean excess return is below 0 with t <= -2."
    else:
        status = "inconclusive"
        decided = "The t of the weighted mean excess return lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": mean_w,
            "statistic": ({"name": "t of the weighted mean, cases of one day grouped", "value": t} if t is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "mean excess 5-day return, upper minus lower half at median forecast",
            "value": supp_val,
            "passed": supp_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
