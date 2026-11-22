import numpy as np
import pandas as pd


def _ols(x, y):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    n = len(x)
    if n < 3:
        return None, None, None, n
    xm = x.mean()
    sxx = float(((x - xm) ** 2).sum())
    if sxx <= 0:
        return None, None, None, n
    b = float(((x - xm) * (y - y.mean())).sum() / sxx)
    a = y.mean() - b * xm
    resid = y - a - b * x
    s2 = float((resid ** 2).sum() / (n - 2))
    se = float(np.sqrt(s2 / sxx))
    t = b / se if se > 0 else None
    return b, se, t, n


def measure(bars):
    H = 48
    MIN_SUNDAY = 300
    raw_col = "debug_info.components.sunday_ret.last_history_value"

    n_active = 0
    n_agree = 0

    # coin mean 48-bar return on the non-overlapping grid of all its windows
    coin_mean = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].to_numpy(dtype=float)
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                rets.extend(list(r[np.isfinite(r)]))
        coin_mean[coin] = float(np.mean(rets)) if rets else np.nan

    main_x, main_y = [], []
    sun_x, sun_y = [], []
    oth_x, oth_y = [], []

    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            wd = ts.dt.weekday.to_numpy()
            hr = ts.dt.hour.to_numpy()
            c = df["close"].to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).to_numpy(dtype=float)
            n = len(df)
            if raw_col in df.columns:
                raw = pd.to_numeric(df[raw_col], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(n, np.nan)
            ret24 = np.full(n, np.nan)
            if n > 24:
                ret24[24:] = c[24:] / c[:-24] - 1.0
            ret48b = np.full(n, np.nan)
            if n > H:
                ret48b[H:] = c[H:] / c[:-H] - 1.0
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[:-H] = c[H:] / c[:-H] - 1.0

            sunday_bar = (wd == 6) & (hr == 23)  # close is Monday 00:00 UTC
            other_bar = (wd <= 5) & (hr == 23)   # close is 00:00 Tue..Sun

            # situation check
            sig_raw = np.where(np.isfinite(raw), raw, ret24)
            active = f != 0
            n_active += int(active.sum())
            agree = active & sunday_bar & np.isfinite(sig_raw) & (np.sign(f) == -np.sign(sig_raw)) & (sig_raw != 0)
            n_agree += int(agree.sum())

            # main measure cases
            cm = coin_mean.get(coin, np.nan)
            sel = sunday_bar & active & np.isfinite(fwd)
            for i in np.where(sel)[0]:
                main_x.append(f[i] / 10.0)
                main_y.append(fwd[i] - cm)
                if np.isfinite(ret24[i]):
                    sun_x.append(ret24[i])
                    sun_y.append(fwd[i])
            sel_o = other_bar & np.isfinite(fwd) & np.isfinite(ret48b)
            for i in np.where(sel_o)[0]:
                oth_x.append(ret48b[i])
                oth_y.append(fwd[i])

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "slope t of demeaned next-48-bar return on forecast/10",
                             "value": None, "statistic": None,
                             "threshold": "confirm slope > 0 with t >= 2; reject t <= -2"},
            "supporting_check": None,
            "counts": {"Sunday cases": 0},
            "decided_by": "No bar has a nonzero forecast, so the minimum of 300 Sunday cases is not reached.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "agreeing bars": int(n_agree)},
            "decided_by": "Fewer than 90% of nonzero-forecast bars are Sunday 23:00 UTC bars with a forecast opposite to Sunday's 24-bar return.",
            "reading": "Situation bars are those starting Sunday 23:00 UTC; the expected side is the opposite of the recorded raw 24-bar return (recomputed from closes where missing).",
        }

    b, se, t, n_main = _ols(main_x, main_y)
    bs, ses, ts_, ns = _ols(sun_x, sun_y)
    bo, seo, to_, no = _ols(oth_x, oth_y)
    diff = diff_t = None
    if bs is not None and bo is not None and ses is not None and seo is not None:
        diff = bs - bo
        den = np.sqrt(ses ** 2 + seo ** 2)
        diff_t = float(diff / den) if den > 0 else None

    sup_pass = (diff_t is not None and diff_t <= -2)
    counts = {"Sunday cases": int(n_main),
              "Sunday cases in supporting check": int(ns),
              "other weekday cases": int(no)}

    if n_main < MIN_SUNDAY or t is None:
        status = "not observable"
        decided = "Fewer than 300 Sunday cases across coins and windows (the plan's minimum)."
    elif t <= -2:
        status = "rejected"
        decided = "Main slope t <= -2: Sunday's move continues into the week."
    elif b > 0 and t >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "Main slope positive with t >= 2 and slope difference t <= -2."
        elif diff_t is not None and diff_t >= 2:
            status = "rejected"
            decided = "Main slope confirms but slope difference t >= 2: weekday returns of the same size reverse more."
        else:
            status = "inconclusive"
            decided = "Main slope confirms but the slope difference t is not <= -2 (between -2 and 2 or not computable)."
    else:
        status = "inconclusive"
        decided = "Main slope t between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "slope of next-48-bar return minus coin mean on forecast/10",
            "value": None if b is None else float(b),
            "statistic": None if t is None else {"name": "OLS slope t", "value": float(t)},
            "threshold": "confirm: slope > 0 with t >= 2 (and support passes); reject: t <= -2",
        },
        "supporting_check": {
            "name": "slope difference (Sunday 24h-return slope minus other-days 48h-return slope), t",
            "value": None if diff_t is None else float(diff_t),
            "passed": None if diff_t is None else bool(sup_pass),
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Sunday cases are bars starting Sunday 23:00 UTC with nonzero forecast and 48 later rows in the window, "
                    "the coin mean is over the non-overlapping 48-bar grid of all its windows, the supporting slopes use raw "
                    "(not demeaned) next-48-bar returns with returns recomputed from closes as fractions and other-day cases "
                    "at 23:00 bars Monday to Saturday, the slope-difference t is (b1-b2)/sqrt(se1^2+se2^2), and the plan's "
                    "300-case minimum yields 'not observable'."),
    }
