import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 10
    BAND = 2.0
    EPS = 1e-9
    FC = "forecast"

    def _num(df, col):
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        return pd.Series(np.nan, index=df.index)

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            o, h, l, c = (_num(df, k) for k in ("open", "high", "low", "close"))
            f = _num(df, FC).fillna(0.0)
            rng = h - l
            rise5 = c / c.shift(5) - 1.0
            mean_rng = rng.rolling(20, min_periods=20).mean()
            wide = rng / mean_rng.replace(0, np.nan)
            body = (c - o).abs() / rng.replace(0, np.nan)
            computable = rise5.notna() & wide.notna() & body.notna()
            sit = (rise5 > 0) & (wide >= 1.5 - EPS) & (body <= 0.1 + EPS)
            # bars too early in the window to recompute: use the detector's own decision
            if "regime" in df.columns:
                reg = df["regime"].astype(str) == "trending"
                sit = sit.where(computable, reg)
            else:
                sit = sit & computable
            active = f != 0
            n_active += int(active.sum())
            n_agree += int((active & sit & (f > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean unusual 10-bar move of the cases (before costs)"
    threshold = "confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2"
    sup_name = "Spearman correlation of case forecast vs unusual move > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are long bars of the plan's "
                           "situation (5-day return > 0, range / 20-day mean range >= 1.5, body <= 10 % of range)."
                           if n_active > 0 else "The record has no active bar, so the forecast does not hold the plan's situation."),
            "reading": "Situation recomputed from prices per window; bars without 20 bars of history use the recorded regime 'trending'.",
        }

    # ---------- 2. criterion ----------
    cases = []  # (coin, day, forecast, ret, sign)
    drift = {}
    for coin, wins in bars.items():
        grid_rets = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            c = _num(df, "close").values
            f = _num(df, FC).fillna(0.0).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            # normal drift grid
            for p in range(0, n - H, H):
                if np.isfinite(c[p]) and np.isfinite(c[p + H]) and c[p] != 0:
                    grid_rets.append(c[p + H] / c[p] - 1.0)
            # bets
            side = 0
            ref = 0.0
            first_in_cell = {}
            for t in range(n):
                ft = f[t]
                s = 1 if ft > 0 else (-1 if ft < 0 else 0)
                if s == 0:
                    side, ref = 0, 0.0
                    continue
                if s != side:
                    side, ref = s, 0.0
                mag = abs(ft)
                ref = min(ref, mag)
                if mag - ref >= BAND - EPS:
                    ref = mag
                    cell = t // H
                    if cell not in first_in_cell:
                        first_in_cell[cell] = (t, s)
            for cell, (t, s) in first_in_cell.items():
                if t + H < n and np.isfinite(c[t]) and np.isfinite(c[t + H]) and c[t] != 0:
                    r = c[t + H] / c[t] - 1.0
                    cases.append((coin, ts.iloc[t].strftime("%Y-%m-%d"), float(f[t]), float(r), s))
        drift[coin] = float(np.mean(grid_rets)) if len(grid_rets) else np.nan

    rows = [(cn, d, fc, (r - drift[cn]) * s) for cn, d, fc, r, s in cases if np.isfinite(drift.get(cn, np.nan))]
    n_cases = len(rows)
    days = sorted(set(r[1] for r in rows))
    n_days = len(days)
    counts = {"cases": int(n_cases), "distinct case days": int(n_days)}

    mean_u = None
    t_stat = None
    rho = None
    if n_cases > 0:
        u = np.array([r[3] for r in rows])
        fc = np.array([r[2] for r in rows])
        mean_u = float(u.mean())
        dev = pd.Series(u - mean_u).groupby([r[1] for r in rows]).sum().values
        D = len(dev)
        if D > 1:
            var = (D / (D - 1)) * np.sum(dev ** 2) / (n_cases ** 2)
            if var > 0:
                t_stat = float(mean_u / np.sqrt(var))
        if n_cases > 2 and np.std(fc) > 0 and np.std(u) > 0:
            rho = float(stats.spearmanr(fc, u).correlation)

    sup_pass = None if rho is None else bool(rho > 0)

    if n_cases < 30 or n_days < 30:
        status = "not observable"
        decided = (f"Minimum counts not reached: {n_cases} cases and {n_days} distinct case days, "
                   "the plan needs at least 30 of each.")
    elif t_stat is None:
        status = "inconclusive"
        decided = "The t of the mean unusual move cannot be computed, so neither confirm nor reject is met."
    elif mean_u > 0 and t_stat >= 2 and sup_pass:
        status = "confirmed"
        decided = "Mean unusual move above 0 with t >= 2 and a positive Spearman correlation: the confirm rule."
    elif mean_u < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: the reject rule."
    elif t_stat >= 2:
        status = "inconclusive"
        decided = "t >= 2 but the Spearman correlation is 0 or below (or not computable): inconclusive by the plan."
    else:
        status = "inconclusive"
        decided = "t between -2 and 2: inconclusive by the plan."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_u,
            "statistic": None if t_stat is None else {"name": "t of the mean, cases of one day summed together", "value": t_stat},
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": rho, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": ("A case is the first bet (forecast rise >= 2 from its low on its side since the last bet) in each "
                    "10-bar grid cell from each window's first row, kept only if 10 bars follow in its window; the drift "
                    "is the coin's mean 10-bar return on that grid over all its windows; a day is the UTC date of the "
                    "case bar; situation bars without 20 bars of history use the recorded regime 'trending'."),
    }
