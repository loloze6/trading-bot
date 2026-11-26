import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in H}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
            lr = pd.Series(np.log(c)).diff()
            sd = lr.rolling(30).std().values
            r3 = np.full(n, np.nan); r3[3:] = c[3:] / c[:-3] - 1
            inprof = (df["regime"].astype(str) == "unknown").values
            for h in H:
                for i in range(0, n - h, h):
                    if not inprof[i] or not np.isfinite(sd[i]) or not (r3[i] > 0):
                        continue
                    rows.append({"coin": coin, "win": w, "h": h,
                                 "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 "z": r3[i] / (sd[i] * np.sqrt(3)), "r3": r3[i],
                                 "f": c[i + h] / c[i] - 1, "usd": sd[i]})
        drift[coin] = {h: np.mean(allr[h]) for h in H}
    d = pd.DataFrame(rows)
    d["u"] = -(d["f"] - d.apply(lambda r: drift[r["coin"]][r["h"]], axis=1))
    d["share"] = d["u"] / d["r3"]
    out = {}
    def summ(g):
        x = g["u"]
        sl = stats.linregress(g["z"], g["u"]) if len(g) > 3 else None
        return pd.Series({"n": len(g), "u_mean%": 100 * x.mean(),
                          "u_t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "spearman_z_u": stats.spearmanr(g["z"], g["u"])[0] if len(g) > 3 else np.nan,
                          "slope_t": sl.slope / sl.stderr if sl is not None and sl.stderr > 0 else np.nan})
    out["by_h"] = d.groupby("h").apply(summ)
    d1 = d[d["h"] == 1].copy()
    d1["zq"] = pd.qcut(d1["z"], 4, labels=["q1", "q2", "q3", "q4"])
    out["h1_by_zq"] = d1.groupby("zq").apply(summ)
    out["h1_by_year"] = d1.groupby("year").apply(summ)
    out["h1_by_coin"] = d1.groupby("coin").apply(summ)
    top = d1[d1["zq"].isin(["q3", "q4"])]["share"]; bot = d1[d1["zq"].isin(["q1", "q2"])]["share"]
    out["h1_share_top_minus_bot"] = pd.Series({"top_mean": top.mean(), "bot_mean": bot.mean(),
        "welch_t": stats.ttest_ind(top, bot, equal_var=False).statistic})
    d2 = d[d["h"] == 2].copy()
    d2["zq"] = pd.qcut(d2["z"], 4, labels=["q1", "q2", "q3", "q4"])
    out["h2_by_zq"] = d2.groupby("zq").apply(summ)
    return out
