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
            n = len(b)
            for h in (3, 7, 14):
                fwd = c.shift(-h) / c - 1
                for i in range(0, n, h):
                    if i + h >= n: continue
                    rows.append(dict(coin=coin, w=w, h=h, day=str(b["timestamp"].iloc[i])[:10],
                                     regime=b["regime"].iloc[i], fc=b["forecast"].iloc[i],
                                     scaled=scaled.iloc[i], er=er.iloc[i], fwd=fwd.iloc[i],
                                     sd30=sd30.iloc[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["unus"] = d["fwd"] - d["drift"]
    d["mr"] = d["regime"] == "mean_reversion"

    def summ(g):
        g = g.dropna(subset=["unus", "scaled"])
        if len(g) < 5:
            return pd.Series(dict(n=len(g)))
        rho = stats.spearmanr(g["scaled"], g["unus"])[0]
        sl = stats.linregress(g["scaled"], g["unus"])
        return pd.Series(dict(n=len(g), mean_unus=g["unus"].mean(), rho_scaled_fwd=rho,
                              slope=sl.slope, t_slope=sl.slope / sl.stderr))

    out = {}
    out["by_h_regime"] = d.groupby(["h", "mr"]).apply(summ)
    d7 = d[d.h == 7].copy()
    d7["side"] = np.where(d7["scaled"] > 0, "rise", "fall")
    out["h7_regime_side"] = d7.groupby(["mr", "side"]).apply(summ)
    d7["q"] = pd.qcut(d7["scaled"], 5, labels=False)
    out["h7_quintile_mr"] = d7[d7.mr].groupby("q").agg(n=("unus", "size"), scaled=("scaled", "mean"), unus=("unus", "mean"))
    out["h7_quintile_other"] = d7[~d7.mr].groupby("q").agg(n=("unus", "size"), scaled=("scaled", "mean"), unus=("unus", "mean"))
    out["h7_coin_mr"] = d7[d7.mr].groupby("coin").apply(summ)
    d7["year"] = d7["day"].str[:4]
    out["h7_year_mr"] = d7[d7.mr].groupby("year").apply(summ)
    d7["erq"] = pd.qcut(d7["er"], 4, labels=False)
    out["h7_by_er_quartile_all"] = d7.groupby("erq").apply(summ)
    d7["vq"] = d7.groupby("coin")["sd30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["h7_by_vol_tercile_all"] = d7.groupby("vq").apply(summ)
    out["regime_share"] = d7["regime"].value_counts(normalize=True)
    return out
