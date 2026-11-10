import numpy as np
import pandas as pd


def measure(bars):
    def comp_col(df):
        pref = "debug_info.components.sma_spread.last_history_value"
        if pref in df.columns:
            return pref
        cands = [c for c in df.columns
                 if c.startswith("debug_info.components.") and c.endswith(".last_history_value")]
        return cands[0] if cands else None

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            col = comp_col(df)
            f = pd.to_numeric(df["forecast"], errors="coerce")
            raw = pd.to_numeric(df[col], errors="coerce") if col is not None else pd.Series(np.nan, index=df.index)
            act = f.notna() & (f != 0)
            n_active += int(act.sum())
            # situation: 50-SMA below 200-SMA (raw spread < 0), expected side short (forecast < 0)
            n_agree += int((act & (raw < 0) & (f < 0)).sum())
    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": "|forecast|-weighted mean of next-bar return minus coin mean, short bars",
                             "value": None, "statistic": None,
                             "threshold": "t <= -2 confirms, t >= +2 rejects"},
            "supporting_check": None,
            "counts": {"active bars": n_active},
            "decided_by": ("The plan's situation is the 50-day SMA below the 200-day SMA with a short position, "
                           "but fewer than 90% of the bars with a nonzero forecast are short bars on which the raw "
                           "SMA spread is negative (the forecast is the spread standardised against its own past "
                           "values and clipped at 0, so it goes short whenever the spread is below its recent mean, "
                           "not only when the 50-day SMA is under the 200-day SMA)."),
            "reading": ("Situation taken as raw component value (50-SMA minus 200-SMA as % of 200-SMA) < 0, "
                        "with forecast < 0 as the expected short side."),
        }

    # ---------- 2. Criterion ----------
    all_rets = []
    act_rets, act_w = [], []
    n_stretches = 0
    for coin, wins in bars.items():
        coin_all = []
        coin_act = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            col = comp_col(df)
            raw = pd.to_numeric(df[col], errors="coerce").values if col is not None else np.full(len(df), np.nan)
            nxt = np.full(len(df), np.nan)
            if len(df) > 1:
                nxt[:-1] = close[1:] / close[:-1] - 1.0
            ok = np.isfinite(nxt)
            coin_all.extend(nxt[ok].tolist())
            a = ok & np.isfinite(f) & (f < 0)
            coin_act.append((nxt[a], np.abs(f[a])))
            # separate down-cross stretches: runs of raw spread < 0 that contain at least one active bar
            below = np.isfinite(raw) & (raw < 0)
            i = 0
            n = len(df)
            while i < n:
                if below[i]:
                    j = i
                    while j < n and below[j]:
                        j += 1
                    if np.any(a[i:j]):
                        n_stretches += 1
                    i = j
                else:
                    i += 1
        mu = float(np.mean(coin_all)) if len(coin_all) else np.nan
        all_rets.extend(coin_all)
        for r, wt in coin_act:
            act_rets.extend((r - mu).tolist())
            act_w.extend(wt.tolist())

    x = np.asarray(act_rets, float)
    wts = np.asarray(act_w, float)
    n_act = int(len(x))

    value, tstat = None, None
    if n_act >= 2 and wts.sum() > 0:
        m = float(np.sum(wts * x) / np.sum(wts))
        var = float(np.sum(wts * (x - m) ** 2) / np.sum(wts))
        n_eff = float(wts.sum() ** 2 / np.sum(wts ** 2))
        if n_eff > 1:
            var *= n_eff / (n_eff - 1.0)
        se = np.sqrt(var / n_eff) if n_eff > 0 else np.nan
        value = m
        tstat = float(m / se) if (np.isfinite(se) and se > 0) else None

    # supporting check: share of down bars on active bars vs all bars (binomial z)
    allr = np.asarray(all_rets, float)
    raw_act = x  # sign of excess differs from sign of return; recompute down share on raw returns
    # rebuild raw active returns
    act_raw = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce").values
            f = pd.to_numeric(df["forecast"], errors="coerce").values
            nxt = np.full(len(df), np.nan)
            if len(df) > 1:
                nxt[:-1] = close[1:] / close[:-1] - 1.0
            a = np.isfinite(nxt) & np.isfinite(f) & (f < 0)
            act_raw.extend(nxt[a].tolist())
    act_raw = np.asarray(act_raw, float)
    z = None
    sup_passed = None
    if len(allr) > 0 and len(act_raw) > 0:
        p0 = float(np.mean(allr < 0))
        pa = float(np.mean(act_raw < 0))
        if 0 < p0 < 1:
            z = float((pa - p0) / np.sqrt(p0 * (1 - p0) / len(act_raw)))
            sup_passed = bool(z >= 2.0)

    if n_act < 100 or n_stretches < 2 or tstat is None:
        status = "inconclusive"
        decided_by = ("Inconclusive: fewer than 100 active bars or fewer than 2 separate down-cross stretches "
                      "across the 6 windows (or no t-statistic could be computed).")
    elif value < 0 and tstat <= -2:
        status = "confirmed"
        decided_by = "Confirm: the weighted excess return is negative with t <= -2, so the short gains beyond the coin's drift."
    elif value > 0 and tstat >= 2:
        status = "rejected"
        decided_by = "Reject: the weighted excess return is positive with t >= +2, so prices rise more than usual in down-cross stretches."
    else:
        status = "inconclusive"
        decided_by = "Inconclusive: t lies strictly between -2 and +2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {"name": "|forecast|-weighted mean of next-bar return minus coin mean, short bars",
                         "value": value,
                         "statistic": ({"name": "t of weighted mean", "value": tstat} if tstat is not None else None),
                         "threshold": "t <= -2 with negative mean confirms; t >= +2 with positive mean rejects"},
        "supporting_check": {"name": "down-bar share on active vs all bars (binomial z)",
                             "value": z, "passed": sup_passed},
        "counts": {"active bars": n_act, "down-cross stretches": int(n_stretches)},
        "decided_by": decided_by,
        "reading": ("Coin mean taken over all tested bars of all windows; t of the weighted mean uses the weighted "
                    "variance with Kish effective n; a down-cross stretch is a run of bars with negative raw SMA "
                    "spread containing an active bar; the supporting check passes when z >= 2."),
    }
