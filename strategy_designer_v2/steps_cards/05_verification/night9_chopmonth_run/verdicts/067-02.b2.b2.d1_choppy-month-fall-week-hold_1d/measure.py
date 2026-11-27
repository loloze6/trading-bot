import numpy as np
import pandas as pd


def measure(bars):
    H = 7
    LHV = "debug_info.components.month_fall.last_history_value"
    MIN_DAYS = 30
    MIN_HELD = 20

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            if LHV in df.columns:
                raw = pd.to_numeric(df[LHV], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            # situation: component recorded (choppy-profile regime active), 30-day return below 0; side: short
            situ = raw.notna() & (raw < 0)
            agree = active & situ & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are short bars where the recorded "
                           "30-day return is below 0 in the choppy profile (or no bar is active), so the config does "
                           "not do what the Fidelity says."),
            "reading": "The situation is read as: month_fall recorded (its choppy regime active) with raw 30-day return < 0, and the forecast negative.",
        }

    # ---------- 2. Main measure ----------
    drift = {}
    cases = []  # (day, x, weight)
    held_gains = []
    for coin, wins in bars.items():
        grid_rets = []
        coin_cases = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            fc = pd.to_numeric(df["forecast"], errors="coerce").values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 <= 0:
                    continue
                r = c1 / c0 - 1.0
                grid_rets.append(r)
                if np.isfinite(fc[i]) and fc[i] < 0:
                    coin_cases.append((ts.iloc[i].normalize(), r, abs(fc[i])))
            # supporting check: held short while forecast is 0
            alloc = pd.to_numeric(df["postRebalance_current_allocation"], errors="coerce").values
            for i in range(n - 1):
                if (np.isfinite(fc[i]) and fc[i] == 0 and np.isfinite(alloc[i]) and alloc[i] < 0
                        and np.isfinite(close[i]) and np.isfinite(close[i + 1]) and close[i] > 0):
                    held_gains.append(alloc[i] * (close[i + 1] / close[i] - 1.0))
        if len(grid_rets) > 0:
            d = float(np.mean(grid_rets))
            drift[coin] = d
            for day, r, wgt in coin_cases:
                cases.append((day, -(r - d), wgt))

    n_cases = len(cases)
    days = sorted(set(c[0] for c in cases))
    n_days = len(days)
    n_held = len(held_gains)

    mean_w = None
    t_stat = None
    if n_cases > 0:
        x = np.array([c[1] for c in cases], dtype=float)
        wt = np.array([c[2] for c in cases], dtype=float)
        W = wt.sum()
        if W > 0:
            mean_w = float((wt * x).sum() / W)
            dfc = pd.DataFrame({"day": [c[0] for c in cases], "u": wt * (x - mean_w)})
            u = dfc.groupby("day")["u"].sum().values
            G = len(u)
            if G > 1:
                var = (G / (G - 1.0)) * float((u ** 2).sum()) / (W ** 2)
                se = np.sqrt(var)
                if se > 0:
                    t_stat = float(mean_w / se)

    held_mean = float(np.mean(held_gains)) if n_held > 0 else None
    sup_pass = None if n_held == 0 else bool(held_mean >= 0)

    counts = {"distinct case days": int(n_days), "cases": int(n_cases),
              "held-recovered bars": int(n_held)}

    # ---------- 3. Decision ----------
    if n_days < MIN_DAYS:
        status = "not observable"
        decided_by = f"Fewer than {MIN_DAYS} distinct case days ({n_days}), the plan's minimum count."
    elif n_held < MIN_HELD:
        status = "not observable"
        decided_by = f"Fewer than {MIN_HELD} held-recovered bars ({n_held}), the plan's minimum count for the supporting check."
    elif mean_w is None or t_stat is None:
        status = "inconclusive"
        decided_by = "The weighted mean or its t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_w > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided_by = ("Weighted mean unusual short-direction move above 0 with t >= 2 over at least 30 days, and the "
                          "held-recovered bars' mean gain is at least 0 over at least 20 bars.")
        else:
            status = "inconclusive"
            decided_by = "Confirm-strength main result, but the supporting check fails (held-recovered mean gain below 0)."
    elif mean_w < 0 and t_stat <= -2:
        status = "rejected"
        decided_by = "Weighted mean unusual short-direction move below 0 with t <= -2 over at least 30 distinct days."
    else:
        status = "inconclusive"
        decided_by = "The t lies between -2 and 2 (or its sign disagrees with the mean), meeting neither confirm nor reject."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "|forecast|-weighted mean 7-bar unusual move in the short direction",
            "value": mean_w,
            "statistic": {"name": "t of the weighted mean, cases of one day summed (day-clustered)", "value": t_stat}
            if t_stat is not None else None,
            "threshold": "confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; over at least 30 distinct days",
        },
        "supporting_check": {
            "name": "mean gain before costs on bars held short with forecast 0",
            "value": held_mean,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided_by,
        "reading": ("Situation bars are those with the month_fall component recorded (choppy regime active) and raw 30-day "
                    "return < 0 with a negative forecast; the drift is each coin's mean 7-bar return on the same "
                    "non-overlapping grid of all its windows; the t uses per-day sums of w*(x - weighted mean) as "
                    "cluster deviations, SE = sqrt(G/(G-1)*sum u_d^2)/sum w; held-recovered bars are bars with "
                    "forecast exactly 0 and a negative post-rebalance allocation; and both stated minimums (30 days, "
                    "20 held bars) are treated as minimum counts giving 'not observable' when unmet."),
    }
