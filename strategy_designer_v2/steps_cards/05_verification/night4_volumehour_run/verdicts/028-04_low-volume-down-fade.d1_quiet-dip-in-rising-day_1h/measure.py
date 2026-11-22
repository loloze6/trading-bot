import numpy as np
import pandas as pd


def measure(bars):
    H = 6
    BAND = 2.0
    MIN_CASES = 30
    DIP_COL = "debug_info.components.dip.last_history_value"

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            vol = df["volume"].astype(float)
            fc = df["forecast"].astype(float).fillna(0.0)

            # volume ratio: hour's volume over its mean of the prior 720 hours (current excluded)
            prior_mean = vol.shift(1).rolling(720, min_periods=720).mean()
            ratio = vol / prior_mean
            in_band = (ratio >= 0.67) & (ratio <= 1.5)
            # where the 720-hour history is not inside the window, use the recorded regime
            regime_mr = df["regime"].astype(str) == "mean_reversion"
            in_band = in_band.where(prior_mean.notna(), regime_mr)

            # dip component: positive only when the hour fell and the prior 24h rose
            fell = close < close.shift(1)
            rose = close.shift(1) > close.shift(25)
            dip_from_prices = fell & rose
            if DIP_COL in df.columns:
                raw = pd.to_numeric(df[DIP_COL], errors="coerce")
                dip_pos = (raw > 0).where(raw.notna(), dip_from_prices)
            else:
                dip_pos = dip_from_prices
            dip_pos = dip_pos.fillna(False).astype(bool)

            situation = in_band.fillna(False).astype(bool) & dip_pos
            active = fc != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc > 0)).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.9
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the bars with a non-zero forecast are bars where the hour fell, "
                           "the prior 24h rose and volume was within 0.67-1.5x its 720-hour mean, with a long forecast."),
            "reading": "none",
        }

    # ---------- 2. criterion ----------
    # coin's normal 6-bar drift: mean over non-overlapping grid of all its windows
    drift = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].astype(float).to_numpy()
            for i in range(0, len(c) - H, H):
                if np.isfinite(c[i]) and np.isfinite(c[i + H]) and c[i] != 0:
                    rets.append(c[i + H] / c[i] - 1.0)
        drift[coin] = float(np.mean(rets)) if rets else np.nan

    unusual = []
    weights = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).to_numpy()
            f = df["forecast"].astype(float).fillna(0.0).to_numpy()
            n = len(df)
            # long bets: rise of the positive forecast of at least BAND from its lowest level since last bet
            bets = np.zeros(n, dtype=bool)
            trough = 0.0
            prev_pos = False
            for i in range(n):
                if f[i] > 0:
                    if not prev_pos:
                        trough = 0.0
                    trough = min(trough, f[i])
                    if f[i] - trough >= BAND:
                        bets[i] = True
                        trough = f[i]
                    prev_pos = True
                else:
                    prev_pos = False
                    trough = 0.0
            seen_cells = set()
            for i in np.nonzero(bets)[0]:
                cell = i // H
                if cell in seen_cells:
                    continue
                seen_cells.add(cell)
                if i + H >= n:
                    continue
                if not (np.isfinite(c[i]) and np.isfinite(c[i + H])) or c[i] == 0:
                    continue
                if not np.isfinite(drift[coin]):
                    continue
                unusual.append(c[i + H] / c[i] - 1.0 - drift[coin])
                weights.append(f[i])

    u = np.array(unusual, dtype=float)
    wts = np.array(weights, dtype=float)
    n_cases = int(len(u))
    mean_u = float(u.mean()) if n_cases > 0 else None
    t = None
    if n_cases >= 2:
        sd = float(u.std(ddof=1))
        t = float(mean_u / (sd / np.sqrt(n_cases))) if sd > 0 else None
    wmean = float(np.sum(u * wts) / np.sum(wts)) if n_cases > 0 and np.sum(wts) != 0 else None
    sup_pass = (wmean is not None and wmean > 0) if n_cases > 0 else None

    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Fewer than {MIN_CASES} independent cases ({n_cases}), so the minimum count is not reached."
    elif t is not None and mean_u > 0 and t >= 2 and sup_pass:
        status = "confirmed"
        decided = "The mean unusual move is positive with t >= 2 over at least 30 cases and the forecast-weighted mean is above 0."
    elif t is not None and mean_u < 0 and t <= -2:
        status = "rejected"
        decided = "The mean unusual move is negative with t <= -2 over at least 30 cases."
    elif t is not None and mean_u > 0 and t >= 2:
        status = "inconclusive"
        decided = "A confirming t whose forecast-weighted mean is not above 0."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": "mean 6-bar unusual move of long cases",
            "value": mean_u,
            "statistic": {"name": "t of the mean", "value": t} if t is not None else None,
            "threshold": "positive with t >= 2 to confirm, negative with t <= -2 to reject, over at least 30 cases",
        },
        "supporting_check": {
            "name": "forecast-weighted mean unusual move above 0",
            "value": wmean,
            "passed": sup_pass,
        },
        "counts": {"cases": n_cases, "active bars": int(n_active)},
        "decided_by": decided,
        "reading": ("A case is the first bar of each 6-bar grid cell (counted from each window's first row) where the "
                    "positive forecast rose at least 2 points from its lowest level since the last bet (from 0 after a flat), "
                    "cases whose 6-bar return would leave the window are dropped, and the drift is the coin's mean "
                    "6-bar return on the same grid over all its windows."),
    }
