import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 20
    BAND = 2.0
    MIN_CASES = 30
    UP_COL = "debug_info.components.bounce_up.last_history_value"
    DN_COL = "debug_info.components.bounce_down.last_history_value"

    # ---------------- situation check ----------------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(df)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values

            # raw one-day vol-scaled return: recorded value, else recomputed from prices
            raw = pd.Series(np.nan, index=df.index, dtype=float)
            if UP_COL in df.columns:
                raw = raw.fillna(pd.to_numeric(df[UP_COL], errors="coerce"))
            if DN_COL in df.columns:
                raw = raw.fillna(pd.to_numeric(df[DN_COL], errors="coerce"))
            r1 = pd.Series(close).pct_change()
            vol = r1.rolling(20, min_periods=20).std()
            recomputed = r1 / vol
            raw = raw.fillna(recomputed)
            raw = raw.values

            # 90-day return sign: from prices where 90 bars of the window exist, else the detector's regime
            ret90 = np.full(n, np.nan)
            if n > 90:
                ret90[90:] = close[90:] / close[:-90] - 1.0
            reg = df["regime"].astype(str).values
            side_exp = np.where(
                ~np.isnan(ret90),
                np.where(ret90 < 0, -1, 1),
                np.where(reg == "mean_reversion", -1, np.where(reg == "unknown", 1, 0)),
            )

            for i in range(n):
                if fc[i] == 0:
                    continue
                n_active += 1
                if np.isfinite(raw[i]) and raw[i] > 0 and side_exp[i] != 0 and np.sign(fc[i]) == side_exp[i]:
                    n_agree += 1

    if n_active == 0:
        return {
            "status": "not observable",
            "situation_check": {"agreement": None, "passed": False},
            "main_measure": {"name": "mean 20-day excess return after bounces, up-regime minus down-regime",
                             "value": None, "statistic": None,
                             "threshold": "Welch t >= 2 confirms (with check), t <= -2 rejects"},
            "supporting_check": None,
            "counts": {"up-regime cases": 0, "down-regime cases": 0},
            "decided_by": "No bar has a non-zero forecast, so no case exists.",
            "reading": "none",
        }

    agreement = n_agree / n_active
    if agreement < 0.9:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of active bars are one-day rises traded long when the 90-day "
                           "return is >= 0 and short when it is < 0, as the Fidelity states."),
            "reading": "Situation = raw vol-scaled 1-day return > 0; side from the 90-day return sign "
                       "recomputed from prices where possible, else the recorded regime.",
        }

    # ---------------- cases ----------------
    rows = []
    for coin, wins in bars.items():
        # normal drift: mean of non-overlapping 20-bar returns over all windows of the coin
        grid_rets = []
        prepared = []
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = df["close"].astype(float).values
            n = len(close)
            for p in range(0, n - H, H):
                if np.isfinite(close[p]) and np.isfinite(close[p + H]) and close[p] > 0:
                    grid_rets.append(close[p + H] / close[p] - 1.0)
            prepared.append((df, close))
        if len(grid_rets) == 0:
            continue
        drift = float(np.mean(grid_rets))

        for df, close in prepared:
            n = len(close)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values
            prev_side = 0
            anchor = 0.0
            bets = []
            for i in range(n):
                f = fc[i]
                s = int(np.sign(f))
                if s == 0:
                    prev_side = 0
                    anchor = 0.0
                    continue
                if s != prev_side:
                    anchor = 0.0
                    prev_side = s
                m = abs(f)
                if m - anchor >= BAND:
                    bets.append(i)
                    anchor = m
                else:
                    anchor = min(anchor, m)
            seen = set()
            for i in bets:
                cell = i // H
                if cell in seen:
                    continue
                seen.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(close[i]) and np.isfinite(close[i + H]) and close[i] > 0):
                    continue
                ret = close[i + H] / close[i] - 1.0
                rows.append({"side": int(np.sign(fc[i])), "absf": abs(fc[i]), "x": ret - drift})

    cases = pd.DataFrame(rows, columns=["side", "absf", "x"])
    up = cases[cases["side"] > 0]
    dn = cases[cases["side"] < 0]
    n_up, n_dn = len(up), len(dn)
    counts = {"up-regime cases": int(n_up), "down-regime cases": int(n_dn)}

    reading = ("A case is the first bet (forecast rise >= 2 points on its side from its lowest level since the last bet) "
               "in each 20-bar grid cell of each window, grouped by the forecast's sign (long = 90-day up, short = down), "
               "with raw 20-day return minus the coin's mean non-overlapping 20-day return; the median split puts "
               "|forecast| above the group median in 'larger' and at or below it in 'smaller'; fewer than 30 cases in a "
               "group is reported as not observable.")
    main_name = "mean 20-day return minus drift after bounces, up-regime minus down-regime"
    threshold = "Welch t >= 2 with widening gap confirms; t <= -2 rejects; otherwise inconclusive"

    if n_up < MIN_CASES or n_dn < MIN_CASES:
        diff = float(up["x"].mean() - dn["x"].mean()) if (n_up > 0 and n_dn > 0) else None
        return {
            "status": "not observable",
            "situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": {"name": main_name, "value": diff, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": counts,
            "decided_by": "Fewer than 30 cases in at least one regime group, the plan's minimum.",
            "reading": reading,
        }

    diff = float(up["x"].mean() - dn["x"].mean())
    t = float(stats.ttest_ind(up["x"].values, dn["x"].values, equal_var=False).statistic)

    # supporting check
    def split(g):
        med = g["absf"].median()
        return g[g["absf"] > med], g[g["absf"] <= med]

    up_l, up_s = split(up)
    dn_l, dn_s = split(dn)
    if min(len(up_l), len(up_s), len(dn_l), len(dn_s)) > 0:
        gap_l = float(up_l["x"].mean() - dn_l["x"].mean())
        gap_s = float(up_s["x"].mean() - dn_s["x"].mean())
        sup_val = gap_l - gap_s
        sup_pass = bool(gap_l > gap_s)
    else:
        sup_val = None
        sup_pass = None
    counts.update({"up larger": int(len(up_l)), "up smaller": int(len(up_s)),
                   "down larger": int(len(dn_l)), "down smaller": int(len(dn_s))})

    if t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Welch t >= 2 and the larger-bounce gap exceeds the smaller-bounce gap."
    elif t <= -2:
        status = "rejected"
        decided = "Welch t <= -2: returns after bounces in fallers are reliably higher than in risers."
    elif t >= 2:
        status = "inconclusive"
        decided = "Welch t >= 2 but the up-minus-down gap does not widen for larger bounces."
    else:
        status = "inconclusive"
        decided = "Welch t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": main_name, "value": diff,
                         "statistic": {"name": "Welch t", "value": t}, "threshold": threshold},
        "supporting_check": {"name": "larger-bounce gap minus smaller-bounce gap",
                             "value": sup_val, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
