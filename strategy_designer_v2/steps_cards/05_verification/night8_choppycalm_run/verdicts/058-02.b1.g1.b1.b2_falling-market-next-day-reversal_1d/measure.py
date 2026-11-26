import numpy as np
import pandas as pd


def measure(bars):
    LHV = "debug_info.components.fade_move.last_history_value"
    PPV = "debug_info.components.fade_move.post_pipeline_value"
    POS = "postRebalance_current_allocation"

    # ---------- per coin: next-day returns inside each window, coin mean daily return over all windows ----------
    frames = []
    for coin, wins in bars.items():
        coin_frames = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            d["next_ret"] = close.shift(-1) / close - 1.0  # inside this window only
            d["coin"] = coin
            d["window"] = w
            for c in (LHV, PPV, "forecast", POS):
                if c not in d.columns:
                    d[c] = np.nan
                d[c] = pd.to_numeric(d[c], errors="coerce")
            if "regime" not in d.columns:
                d["regime"] = None
            coin_frames.append(d[["timestamp", "coin", "window", "close", "forecast",
                                  "regime", LHV, PPV, POS, "next_ret"]])
        if not coin_frames:
            continue
        cf = pd.concat(coin_frames, ignore_index=True)
        mu = cf["next_ret"].dropna().mean()
        cf["coin_mu"] = mu if np.isfinite(mu) else np.nan
        frames.append(cf)

    if not frames:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "t of mean daily sum of forecast x (next-day return - coin mean)",
                             "value": None, "statistic": None, "threshold": "t >= 2 confirm, t <= -2 reject"},
            "supporting_check": None,
            "counts": {"distinct days carrying a nonzero forecast": 0},
            "decided_by": "No bars in the record.",
            "reading": "none",
        }

    allb = pd.concat(frames, ignore_index=True)
    allb["day"] = allb["timestamp"].dt.floor("D")

    # ---------- 1. situation check ----------
    fc = allb["forecast"].fillna(0.0)
    active = fc != 0
    n_active = int(active.sum())
    reg = allb["regime"].astype(str).str.lower()
    in_profile = (reg != "chop") & allb[LHV].notna()  # falling profile: the veto (60-bar change >= -10 -> chop) not hit
    raw = allb[LHV]
    expected_side = -np.sign(raw)  # fade: short after a rise, long after a fall
    ok = active & in_profile & (raw != 0) & (np.sign(fc) == expected_side)
    agreement = float(ok.sum() / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "t of the mean over days of the cross-coin daily sum of forecast (post_pipeline_value) x (next-day return - coin mean daily return)"
    threshold = "confirm if t >= 2 and timing part > 0; reject if t <= -2; otherwise inconclusive; at least 200 distinct days with a nonzero forecast"
    reading = ("The falling profile is read from the recorded regime (not 'chop', the config's veto of a 60-bar change >= -10) with the component recorded; "
               "a bar's evidence and book gain are dated by its own bar's day; the 200-day minimum counts all distinct days with a nonzero forecast and, "
               "per the workflow, a shortfall gives 'not observable'; the book's daily return before costs is the mean over the coins present that day of "
               "position held x next-day return, and its market part the same with the coin's mean daily return.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": (f"Only {agreement:.1%} of the bars with a nonzero forecast are bars of the falling profile with the forecast "
                           "opposite in sign to the vol-scaled 1-day move, below the 90% required."),
            "reading": reading,
        }

    # ---------- 2. main measure ----------
    act = allb[active].copy()
    n_days_forecast = int(act["day"].nunique())
    m = act.dropna(subset=[PPV, "next_ret", "coin_mu"]).copy()
    m["contrib"] = m[PPV] * (m["next_ret"] - m["coin_mu"])
    daily = m.groupby("day")["contrib"].sum()
    n_days_measure = int(len(daily))
    mean_daily = float(daily.mean()) if n_days_measure > 0 else None
    if n_days_measure >= 2 and daily.std(ddof=1) > 0:
        t_main = float(daily.mean() / (daily.std(ddof=1) / np.sqrt(n_days_measure)))
    else:
        t_main = None

    # ---------- supporting check: timing part of the book's mean daily return before costs ----------
    b = allb.dropna(subset=["next_ret", "coin_mu"]).copy()
    b[POS] = b[POS].fillna(0.0)
    b["gain"] = b[POS] * b["next_ret"]
    b["mkt"] = b[POS] * b["coin_mu"]
    book_daily = b.groupby("day")[["gain", "mkt"]].mean()
    if len(book_daily) > 0:
        book_mean = float(book_daily["gain"].mean())
        mkt_mean = float(book_daily["mkt"].mean())
        timing = book_mean - mkt_mean
    else:
        timing = None
    timing_pass = bool(timing is not None and timing > 0)

    counts = {
        "distinct days carrying a nonzero forecast": n_days_forecast,
        "days in the main measure": n_days_measure,
        "bars with a nonzero forecast": n_active,
    }

    if n_days_forecast < 200:
        status = "not observable"
        decided_by = f"Only {n_days_forecast} distinct days carry a nonzero forecast, below the plan's minimum of 200."
    elif t_main is None:
        status = "inconclusive"
        decided_by = "The t of the main measure could not be computed."
    elif t_main >= 2 and timing_pass:
        status = "confirmed"
        decided_by = f"The main measure's t is {t_main:.2f} (>= 2) and the timing part is above 0."
    elif t_main <= -2:
        status = "rejected"
        decided_by = f"The main measure's t is {t_main:.2f} (<= -2)."
    elif t_main >= 2:
        status = "inconclusive"
        decided_by = f"The main measure's t is {t_main:.2f} (>= 2) but the timing part is not above 0."
    else:
        status = "inconclusive"
        decided_by = f"The main measure's t is {t_main:.2f}, between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_daily,
            "statistic": ({"name": "t of the mean of daily sums", "value": t_main} if t_main is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book mean daily return before costs minus market-rise gain (timing part) > 0",
            "value": timing,
            "passed": timing_pass if timing is not None else None,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
