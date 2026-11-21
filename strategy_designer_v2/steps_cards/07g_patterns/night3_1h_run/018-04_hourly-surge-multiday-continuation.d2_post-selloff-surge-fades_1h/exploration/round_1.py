import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    H = 120
    rows = []
    hr_rows = []
    d_rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            n = len(c)
            if n < 900: continue
            r24 = c / c.shift(24) - 1
            mabs = r24.abs().rolling(720, min_periods=500).mean()
            surge = r24 / mabs
            r7lag = c.shift(24) / c.shift(192) - 1
            r1 = np.log(c).diff()
            vol30 = r1.rolling(720, min_periods=500).std()
            p7 = r7lag / (vol30 * np.sqrt(168))
            r30 = c / c.shift(720) - 1
            fwd = c.shift(-H) / c - 1
            fwd24 = c.shift(-24) / c - 1
            idx = np.arange(0, n, H)
            sub = pd.DataFrame({"coin": coin, "win": w, "surge": surge.iloc[idx].values,
                                "p7": p7.iloc[idx].values, "vol": vol30.iloc[idx].values,
                                "r30": (r30.iloc[idx] / (vol30.iloc[idx]*np.sqrt(720))).values,
                                "fwd": fwd.iloc[idx].values})
            rows.append(sub)
            # hourly returns by hour
            hr_rows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "r": (c.shift(-1)/c-1)}))
            idx24 = np.arange(0, n, 24)
            d_rows.append(pd.DataFrame({"coin": coin, "surge": surge.iloc[idx24].values,
                                        "p7": p7.iloc[idx24].values, "fwd24": fwd24.iloc[idx24].values,
                                        "wd": ts.iloc[idx24].dt.weekday.values}))
    G = pd.concat(rows).dropna()
    drift = G.groupby("coin")["fwd"].transform("mean")
    sd = G.groupby("coin")["fwd"].transform("std")
    G["ex"] = G["fwd"] - drift
    G["exs"] = G["ex"] / sd
    def summ(g, col="ex"):
        x = g[col]
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    G["sq"] = pd.qcut(G["surge"], 5, labels=False)
    out["fwd120_by_surge_quint"] = G.groupby("sq").apply(summ)
    G["pq"] = pd.qcut(G["p7"], 5, labels=False)
    out["fwd120_by_p7_quint"] = G.groupby("pq").apply(summ)
    G["vq"] = G.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 5, labels=False))
    out["fwd120_by_vol_quint"] = G.groupby("vq").apply(summ)
    G["rq"] = pd.qcut(G["r30"], 5, labels=False)
    out["fwd120_by_r30_quint"] = G.groupby("rq").apply(summ)
    G["big"] = pd.cut(G["surge"], [-np.inf,-2,2,np.inf], labels=["dn","mid","up"])
    G["p7s"] = np.sign(G["p7"])
    out["fwd120_big_x_p7sign"] = G.groupby(["big","p7s"]).apply(summ)
    out["fwd120_by_coin_surge_corr"] = G.groupby("coin").apply(lambda g: pd.Series({"rho_surge": stats.spearmanr(g.surge,g.ex)[0],"rho_p7": stats.spearmanr(g.p7,g.ex)[0],"rho_r30": stats.spearmanr(g.r30,g.ex)[0],"n":len(g)}))
    HR = pd.concat(hr_rows).dropna()
    HR["ex"] = HR["r"] - HR.groupby("coin")["r"].transform("mean")
    out["hourly_ret_by_hour_bps"] = HR.groupby("hour").apply(lambda g: pd.Series({"n":len(g),"bps":g.ex.mean()*1e4,"t":g.ex.mean()/(g.ex.std()/np.sqrt(len(g)))}))
    D = pd.concat(d_rows).dropna()
    D["ex"] = D["fwd24"] - D.groupby("coin")["fwd24"].transform("mean")
    out["fwd24_by_weekday"] = D.groupby("wd").apply(summ)
    D["sq"] = pd.qcut(D["surge"], 10, labels=False)
    out["fwd24_by_surge_decile"] = D.groupby("sq").apply(summ)
    return out
