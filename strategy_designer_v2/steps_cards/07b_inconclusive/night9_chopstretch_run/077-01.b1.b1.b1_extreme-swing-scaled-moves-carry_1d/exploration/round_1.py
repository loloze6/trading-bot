import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    hs = [1, 3, 7, 14, 21]
    # coin normal drift per horizon over all windows, on non-overlapping grids
    for coin, wins in bars.items():
        for h in hs:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                vals.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(vals) if vals else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.swing_move.last_history_value")
            raw = raw.values if raw is not None else np.full(len(c), np.nan)
            reg = df["regime"].values
            n = len(c)
            # 14-day return / 30d swing recomputed
            r = pd.Series(c).pct_change()
            sd = r.rolling(30).std().values
            r14 = pd.Series(c).pct_change(14).values
            vs = r14 / (sd * np.sqrt(14))
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0, n - 7, 7):
                if reg[i] != "unknown" or not np.isfinite(f[i]) or f[i] == 0:
                    continue
                d = {"coin": coin, "w": w, "year": yr[i], "day": day[i], "f": f[i], "raw": raw[i], "vs": vs[i]}
                for h in hs:
                    if i + h < n:
                        d[f"u{h}"] = np.sign(f[i]) * (c[i + h] / c[i] - 1 - drift[(coin, h)])
                rows.append(d)
    t = pd.DataFrame(rows)
    t["af"] = t["f"].abs()
    t["side"] = np.where(t["f"] > 0, "long", "short")

    def summ(g):
        out = {"n": len(g), "days": g["day"].nunique()}
        for h in hs:
            x = g[f"u{h}"].dropna()
            out[f"m{h}"] = x.mean()
            out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)

    res = {}
    res["all"] = summ(t).to_frame().T
    res["by_side"] = t.groupby("side").apply(summ)
    t["q"] = pd.qcut(t["af"].rank(method="first"), 5, labels=False)
    res["by_absf_quintile"] = t.groupby("q").apply(summ)
    res["absf_quintile_ranges"] = t.groupby("q")["af"].agg(["min", "max"])
    t["vq"] = pd.qcut(t["vs"].abs().rank(method="first"), 5, labels=False)
    res["by_abs_vs_quintile"] = t.groupby("vq").apply(summ)
    res["by_side_q"] = t.groupby(["side", "q"]).apply(summ)[["n", "m7", "t7"]]
    res["by_coin"] = t.groupby("coin").apply(summ)[["n", "m3", "t3", "m7", "t7", "m14", "t14"]]
    res["by_year"] = t.groupby("year").apply(summ)[["n", "m3", "t3", "m7", "t7", "m14", "t14"]]
    res["corr_f_vs"] = float(np.corrcoef(t["f"], t["vs"].fillna(0))[0, 1])
    res["sign_agree_f_vs"] = float((np.sign(t["f"]) == np.sign(t["vs"])).mean())
    return res
