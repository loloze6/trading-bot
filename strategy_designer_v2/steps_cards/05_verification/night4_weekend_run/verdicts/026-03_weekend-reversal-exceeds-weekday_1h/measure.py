import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 48
    LHV = "debug_info.components.wkend_ret.last_history_value"

    def _prep(df):
        df = df.sort_values("timestamp").reset_index(drop=True).copy()
        ts = pd.to_datetime(df["timestamp"], utc=True)
        end = ts + pd.Timedelta(hours=1)  # the bar's close time = next bar's start
        df["_end_dow"] = end.dt.dayofweek.values
        df["_end_hour"] = end.dt.hour.values
        df["_end_min"] = end.dt.minute.values
        close = df["close"].astype(float)
        df["_past"] = close / close.shift(H) - 1.0
        df["_next"] = close.shift(-H) / close - 1.0
        df["_fc"] = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
        if LHV in df.columns:
            raw = pd.to_numeric(df[LHV], errors="coerce")
        else:
            raw = pd.Series(np.nan, index=df.index)
        df["_raw"] = raw.where(raw.notna(), df["_past"])
        return df

    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepped = {}
    for coin, wins in bars.items():
        prepped[coin] = {}
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            d = _prep(df)
            prepped[coin][w] = d
            active = d["_fc"] != 0
            situ = (d["_end_dow"] == 0) & (d["_end_hour"] == 0) & (d["_end_min"] == 0)
            raw = d["_raw"]
            side_ok = (raw.notna()) & (raw != 0) & (np.sign(d["_fc"]) == -np.sign(raw))
            n_active += int(active.sum())
            n_agree += int((active & situ & side_ok).sum())

    agreement = float(n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "mean reversal score, weekend (Mon 00:00) minus weekday (Wed/Fri 00:00) cases"
    main_thr = "Welch t >= 2 to confirm (with supporting check t >= 2); t <= -2 rejects"
    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("Fewer than 90% of the active forecast bars are bars closing at Monday 00:00 UTC "
                           "with the forecast opposite to the 48-bar weekend return, as the Fidelity's situation "
                           "and reversal side require." if n_active > 0 else
                           "The forecast is never non-zero, so the plan's weekend situation is never traded."),
            "reading": "The situation bar is the bar whose close (timestamp + 1h) is Monday 00:00 UTC; the expected side is minus the sign of the raw 48-bar return.",
        }

    # ---------- 2. criterion ----------
    wk_scores, wd_scores = [], []
    sup_vals, sup_w = [], []
    for coin, wins in prepped.items():
        # coin's usual 48-bar move and normal drift: non-overlapping grid of all its windows
        grid = []
        for w, d in wins.items():
            c = d["close"].astype(float).values
            idx = np.arange(0, len(c) - H, H)
            if len(idx):
                r = c[idx + H] / c[idx] - 1.0
                grid.extend(list(r[np.isfinite(r)]))
        grid = np.asarray(grid, dtype=float)
        if len(grid) < 2:
            continue
        usual = float(np.std(grid, ddof=1))
        drift = float(np.mean(grid))
        if not np.isfinite(usual) or usual <= 0:
            continue
        for w, d in wins.items():
            ok = d["_past"].notna() & d["_next"].notna() & (d["_end_hour"] == 0) & (d["_end_min"] == 0)
            score = -(d["_past"] / usual) * ((d["_next"] - drift) / usual)
            wk = ok & (d["_end_dow"] == 0)
            wd = ok & d["_end_dow"].isin([2, 4])
            wk_scores.extend(list(score[wk].values))
            wd_scores.extend(list(score[wd].values))
            sp = wk & (d["_fc"] != 0)
            if sp.any():
                f = d.loc[sp, "_fc"].values
                v = np.sign(f) * (d.loc[sp, "_next"].values - drift)
                sup_vals.extend(list(v))
                sup_w.extend(list(np.abs(f)))

    wk_scores = np.asarray(wk_scores, float)
    wd_scores = np.asarray(wd_scores, float)
    wk_scores = wk_scores[np.isfinite(wk_scores)]
    wd_scores = wd_scores[np.isfinite(wd_scores)]
    n_wk, n_wd = int(len(wk_scores)), int(len(wd_scores))

    diff, t_diff = None, None
    if n_wk >= 2 and n_wd >= 2:
        diff = float(wk_scores.mean() - wd_scores.mean())
        t = stats.ttest_ind(wk_scores, wd_scores, equal_var=False).statistic
        t_diff = float(t) if np.isfinite(t) else None

    sup_vals = np.asarray(sup_vals, float)
    sup_w = np.asarray(sup_w, float)
    m = np.isfinite(sup_vals) & np.isfinite(sup_w)
    sup_vals, sup_w = sup_vals[m], sup_w[m]
    n_sup = int(len(sup_vals))
    sup_mean, sup_t = None, None
    if n_sup >= 2 and sup_w.sum() > 0:
        sup_mean = float(np.sum(sup_vals * sup_w) / np.sum(sup_w))
        prod = sup_vals * sup_w
        sd = np.std(prod, ddof=1)
        if sd > 0:
            sup_t = float(prod.mean() / (sd / np.sqrt(n_sup)))
    sup_pass = None if sup_t is None else bool(sup_mean > 0 and sup_t >= 2)

    counts = {"weekend cases": n_wk, "weekday cases": n_wd, "weekend cases with a forecast": n_sup}

    if n_wk < 300 or n_wd < 300:
        status = "not observable"
        decided = f"The plan needs at least 300 weekend and 300 weekday cases; the record has {n_wk} and {n_wd}."
    elif t_diff is not None and t_diff >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "The weekend-minus-weekday difference has Welch t >= 2 and the weekend unusual move in the forecast's direction has a positive mean with t >= 2."
    elif (t_diff is not None and t_diff <= -2) or (sup_t is not None and sup_t <= -2):
        status = "rejected"
        decided = "Either the weekend-minus-weekday difference has t <= -2 or the weekend cases' unusual move in the forecast's direction has t <= -2."
    else:
        status = "inconclusive"
        decided = "Neither the confirm rule (difference t >= 2 with the weekend check passing) nor the reject rule (a t <= -2) is met."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": diff,
            "statistic": None if t_diff is None else {"name": "Welch t", "value": t_diff},
            "threshold": main_thr,
        },
        "supporting_check": {
            "name": "weekend unusual 48-bar move in forecast direction, |forecast|-weighted mean",
            "value": sup_mean,
            "passed": sup_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": ("Cases are bars whose close (timestamp + 1h) is Monday, Wednesday or Friday 00:00 UTC with 48 bars "
                    "before and after inside the window (positional close[t±48]); the usual move and drift are the std and mean "
                    "of the coin's 48-bar returns on a non-overlapping grid of all its windows; the supporting check uses the "
                    "weekend cases with a non-zero forecast, and its t is the ordinary t of the |forecast|-weighted values; "
                    "the plan's minimum of 300 cases per group is applied as 'not observable'."),
    }
