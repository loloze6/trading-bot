import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 30
    BAND = 2.0
    S90_COL = "debug_info.components.fall90.last_history_value"
    REGIME_NAME = "mean_reversion"
    EPS = 1e-9

    def wkey(w):
        try:
            return int(str(w).lstrip("wW"))
        except Exception:
            return 10 ** 9

    def to_days(ts):
        if pd.api.types.is_numeric_dtype(ts):
            mx = float(np.nanmax(ts.to_numpy(float))) if len(ts) else 0.0
            unit = "ms" if mx > 1e11 else "s"
            dt = pd.to_datetime(ts, unit=unit, utc=True)
        else:
            dt = pd.to_datetime(ts, utc=True)
        return dt.dt.floor("D")

    # ---------- prepare windows ----------
    prepared = {}
    for coin in sorted(bars.keys()):
        wins = bars[coin]
        plist = []
        for w in sorted(wins.keys(), key=wkey):
            df = wins[w]
            if df is None or len(df) == 0:
                continue
            df = df.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(float)
            n = len(close)
            fwd = np.full(n, np.nan)
            if n > H:
                fwd[: n - H] = close[H:] / close[: n - H] - 1.0
            r30 = np.full(n, np.nan)
            if n > 30:
                r30[30:] = close[30:] / close[:-30] - 1.0
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(float)
            if S90_COL in df.columns:
                s90 = pd.to_numeric(df[S90_COL], errors="coerce").to_numpy(float)
            else:
                s90 = np.full(n, np.nan)
            regime = df["regime"].astype(str).str.lower().to_numpy() if "regime" in df.columns else np.array([""] * n)
            days = to_days(df["timestamp"]).to_numpy()
            plist.append(dict(n=n, close=close, fwd=fwd, r30=r30, fc=fc, s90=s90, regime=regime, days=days))
        prepared[coin] = plist

    # ---------- situation check ----------
    denom = 0
    agree = 0
    for coin, plist in prepared.items():
        for p in plist:
            fc, s90, r30 = p["fc"], p["s90"], p["r30"]
            for i in range(p["n"]):
                f = fc[i]
                if not np.isfinite(f) or f == 0:
                    continue
                s_ok = np.isfinite(s90[i]) and s90[i] <= -1.0 + EPS
                side_ok = f > 0
                if not np.isfinite(r30[i]):
                    if s_ok and side_ok:
                        continue  # r30 cannot be computed inside the window: unverifiable, left out
                    denom += 1
                    continue
                denom += 1
                if s_ok and side_ok and r30[i] < 0:
                    agree += 1
    agreement = (agree / denom) if denom > 0 else None
    passed = agreement is not None and agreement >= 0.9

    reading = ("The 30-day return is recomputed as close[t]/close[t-30]-1 inside the window and active bars where it "
               "cannot be computed (first 30 bars) but whose s90 and side agree are left out of the check, s90 is the "
               "recorded fall90 raw value (same component and parameters), bets are detected per window starting from "
               "a forecast of 0, the first case in each 30-bar grid cell counts, cases without a full 30 bars ahead in "
               "their window are dropped, the day-clustered t uses the G/(G-1) correction, in-regime grid bars are "
               "those with regime 'mean_reversion', and the plan's 'fewer than 30 cases / fewer than 20 days' are "
               "treated as minimum counts giving 'not observable'.")

    main_name = "mean unusual 30-bar move of long cases (return minus coin's normal 30-bar drift)"
    threshold = "confirm: mean > 0 with day-clustered t >= 2 and supporting check passing; reject: mean < 0 with t <= -2"
    sup_name = "Spearman(forecast, excess 30-bar return) on in-regime 30-bar grid bars > 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement) if agreement is not None else None, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars checked": int(denom)},
            "decided_by": ("Fewer than 90 % of the active bars have s90 <= -1, a 30-day return below 0 and a long "
                           "forecast, so the config does not trade the plan's situation on its side."),
            "reading": reading,
        }

    # ---------- drift per coin ----------
    drift = {}
    for coin, plist in prepared.items():
        rr = []
        for p in plist:
            g = p["fwd"][np.arange(0, p["n"], H)]
            rr.extend(g[np.isfinite(g)].tolist())
        drift[coin] = float(np.mean(rr)) if len(rr) else np.nan

    # ---------- cases ----------
    case_moves = []
    case_days = []
    sup_fc = []
    sup_ex = []
    for coin, plist in prepared.items():
        d = drift[coin]
        for p in plist:
            fc = p["fc"]
            n = p["n"]
            base = 0.0
            on_long = False
            bet_bars = []
            for i in range(n):
                f = fc[i]
                if not np.isfinite(f) or f <= 0:
                    on_long = False
                    base = 0.0
                    continue
                if not on_long:
                    on_long = True
                    base = 0.0
                if f - base >= BAND - EPS:
                    bet_bars.append(i)
                    base = f
                else:
                    base = min(base, f)
            seen_cells = set()
            for i in bet_bars:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                r = p["fwd"][i]
                if np.isfinite(r) and np.isfinite(d):
                    case_moves.append(r - d)
                    case_days.append(p["days"][i])
            # supporting check rows
            for i in range(0, n, H):
                if p["regime"][i] != REGIME_NAME:
                    continue
                r = p["fwd"][i]
                f = fc[i]
                if np.isfinite(r) and np.isfinite(f) and np.isfinite(d):
                    sup_fc.append(f)
                    sup_ex.append(r - d)

    x = np.array(case_moves, float)
    n_cases = int(len(x))
    n_days = int(len(set(case_days)))
    mean_move = float(np.mean(x)) if n_cases else None

    t_stat = None
    if n_cases >= 2 and n_days >= 2:
        dev = x - x.mean()
        s = pd.Series(dev).groupby(pd.Series(case_days)).sum().to_numpy(float)
        G = len(s)
        var = (G / (G - 1)) * np.sum(s ** 2) / (n_cases ** 2)
        if var > 0:
            t_stat = float(x.mean() / np.sqrt(var))

    rho = None
    if len(sup_fc) >= 3 and np.std(sup_fc) > 0 and np.std(sup_ex) > 0:
        rr = stats.spearmanr(sup_fc, sup_ex)
        rv = float(rr.correlation if hasattr(rr, "correlation") else rr[0])
        rho = rv if np.isfinite(rv) else None
    sup_pass = bool(rho is not None and rho > 0)

    counts = {"cases": n_cases, "distinct days": n_days, "in-regime grid bars": int(len(sup_fc))}

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 cases ({n_cases}), the plan's minimum count, so the data could not show the idea."
    elif n_days < 20:
        status = "not observable"
        decided = f"Cases fall on fewer than 20 distinct days ({n_days}), the plan's minimum count."
    elif t_stat is None:
        status = "inconclusive"
        decided = "The day-clustered t could not be computed, so neither the confirm nor the reject rule is met."
    elif mean_move > 0 and t_stat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The mean unusual move is above 0 with a day-clustered t of 2 or more and the Spearman check is above 0."
        else:
            status = "inconclusive"
            decided = "The day-clustered t is 2 or more but the supporting Spearman check fails."
    elif mean_move < 0 and t_stat <= -2:
        status = "rejected"
        decided = "The mean unusual move is below 0 with a day-clustered t of -2 or less."
    else:
        status = "inconclusive"
        decided = "The day-clustered t lies between -2 and 2, so neither the confirm nor the reject rule is met."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_move,
            "statistic": {"name": "day-clustered t", "value": t_stat} if t_stat is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {"name": sup_name, "value": rho, "passed": sup_pass},
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
