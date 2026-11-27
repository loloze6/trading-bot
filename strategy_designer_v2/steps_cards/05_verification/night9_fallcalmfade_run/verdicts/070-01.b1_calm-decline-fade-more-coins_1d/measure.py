import numpy as np
import pandas as pd
from scipy import stats


def measure(bars):
    LHV = "debug_info.components.run_len.last_history_value"

    def get_lhv(df):
        if LHV in df.columns:
            return pd.to_numeric(df[LHV], errors="coerce")
        if "debug_info.components" in df.columns:
            def ext(x):
                try:
                    if isinstance(x, dict):
                        v = x.get("run_len", {})
                        if isinstance(v, dict):
                            return v.get("last_history_value", np.nan)
                except Exception:
                    pass
                return np.nan
            return pd.to_numeric(df["debug_info.components"].map(ext), errors="coerce")
        return pd.Series(np.nan, index=df.index)

    def run_from_closes(close):
        c = close.values
        n = len(c)
        out = np.full(n, np.nan)
        for t in range(1, n):
            if not (c[t] > c[t - 1]):
                out[t] = 0.0
                continue
            k = 0
            j = t - 1
            while j >= 1 and c[j] < c[j - 1] and k < 30:
                k += 1
                j -= 1
            out[t] = float(k)
        return out

    def run_from_lhv(p):
        p = np.asarray(p, dtype=float)
        out = np.full(len(p), np.nan)
        ok = np.isfinite(p)
        pc = np.clip(p[ok], 1e-15, 1 - 1e-15)
        n = np.log(pc / (1 - pc))
        n = np.where(p[ok] >= 1 - 1e-15, 30.0, n)
        out[ok] = np.round(n)
        return out

    rows = []
    n_active = 0
    n_agree = 0
    for coin, wins in bars.items():
        coin_rets = []
        coin_rows = []
        for w, df in wins.items():
            if df is None or len(df) == 0:
                continue
            df = df.reset_index(drop=True)
            close = pd.to_numeric(df["close"], errors="coerce")
            fc = pd.to_numeric(df["forecast"], errors="coerce").fillna(0.0)
            regime = df["regime"].astype(str)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            nxt = close.shift(-1) / close - 1.0
            coin_rets.append(nxt.dropna().values)

            rl = run_from_lhv(get_lhv(df).values)
            rc = run_from_closes(close)
            run = np.where(np.isfinite(rl), rl, rc)

            situation = (regime.values == "mean_reversion") & np.isfinite(run) & (run >= 1)
            active = fc.values != 0
            n_active += int(active.sum())
            n_agree += int((active & situation & (fc.values < 0)).sum())

            for i in range(len(df)):
                if fc.iloc[i] < 0 and np.isfinite(nxt.iloc[i]):
                    coin_rows.append({"coin": coin, "day": ts.iloc[i].floor("D"),
                                      "ret": float(nxt.iloc[i]),
                                      "run": float(run[i]) if np.isfinite(run[i]) else np.nan})
        if coin_rets:
            allr = np.concatenate(coin_rets)
            mu = float(np.mean(allr)) if len(allr) else np.nan
        else:
            mu = np.nan
        for r in coin_rows:
            r["excess"] = r["ret"] - mu
            r["short_excess"] = -(r["ret"] - mu)
            rows.append(r)

    agreement = (n_agree / n_active) if n_active > 0 else 0.0
    passed = bool(n_active > 0 and agreement >= 0.9)
    main_name = "mean next-day return beyond the coin's drift, short direction, on forecast<0 bars"
    main_thr = "above 0 with t >= 2 confirms; below 0 with t <= -2 rejects"
    reading = ("The falling-calm profile is read from the recorded regime ('mean_reversion' means both vetoes passed) "
               "since its components are not recorded, the run length from run_len's last_history_value (logit of the sigmoid) "
               "or from closes inside the window; the main mean is over cases with a t whose deviations are summed per day; "
               "the supporting check uses the unflipped excess return; 'fewer than 150 cases on fewer than 80 days' is read "
               "as two minimum counts, either one missed making the result not observable.")

    if not passed:
        return {
            "status": "mismatch",
            "situation_check": {"agreement": float(agreement), "passed": False},
            "main_measure": {"name": main_name, "value": None, "statistic": None, "threshold": main_thr},
            "supporting_check": None,
            "counts": {"active bars": int(n_active), "cases": None, "distinct days": None},
            "decided_by": ("Only {:.1%} of bars with a non-zero forecast are short run-break days in the falling calm "
                           "regime, below the 90% the plan's situation requires.").format(agreement),
            "reading": reading,
        }

    d = pd.DataFrame(rows)
    N = len(d)
    D = int(d["day"].nunique()) if N else 0

    main_val, main_t = None, None
    if N >= 2:
        x = d["short_excess"].values
        m = float(np.mean(x))
        dev = d.assign(e=x - m).groupby("day")["e"].sum().values
        if D > 1:
            se = np.sqrt(np.sum(dev ** 2) * D / (D - 1)) / N
            main_t = float(m / se) if se > 0 else None
        main_val = m

    sup_val, sup_t, sup_pass = None, None, None
    n_long, n_short = 0, 0
    if N:
        lg = d.loc[d["run"] >= 3, "excess"].dropna().values
        sh = d.loc[(d["run"] >= 1) & (d["run"] <= 2), "excess"].dropna().values
        n_long, n_short = len(lg), len(sh)
        if n_long >= 2 and n_short >= 2:
            sup_val = float(np.mean(lg) - np.mean(sh))
            tt = stats.ttest_ind(lg, sh, equal_var=False)
            sup_t = float(tt.statistic) if np.isfinite(tt.statistic) else None
            sup_pass = bool(sup_val < 0)

    counts = {"cases": int(N), "distinct days": int(D),
              "cases with runs of 3 or more": int(n_long), "cases with runs of 1 to 2": int(n_short)}
    supporting = {"name": "next-day excess return, runs >=3 minus runs 1-2 (Welch t {})".format(
                      "n/a" if sup_t is None else round(sup_t, 3)),
                  "value": sup_val, "passed": sup_pass}
    main = {"name": main_name, "value": main_val,
            "statistic": {"name": "t of the mean, cases summed per day", "value": main_t} if main_t is not None else None,
            "threshold": main_thr}
    base = {"situation_check": {"agreement": float(agreement), "passed": True},
            "main_measure": main, "supporting_check": supporting, "counts": counts, "reading": reading}

    if N < 150 or D < 80:
        return dict(base, status="not observable",
                    decided_by="The plan's minimum of 150 cases on 80 distinct days is not reached ({} cases, {} days).".format(N, D))
    if main_val is None or main_t is None:
        return dict(base, status="inconclusive", decided_by="The main t could not be computed, so neither confirm nor reject is met.")

    if main_val < 0 and main_t <= -2:
        return dict(base, status="rejected",
                    decided_by="Reject: the main measure is below 0 with t <= -2 (run-break days are followed by rises beyond the drift).")
    if sup_val is not None and sup_t is not None and sup_val > 0 and sup_t >= 2:
        return dict(base, status="rejected",
                    decided_by="Reject: the longer-minus-shorter difference is above 0 with t >= 2.")
    if main_val > 0 and main_t >= 2 and sup_pass is True:
        return dict(base, status="confirmed",
                    decided_by="Confirm: the main measure is above 0 with t >= 2 and the longer-minus-shorter difference is below 0.")
    if main_t >= 2:
        return dict(base, status="inconclusive",
                    decided_by="Inconclusive: main t >= 2 but the longer-minus-shorter difference is 0 or above (or could not be measured).")
    return dict(base, status="inconclusive", decided_by="Inconclusive: the main t lies between -2 and 2.")
