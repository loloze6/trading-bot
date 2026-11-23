import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    WE_RAW = "debug_info.components.fall_we.last_history_value"
    WD_RAW = "debug_info.components.fall_wd.last_history_value"

    # ---------- collect rows ----------
    rows = []
    coin_rets = {}
    for coin, wins in bars.items():
        rets_all = []
        for w, df in wins.items():
            d = df.copy()
            if "timestamp" in d.columns:
                d = d.sort_values("timestamp").reset_index(drop=True)
            close = pd.to_numeric(d["close"], errors="coerce")
            nxt = close.shift(-1) / close - 1.0  # inside the window only
            rets_all.append(nxt.dropna().values)
            raw_we = pd.to_numeric(d[WE_RAW], errors="coerce") if WE_RAW in d.columns else pd.Series(np.nan, index=d.index)
            raw_wd = pd.to_numeric(d[WD_RAW], errors="coerce") if WD_RAW in d.columns else pd.Series(np.nan, index=d.index)
            raw = raw_we.where(raw_we.notna(), raw_wd)
            ts = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            out = pd.DataFrame({
                "coin": coin,
                "forecast": pd.to_numeric(d["forecast"], errors="coerce").fillna(0.0).values,
                "regime": d["regime"].astype(str).values,
                "raw": raw.values,
                "dow": ts.dt.dayofweek.values,
                "ret": nxt.values,
            })
            rows.append(out)
        coin_rets[coin] = np.concatenate(rets_all) if rets_all else np.array([])

    if not rows:
        return {"status": "not observable", "situation_check": {"agreement": None, "passed": False},
                "main_measure": None, "supporting_check": None, "counts": {},
                "decided_by": "no bars in the record", "reading": "none"}
    all_df = pd.concat(rows, ignore_index=True)

    # ---------- situation check ----------
    active = all_df[all_df["forecast"] != 0]
    n_active = len(active)
    if n_active > 0:
        is_weekend_day = active["dow"].isin([5, 6])
        regime_ok = np.where(active["regime"] == "mean_reversion", is_weekend_day, ~is_weekend_day)
        situation = (active["raw"] > 0) & regime_ok
        on_side = active["forecast"] > 0
        agreement = float((situation & on_side).mean())
    else:
        agreement = 0.0
    passed = agreement >= 0.9

    reading = ("Situation bars are those whose recorded raw fall-times-volume value is above 0 with the regime "
               "matching the bar's own day (mean_reversion on Saturday/Sunday bars, unknown otherwise), expected side long; "
               "the regressions pool all coins and windows with every bar as a 1-bar case, the coin's mean daily return "
               "taken over all its windows, and the difference t is (b_we - b_wd)/sqrt(se_we^2 + se_wd^2).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": None,
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": ("fewer than 90% of active bars are positive-fall-volume bars in the regime of their own "
                           "weekday (weekend vs weekday) with a long forecast, so the config does not do what the "
                           "Fidelity says"),
            "reading": reading,
        }

    # ---------- criterion ----------
    mean_ret = {c: (float(np.mean(r)) if len(r) else np.nan) for c, r in coin_rets.items()}
    all_df["excess"] = all_df["ret"] - all_df["coin"].map(mean_ret)
    base = all_df[(all_df["forecast"] > 0) & all_df["excess"].notna()]
    we = base[base["regime"] == "mean_reversion"]
    wd = base[base["regime"] == "unknown"]
    n_we, n_wd = int(len(we)), int(len(wd))

    def reg(g):
        if len(g) < 3 or np.var(g["forecast"].values) == 0:
            return None, None, None
        r = stats.linregress(g["forecast"].values, g["excess"].values)
        se = float(r.stderr)
        t = float(r.slope / se) if se > 0 else None
        return float(r.slope), se, t

    b_we, se_we, t_we = reg(we)
    b_wd, se_wd, t_wd = reg(wd)
    diff = t_diff = None
    if b_we is not None and b_wd is not None:
        diff = b_we - b_wd
        den = np.sqrt(se_we ** 2 + se_wd ** 2)
        t_diff = float(diff / den) if den > 0 else None

    counts = {"weekend cases with forecast > 0": n_we, "weekday cases with forecast > 0": n_wd}
    main = {"name": "weekend-regime slope of next-day excess return on forecast",
            "value": b_we,
            "statistic": {"name": "OLS slope t", "value": t_we} if t_we is not None else None,
            "threshold": "confirm t >= 2 (with difference t >= 2); reject t <= -2"}
    supp = {"name": "weekend slope minus weekday slope (Welch-style t)",
            "value": diff,
            "passed": (t_diff >= 2) if t_diff is not None else None}
    sc = {"agreement": agreement, "passed": True}

    if n_we < 200 or n_wd < 200:
        status = "not observable"
        decided = f"minimum of 200 weekend and 200 weekday cases with forecast > 0 not reached ({n_we}, {n_wd})"
    elif t_we is None or t_diff is None:
        status = "inconclusive"
        decided = "a slope t could not be computed, so neither the confirm nor the reject rule is met"
    elif t_we <= -2 or t_diff <= -2:
        status = "rejected"
        decided = (f"reject rule: weekend slope t {t_we:.2f} <= -2 or weekend-minus-weekday difference t "
                   f"{t_diff:.2f} <= -2")
    elif t_we >= 2 and t_diff >= 2:
        status = "confirmed"
        decided = (f"confirm rule: weekend slope t {t_we:.2f} >= 2 and weekend-minus-weekday difference t "
                   f"{t_diff:.2f} >= 2")
    else:
        status = "inconclusive"
        decided = (f"inconclusive rule: weekend slope t {t_we:.2f} and difference t {t_diff:.2f} meet neither "
                   f"the confirm nor the reject rule")

    return {"status": status, "situation_check": sc, "main_measure": main, "supporting_check": supp,
            "counts": counts, "decided_by": decided, "reading": reading}
