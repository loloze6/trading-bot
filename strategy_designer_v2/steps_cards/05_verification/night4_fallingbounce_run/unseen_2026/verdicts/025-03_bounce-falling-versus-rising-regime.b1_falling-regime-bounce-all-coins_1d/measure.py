import numpy as np
import pandas as pd
from scipy import stats

H = 5
BAND = 2.0
COMP = {
    "mean_reversion": "debug_info.components.rise_in_fall.last_history_value",
    "trending": "debug_info.components.rise_in_rise.last_history_value",
}


def _raw_rise(df):
    """Raw rise reading per bar: the active regime's component value, else the price's 1-bar return."""
    vals = pd.Series(np.nan, index=df.index, dtype=float)
    for col in COMP.values():
        if col in df.columns:
            v = pd.to_numeric(df[col], errors="coerce")
            vals = vals.where(vals.notna(), v)
    close = pd.to_numeric(df["close"], errors="coerce")
    r1 = close / close.shift(1) - 1.0
    return vals.where(vals.notna(), r1), vals


def _expected_side(df):
    """+1 long when the 90-bar return >= 0, -1 short when < 0; from prices if computable, else the regime."""
    close = pd.to_numeric(df["close"], errors="coerce")
    r90 = close / close.shift(90) - 1.0
    side = pd.Series(np.nan, index=df.index, dtype=float)
    side[r90 >= 0] = 1.0
    side[r90 < 0] = -1.0
    reg = df["regime"].astype(str)
    fb = pd.Series(np.nan, index=df.index, dtype=float)
    fb[reg == "trending"] = 1.0
    fb[reg == "mean_reversion"] = -1.0
    return side.where(side.notna(), fb)


def _bets(forecast):
    f = np.nan_to_num(np.asarray(forecast, dtype=float))
    out = np.zeros(len(f), dtype=bool)
    prev_side, trough = 0, 0.0
    for i, x in enumerate(f):
        s = int(np.sign(x))
        if s == 0:
            prev_side, trough = 0, 0.0
            continue
        if s != prev_side:
            trough = 0.0
            prev_side = s
        m = abs(x)
        if m - trough >= BAND:
            out[i] = True
            trough = m
        else:
            trough = min(trough, m)
    return out


def _welch(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    if len(a) < 2 or len(b) < 2:
        return None
    t = stats.ttest_ind(a, b, equal_var=False).statistic
    return None if not np.isfinite(t) else float(t)


def measure(bars):
    # ---------- situation check ----------
    n_active, n_agree = 0, 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            rise, _ = _raw_rise(df)
            side = _expected_side(df)
            act = fc != 0
            n_active += int(act.sum())
            ok = act & (rise > 0) & (np.sign(fc) == side)
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
            "decided_by": "Fewer than 90% of active bars are one-day rises traded short when the 90-day return is "
                          "negative and long when it is non-negative, as the Fidelity's situation requires.",
            "reading": "The 90-day return is recomputed from window prices where 90 past bars exist, otherwise the "
                       "recorded regime is used; the rise is the recorded component value (or the 1-bar return).",
        }

    # ---------- cases ----------
    rows = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            n = len(df)
            for p in range(0, n - H, H):
                r = close[p + H] / close[p] - 1.0
                if np.isfinite(r):
                    grid_rets.append(r)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            bets = _bets(fc)
            _, rec = _raw_rise(df)
            reg = df["regime"].astype(str).values
            seen = set()
            for i in np.where(bets)[0]:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                r = close[i + H] / close[i] - 1.0
                if not np.isfinite(r):
                    continue
                if reg[i] not in COMP:
                    continue
                coin_cases.append((reg[i], r, float(rec.iloc[i]) if pd.notna(rec.iloc[i]) else np.nan))
        drift = float(np.mean(grid_rets)) if grid_rets else np.nan
        if not np.isfinite(drift):
            continue
        for reg_i, r, lv in coin_cases:
            rows.append({"regime": reg_i, "unusual": r - drift, "lhv": lv})

    cases = pd.DataFrame(rows, columns=["regime", "unusual", "lhv"])
    mr = cases.loc[cases["regime"] == "mean_reversion", "unusual"].values
    tr = cases.loc[cases["regime"] == "trending", "unusual"].values
    n_mr, n_tr = int(len(mr)), int(len(tr))

    diff = float(np.mean(mr) - np.mean(tr)) if n_mr > 0 and n_tr > 0 else None
    t = _welch(mr, tr) if n_mr > 0 and n_tr > 0 else None

    sub = cases.dropna(subset=["lhv"])
    sup_val, sup_pass = None, None
    n_sub_mr = n_sub_tr = 0
    if len(sub) > 0:
        med = float(sub["lhv"].median())
        big = sub[sub["lhv"] > med]
        smr = big.loc[big["regime"] == "mean_reversion", "unusual"].values
        strn = big.loc[big["regime"] == "trending", "unusual"].values
        n_sub_mr, n_sub_tr = int(len(smr)), int(len(strn))
        if n_sub_mr > 0 and n_sub_tr > 0:
            sup_val = float(np.mean(smr) - np.mean(strn))
            if diff is not None:
                sup_pass = bool(sup_val < diff)
    if sup_pass is None and diff is not None:
        sup_pass = False

    counts = {
        "mean_reversion cases": n_mr,
        "trending cases": n_tr,
        "mean_reversion cases above median rise": n_sub_mr,
        "trending cases above median rise": n_sub_tr,
    }

    if n_mr < 30 or n_tr < 30 or t is None:
        status = "not observable"
        decided = "Fewer than 30 cases in at least one regime, the plan's minimum count."
    elif t <= -2 and sup_pass:
        status = "confirmed"
        decided = "Welch t <= -2 on the main difference and the above-median difference is more negative."
    elif t >= 2:
        status = "rejected"
        decided = "Welch t >= +2: bounces in falling markets are followed by higher 5-day returns than in rising markets."
    elif t <= -2:
        status = "inconclusive"
        decided = "Main Welch t <= -2 but the supporting check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "Main Welch t lies between -2 and +2, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean unusual 5-bar move, mean_reversion cases minus trending cases",
            "value": diff,
            "statistic": {"name": "Welch t", "value": t} if t is not None else None,
            "threshold": "confirm at Welch t <= -2 with the supporting check passing; reject at Welch t >= +2",
        },
        "supporting_check": {
            "name": "same difference on cases with rise reading above pooled median, more negative than main",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "The unusual move is the raw 5-bar return minus the coin's mean 5-bar grid return, not signed by "
                   "the bet's direction (the plan compares returns across regimes), the case's regime is the bar's "
                   "recorded regime, the first bet of each 5-bar grid cell is the case, and the plan's 30-case "
                   "minimum per regime is applied as 'not observable'.",
    }
