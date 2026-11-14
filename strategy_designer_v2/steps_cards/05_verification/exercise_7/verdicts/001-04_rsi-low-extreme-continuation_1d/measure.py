import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    RAW = "debug_info.components.rsi_low.last_history_value"
    FC = "forecast"
    POS = "postRebalance_current_allocation"

    def fnum(x):
        try:
            x = float(x)
        except Exception:
            return None
        return None if not np.isfinite(x) else x

    def wilder_rsi(close, period=14):
        d = close.diff()
        up = d.clip(lower=0.0)
        dn = (-d).clip(lower=0.0)
        au = up.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        ad = dn.ewm(alpha=1.0 / period, adjust=False, min_periods=period).mean()
        rs = au / ad
        rsi = 100.0 - 100.0 / (1.0 + rs)
        rsi = rsi.where(~((ad == 0) & (au > 0)), 100.0)
        rsi = rsi.where(~((ad == 0) & (au == 0)), 50.0)
        return rsi

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if FC not in df.columns or RAW not in df.columns:
                continue
            sub = df[[FC, RAW]].dropna()
            active = sub[FC] != 0
            n_active += int(active.sum())
            ok = active & (sub[RAW] > 0) & (sub[FC] < 0)
            n_agree += int(ok.sum())
    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = n_active > 0 and agreement >= 0.90

    main_name = "pooled 5-bar forward return after extreme bars (raw >= 8) minus after neutral bars (RSI 40-60)"
    threshold = "confirm if difference < 0 with Welch t <= -2 and negative in at least 2 coins; reject if difference >= 0"

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": "The plan's situation is RSI below 50 (raw component > 0) with a short position, "
                          "but fewer than 90% of the active bars (forecast != 0) are such bars with a negative forecast.",
            "reading": "none",
        }

    # ---------- 2. main measure ----------
    ext_all, neu_all = [], []
    per_coin = {}
    for coin, wins in bars.items():
        ext_c, neu_c = [], []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            rsi = wilder_rsi(close, 14)
            fwd = close.shift(-H) / close - 1.0
            raw = df[RAW].astype(float) if RAW in df.columns else pd.Series(np.nan, index=df.index)
            grid = np.arange(0, len(df), H)
            for i in grid:
                r = fwd.iloc[i]
                if not np.isfinite(r):
                    continue
                rv = raw.iloc[i]
                if np.isfinite(rv) and rv >= 8:
                    ext_c.append(r)
                ri = rsi.iloc[i]
                if np.isfinite(ri) and 40 <= ri <= 60:
                    neu_c.append(r)
        per_coin[coin] = (ext_c, neu_c)
        ext_all += ext_c
        neu_all += neu_c

    ext_all = np.array(ext_all)
    neu_all = np.array(neu_all)
    diff = np.nan
    tstat = np.nan
    if len(ext_all) > 0 and len(neu_all) > 0:
        diff = ext_all.mean() - neu_all.mean()
    if len(ext_all) >= 2 and len(neu_all) >= 2:
        tstat = stats.ttest_ind(ext_all, neu_all, equal_var=False).statistic

    coin_diffs = {}
    for coin, (e, n) in per_coin.items():
        if len(e) > 0 and len(n) > 0:
            coin_diffs[coin] = float(np.mean(e) - np.mean(n))
        else:
            coin_diffs[coin] = np.nan
    n_neg_coins = int(sum(1 for v in coin_diffs.values() if np.isfinite(v) and v < 0))

    counts = {"non-overlapping extreme cases pooled": int(len(ext_all)),
              "non-overlapping neutral cases pooled": int(len(neu_all)),
              "coins with negative difference": n_neg_coins}
    for coin, (e, n) in per_coin.items():
        counts[f"extreme cases {coin}"] = int(len(e))

    # ---------- 3. supporting check ----------
    excess = {}
    for coin, wins in bars.items():
        strat = 0.0
        all_pos = []
        rets_sum = 0.0
        pieces = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            r1 = close.shift(-1) / close - 1.0
            pos = df[POS].astype(float)
            m = pos.notna() & r1.notna()
            strat += float((pos[m] * r1[m]).sum())
            all_pos.append(pos[m].values)
            pieces.append(r1[m].values)
        if all_pos:
            ap = np.concatenate(all_pos)
            rr = np.concatenate(pieces)
            if len(ap) > 0:
                avg = float(ap.mean())
                excess[coin] = strat - avg * float(rr.sum())
    sup_vals = [v for v in excess.values() if np.isfinite(v)]
    sup_val = float(np.mean(sup_vals)) if sup_vals else None
    sup_pass = (all(v > 0 for v in sup_vals) if sup_vals else None)

    # ---------- 4. decision ----------
    too_few = len(ext_all) < 30 or any(len(e) < 8 for e, _ in per_coin.values())
    if too_few:
        status = "inconclusive"
        decided = "Fewer than 30 non-overlapping extreme cases pooled, or fewer than 8 for a coin: inconclusive whatever the sign."
    elif not np.isfinite(diff):
        status = "inconclusive"
        decided = "The extreme-minus-neutral difference could not be computed (no neutral cases), so no rule is met."
    elif diff >= 0:
        status = "rejected"
        decided = "The pooled extreme-minus-neutral 5-bar return is >= 0: reject."
    elif np.isfinite(tstat) and tstat <= -2 and n_neg_coins >= 2:
        status = "confirmed"
        decided = "The pooled extreme-minus-neutral 5-bar return is below 0 with t <= -2 and negative in at least 2 coins: confirm."
    else:
        status = "inconclusive"
        decided = "A negative pooled difference but with t between -2 and 0, or coins that disagree in sign: inconclusive."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {
            "name": main_name,
            "value": fnum(diff),
            "statistic": {"name": "Welch t", "value": fnum(tstat)} if np.isfinite(tstat) else None,
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "per-coin strategy cumulative return before costs minus same-average-size short hold (mean over coins; passes if positive for every coin)",
            "value": sup_val,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": "Neutral RSI is Wilder RSI(14) recomputed from each window's own closes (first 14 bars of a window have none), "
                   "the 'at least 2 of the 3 coins' and 'fewer than 8 for any coin' rules are applied to the coins present in the record, "
                   "and cumulative return is the sum of per-bar position gains across windows.",
    }
