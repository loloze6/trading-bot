import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
            usual[(coin, h)] = np.std(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values
            hi = df["high"]; lo = df["low"]
            prior_hi = hi.shift(1).rolling(60, min_periods=60).max().values
            mr = (hi - lo).rolling(60, min_periods=60).mean().values
            dist = (c - prior_hi) / mr
            ch = df["close"]
            er = ((ch - ch.shift(60)).abs() / ch.diff().abs().rolling(60).sum()).values
            ret60 = (ch / ch.shift(60) - 1).values
            # case detection: rise >=2 from lowest level since last bet / flat
            low = 0.0
            cand = np.zeros(len(f), bool)
            for i in range(len(f)):
                if f[i] <= 0:
                    low = 0.0; continue
                if f[i] - low >= 2:
                    cand[i] = True; low = f[i]
                else:
                    low = min(low, f[i])
            cell = np.arange(len(f)) // 5
            seen = set()
            for i in np.where(cand)[0]:
                if cell[i] in seen: continue
                seen.add(cell[i])
                r = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                     "fc": f[i], "dist": dist[i], "er": er[i], "ret60": ret60[i]}
                for h in H:
                    r[f"u{h}"] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < len(c) else np.nan
                rows.append(r)
    cs = pd.DataFrame(rows)
    def summ(g, col="u5"):
        x = g.dropna(subset=[col])
        d = x.groupby("day")[col].sum()
        n = len(x); D = len(d)
        m = x[col].mean() if n else np.nan
        t = (d.sum() / n) / (np.sqrt(D / (D - 1) * ((d - d.count() and 0) if False else 0) + 1e-18)) if False else np.nan
        # day-summed t
        dev = x.groupby("day")[col].apply(lambda s: (s - m).sum())
        se = np.sqrt(D / (D - 1) * (dev ** 2).sum()) / n if D > 1 else np.nan
        return pd.Series({"n": n, "days": D, "mean": m, "t": m / se if se else np.nan, "hit": (x[col] > 0).mean()})
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: summ(cs, f"u{h}") for h in H}).T
    out["by_coin_u5"] = cs.groupby("coin").apply(summ)
    out["by_window_u5"] = cs.groupby("win").apply(summ)
    cs["fc_q"] = pd.qcut(cs["fc"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_fc_quartile_u5"] = cs.groupby("fc_q").apply(summ)
    out["by_fc_quartile_u10"] = cs.groupby("fc_q").apply(lambda g: summ(g, "u10"))
    cs["dist_q"] = pd.qcut(cs["dist"].rank(method="first"), 4, labels=["d1", "d2", "d3", "d4"])
    out["by_dist_quartile_u5"] = cs.groupby("dist_q").apply(summ)
    out["dist_q_means"] = cs.groupby("dist_q")[["dist", "fc", "er"]].mean()
    cs["er_q"] = pd.qcut(cs["er"].rank(method="first"), 3, labels=["e1", "e2", "e3"])
    out["by_er_tercile_u5"] = cs.groupby("er_q").apply(summ)
    out["by_ret60_sign_u5"] = cs.groupby(np.sign(cs["ret60"])).apply(summ)
    out["corr"] = cs[["fc", "dist", "er", "ret60", "u1", "u5", "u10", "u20"]].corr().loc[["fc", "dist", "er", "ret60"], ["u1", "u5", "u10", "u20"]]
    return out
