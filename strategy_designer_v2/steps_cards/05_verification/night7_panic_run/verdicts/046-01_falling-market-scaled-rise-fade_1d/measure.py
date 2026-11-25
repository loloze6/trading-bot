import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.scaled_rise.last_history_value"

    # ---------- collect per coin ----------
    coin_frames = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            d["close"] = pd.to_numeric(d["close"], errors="coerce")
            d["forecast"] = pd.to_numeric(d["forecast"], errors="coerce")
            d["ret1"] = d["close"].shift(-1) / d["close"] - 1.0      # next-day return, inside the window
            d["day_ret"] = d["close"] / d["close"].shift(1) - 1.0    # the bar's own return, inside the window
            d["coin"] = coin
            d["window"] = w
            if LHV in d.columns:
                d["lhv"] = pd.to_numeric(d[LHV], errors="coerce")
            else:
                d["lhv"] = np.nan
            coin_frames.setdefault(coin, []).append(d)

    all_rows = []
    for coin, frames in coin_frames.items():
        cdf = pd.concat(frames, ignore_index=True)
        mu = cdf["ret1"].dropna().mean()  # coin's mean daily return over all windows
        cdf["mu"] = mu
        all_rows.append(cdf)

    if not all_rows:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": True},
            "main_measure": {"name": "|forecast|-weighted mean next-day unusual move, short direction",
                             "value": None, "statistic": None,
                             "threshold": "confirm: > 0 with t >= 2 and positive slope; reject: < 0 with t <= -2"},
            "supporting_check": None,
            "counts": {"cases": 0, "case days": 0},
            "decided_by": "Fewer than 100 cases: the record holds no bars.",
            "reading": "none",
        }

    data = pd.concat(all_rows, ignore_index=True)

    # ---------- situation check ----------
    active = data[data["forecast"].notna() & (data["forecast"] != 0)].copy()
    n_active = len(active)
    if n_active > 0:
        falling = active["regime"].astype(str) == "unknown"
        rise_val = active["lhv"].where(active["lhv"].notna(), active["day_ret"])
        up_day = rise_val > 0
        short_side = active["forecast"] < 0
        agree = float((falling & up_day & short_side).mean())
        passed = agree >= 0.90
    else:
        agree = None
        passed = True

    reading = ("The falling profile is read from the recorded regime (the detector's decision: 'unknown' = "
               "60-bar price change below -10, the only regime with a strategy) since the detector's component "
               "is not recorded, the up day is a positive raw scaled_rise value (the bar's own in-window return "
               "where it is missing), the 100-case minimum counts coin-bar cases with forecast < 0 and a next-day "
               "return, and the day-clustered t sums each day's weighted deviations w*(u - mean) over sum(w).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agree, "passed": False},
            "main_measure": {"name": "|forecast|-weighted mean next-day unusual move, short direction",
                             "value": None, "statistic": None,
                             "threshold": "confirm: > 0 with t >= 2 and positive slope; reject: < 0 with t <= -2"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agree:.1%} of active bars are short positions on up days in the falling "
                           "profile; the plan's situation and the config's forecast disagree (below 90 %)."),
            "reading": reading,
        }

    # ---------- main measure ----------
    cases = data[(data["forecast"] < 0) & data["ret1"].notna()].copy()
    cases["excess"] = cases["ret1"] - cases["mu"]
    cases["u"] = -cases["excess"]           # short direction
    cases["w"] = cases["forecast"].abs()
    cases["day"] = cases["timestamp"].dt.floor("D")
    n_cases = int(len(cases))
    n_days = int(cases["day"].nunique()) if n_cases else 0

    threshold = "confirm: > 0 with t >= 2 and positive slope; reject: < 0 with t <= -2; else inconclusive"
    name = "|forecast|-weighted mean next-day unusual move, short direction"

    value = None
    tval = None
    slope = None
    if n_cases > 0 and cases["w"].sum() > 0:
        W = cases["w"].sum()
        m = float((cases["w"] * cases["u"]).sum() / W)
        value = m
        dev = cases["w"] * (cases["u"] - m)
        D = dev.groupby(cases["day"]).sum().values
        G = len(D)
        if G > 1:
            se = np.sqrt((D ** 2).sum() * G / (G - 1)) / W
            tval = float(m / se) if se > 0 else None
        if n_cases > 2 and cases["forecast"].nunique() > 1:
            lr = stats.linregress(cases["forecast"].values, cases["excess"].values)
            slope = float(lr.slope)

    slope_pass = None if slope is None else bool(slope > 0)
    counts = {"cases": n_cases, "case days": n_days}

    if n_cases < 100:
        status = "not observable"
        decided_by = f"Fewer than 100 cases ({n_cases}): too few to judge."
    elif value is None or tval is None:
        status = "inconclusive"
        decided_by = "The t of the weighted mean could not be computed, so neither confirm nor reject is met."
    elif value > 0 and tval >= 2 and slope_pass:
        status = "confirmed"
        decided_by = "The weighted mean unusual move is above 0 with t >= 2 and the supporting slope is positive."
    elif value < 0 and tval <= -2:
        status = "rejected"
        decided_by = "The weighted mean unusual move is below 0 with t <= -2."
    elif value > 0 and tval >= 2:
        status = "inconclusive"
        decided_by = "A main t >= 2 with a slope that is zero or negative is inconclusive."
    else:
        status = "inconclusive"
        decided_by = "The main t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agree, "passed": bool(passed)},
        "main_measure": {
            "name": name,
            "value": value,
            "statistic": None if tval is None else {"name": "t of the weighted mean, cases of one day summed",
                                                    "value": tval},
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "slope of next-day excess return on forecast over the cases",
            "value": slope,
            "passed": slope_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": reading,
    }
