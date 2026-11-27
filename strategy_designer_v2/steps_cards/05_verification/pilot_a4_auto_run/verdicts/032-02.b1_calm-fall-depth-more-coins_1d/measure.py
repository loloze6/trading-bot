import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    LHV = "debug_info.components.depth_below_high.last_history_value"
    PPV = "debug_info.components.depth_below_high.post_pipeline_value"

    # ---------- 1. Situation check ----------
    # The situation is a falling calm profile (regime 'unknown', the one regime not vetoed to chop)
    # with the close below its 30-day closing high (raw depth < 0). The expected side is short.
    n_active = 0
    n_ok = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            active = fc != 0
            n_active += int(active.sum())
            if LHV in df.columns:
                depth = pd.to_numeric(df[LHV], errors="coerce")
            else:
                depth = pd.Series(np.nan, index=df.index)
            reg = df["regime"].astype(str)
            situ = (reg == "unknown") & (depth < 0)
            ok = active & situ & (fc < 0)
            n_ok += int(ok.sum())
    agreement = float(n_ok / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    main_name = "clustered-by-day LS slope of coin excess 3-bar return on post_pipeline_value"
    threshold = "confirm if slope t >= 2 and mean short-direction unusual move > 0; reject if slope t <= -2"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "active bars in situation on short side": int(n_ok)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars of the falling calm "
                           "profile with the close below its 30-day closing high; the config does not do what the "
                           "plan's situation and side say."),
            "reading": "The profile is read from the recorded regime ('unknown' = not vetoed to chop) and the depth from last_history_value < 0.",
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        coin_all_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            ppv = (pd.to_numeric(df[PPV], errors="coerce").values
                   if PPV in df.columns else np.full(len(df), np.nan))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                r = c1 / c0 - 1.0
                coin_all_rets.append(r)
                if fc[i] != 0 and np.isfinite(ppv[i]):
                    coin_cases.append((r, ppv[i], ts.iloc[i].normalize()))
        if len(coin_all_rets) == 0:
            continue
        drift = float(np.mean(coin_all_rets))
        for r, x, day in coin_cases:
            rows.append({"coin": coin, "y": r - drift, "x": x, "day": day,
                         "unusual_short": -(r - drift)})

    cases = pd.DataFrame(rows, columns=["coin", "y", "x", "day", "unusual_short"])
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0
    counts = {"grid cases": n_cases, "distinct days": n_days}

    slope = None
    t_slope = None
    mean_unusual = None
    if n_cases >= 3:
        x = cases["x"].values.astype(float)
        y = cases["y"].values.astype(float)
        xd = x - x.mean()
        sxx = float(np.sum(xd ** 2))
        if sxx > 0:
            b = float(np.sum(xd * (y - y.mean())) / sxx)
            a = y.mean() - b * x.mean()
            e = y - a - b * x
            score = pd.Series(xd * e).groupby(cases["day"].values).sum().values
            G = len(score)
            if G > 1:
                var_b = (G / (G - 1.0)) * float(np.sum(score ** 2)) / sxx ** 2
                if var_b > 0:
                    t_slope = float(b / np.sqrt(var_b))
            slope = b
        mean_unusual = float(cases["unusual_short"].mean())

    support_pass = None if mean_unusual is None else bool(mean_unusual > 0)

    if n_cases < 100 or n_days < 30:
        status = "not observable"
        decided_by = (f"The plan's minimum of 100 grid cases over 30 distinct days is not reached "
                      f"({n_cases} cases over {n_days} days).")
    elif t_slope is None:
        status = "inconclusive"
        decided_by = "The slope t could not be computed, so neither the confirm nor the reject rule is met."
    elif t_slope >= 2 and support_pass:
        status = "confirmed"
        decided_by = "The slope t is 2 or more and the mean short-direction unusual move is above 0."
    elif t_slope <= -2:
        status = "rejected"
        decided_by = "The slope t is -2 or less: deeper falls are followed by relatively higher returns."
    elif t_slope >= 2:
        status = "inconclusive"
        decided_by = "The slope t is 2 or more but the mean short-direction unusual move is at or below 0."
    else:
        status = "inconclusive"
        decided_by = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": slope,
            "statistic": None if t_slope is None else {"name": "slope t, clustered by day", "value": t_slope},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean short-direction unusual 3-bar move",
            "value": mean_unusual,
            "passed": support_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Grid bars are positions 0,3,6,... of each window with a full 3-bar return inside the window; "
                    "the coin's mean 3-bar return (the drift) is taken over all its grid bars in all windows; "
                    "the slope t uses a day-clustered (UTC date) sandwich standard error with a G/(G-1) correction; "
                    "the profile is read from the recorded regime and the depth from last_history_value."),
    }
