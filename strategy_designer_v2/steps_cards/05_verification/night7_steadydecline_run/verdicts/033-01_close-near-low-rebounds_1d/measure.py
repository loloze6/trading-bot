import numpy as np
import pandas as pd


def measure(bars):
    COMP = "debug_info.components.close_near_low.last_history_value"
    COMP_POST = "debug_info.components.close_near_low.post_pipeline_value"
    WIN, MINP = 60, 20

    # ---------- collect per-bar data, window by window (never joined) ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.sort_values("timestamp").reset_index(drop=True).copy()
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            high = pd.to_numeric(d["high"], errors="coerce")
            low = pd.to_numeric(d["low"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")

            # raw component: distance of close from the high as share of range (0 at high, 1 at low)
            rng = (high - low).replace(0, np.nan)
            raw_px = (high - close) / rng
            if COMP in d.columns:
                raw = pd.to_numeric(d[COMP], errors="coerce").where(lambda s: s.notna(), raw_px)
            else:
                raw = raw_px
            # usual level = mean of |raw| over the past 60 bars, bar t left out (standardise's divisor)
            usual = raw.abs().shift(1).rolling(WIN, min_periods=MINP).mean()
            std_val = np.where(usual > 0, np.clip(raw * 10.0 / usual, -20, 20), np.nan)
            std_val = pd.Series(std_val, index=d.index)
            # bars without enough in-window history: use the recorded standardised value
            if COMP_POST in d.columns:
                post = pd.to_numeric(d[COMP_POST], errors="coerce")
                std_val = std_val.where(std_val.notna(), post)

            r_next = close.shift(-1) / close - 1.0  # inside the window only

            rows.append(pd.DataFrame({
                "coin": coin, "window": w,
                "day": ts.dt.floor("D"),
                "forecast": fc, "std_val": std_val, "r_next": r_next,
            }))

    if not rows:
        return {"status": "not observable",
                "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None,
                "counts": {"distinct days of cases": 0},
                "decided_by": "No bars in the record.", "reading": "none"}

    allb = pd.concat(rows, ignore_index=True)

    # ---------- situation check ----------
    # Fidelity: close nearer the low than the coin's usual location -> long; nearer the high than usual -> short.
    active = allb[allb["forecast"].notna() & (allb["forecast"] != 0)]
    chk = active[active["std_val"].notna()]
    if len(chk) > 0:
        expected_side = np.sign(chk["std_val"].values - 10.0)
        agree = float(np.mean((expected_side != 0) & (expected_side == np.sign(chk["forecast"].values))))
    else:
        agree = 0.0
    passed = bool(agree >= 0.90)

    reading = ("The situation is rebuilt as the standardised close-from-high share (raw over the mean of its past 60 "
               "in-window raw values, recorded post-pipeline value where the window lacks history) above 10 for long "
               "and below 10 for short; the main measure's days are all calendar days with a bar that has a next-day "
               "return (zero-forecast bars add 0); 'days of cases' are distinct days holding a bar with non-zero "
               "forecast and a next-day return; excess return is the next-day return minus the coin's mean next-day "
               "return over all its windows; a minimum count not reached gives 'not observable'.")

    if not passed:
        return {"status": "mismatch",
                "situation_check": {"agreement": agree, "passed": False},
                "main_measure": None, "supporting_check": None,
                "counts": {"active bars checked": int(len(chk))},
                "decided_by": ("Fewer than 90 % of the non-zero-forecast bars are long when the close sits nearer the "
                               "low than its usual location (short when nearer the high), as the Fidelity requires."),
                "reading": reading}

    # ---------- criterion ----------
    v = allb[allb["r_next"].notna() & allb["forecast"].notna()].copy()
    mu = v.groupby("coin")["r_next"].mean()
    v["excess"] = v["r_next"] - v["coin"].map(mu)
    v["contrib"] = (v["forecast"] / 10.0) * v["excess"]

    daily = v.groupby("day")["contrib"].sum()
    n_days = int(len(daily))
    if n_days >= 2 and daily.std(ddof=1) > 0:
        mean_d = float(daily.mean())
        t = float(mean_d / (daily.std(ddof=1) / np.sqrt(n_days)))
    else:
        mean_d = float(daily.mean()) if n_days else None
        t = None

    case_days = int(v.loc[v["forecast"] != 0, "day"].nunique())

    hi = v.loc[v["forecast"] >= 2.5, "excess"]
    lo = v.loc[v["forecast"] <= -2.5, "excess"]
    if len(hi) > 0 and len(lo) > 0:
        diff = float(hi.mean() - lo.mean())
        check_pass = bool(diff > 0)
    else:
        diff, check_pass = None, False

    counts = {"distinct days of cases": case_days,
              "days in main measure": n_days,
              "bars with forecast >= +2.5": int(len(hi)),
              "bars with forecast <= -2.5": int(len(lo))}

    if case_days < 500:
        status = "not observable"
        decided = f"Only {case_days} distinct days of cases, below the plan's minimum of 500."
    elif t is None:
        status = "inconclusive"
        decided = "The main-measure t cannot be computed, so neither the confirm nor the reject rule is met."
    elif t >= 2 and check_pass:
        status = "confirmed"
        decided = "The main-measure t is >= 2 and the supporting check's difference is above 0."
    elif t <= -2:
        status = "rejected"
        decided = "The main-measure t is <= -2."
    elif t >= 2:
        status = "inconclusive"
        decided = "The main-measure t is >= 2 but the supporting check's difference is not above 0."
    else:
        status = "inconclusive"
        decided = "The main-measure t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agree, "passed": passed},
        "main_measure": {
            "name": "mean over days of the summed (forecast/10) x next-day excess return",
            "value": mean_d,
            "statistic": ({"name": "t of the mean over days", "value": t} if t is not None else None),
            "threshold": "confirm if t >= 2 (with check passing); reject if t <= -2; at least 500 distinct days of cases",
        },
        "supporting_check": {
            "name": "mean next-day excess return, forecast >= +2.5 minus forecast <= -2.5",
            "value": diff,
            "passed": check_pass if diff is not None else None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
