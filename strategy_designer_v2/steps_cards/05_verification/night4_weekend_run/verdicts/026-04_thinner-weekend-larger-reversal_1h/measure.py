import numpy as np
import pandas as pd


def measure(bars):
    H = 48
    RAW = "debug_info.components.weekend_thin_move.last_history_value"

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        d["close"] = pd.to_numeric(d["close"], errors="coerce")
        d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
        return d

    # ---- normal 48-bar drift per coin: non-overlapping grid 0, H, 2H ... in each window
    data = {}
    drift = {}
    for coin, wins in bars.items():
        rets = []
        data[coin] = {}
        for w, df in wins.items():
            d = prep(df)
            data[coin][w] = d
            c = d["close"].values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                rets.extend(r[np.isfinite(r)].tolist())
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    # ---- situation check and case collection
    n_active = 0
    n_agree = 0
    xs, ys, ds = [], [], []
    n_signal_nonzero = 0
    for coin, wins in data.items():
        for w, d in wins.items():
            ts = d["timestamp"]
            c = d["close"].values
            f = d["forecast"].values
            n = len(d)
            # Sunday's last bar: a Sunday bar whose next bar (next row, or the hour after if last row)
            # starts on or after the following Monday 00:00
            nxt = ts.shift(-1)
            nxt = nxt.where(nxt.notna(), ts + pd.Timedelta(hours=1))
            monday0 = ts.dt.floor("D") + pd.Timedelta(days=1)
            situ = ((ts.dt.dayofweek == 6) & (nxt >= monday0)).values

            # the weekend move's sign: raw component value, else the 48-hour price return
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce").values
            else:
                raw = np.full(n, np.nan)
            s_close = pd.Series(c, index=ts)
            back = s_close.reindex(ts - pd.Timedelta(hours=H)).values
            pr = c / back - 1.0
            move = np.where(np.isfinite(raw), raw, pr)
            expected = -np.sign(move)

            active = f != 0
            n_active += int(active.sum())
            ok = active & situ & np.isfinite(move) & (np.sign(f) == expected) & (expected != 0)
            n_agree += int(ok.sum())

            # cases: Sunday's last bar with a nonzero forecast
            sig = situ & active
            for i in np.where(sig)[0]:
                n_signal_nonzero += 1
                if i + H < n and np.isfinite(c[i]) and np.isfinite(c[i + H]) and np.isfinite(drift[coin]):
                    r = c[i + H] / c[i] - 1.0
                    xs.append(float(f[i]))
                    ys.append(float(r - drift[coin]))
                    ds.append(float((r - drift[coin]) * np.sign(f[i])))

    reading = ("Signal bars are the Sunday bars whose next bar starts on or after Monday 00:00 UTC with a nonzero "
               "forecast; the 48-bar return is close[t+48]/close[t]-1 by row inside the window, the drift is the coin's "
               "mean 48-bar return on the non-overlapping grid of all its windows, the slope is OLS with an intercept, "
               "and the count of 300 is of signal bars with a nonzero forecast and a full 48-bar return.")
    thr = "t >= 2 confirms (with mean unusual move > 0), t <= -2 rejects, otherwise inconclusive; at least 300 signal bars"
    mm_name = "OLS slope of 48-bar return minus drift on forecast, signal bars pooled"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": {"name": "mean unusual move in signal direction > 0", "value": None, "passed": None},
            "counts": {"signal bars with a nonzero forecast": 0},
            "decided_by": "No bar has a nonzero forecast, so fewer than 300 signal bars with a nonzero forecast.",
            "reading": reading,
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mm_name, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars on the plan's situation and side": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a nonzero forecast are Sunday's last bar with a forecast "
                           "against the weekend's 48-bar move, as the plan's Fidelity requires."),
            "reading": reading,
        }

    x = np.array(xs)
    y = np.array(ys)
    n = len(x)
    counts = {"signal bars with a nonzero forecast": int(n),
              "signal bars with a nonzero forecast (before return availability)": int(n_signal_nonzero)}

    slope = None
    tval = None
    mean_dir = None
    if n >= 3 and np.var(x) > 0:
        xm = x - x.mean()
        slope = float((xm * (y - y.mean())).sum() / (xm ** 2).sum())
        intercept = y.mean() - slope * x.mean()
        resid = y - intercept - slope * x
        s2 = (resid ** 2).sum() / (n - 2)
        se = np.sqrt(s2 / (xm ** 2).sum())
        tval = float(slope / se) if se > 0 else None
    if n > 0:
        mean_dir = float(np.mean(ds))
    supp_pass = None if mean_dir is None else bool(mean_dir > 0)

    if n < 300:
        status = "not observable"
        decided = f"Only {n} signal bars with a nonzero forecast, fewer than the plan's minimum of 300."
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t cannot be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and supp_pass:
        status = "confirmed"
        decided = "The slope has t >= 2 and the mean unusual move in the signal's direction is above 0."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope has t >= 2 but the mean unusual move in the signal's direction is not above 0."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope has t <= -2: a thinner weekend's move is continued rather than reversed."
    else:
        status = "inconclusive"
        decided = "The slope's t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": mm_name,
                         "value": slope,
                         "statistic": None if tval is None else {"name": "OLS slope t", "value": tval},
                         "threshold": thr},
        "supporting_check": {"name": "mean unusual move in signal direction > 0",
                             "value": mean_dir, "passed": supp_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
