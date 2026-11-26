def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            ret7 = c / c.shift(7) - 1
            net30 = (c - c.shift(30)).abs()
            path30 = c.diff().abs().rolling(30, min_periods=20).sum()
            er = net30 / path30
            scaled = ret7 / (sd30 * np.sqrt(7))
            # causal rank of sd30 within the window so far (proxy of agitation vs own past)
            vrank = sd30.expanding(min_periods=20).rank(pct=True)
            ret30 = c / c.shift(30) - 1
            n = len(b)
            for h in (3, 7, 14):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    if i + h >= n: continue
                    rows.append(dict(coin=coin, w=w, h=h, day=str(b["timestamp"].iloc[i])[:10],
                                     regime=b["regime"].iloc[i], scaled=scaled.iloc[i],
                                     er=er.iloc[i], fwd=fwd.iloc[i], sd30=sd30.iloc[i],
                                     vrank=vrank.iloc[i], ret30=ret30.iloc[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["unus"] = d["fwd"] - d["drift"]
    d["usual"] = d.groupby(["coin", "h"])["fwd"].transform("std")
    d["mr"] = d["regime"] == "mean_reversion"
    d["year"] = d["day"].str[:4]
    d = d.dropna(subset=["scaled", "unus", "sd30"])
    d["vq"] = d.groupby(["coin", "h"])["sd30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    d["side"] = np.where(d["scaled"] > 0, "rise", "fall")
    d["erhi"] = d["er"] > 0.3

    def clus_t(g, col):
        m = g[col].mean(); N = len(g)
        dev = (g[col] - m).groupby(g["day"]).sum(); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / N
        return m / se if se > 0 else np.nan

    def summ(g):
        if len(g) < 8: return pd.Series(dict(n=len(g)))
        g = g.copy()
        g["cu"] = np.sign(g["scaled"]) * g["unus"]
        g["cs"] = g["cu"] / g["usual"]
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), cont_mean=g["cu"].mean(),
                              cont_t=clus_t(g, "cu"), strength=g["cs"].mean(),
                              rho=stats.spearmanr(g["scaled"], g["unus"])[0]))
    out = {}
    out["vq2_h_er_side"] = d[d.vq == 2].groupby(["h", "erhi", "side"]).apply(summ).unstack(level=[1, 2]).T if False else d[d.vq == 2].groupby(["h", "erhi"]).apply(summ)
    d7 = d[d.h == 7]
    out["h7_vq2_side"] = d7[d7.vq == 2].groupby("side").apply(summ)
    out["h7_vq2_erhi_side"] = d7[(d7.vq == 2) & d7.erhi].groupby("side").apply(summ)
    out["h7_vq2_erhi_year"] = d7[(d7.vq == 2) & d7.erhi].groupby("year").apply(summ)
    out["h7_vq2_erhi_coin"] = d7[(d7.vq == 2) & d7.erhi].groupby("coin").apply(summ)
    d7 = d7.copy()
    d7["vrq"] = pd.cut(d7["vrank"], [0, 0.5, 0.8, 1.0], labels=False)
    out["h7_by_vrank"] = d7.groupby("vrq").apply(summ)
    out["h7_vrank_hi_er"] = d7[d7.vrq == 2].groupby("erhi").apply(summ)
    out["h7_mr_side"] = d7[d7.mr].groupby("side").apply(summ)
    out["mr_by_h"] = d[d.mr].groupby("h").apply(summ)
    return out
