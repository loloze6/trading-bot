import numpy as np
import pandas as pd


def measure(bars):
    H = 3
    RAW = "debug_info.components.flush.last_history_value"
    VOL_P = 20
    VOLU_P = 30
    MIN_CASES = 100

    def _f(x):
        if x is None:
            return None
        try:
            x = float(x)
        except Exception:
            return None
        return x if np.isfinite(x) else None

    # ---------- 1. Situation check: active bars must be falling bars, long side ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            active = fc.notna() & (fc != 0)
            close = pd.to_numeric(d["close"], errors="coerce")
            pret = close / close.shift(1) - 1.0  # inside the window only
            if RAW in d.columns:
                raw = pd.to_numeric(d[RAW], errors="coerce")
                raw_fall = raw < 0
                raw_known = raw.notna()
            else:
                raw_fall = pd.Series(False, index=d.index)
                raw_known = pd.Series(False, index=d.index)
            price_fall = pret < 0
            price_known = pret.notna()
            # a falling bar: raw reading negative where recorded, and the close below the previous close where measurable
            fall = (
                (raw_fall | ~raw_known)
                & (price_fall | ~price_known)
                & (raw_known | price_known)
            )
            situation_on_side = fall & (fc > 0)
            n_active += int(active.sum())
            n_agree += int((active & situation_on_side).sum())

    if n_active > 0:
        agreement = n_agree / n_active
        passed = agreement >= 0.90
    else:
        agreement = None
        passed = True

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": _f(agreement), "passed": False},
            "main_measure": {
                "name": "OLS slope of 3-bar excess return on forecast",
                "value": None,
                "statistic": None,
                "threshold": "slope t >= 2 confirms (with positive volume-ratio coefficient); t <= -2 rejects",
            },
            "supporting_check": None,
            "counts": {"independent cases with forecast > 0 on the grid": None},
            "decided_by": "Fewer than 90% of the bars with a non-zero forecast are falling bars with a long (positive) forecast, "
                          "so the config does not trade the plan's situation (a sharp fall, long side).",
            "reading": "The situation is read as a down bar (negative raw component value and close below the previous close where measurable), on the long side.",
        }

    # ---------- 2. Build the grid sample ----------
    rows = []
    coin_grid_rets = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = df.reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            volume = pd.to_numeric(d["volume"], errors="coerce")
            fc = pd.to_numeric(d["forecast"], errors="coerce")
            ret1 = close / close.shift(1) - 1.0
            sd20 = ret1.rolling(VOL_P, min_periods=VOL_P).std()
            usual = ret1 / sd20
            vratio = volume / volume.rolling(VOLU_P, min_periods=VOLU_P).mean()
            fwd = close.shift(-H) / close - 1.0
            n = len(d)
            for i in range(0, n, H):
                r = fwd.iloc[i]
                if pd.isna(r) or not np.isfinite(r):
                    continue
                allr.append(float(r))
                f = fc.iloc[i]
                if pd.notna(f) and f > 0:
                    rows.append({
                        "coin": coin,
                        "fwd": float(r),
                        "fc": float(f),
                        "vratio": float(vratio.iloc[i]) if pd.notna(vratio.iloc[i]) else np.nan,
                        "fall": float(-usual.iloc[i]) if pd.notna(usual.iloc[i]) and np.isfinite(usual.iloc[i]) else np.nan,
                    })
        if allr:
            coin_grid_rets[coin] = float(np.mean(allr))

    s = pd.DataFrame(rows, columns=["coin", "fwd", "fc", "vratio", "fall"])
    if len(s):
        s["excess"] = s["fwd"] - s["coin"].map(coin_grid_rets)
        s = s[np.isfinite(s["excess"]) & np.isfinite(s["fc"])]
    n_cases = int(len(s))

    # ---------- main measure ----------
    slope = None
    tstat = None
    if n_cases >= 3:
        x = s["fc"].to_numpy(float)
        y = s["excess"].to_numpy(float)
        xm = x - x.mean()
        sxx = float((xm ** 2).sum())
        if sxx > 0:
            b = float((xm * (y - y.mean())).sum() / sxx)
            a = y.mean() - b * x.mean()
            resid = y - a - b * x
            sig2 = float((resid ** 2).sum() / (n_cases - 2))
            se = np.sqrt(sig2 / sxx)
            slope = b
            tstat = b / se if se > 0 else None

    # ---------- supporting check ----------
    coef_v = None
    sup_pass = None
    n_sup = 0
    if len(s):
        ss = s.dropna(subset=["vratio", "fall", "excess"])
        ss = ss[np.isfinite(ss["vratio"]) & np.isfinite(ss["fall"])]
        n_sup = int(len(ss))
        if n_sup >= 4:
            X = np.column_stack([np.ones(n_sup), ss["vratio"].to_numpy(float), ss["fall"].to_numpy(float)])
            y = ss["excess"].to_numpy(float)
            if np.linalg.matrix_rank(X) == 3:
                beta, *_ = np.linalg.lstsq(X, y, rcond=None)
                coef_v = float(beta[1])
                sup_pass = bool(coef_v > 0)

    # ---------- decision ----------
    if n_cases < MIN_CASES:
        status = "not observable"
        decided = f"Only {n_cases} independent cases with forecast > 0 on the grid, below the plan's minimum of {MIN_CASES}."
    elif tstat is None:
        status = "inconclusive"
        decided = "The slope t could not be computed (no variation in the forecast), so neither the confirm nor the reject rule is met."
    elif tstat >= 2:
        if sup_pass:
            status = "confirmed"
            decided = "The slope t is 2 or more and the volume-ratio coefficient in the supporting regression is positive."
        else:
            status = "inconclusive"
            decided = "The slope t is 2 or more but the volume-ratio coefficient is not positive, which the plan calls inconclusive."
    elif tstat <= -2:
        status = "rejected"
        decided = "The slope t is -2 or less."
    else:
        status = "inconclusive"
        decided = "The slope t lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": _f(agreement), "passed": bool(passed)},
        "main_measure": {
            "name": "OLS slope of 3-bar excess return on forecast",
            "value": _f(slope),
            "statistic": {"name": "OLS slope t", "value": _f(tstat)} if tstat is not None else None,
            "threshold": "slope t >= 2 confirms (with positive volume-ratio coefficient); t <= -2 rejects; otherwise inconclusive",
        },
        "supporting_check": {
            "name": "volume-ratio coefficient in excess ~ volume ratio + fall size",
            "value": _f(coef_v),
            "passed": sup_pass,
        },
        "counts": {
            "independent cases with forecast > 0 on the grid": n_cases,
            "cases in the supporting regression": n_sup,
        },
        "decided_by": decided,
        "reading": "The coin's mean 3-bar return is the mean of its non-overlapping grid 3-bar returns over all windows; the volume ratio is the bar's volume over the mean of the last 30 volumes including it, and the fall size is minus the bar's return over the 20-bar standard deviation of daily returns including it, both computed within each window (bars without full history left out of the supporting regression, which has an intercept); fewer than 100 cases is reported as not observable.",
    }
