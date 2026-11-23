import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 3
    MIN_CASES = 200
    comp_col = "debug_info.components.sunday_fade.last_history_value"

    # ---------- per-coin normal drift and usual 3-bar move (non-overlapping grid, all windows pooled) ----------
    coin_stats = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] > 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        rets = np.asarray(rets, dtype=float)
        if len(rets) >= 2:
            coin_stats[coin] = (float(np.mean(rets)), float(np.std(rets, ddof=1)))
        elif len(rets) == 1:
            coin_stats[coin] = (float(rets[0]), np.nan)
        else:
            coin_stats[coin] = (np.nan, np.nan)

    # ---------- situation check and case collection ----------
    n_active = 0
    n_agree = 0
    cases = []  # (gain, strength, volume_factor)
    for coin, wins in bars.items():
        mean3, sd3 = coin_stats[coin]
        for w, df in wins.items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(d["timestamp"], utc=True)
            close = d["close"].astype(float)
            vol = d["volume"].astype(float)
            fc = d["forecast"].astype(float).fillna(0.0)
            ret1 = close / close.shift(1) - 1.0
            raw = d[comp_col].astype(float) if comp_col in d.columns else pd.Series(np.nan, index=d.index)
            move_sign = np.sign(ret1)
            move_sign = move_sign.where(ret1.notna(), np.sign(raw))
            r3 = close.shift(-H) / close - 1.0
            base = vol.shift(2).rolling(20, min_periods=20).mean()      # bars t-21 .. t-2
            weekend = vol.rolling(2, min_periods=2).mean()              # Saturday and Sunday
            vfac = base / weekend.replace(0.0, np.nan)
            is_sunday = (ts.dt.dayofweek == 6).values

            for i in range(len(d)):
                f = fc.iloc[i]
                if f == 0 or not np.isfinite(f):
                    continue
                n_active += 1
                ms = move_sign.iloc[i]
                if is_sunday[i] and np.isfinite(ms) and ms != 0 and np.sign(f) == -ms:
                    n_agree += 1
                if not is_sunday[i]:
                    continue
                rr = r3.iloc[i]
                if not np.isfinite(rr) or not np.isfinite(mean3):
                    continue
                gain = f / 10.0 * (rr - mean3)
                strength = np.nan
                if np.isfinite(sd3) and sd3 > 0:
                    strength = np.sign(f) * (rr - mean3) / sd3
                cases.append((gain, strength, vfac.iloc[i]))

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean of forecast/10 x (3-bar return minus coin mean 3-bar return) on Sunday cases",
                             "value": None, "statistic": None, "threshold": "t >= 2 confirms, t <= -2 rejects, over at least 200 cases"},
            "supporting_check": None,
            "counts": {"cases": 0},
            "decided_by": "No bar has a non-zero forecast, so the minimum of 200 cases is not reached.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active_bars": int(n_active)},
            "decided_by": "Fewer than 90 % of the bars with a non-zero forecast are Sunday bars faded against the Sunday close-to-close move, as the plan's situation and side require.",
            "reading": "Sunday bars are those whose UTC start timestamp falls on a Sunday; the move's sign is the price return close[t]/close[t-1]-1, or the recorded component's sign on a window's first bar.",
        }

    # ---------- main measure ----------
    gains = np.array([c[0] for c in cases], dtype=float)
    n = len(gains)
    mean_gain = float(np.mean(gains)) if n > 0 else None
    t_main = None
    if n >= 2:
        sd = np.std(gains, ddof=1)
        t_main = float(mean_gain / (sd / np.sqrt(n))) if sd > 0 else None

    # ---------- supporting check ----------
    sup = [(c[1], c[2]) for c in cases if np.isfinite(c[1]) and np.isfinite(c[2])]
    t_sup = None
    sup_passed = None
    n_thin = n_heavy = 0
    if len(sup) > 0:
        s = np.array([x[0] for x in sup])
        v = np.array([x[1] for x in sup])
        med = np.median(v)
        thin = s[v > med]
        heavy = s[v <= med]
        n_thin, n_heavy = len(thin), len(heavy)
        if n_thin >= 2 and n_heavy >= 2:
            tt = stats.ttest_ind(thin, heavy, equal_var=False).statistic
            if np.isfinite(tt):
                t_sup = float(tt)
                sup_passed = bool(t_sup >= 1.0)
    sup_ok = bool(sup_passed) if sup_passed is not None else False

    # ---------- decision ----------
    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} Sunday cases with a non-zero forecast, below the plan's minimum of 200 cases."
    elif t_main is None:
        status = "inconclusive"
        decided = "The main t could not be computed (no spread in the gains), which meets neither the confirm nor the reject rule."
    elif t_main >= 2 and sup_ok:
        status = "confirmed"
        decided = "The main t is 2 or more over at least 200 cases and the thin-minus-heavy Welch t is 1 or more."
    elif t_main >= 2:
        status = "inconclusive"
        decided = "The main t is 2 or more but the thin-minus-heavy Welch t is below 1 (or could not be computed), which the plan calls inconclusive."
    elif t_main <= -2:
        status = "rejected"
        decided = "The main t is -2 or less over at least 200 cases: Sunday moves continue rather than fade."
    else:
        status = "inconclusive"
        decided = "The main t lies between -2 and 2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": "mean of forecast/10 x (3-bar return minus coin mean 3-bar return) on Sunday cases",
            "value": mean_gain,
            "statistic": {"name": "ordinary t of the mean", "value": t_main} if t_main is not None else None,
            "threshold": "t >= 2 confirms (with the supporting check), t <= -2 rejects, over at least 200 cases",
        },
        "supporting_check": {
            "name": "thin minus heavy weekend-volume half, strength (fade-direction unusual 3-bar move / usual 3-bar move), Welch t >= 1",
            "value": t_sup,
            "passed": sup_passed,
        },
        "counts": {"cases": int(n), "thin_half": int(n_thin), "heavy_half": int(n_heavy)},
        "decided_by": decided,
        "reading": ("Cases are bars starting on a UTC Sunday with a non-zero forecast and a full 3-bar return inside the window; "
                    "the coin's mean and usual 3-bar move come from the non-overlapping grid 0,3,6,... of each window pooled over its windows; "
                    "the volume factor is the mean volume of bars t-21..t-2 over the mean of bars t-1 and t, thin half above the pooled median and heavy half at or below it; "
                    "the fade direction is the forecast's sign."),
    }
