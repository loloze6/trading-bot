import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        wl = sorted(wins.keys(), key=lambda s: int(s[1:]))
        for wi, w in enumerate(wl):
            df = wins[w]
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            n = len(c)
            if n < 900: continue
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=500).mean()
            surge = r24 / mabs
            r1 = np.log(c).diff()
            vol30 = r1.rolling(720, min_periods=500).std()
            p7 = (c / c.shift(168) - 1) / (vol30*np.sqrt(168))
            idx = np.arange(0, n, 24)
            d = {"coin": coin, "wi": wi, "surge": surge.iloc[idx].values, "p7": p7.iloc[idx].values,
                 "vol": vol30.iloc[idx].values, "wd": ts.iloc[idx].dt.weekday.values,
                 "hr": ts.iloc[idx].dt.hour.values}
            for h in [6, 24, 48, 72, 120]:
                d["f%d" % h] = (c.shift(-h) / c - 1).iloc[idx].values
            rows.append(pd.DataFrame(d))
    D = pd.concat(rows).dropna(subset=["surge", "f24", "p7", "vol"])
    for h in [6, 24, 48, 72, 120]:
        D["e%d" % h] = D["f%d" % h] - D.groupby("coin")["f%d" % h].transform("mean")
    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))})
    D["sd"] = pd.qcut(D["surge"], 10, labels=False)
    out["horizons_by_surge_decile"] = D.groupby("sd").apply(lambda g: pd.Series({**{"m%d"%h: g["e%d"%h].mean() for h in [6,24,48,72,120]}, "t24": summ(g.e24)["t"], "t72": summ(g.e72)["t"], "n": len(g)}))
    low = D[D.surge < 0]
    out["fall_side_by_coin"] = low.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "slope_e24_on_surge": stats.linregress(g.surge, g.e24).slope, "rho": stats.spearmanr(g.surge, g.e24)[0], "p": stats.spearmanr(g.surge, g.e24)[1]}))
    D["half"] = np.where(D.wi < 12, "w1-12", "w13-24")
    out["bottom2dec_by_half_coin"] = D[D.sd <= 1].groupby(["half"]).apply(lambda g: summ(g.e24))
    D["vq"] = D.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False))
    out["bottom2dec_by_vol_tercile"] = D[D.sd <= 1].groupby("vq").apply(lambda g: summ(g.e24))
    D["p7s"] = np.sign(D.p7)
    out["bottom2dec_by_p7sign"] = D[D.sd <= 1].groupby("p7s").apply(lambda g: summ(g.e24))
    out["weekday_by_coin_t"] = D.groupby(["coin", "wd"]).apply(lambda g: summ(g.e24)["t"]).unstack()
    out["weekday_by_half"] = D.groupby(["half", "wd"]).apply(lambda g: summ(g.e24)["mean"]).unstack()
    D["pq"] = pd.qcut(D["p7"], 5, labels=False)
    out["p7quint_e120_by_half"] = D.groupby(["half", "pq"]).apply(lambda g: summ(g.e120)["t"]).unstack()
    return out
