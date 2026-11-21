import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    MOM = 28
    MIN_CASES = 200
    LHV = "debug_info.components.combo.last_history_value"

    def prep(df):
        d = df.copy()
        d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
        d = d.sort_values("timestamp").reset_index(drop=True)
        return d

    data = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            data[(coin, w)] = prep(df)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for (coin, w), d in data.items():
        close = d["close"].astype(float)
        mom = close / close.shift(MOM) - 1.0          # inside the window only
        reg_trend = d["regime"].astype(str) == "trending"
        # 28-day change from prices where the window has 28 past bars, else the recorded regime decision
        trend = pd.Series(np.where(mom.notna(), mom > 0, reg_trend), index=d.index).astype(bool)
        fc = pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0)
        raw = pd.to_numeric(d[LHV], errors="coerce") if LHV in d.columns else pd.Series(np.nan, index=d.index)
        active = fc != 0
        side_ok = raw.notna() & (np.sign(raw) == np.sign(fc)) & (raw != 0)
        ok = active & trend & side_ok
        n_active += int(active.sum())
        n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("Fewer than 90% of the active bars are bars where the 28-day return is above zero "
                           "with the forecast on the side of the past-predictive-power composite's sign"
                           if n_active > 0 else "The record has no active bar, so the config does not trade the plan's situation"),
            "reading": "The situation is the 28-day close-to-close change above zero (from prices, or the recorded regime "
                       "where a window lacks 28 past bars) and the expected side is the sign of the composite's raw value.",
        }

    # ---------- 2. main measure ----------
    # coin drift: mean 5-bar return on the non-overlapping grid of all its windows
    grid_rows = []
    for (coin, w), d in data.items():
        close = d["close"].astype(float).values
        n = len(d)
        for p in range(0, n, H):
            if p + H < n:
                r = close[p + H] / close[p] - 1.0
                fc = d["forecast"].iloc[p]
                grid_rows.append((coin, r, str(d["regime"].iloc[p]),
                                  float(fc) if pd.notna(fc) else np.nan))
    g = pd.DataFrame(grid_rows, columns=["coin", "ret", "regime", "forecast"])
    drift = g.groupby("coin")["ret"].mean()
    s = g[(g["regime"] == "trending") & g["forecast"].notna() & (g["forecast"] != 0) & g["ret"].notna()].copy()
    s["excess"] = s["ret"] - s["coin"].map(drift)
    n_cases = int(len(s))

    slope = None
    t_slope = None
    if n_cases >= 3 and s["forecast"].nunique() > 1:
        lr = stats.linregress(s["forecast"].values, s["excess"].values)
        slope = float(lr.slope)
        t_slope = float(lr.slope / lr.stderr) if lr.stderr and lr.stderr > 0 else None

    # ---------- supporting check: timing part of the book ----------
    coin_daily = {}
    per_win = []
    for (coin, w), d in data.items():
        d2 = d.copy()
        d2["day"] = d2["timestamp"].dt.floor("D")
        last = d2.groupby("day").tail(1).set_index("day")
        cret = last["close"].astype(float).pct_change()
        coin_daily.setdefault(coin, []).append(cret.dropna())
        per_win.append((coin, last))
    coin_mean = {c: float(pd.concat(v).mean()) if len(v) and len(pd.concat(v)) else np.nan
                 for c, v in coin_daily.items()}
    rows = []
    for coin, last in per_win:
        val = pd.to_numeric(last["postRebalance_total_value"], errors="coerce")
        bret = val.pct_change()
        pos_prev = pd.to_numeric(last["postRebalance_current_allocation"], errors="coerce").shift(1)
        mkt = pos_prev * coin_mean[coin]
        tmp = pd.DataFrame({"book": bret, "mkt": mkt}).dropna()
        tmp["day"] = tmp.index
        rows.append(tmp)
    timing = None
    if rows:
        allr = pd.concat(rows, ignore_index=True)
        if len(allr):
            daily = allr.groupby("day")[["book", "mkt"]].mean()
            timing = float(daily["book"].mean() - daily["mkt"].mean())
    timing_pass = None if timing is None else bool(timing > 0)

    # ---------- decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping trending cases, fewer than the plan's minimum of 200."
    elif t_slope is None:
        status = "inconclusive"
        decided = "The slope's t could not be computed on the trending cases."
    elif t_slope >= 2:
        if timing_pass:
            status = "confirmed"
            decided = "The slope's t is 2 or more with at least 200 cases and the book's timing part is positive."
        else:
            status = "inconclusive"
            decided = "The slope's t is 2 or more but the book's timing part is 0 or below, which the plan calls inconclusive."
    elif t_slope <= -2:
        status = "rejected"
        decided = "The slope's t is -2 or less with at least 200 cases."
    else:
        status = "inconclusive"
        decided = "The slope's t is between -2 and 2 with at least 200 cases."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "slope of 5-bar forward return minus coin drift on forecast, trending grid bars",
            "value": slope,
            "statistic": {"name": "OLS t of the slope", "value": t_slope} if t_slope is not None else None,
            "threshold": "t >= 2 with at least 200 cases to confirm; t <= -2 with at least 200 cases to reject",
        },
        "supporting_check": {
            "name": "book mean daily return minus gain from market rise (timing part) > 0",
            "value": timing,
            "passed": timing_pass,
        },
        "counts": {"non-overlapping trending cases": n_cases},
        "decided_by": decided,
        "reading": ("The regression pools all coins' grid bars (positions 0,5,10,... of each window with a full 5-bar "
                    "return inside it) that are trending with non-zero forecast, the drift is each coin's mean 5-bar "
                    "return on that grid over all its windows, and the book's daily return is the change of "
                    "postRebalance_total_value between consecutive daily bars with the market gain taken as the "
                    "previous bar's held allocation times the coin's mean daily return."),
    }
