import numpy as np
import pandas as pd


def measure(bars):
    H = 5
    BAND = 2.0

    def comp_value(df, cid, field="last_history_value"):
        col = "debug_info.components.%s.%s" % (cid, field)
        if col in df.columns:
            return pd.to_numeric(df[col], errors="coerce")
        if "debug_info.components" in df.columns:
            out = []
            for v in df["debug_info.components"].values:
                x = np.nan
                if isinstance(v, dict):
                    c = v.get(cid)
                    if isinstance(c, dict):
                        try:
                            x = float(c.get(field)) if c.get(field) is not None else np.nan
                        except (TypeError, ValueError):
                            x = np.nan
                out.append(x)
            return pd.Series(out, index=df.index, dtype=float)
        return pd.Series(np.nan, index=df.index, dtype=float)

    n_active = 0
    n_agree = 0
    cases = []          # (coin, day, fwd return)
    grid_returns = {}   # coin -> list of non-overlapping 5-bar returns
    supp_f, supp_r = [], []

    for coin in sorted(bars.keys()):
        grid_returns.setdefault(coin, [])
        for w in sorted(bars[coin].keys()):
            df = bars[coin][w].reset_index(drop=True)
            if len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").values.astype(float)
            high = pd.to_numeric(df["high"], errors="coerce").values.astype(float)
            low = pd.to_numeric(df["low"], errors="coerce").values.astype(float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0).values.astype(float)
            regime = df["regime"].astype(str).values
            ts = pd.to_datetime(df["timestamp"], utc=True)
            days = ts.dt.strftime("%Y-%m-%d").values
            n = len(df)

            # --- situation check ---
            rng = high - low
            with np.errstate(divide="ignore", invalid="ignore"):
                loc = np.where(rng > 0, (close - low) / rng, np.nan)
            ret5_px = (pd.Series(close) / pd.Series(close).shift(5) - 1.0).values * 100.0
            ret5_rec = comp_value(df, "fall5").values
            ret5 = np.where(np.isfinite(ret5_rec), ret5_rec, ret5_px)
            profile = regime != "chop"
            situation = profile & (np.nan_to_num(loc, nan=-1.0) > 0.5) & (np.nan_to_num(ret5, nan=1.0) < 0.0)
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc < 0)).sum())

            # --- forward returns ---
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0

            # normal drift grid and supporting check
            for p in range(0, n, H):
                if np.isfinite(fwd[p]):
                    grid_returns[coin].append(fwd[p])
                    if fc[p] < 0:
                        supp_f.append(fc[p])
                        supp_r.append(fwd[p])

            # --- short bets: forecast falling by >= band from its lowest level on the short side since last bet ---
            bet = np.zeros(n, dtype=bool)
            ref = 0.0
            prev_short = False
            for i in range(n):
                m = -fc[i] if fc[i] < 0 else 0.0
                if m <= 0:
                    ref = 0.0
                    prev_short = False
                    continue
                if not prev_short:
                    ref = 0.0
                if m - ref >= BAND - 1e-12:
                    bet[i] = True
                    ref = m
                else:
                    ref = min(ref, m)
                prev_short = True
            seen = set()
            for i in range(n):
                if bet[i]:
                    cell = i // H
                    if cell in seen:
                        continue
                    seen.add(cell)
                    if np.isfinite(fwd[i]):
                        cases.append((coin, days[i], fwd[i]))

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    thr = "t of the unusual move >= 2 (with supporting correlation > 0) confirms; t <= -2 rejects"
    mname = "mean unusual 5-bar move per short case, in the short direction, before costs"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": mname, "value": None, "statistic": None, "threshold": thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "fewer than 90% of the bars with a non-zero forecast are short bars of the choppy agitated profile with close location above 0.5 after a negative 5-day return",
            "reading": "the choppy agitated profile is read from the regime column (not 'chop', as its vetoes cannot be recomputed from the windows' bars), close location and the 5-day return in percent from the prices and the recorded fall5 value",
        }

    drift = {c: (float(np.mean(v)) if len(v) else np.nan) for c, v in grid_returns.items()}
    u = []
    d = []
    for coin, day, r in cases:
        if np.isfinite(drift.get(coin, np.nan)):
            u.append(-(r - drift[coin]))
            d.append(day)
    u = np.array(u, dtype=float)
    N = len(u)
    D = len(set(d))

    mean_u = float(np.mean(u)) if N else None
    t = None
    if N >= 2 and D >= 2:
        dev = pd.Series(u - mean_u).groupby(pd.Series(d)).sum().values
        var = (dev ** 2).sum() / (N ** 2) * (D / (D - 1.0))
        if var > 0:
            t = float(mean_u / np.sqrt(var))

    corr = None
    if len(supp_f) >= 3 and np.std(supp_f) > 0 and np.std(supp_r) > 0:
        corr = float(np.corrcoef(supp_f, supp_r)[0, 1])
    supp_pass = bool(corr is not None and corr > 0)

    counts = {"cases": int(N), "distinct days": int(D), "supporting grid bars": int(len(supp_f))}

    if N < 30 or D < 20:
        status = "not observable"
        decided = "minimum count not reached: %d cases (need 30) on %d distinct days (need 20)" % (N, D)
    elif t is None:
        status = "inconclusive"
        decided = "the t of the unusual move could not be computed"
    elif t >= 2 and supp_pass:
        status = "confirmed"
        decided = "the unusual move's t is 2 or more and the supporting correlation is above 0"
    elif t <= -2:
        status = "rejected"
        decided = "the unusual move's t is -2 or less: prices rise after these bars against the coin's drift"
    elif t >= 2:
        status = "inconclusive"
        decided = "the unusual move's t is 2 or more but the supporting correlation is at or below 0"
    else:
        status = "inconclusive"
        decided = "the unusual move's t is between -2 and 2"

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": mname,
            "value": mean_u,
            "statistic": ({"name": "t of the mean, cases of one day taken together", "value": t} if t is not None else None),
            "threshold": thr,
        },
        "supporting_check": {
            "name": "correlation of forecast and next 5-bar return on grid bars with forecast < 0",
            "value": corr,
            "passed": supp_pass if corr is not None else None,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "the profile is read from the regime column (not 'chop'), a case is the first short bet (forecast magnitude rising >= 2 from its lowest short level since the last bet) in each 5-bar grid cell of a window, the drift is the coin's mean non-overlapping 5-bar return over all its windows, the t uses day-clustered deviations, and the plan's 'fewer than 30 cases or 20 days' is applied as the minimum counts (not observable)",
    }
