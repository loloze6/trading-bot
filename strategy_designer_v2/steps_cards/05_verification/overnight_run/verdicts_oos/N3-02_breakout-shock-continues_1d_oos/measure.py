import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    H = 5
    FC = "forecast"
    LHV = "debug_info.components.shock.last_history_value"

    total_active = 0
    agree_active = 0
    coin_frames = {}

    for coin, wins in bars.items():
        coin_frames[coin] = {}
        for w, df in wins.items():
            d = df.reset_index(drop=True).copy()
            close = pd.to_numeric(d["close"], errors="coerce")
            fc = pd.to_numeric(d[FC], errors="coerce")
            n = len(d)

            # Situation: close is the highest close of the current bar and the prior 20 bars.
            rmax = close.rolling(21, min_periods=21).max()
            nh_price = close >= rmax * (1 - 1e-12)
            computable = rmax.notna() & close.notna()
            regime_trend = d["regime"].astype(str).str.lower().eq("trending") if "regime" in d.columns else pd.Series(False, index=d.index)
            new_high = pd.Series(np.where(computable, nh_price, regime_trend), index=d.index).astype(bool)

            # Up day: positive one-day return (from prices; first row falls back to the recorded raw value).
            r1 = close.pct_change() * 100.0
            if LHV in d.columns:
                lhv = pd.to_numeric(d[LHV], errors="coerce")
                r1_up = r1.where(r1.notna(), lhv)
            else:
                r1_up = r1
            up_day = r1_up > 0

            situation = new_high & up_day
            active = fc.notna() & (fc != 0)
            ok = active & situation & (fc > 0)
            total_active += int(active.sum())
            agree_active += int(ok.sum())

            # Standardised one-day return: r / mean|r| over its last 60 values (incl. current), min 20, scaled so average = 10.
            mabs = r1.abs().rolling(60, min_periods=20).mean()
            s = 10.0 * r1 / mabs.replace(0, np.nan)

            fwd = close.shift(-H) / close - 1.0
            coin_frames[coin][w] = {"fc": fc, "s": s, "fwd": fwd, "n": n}

    if total_active > 0:
        agreement = agree_active / total_active
    else:
        agreement = None
    passed = True if agreement is None else bool(agreement >= 0.9)

    reading = ("Situation recomputed from closes as close >= max of current and prior 20 closes within each window "
               "(regime=='trending' used where fewer than 21 bars exist) plus a positive one-day return, side long; "
               "the coin baseline is the mean of all bars' 5-bar forward returns pooled across its windows; signals "
               "within 5 bars (distance <= 5) of the last kept case are merged into it, the case being its first bar, "
               "and the same merging is applied to the inside-range group; the standardised return is 10 x r / mean|r| "
               "over the last 60 one-day returns including the current one (min 20); t is the ordinary t of the mean.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": "mean excess 5-bar return after shock-up new-high cases", "value": None,
                             "statistic": None, "threshold": "t >= 2 to confirm, t <= -2 to reject"},
            "supporting_check": None,
            "counts": {"non-overlapping cases pooled across coins": None},
            "decided_by": ("Fewer than 90% of bars with a non-zero forecast are long bars on a new 21-bar closing high "
                           "with an up day, so the config does not trade the plan's situation."),
            "reading": reading,
        }

    def merge(idx):
        kept = []
        last = None
        for i in idx:
            if last is None or i - last > H:
                kept.append(i)
                last = i
        return kept

    nh_ex = []
    in_ex = []
    for coin, wins in coin_frames.items():
        allf = pd.concat([v["fwd"] for v in wins.values()], ignore_index=True).dropna()
        if len(allf) == 0:
            continue
        base = float(allf.mean())
        for w, v in wins.items():
            fc, s, fwd = v["fc"], v["s"], v["fwd"]
            case_idx = list(np.where((fc >= 10).fillna(False).values)[0])
            for i in merge(case_idx):
                if pd.notna(fwd.iloc[i]):
                    nh_ex.append(float(fwd.iloc[i]) - base)
            in_mask = ((s >= 10) & (fc == 0)).fillna(False).values
            in_idx = list(np.where(in_mask)[0])
            for i in merge(in_idx):
                if pd.notna(fwd.iloc[i]):
                    in_ex.append(float(fwd.iloc[i]) - base)

    n_cases = len(nh_ex)
    n_in = len(in_ex)
    mean_ex = float(np.mean(nh_ex)) if n_cases > 0 else None
    t = None
    if n_cases >= 2:
        sd = float(np.std(nh_ex, ddof=1))
        if sd > 0:
            t = mean_ex / (sd / np.sqrt(n_cases))
        else:
            t = float(np.sign(mean_ex) * np.inf) if mean_ex != 0 else 0.0

    diff = None
    sup_pass = None
    if n_cases > 0 and n_in > 0:
        diff = mean_ex - float(np.mean(in_ex))
        sup_pass = bool(diff > 0)

    if n_cases < 30:
        status = "not observable"
        decided = f"Only {n_cases} non-overlapping cases pooled across coins, below the plan's minimum of 30."
    elif t is not None and mean_ex > 0 and t >= 2 and sup_pass is True:
        status = "confirmed"
        decided = "Mean excess 5-bar return after cases is positive with t >= 2 and the supporting difference is positive."
    elif t is not None and mean_ex < 0 and t <= -2:
        status = "rejected"
        decided = "Mean excess 5-bar return is negative with t <= -2: prices reverse after shock-up new highs."
    else:
        status = "inconclusive"
        if t is not None and t >= 2:
            decided = "t >= 2 but the supporting difference is not positive, so neither confirm nor reject is met."
        else:
            decided = "t lies between -2 and 2, which the plan calls inconclusive."

    def clean(x):
        if x is None:
            return None
        x = float(x)
        return x if np.isfinite(x) else (1e308 if x > 0 else -1e308)

    return {
        "status": status,
        "situation_check": {"agreement": None if agreement is None else float(agreement), "passed": passed},
        "main_measure": {
            "name": "mean excess 5-bar return after shock-up new-high cases (forecast >= 10), before costs",
            "value": clean(mean_ex),
            "statistic": None if t is None else {"name": "t of the mean", "value": clean(t)},
            "threshold": "confirm if mean > 0 with t >= 2 (and supporting difference > 0); reject if mean < 0 with t <= -2",
        },
        "supporting_check": {
            "name": "mean excess after new-high cases minus mean excess after inside-range shock-up days",
            "value": clean(diff),
            "passed": sup_pass,
        },
        "counts": {
            "non-overlapping cases pooled across coins": int(n_cases),
            "inside-range shock-up cases": int(n_in),
        },
        "decided_by": decided,
        "reading": reading,
    }
