import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    RAW = "debug_info.components.dryup.last_history_value"

    def _regime_trending(df):
        if "regime" not in df.columns:
            return pd.Series(False, index=df.index)
        return df["regime"].astype(str).str.lower().str.strip().eq("trending")

    # ---------- 1. Situation check ----------
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float)
            fc = pd.to_numeric(df[FC], errors="coerce")
            trending = _regime_trending(df)

            # 20-day return in percent, from prices inside the window
            r20 = (close / close.shift(20) - 1.0) * 100.0
            r20_ok = (r20 >= -20.0) & (r20 < 0.0)
            # Not computable inside the window: fall back to the recorded regime
            r20_cond = r20_ok.where(r20.notna(), trending)

            # Falling profile: 60-day return below -10 %
            r60 = (close / close.shift(60) - 1.0) * 100.0
            prof_ok = r60 < -10.0
            prof_cond = prof_ok.where(r60.notna(), trending)

            # Volume shrunk: raw log ratio of 30-day mean volumes below 0
            if RAW in df.columns:
                raw = pd.to_numeric(df[RAW], errors="coerce")
            else:
                raw = pd.Series(np.nan, index=df.index)
            vol = df["volume"].astype(float)
            m_recent = vol.rolling(30, min_periods=30).mean()
            m_prior = vol.shift(30).rolling(30, min_periods=30).mean()
            with np.errstate(divide="ignore", invalid="ignore"):
                raw_re = np.log(m_recent / m_prior)
            raw = raw.where(raw.notna(), raw_re)
            shrink = (raw < 0).fillna(False)

            situation = r20_cond.fillna(False).astype(bool) & prof_cond.fillna(False).astype(bool) & shrink
            active = fc.fillna(0) != 0
            agree = active & situation & (fc < 0)
            n_active += int(active.sum())
            n_agree += int(agree.sum())

    agreement = float(n_agree / n_active) if n_active > 0 else None
    passed = bool(agreement is not None and agreement >= 0.90)

    main_name = "mean of (5-bar forward return minus coin mean 5-bar return) x forecast/10 on grid bars with forecast < 0"
    threshold = "confirm: mean > 0 with t >= 2 over >= 30 cases and check passes; reject: mean < 0 with t <= -2 over >= 30 cases"
    reading_base = ("Situation taken as 20-day return in [-20 %, 0 %), 60-day return below -10 % (the falling profile of the config's veto) "
                    "and a negative raw log volume ratio, short side, using the recorded regime where a window lacks the price history; "
                    "'inside the regime' read as bars whose recorded regime is 'trending', and the coin's mean 5-bar return taken "
                    "on the same non-overlapping grid over all its windows.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": agreement, "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": threshold},
            "supporting_check": None,
            "counts": {"active grid cases": None, "active bars": int(n_active)},
            "decided_by": ("Fewer than 90 % of the bars with a non-zero forecast are short bars in a moderate fall "
                           "(20-day return -20 % to 0 %, falling profile) with shrunk volume, as the Fidelity states."),
            "reading": reading_base,
        }

    # ---------- 2. Criterion ----------
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = df["close"].astype(float).values
            fc = pd.to_numeric(df[FC], errors="coerce").values
            trending = _regime_trending(df).values
            n = len(df)
            for i in range(0, n, H):
                if i + H >= n:
                    continue
                c0, c1 = close[i], close[i + H]
                if not (np.isfinite(c0) and np.isfinite(c1)) or c0 == 0:
                    continue
                rows.append({"coin": coin, "ret": c1 / c0 - 1.0, "fc": fc[i], "trending": bool(trending[i])})

    g = pd.DataFrame(rows, columns=["coin", "ret", "fc", "trending"])
    if len(g) > 0:
        g["mean_ret"] = g.groupby("coin")["ret"].transform("mean")
        g["excess"] = g["ret"] - g["mean_ret"]
    else:
        g["mean_ret"] = []
        g["excess"] = []

    act = g[g["fc"].notna() & (g["fc"] < 0)]
    prod = (act["excess"] * act["fc"] / 10.0).dropna().values
    n_cases = int(len(prod))

    mean_prod = float(np.mean(prod)) if n_cases > 0 else None
    t_prod = None
    if n_cases > 1:
        sd = float(np.std(prod, ddof=1))
        if sd > 0:
            t_prod = float(mean_prod / (sd / np.sqrt(n_cases)))

    reg = g[g["trending"] & g["fc"].notna()]
    shr = reg[reg["fc"] < 0]["excess"].dropna().values
    grw = reg[reg["fc"] == 0]["excess"].dropna().values
    if len(shr) > 0 and len(grw) > 0:
        diff = float(np.mean(shr) - np.mean(grw))
        chk_pass = bool(diff < 0)
    else:
        diff = None
        chk_pass = None

    counts = {
        "active grid cases": n_cases,
        "regime shrink grid bars": int(len(shr)),
        "regime growth grid bars": int(len(grw)),
    }

    if n_cases < 30:
        status = "not observable"
        decided = f"Fewer than 30 active grid cases ({n_cases}), the plan's minimum count."
    elif t_prod is None:
        status = "inconclusive"
        decided = "The t of the mean product cannot be computed (zero dispersion), so it is not beyond -2 or 2."
    elif mean_prod > 0 and t_prod >= 2:
        if chk_pass is True:
            status = "confirmed"
            decided = "The mean product is above 0 with t >= 2 over at least 30 cases and the shrink-minus-growth excess return is below 0."
        else:
            status = "inconclusive"
            decided = "The main measure meets the confirm rule but the supporting check fails (shrink-minus-growth excess return not below 0 or not computable)."
    elif mean_prod < 0 and t_prod <= -2:
        status = "rejected"
        decided = "The mean product is below 0 with t <= -2 over at least 30 cases."
    else:
        status = "inconclusive"
        decided = "The t of the mean product lies between -2 and 2."

    return {
        "status": status,
        "situation_check": {"agreement": agreement, "passed": True},
        "main_measure": {
            "name": main_name,
            "value": mean_prod,
            "statistic": ({"name": "t of the mean", "value": t_prod} if t_prod is not None else None),
            "threshold": threshold,
        },
        "supporting_check": {
            "name": "mean excess 5-bar return, shrink bars minus growth bars, inside the regime (must be < 0)",
            "value": diff,
            "passed": chk_pass,
        },
        "counts": counts,
        "decided_by": decided,
        "reading": reading_base,
    }
