import numpy as np
import pandas as pd
from scipy import stats

H = 48
VOL_SHORT = 48
VOL_LONG = 120
MIN_CASES = 100

F_COL = "forecast"
MOVE_RAW = "debug_info.components.move.last_history_value"


def _prep(df):
    d = df.copy()
    d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
    d = d.sort_values("timestamp").reset_index(drop=True)
    return d


def _situation(d):
    """Return arrays: is_sunday_23, gate (vr>1, or NaN if not computable), side (+1/-1/0/NaN)."""
    ts = d["timestamp"]
    sunday23 = ((ts.dt.dayofweek == 6) & (ts.dt.hour == 23)).to_numpy()
    close = d["close"].to_numpy(dtype=float)
    vol = d["volume"].to_numpy(dtype=float)
    n = len(d)
    gate = np.full(n, np.nan)
    side = np.full(n, np.nan)
    cs = np.concatenate([[0.0], np.nancumsum(np.nan_to_num(vol, nan=0.0))])
    for t in range(n):
        # volume ratio: mean of the last 48 bars (current included) over the mean of the 120 bars before them
        if t - VOL_SHORT - VOL_LONG + 1 >= 0:
            short_mean = (cs[t + 1] - cs[t + 1 - VOL_SHORT]) / VOL_SHORT
            lo = t + 1 - VOL_SHORT - VOL_LONG
            long_mean = (cs[t + 1 - VOL_SHORT] - cs[lo]) / VOL_LONG
            if long_mean > 0:
                gate[t] = 1.0 if short_mean > long_mean else 0.0
        # weekend move: 48-bar return to this close
        if t - H >= 0 and close[t - H] > 0:
            side[t] = np.sign(close[t] / close[t - H] - 1.0)
    # fallbacks where the record's history is too short
    if "regime" in d.columns:
        reg = (d["regime"].astype(str) == "trending").to_numpy()
        miss = np.isnan(gate)
        gate[miss] = reg[miss].astype(float)
    if MOVE_RAW in d.columns:
        mv = pd.to_numeric(d[MOVE_RAW], errors="coerce").to_numpy(dtype=float)
        miss = np.isnan(side) & ~np.isnan(mv)
        side[miss] = np.sign(mv[miss])
    return sunday23, gate, side


def measure(bars):
    reading = ("Situation bars are bars starting Sunday 23:00 UTC with the mean volume of the last 48 bars above "
               "that of the 120 bars before them and the side taken as the sign of the 48-bar close-to-close move "
               "(by row position within the window, falling back to the recorded regime and the move component's "
               "raw sign where the window's history is too short); cases are all Sunday 23:00 bars with a non-zero "
               "forecast and a close 48 rows later in the same window; the coin's mean 48-bar return is taken on "
               "the non-overlapping grid 0, 48, 96... of all its windows pooled; the top and bottom halves of "
               "|forecast| are the n//2 largest and n//2 smallest cases pooled over all coins (stable sort, "
               "middle case dropped when n is odd).")

    n_active = 0
    n_agree = 0
    case_vals = []
    case_absf = []

    for coin in sorted(bars.keys()):
        wins = bars[coin]
        preps = {}
        grid_rets = []
        for w in sorted(wins.keys()):
            d = _prep(wins[w])
            preps[w] = d
            c = d["close"].to_numpy(dtype=float)
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                r = r[np.isfinite(r)]
                grid_rets.extend(r.tolist())
        drift = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

        for w, d in preps.items():
            f = pd.to_numeric(d[F_COL], errors="coerce").to_numpy(dtype=float)
            sunday23, gate, side = _situation(d)
            active = np.isfinite(f) & (f != 0)
            n_active += int(active.sum())
            ok = active & sunday23 & (gate == 1.0) & (side == np.sign(f))
            n_agree += int(ok.sum())

            c = d["close"].to_numpy(dtype=float)
            for t in np.where(active & sunday23)[0]:
                if t + H >= len(c) or not np.isfinite(drift):
                    continue
                r = c[t + H] / c[t] - 1.0
                if not np.isfinite(r):
                    continue
                case_vals.append((r - drift) * np.sign(f[t]))
                case_absf.append(abs(f[t]))

    agreement = (n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "t of mean signed 48-bar return minus coin's mean 48-bar return, Sunday 23:00 cases"
    threshold = "t >= 2 over at least 100 cases confirms (with supporting check); t <= -2 over at least 100 cases rejects"
    sup_name = "mean signed unusual move, top half of |forecast| minus bottom half"

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": {"name": sup_name, "value": None, "passed": None},
            "counts": {"cases": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 100 cases is not reached.",
            "reading": reading,
        }

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active_bars": int(n_active), "agreeing_bars": int(n_agree)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are Sunday 23:00 bars with heavier "
                           "48-bar than prior 120-bar volume and a forecast on the side of the weekend's 48-bar move."),
            "reading": reading,
        }

    vals = np.asarray(case_vals, dtype=float)
    absf = np.asarray(case_absf, dtype=float)
    n = len(vals)

    mean_v = float(vals.mean()) if n > 0 else None
    t_v = None
    if n > 1:
        sd = vals.std(ddof=1)
        t_v = float(mean_v / (sd / np.sqrt(n))) if sd > 0 else None

    diff = None
    sup_pass = None
    if n >= 2:
        order = np.argsort(-absf, kind="mergesort")
        k = n // 2
        top = vals[order[:k]]
        bot = vals[order[n - k:]]
        diff = float(top.mean() - bot.mean())
        sup_pass = bool(diff > 0)

    main = {"name": main_name, "value": mean_v,
            "statistic": {"name": "t of the mean", "value": t_v} if t_v is not None else None,
            "threshold": threshold}
    sup = {"name": sup_name, "value": diff, "passed": sup_pass}
    counts = {"cases": int(n)}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} cases, below the plan's minimum of 100 cases."
    elif t_v is None:
        status = "inconclusive"
        decided = "The main t could not be computed (no spread), so neither the confirm nor the reject rule is met."
    elif t_v >= 2 and sup_pass:
        status = "confirmed"
        decided = "The main t is 2 or more over at least 100 cases and the top-minus-bottom difference is above 0."
    elif t_v >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more but the supporting difference is not above 0."
    elif t_v <= -2:
        status = "rejected"
        decided = "The main t is -2 or less over at least 100 cases: heavy-volume weekend moves are reversed."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2 over at least 100 cases."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": main,
        "supporting_check": sup,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
