import numpy as np
import pandas as pd


def _wilder_rsi(close, period):
    close = pd.Series(close, dtype=float)
    d = close.diff()
    up = d.clip(lower=0.0)
    dn = (-d).clip(lower=0.0)
    au = up.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    ad = dn.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
    rs = au / ad
    rsi = 100.0 - 100.0 / (1.0 + rs)
    rsi = rsi.where(ad != 0, 100.0)
    rsi = rsi.where(~((au == 0) & (ad == 0)), 50.0)
    rsi[au.isna() | ad.isna()] = np.nan
    return rsi


def _tstat(x):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return None
    sd = np.std(x, ddof=1)
    if not np.isfinite(sd) or sd == 0:
        return None
    return float(np.mean(x) / (sd / np.sqrt(n)))


def measure(bars):
    H = 168
    PERIOD = 336
    MIN_CASES = 300
    raw_col = "debug_info.components.rsi_mid.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin in sorted(bars.keys()):
        for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) == 0:
                continue
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            if raw_col in df.columns:
                raw = pd.to_numeric(df[raw_col], errors="coerce").to_numpy(dtype=float)
            else:
                raw = np.full(len(df), np.nan)
            miss = ~np.isfinite(raw)
            if miss.any():
                rsi = _wilder_rsi(df["close"].to_numpy(dtype=float), PERIOD).to_numpy()
                raw = np.where(miss, 50.0 - rsi, raw)
            # situation: signed distance RSI - 50 = -raw; expected side = sign(RSI - 50)
            dist = -raw
            active = np.isfinite(fc) & (fc != 0)
            n_active += int(active.sum())
            ok = active & np.isfinite(dist) & (dist != 0) & (np.sign(fc) == np.sign(dist))
            n_agree += int(ok.sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)

    main_name = "t of the mean of forecast/10 x 168-bar excess return (non-overlapping, pooled)"
    threshold = "confirm: mean > 0 with t >= 2.0 and coin check passes; reject: mean < 0 with t <= -2.0; at least 300 cases"
    reading = ("The supporting check '2 of the 3 coins' is applied to the coins present in the record, requiring at "
               "least 2 coins with a positive mean product (all coins when only 2 are present); the coin's mean "
               "168-bar return is the mean over its non-overlapping grid cases across all its windows; cases with "
               "forecast 0 are kept (product 0); the 300-case minimum, if unmet, gives 'not observable'.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"non-overlapping cases": 0, "active bars": n_active},
            "decided_by": (f"Only {agreement:.1%} of active bars have a forecast sign equal to the sign of RSI(336) - 50 "
                           "(long above 50, short below), below the 90% needed for the plan's situation."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    cases = {}  # coin -> list of (forecast, ret)
    for coin in sorted(bars.keys()):
        lst = []
        for w in sorted(bars[coin].keys(), key=lambda s: (len(str(s)), str(s))):
            df = bars[coin][w]
            if df is None or len(df) <= H:
                continue
            close = pd.to_numeric(df["close"], errors="coerce").to_numpy(dtype=float)
            fc = pd.to_numeric(df["forecast"], errors="coerce").to_numpy(dtype=float)
            for t in range(0, len(df) - H, H):
                c0, c1, f = close[t], close[t + H], fc[t]
                if np.isfinite(c0) and np.isfinite(c1) and np.isfinite(f) and c0 > 0:
                    lst.append((f, c1 / c0 - 1.0))
        cases[coin] = lst

    all_prod = []
    coin_means = {}
    for coin, lst in cases.items():
        if not lst:
            continue
        arr = np.array(lst, dtype=float)
        mean_ret = arr[:, 1].mean()
        prod = arr[:, 0] / 10.0 * (arr[:, 1] - mean_ret)
        coin_means[coin] = float(prod.mean())
        all_prod.extend(prod.tolist())

    n = len(all_prod)
    counts = {"non-overlapping cases": n}
    for coin in sorted(cases.keys()):
        counts[f"cases {coin}"] = len(cases[coin])

    mean_prod = float(np.mean(all_prod)) if n > 0 else None
    t = _tstat(all_prod) if n > 0 else None

    n_pos = sum(1 for v in coin_means.values() if v > 0)
    n_coins = len(coin_means)
    need = min(2, n_coins) if n_coins > 0 else 2
    sup_passed = bool(n_coins > 0 and n_pos >= need)
    supporting = {"name": "coins with mean product > 0 (need 2 of 3, of those present)",
                  "value": float(n_pos), "passed": sup_passed}

    main = {"name": main_name, "value": mean_prod,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": threshold}

    if n < MIN_CASES:
        status = "not observable"
        decided = f"Only {n} non-overlapping cases, fewer than the plan's minimum of 300."
    elif t is not None and mean_prod > 0 and t >= 2.0 and sup_passed:
        status = "confirmed"
        decided = "Pooled mean product is above 0 with t >= 2.0 and the coin check passes."
    elif t is not None and mean_prod < 0 and t <= -2.0:
        status = "rejected"
        decided = "Pooled mean product is below 0 with t <= -2.0."
    elif t is not None and mean_prod > 0 and t >= 2.0 and not sup_passed:
        status = "inconclusive"
        decided = "t >= 2.0 but the coin check fails, which the plan calls inconclusive."
    else:
        status = "inconclusive"
        decided = "The t lies between -2.0 and 2.0, which the plan calls inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": main,
        "supporting_check": supporting,
        "counts": counts,
        "decided_by": decided,
        "reading": reading,
    }
