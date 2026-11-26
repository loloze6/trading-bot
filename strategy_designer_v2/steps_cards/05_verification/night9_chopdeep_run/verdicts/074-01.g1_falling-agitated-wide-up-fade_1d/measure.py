import json
import numpy as np
import pandas as pd


def _comp_series(df, cid, field="last_history_value"):
    """Raw value of a strategy component, from the flat column or from the nested debug_info.components column."""
    flat = f"debug_info.components.{cid}.{field}"
    if flat in df.columns:
        return pd.to_numeric(df[flat], errors="coerce")
    if "debug_info.components" in df.columns:
        out = []
        for v in df["debug_info.components"].values:
            val = np.nan
            try:
                d = v
                if isinstance(d, str):
                    d = json.loads(d)
                if isinstance(d, dict) and cid in d and isinstance(d[cid], dict):
                    x = d[cid].get(field, np.nan)
                    val = float(x) if x is not None else np.nan
            except Exception:
                val = np.nan
            out.append(val)
        return pd.Series(out, index=df.index, dtype=float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def measure(bars):
    # ---------- 1. situation check ----------
    n_active = 0
    n_agree = 0
    prepared = {}
    for coin in sorted(bars):
        for w in sorted(bars[coin], key=lambda s: int(str(s).lstrip("w")) if str(s).lstrip("w").isdigit() else str(s)):
            df = bars[coin][w].copy().reset_index(drop=True)
            if len(df) == 0:
                continue
            for c in ["open", "high", "low", "close", "forecast"]:
                df[c] = pd.to_numeric(df[c], errors="coerce")
            df["ts"] = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
            up = df["close"] / df["close"].shift(1) - 1.0
            rng_px = (df["high"] - df["low"])
            mult_px = rng_px / rng_px.rolling(20, min_periods=20).mean()
            mult_rec = _comp_series(df, "width")
            mult = mult_rec.where(mult_rec.notna(), mult_px)
            determinable = up.notna() & mult.notna()
            situation = (up > 0) & (mult > 1.0)
            active = df["forecast"].notna() & (df["forecast"] != 0) & determinable
            n_active += int(active.sum())
            n_agree += int((active & situation & (df["forecast"] < 0)).sum())
            df["next_ret"] = df["close"].shift(-1) / df["close"] - 1.0
            prepared.setdefault(coin, []).append(df)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.90)
    reading = ("Situation computed from close-to-close return > 0 and the recorded width multiple (or high-low range over its "
               "20-bar mean incl. the bar, recomputed when unrecorded) > 1.0, bars where it cannot be computed left out; "
               "a case is a bar with forecast < 0 whose previous bar in the window is not < 0 (a window's first bar counts if < 0); "
               "the wider half is |forecast| strictly above the cases' median, the narrower at or below; "
               "the plan's 'fewer than 100 cases' is applied as the minimum count (not observable).")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean unusual next-day move, short direction", "value": None, "statistic": None,
                             "threshold": "mean > 0 with day-pooled t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"active bars": int(n_active)},
            "decided_by": (f"Only {agreement:.1%} of the active bars are up days with range above 1.0x its 20-day mean on the short "
                           "side, below the 90% the plan's situation requires."),
            "reading": reading,
        }

    # ---------- 2. criterion ----------
    rows = []
    for coin, dfs in prepared.items():
        all_ret = pd.concat([d["next_ret"] for d in dfs]).dropna()
        drift = float(all_ret.mean()) if len(all_ret) else np.nan
        for df in dfs:
            f = df["forecast"]
            prev = f.shift(1)
            turn = (f < 0) & ~(prev < 0)
            sel = df[turn & df["next_ret"].notna()]
            for _, r in sel.iterrows():
                rows.append({"coin": coin, "day": r["ts"].floor("D") if pd.notna(r["ts"]) else None,
                             "absf": abs(float(r["forecast"])),
                             "u": -(float(r["next_ret"]) - drift)})
    cases = pd.DataFrame(rows, columns=["coin", "day", "absf", "u"]).dropna(subset=["u"])
    n = int(len(cases))

    mean_u = float(cases["u"].mean()) if n else None
    t_val = None
    n_days = 0
    if n:
        day_sum = cases.groupby("day")["u"].sum()
        day_n = cases.groupby("day")["u"].size()
        n_days = int(len(day_sum))
        if n_days > 1:
            resid = day_sum - day_n * mean_u
            var = (resid ** 2).sum() * n_days / (n_days - 1)
            se = np.sqrt(var) / n
            t_val = float(mean_u / se) if se > 0 else None

    supp_val = None
    supp_pass = None
    n_wide = n_narrow = 0
    if n:
        med = cases["absf"].median()
        wide = cases[cases["absf"] > med]["u"]
        narrow = cases[cases["absf"] <= med]["u"]
        n_wide, n_narrow = int(len(wide)), int(len(narrow))
        if n_wide > 0 and n_narrow > 0:
            supp_val = float(wide.mean() - narrow.mean())
            supp_pass = bool(supp_val > 0)
        else:
            supp_pass = False

    if n < 100:
        status = "not observable"
        decided = f"Only {n} cases, fewer than the plan's 100."
    elif t_val is not None and mean_u > 0 and t_val >= 2:
        if supp_pass:
            status = "confirmed"
            decided = "Mean unusual move above 0 with t >= 2 and the wider half beats the narrower half: confirm rule met."
        else:
            status = "inconclusive"
            decided = "Confirming mean and t, but the wider-minus-narrower check fails: inconclusive by the plan."
    elif t_val is not None and mean_u < 0 and t_val <= -2:
        status = "rejected"
        decided = "Mean unusual move below 0 with t <= -2: the next day rises more than the coin's drift, reject rule met."
    else:
        status = "inconclusive"
        decided = "The t lies between -2 and 2: inconclusive by the plan."

    return {
        "status": status,
        "situation_check": {"agreement": float(agreement), "passed": True},
        "main_measure": {"name": "mean unusual next-day move, short direction",
                         "value": mean_u,
                         "statistic": ({"name": "t of the mean, cases of one day pooled", "value": t_val}
                                       if t_val is not None else None),
                         "threshold": "mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject"},
        "supporting_check": {"name": "wider half minus narrower half mean unusual move (|forecast| median split)",
                             "value": supp_val, "passed": supp_pass},
        "counts": {"cases": n, "days": n_days, "wider half cases": n_wide, "narrower half cases": n_narrow},
        "decided_by": decided,
        "reading": reading,
    }
