import numpy as np
import pandas as pd


def measure(bars):
    H = 20
    MIN_CASES = 100

    def wkey(w):
        try:
            return int(str(w).lstrip("w"))
        except Exception:
            return 10**9

    coins = sorted(bars.keys())

    # ---------- 1. Situation check: regime 'trending' (close > 200-day SMA), long side ----------
    n_active = 0
    n_agree = 0
    for c in coins:
        for w, df in bars[c].items():
            if df is None or len(df) == 0 or "forecast" not in df.columns:
                continue
            f = pd.to_numeric(df["forecast"], errors="coerce")
            active = f.notna() & (f != 0)
            n_active += int(active.sum())
            if "regime" in df.columns:
                reg = df["regime"].astype(str).str.strip().str.lower()
                ok = active & (reg == "trending") & (f > 0)
                n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.9)

    main_name = "mean of (forecast/10) x (next 20-bar return minus coin's mean 20-bar return) on grid bars with forecast > 0"
    threshold = "mean > 0 with t >= 2 to confirm, mean < 0 with t <= -2 to reject, on at least 100 cases"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("No active bars in the record." if n_active == 0 else
                           "Fewer than 90% of bars with a non-zero forecast are long bars in the 'trending' regime "
                           "(close above its 200-day SMA), as the plan's situation requires."),
            "reading": "The plan's situation (close above its 200-day SMA) is checked on the detector's 'regime' column equal to 'trending', with the expected side long (forecast > 0).",
        }

    # ---------- 2. Main measure ----------
    grid_rows = []  # (coin, forecast, fwd return)
    for c in coins:
        for w in sorted(bars[c].keys(), key=wkey):
            df = bars[c][w]
            if df is None or len(df) == 0:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            f = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            n = len(df)
            for t in range(0, n, H):
                if t + H >= n:
                    break
                c0, c1 = close[t], close[t + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                grid_rows.append((c, f[t], c1 / c0 - 1.0))
    g = pd.DataFrame(grid_rows, columns=["coin", "forecast", "ret"])
    if len(g):
        coin_mean = g.groupby("coin")["ret"].mean()
        g["excess"] = g["ret"] - g["coin"].map(coin_mean)
        sel = g[g["forecast"].notna() & (g["forecast"] > 0)].copy()
        sel["val"] = (sel["forecast"] / 10.0) * sel["excess"]
        vals = sel["val"].dropna().to_numpy(dtype=float)
    else:
        vals = np.array([], dtype=float)
    n_cases = int(len(vals))
    mean_val = float(np.mean(vals)) if n_cases > 0 else None
    t_stat = None
    if n_cases > 1:
        sd = float(np.std(vals, ddof=1))
        if sd > 0:
            t_stat = float(mean_val / (sd / np.sqrt(n_cases)))

    # ---------- 3. Supporting check: Calmar of book vs holding ----------
    all_windows = sorted({w for c in coins for w in bars[c].keys()}, key=wkey)

    def chained_daily(col):
        out = []
        for w in all_windows:
            parts = []
            for c in coins:
                if w not in bars[c]:
                    continue
                df = bars[c][w]
                if df is None or len(df) == 0 or col not in df.columns:
                    continue
                d = pd.DataFrame({
                    "ts": pd.to_datetime(df["timestamp"]),
                    "v": pd.to_numeric(df[col], errors="coerce"),
                }).dropna()
                if len(d) < 2:
                    continue
                d["day"] = d["ts"].dt.floor("D")
                daily = d.groupby("day")["v"].last()
                r = daily.pct_change().dropna()
                parts.append(r.rename(c))
            if parts:
                m = pd.concat(parts, axis=1).mean(axis=1, skipna=True).sort_index().dropna()
                out.extend(m.to_list())
        return np.array(out, dtype=float)

    def calmar(r):
        r = r[np.isfinite(r)]
        if len(r) == 0:
            return None
        eq = np.cumprod(1.0 + r)
        total = eq[-1]
        if total <= 0:
            yearly = -1.0
        else:
            yearly = total ** (365.0 / len(r)) - 1.0
        path = np.concatenate([[1.0], eq])
        peak = np.maximum.accumulate(path)
        mdd = float(np.max(1.0 - path / peak))
        if mdd <= 0:
            return float("inf") if yearly > 0 else 0.0
        return float(yearly / mdd)

    book_cal = calmar(chained_daily("postRebalance_total_value"))
    hold_cal = calmar(chained_daily("close"))
    if book_cal is None or hold_cal is None:
        calmar_pass = None
        diff = None
    else:
        calmar_pass = bool(book_cal >= hold_cal)
        diff = (book_cal - hold_cal) if np.isfinite(book_cal) and np.isfinite(hold_cal) else None

    # ---------- 4. Decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} grid cases with a positive forecast, fewer than the plan's minimum of 100."
    elif t_stat is not None and mean_val > 0 and t_stat >= 2:
        if calmar_pass:
            status = "confirmed"
            decided = "Mean above 0 with t >= 2 on at least 100 cases and the book's Calmar at least the holding Calmar."
        else:
            status = "inconclusive"
            decided = "A confirming t (mean > 0, t >= 2) but the Calmar check fails."
    elif t_stat is not None and mean_val < 0 and t_stat <= -2:
        status = "rejected"
        decided = "Mean below 0 with t <= -2 on at least 100 cases."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2 (or is undefined), meeting neither the confirm nor the reject rule."

    def clean(x):
        if x is None:
            return None
        x = float(x)
        return x if np.isfinite(x) else (1e308 if x > 0 else -1e308)

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": passed},
        "main_measure": {
            "name": main_name,
            "value": clean(mean_val),
            "statistic": {"name": "t of the mean", "value": clean(t_stat)} if t_stat is not None else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "book Calmar minus holding Calmar (before costs), passes if >= 0",
            "value": clean(diff) if diff is not None else (None if calmar_pass is None else (1.0 if calmar_pass else -1.0)),
            "passed": calmar_pass,
        },
        "counts": {
            "grid cases with a positive forecast": n_cases,
            "active bars": int(n_active),
        },
        "decided_by": decided,
        "reading": ("Situation checked on regime == 'trending' with forecast > 0; grid bars are positions 0, 20, 40, ... of each "
                    "window that have a bar 20 ahead in the same window; the coin's mean 20-bar return is the mean over all its "
                    "grid samples in all windows; the book is postRebalance_total_value per bar, coins averaged per day, chained "
                    "over windows w1..wN in order, and holding is the same from closes."),
    }
