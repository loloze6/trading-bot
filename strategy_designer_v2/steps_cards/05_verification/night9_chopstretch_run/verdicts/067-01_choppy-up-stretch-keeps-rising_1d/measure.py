import numpy as np
import pandas as pd


def measure(bars):
    H = 10
    SCOL = "debug_info.components.stretch.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            if "forecast" not in d.columns:
                continue
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            close = pd.to_numeric(d["close"], errors="coerce")
            sma = close.rolling(20, min_periods=20).mean()
            price_sign = np.sign(close - sma)
            if SCOL in d.columns:
                raw = pd.to_numeric(d[SCOL], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=d.index)
            stretch_sign = np.sign(raw).where(raw.notna(), price_sign)
            regime = d["regime"].astype(str) if "regime" in d.columns else pd.Series("unknown", index=d.index)
            choppy = regime.str.lower() != "chop"
            active = fc.notna() & (fc != 0)
            agree = active & choppy & stretch_sign.notna() & (stretch_sign == np.sign(fc)) & (stretch_sign != 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    reading = ("Choppy bars are bars whose recorded regime is not the veto regime 'chop' (the profile's "
               "trend gate, whose component is not recorded); the stretch's side is the sign of the raw "
               "stretch, or of close minus its 20-bar SMA when the raw value is missing; the drift is the mean "
               "next-10-bar return over every grid bar of all the coin's windows; the slope t uses an OLS slope "
               "with a standard error clustered by date (residual-weighted deviations summed per date, G/(G-1) "
               "correction); the plan's 'fewer than 100 / 30' rule is treated as a minimum count (not observable).")
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "slope of 10-bar excess return on forecast", "value": None,
                             "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are choppy-profile bars where "
                           "the forecast's sign equals the sign of the close's stretch from its 20-day average."),
            "reading": reading,
        }

    # ---------- 2. grid cases ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_rows = []
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce").values
            fc = pd.to_numeric(d["forecast"], errors="coerce").values
            ts = pd.to_datetime(d["timestamp"], utc=True)
            n = len(d)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] != 0:
                    coin_rows.append((coin, ts.iloc[i].normalize(), float(fc[i]), r))
        if not grid_rets:
            continue
        drift = float(np.mean(grid_rets))
        for c, dt, f, r in coin_rows:
            rows.append({"coin": c, "date": dt, "x": f, "y": r - drift})

    cases = pd.DataFrame(rows, columns=["coin", "date", "x", "y"])
    n_total = int(len(cases))
    n_long = int((cases["x"] > 0).sum()) if n_total else 0
    n_short = int((cases["x"] < 0).sum()) if n_total else 0
    n_dates = int(cases["date"].nunique()) if n_total else 0
    counts = {"grid cases in total": n_total, "long cases": n_long, "short cases": n_short,
              "dates": n_dates}

    long_mean = float(cases.loc[cases["x"] > 0, "y"].mean()) if n_long else None
    short_mean = float((-cases.loc[cases["x"] < 0, "y"]).mean()) if n_short else None

    slope = None
    tval = None
    if n_total >= 3 and cases["x"].nunique() > 1:
        x = cases["x"].values
        y = cases["y"].values
        xm = x.mean()
        dx = x - xm
        sxx = float(np.sum(dx ** 2))
        slope = float(np.sum(dx * (y - y.mean())) / sxx)
        intercept = y.mean() - slope * xm
        e = y - intercept - slope * x
        sc = pd.Series(dx * e).groupby(cases["date"].values).sum().values
        G = len(sc)
        if G > 1:
            var = float(np.sum(sc ** 2)) / sxx ** 2 * G / (G - 1)
            if var > 0:
                tval = float(slope / np.sqrt(var))

    sup_pass = None
    if long_mean is not None and short_mean is not None:
        sup_pass = bool(long_mean > 0 and short_mean > 0)
    elif n_total:
        sup_pass = False

    main = {"name": "slope of 10-bar excess return on forecast (grid, active bars)",
            "value": slope,
            "statistic": {"name": "slope t, cases summed by date", "value": tval} if tval is not None else None,
            "threshold": "t >= 2 (with both sides' mean positive) confirms; t <= -2 rejects"}
    supporting = {"name": "mean excess return in forecast direction, long and short sides",
                  "value": min(long_mean, short_mean) if (long_mean is not None and short_mean is not None) else None,
                  "passed": sup_pass,
                  "long_mean": long_mean, "short_mean": short_mean}

    if n_total < 100 or n_long < 30 or n_short < 30:
        status = "not observable"
        decided = ("Minimum counts not reached: the plan needs at least 100 grid cases in total and 30 on "
                   "each side (got %d total, %d long, %d short)." % (n_total, n_long, n_short))
    elif tval is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed, so neither the confirm nor the reject rule is met."
    elif tval >= 2 and sup_pass:
        status = "confirmed"
        decided = "The slope's t is 2 or more and the mean excess return in the forecast's direction is positive on both sides."
    elif tval >= 2:
        status = "inconclusive"
        decided = "The slope's t is 2 or more but one side's mean excess return in the forecast's direction is not positive."
    elif tval <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less: larger stretches are followed by a return toward the average."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
