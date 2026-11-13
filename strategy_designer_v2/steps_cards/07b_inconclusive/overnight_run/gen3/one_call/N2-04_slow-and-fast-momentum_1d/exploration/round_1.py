import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allfwd = []
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            if n > 20:
                allfwd.append(c[20:] / c[:-20] - 1)
        cmean = np.concatenate(allfwd).mean() if allfwd else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n - 20, 20):
                fwd = c[i + 20] / c[i] - 1
                r20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                r60 = c[i] / c[i - 60] - 1 if i >= 60 else np.nan
                vol = np.std(np.diff(np.log(c[max(0, i - 20):i + 1]))) if i >= 5 else np.nan
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, i=i,
                                 f=df["forecast"].iloc[i], fwd=fwd, ex=fwd - cmean,
                                 r20=r20, r60=r60, vol=vol))
    d = pd.DataFrame(rows)
    a = d[d.f > 0].copy()

    def summ(g):
        x = g["ex"]
        return pd.Series(dict(n=len(x), mean=x.mean(), med=x.median(),
                              t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              hit=(g["fwd"] > 0).mean()))
    out = {}
    out["all_active"] = summ(a)
    out["inactive"] = summ(d[d.f <= 0])
    out["by_coin"] = a.groupby("coin").apply(summ)
    out["by_year"] = a.groupby("year").apply(summ)
    a["fq"] = pd.qcut(a.f.rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_fq"] = a.groupby("fq").apply(summ)
    a["vq"] = pd.qcut(a.vol.rank(method="first"), 3, labels=["lowvol", "mid", "hivol"])
    out["by_vol"] = a.groupby("vq").apply(summ)
    a["r20q"] = pd.qcut(a.r20.rank(method="first"), 3, labels=["r20lo", "mid", "r20hi"])
    out["by_r20"] = a.groupby("r20q").apply(summ)
    a["r60q"] = pd.qcut(a.r60.rank(method="first"), 3, labels=["r60lo", "mid", "r60hi"])
    out["by_r60"] = a.groupby("r60q").apply(summ)
    # BTC market state at same window/bar index
    btc = d[d.coin == "BTCUSD"][["win", "i", "fwd", "r60"]].rename(columns={"fwd": "btcfwd", "r60": "btcr60"})
    m = a.merge(btc, on=["win", "i"], how="left")
    m["btcup"] = np.where(m.btcr60 > 0, "btc60up", "btc60dn")
    out["by_btcstate"] = m.groupby("btcup").apply(summ)
    nb = m[m.coin != "BTCUSD"].dropna(subset=["btcfwd"])
    out["alts_minus_btc"] = pd.Series(dict(n=len(nb), mean=(nb.fwd - nb.btcfwd).mean(),
                                           t=(nb.fwd - nb.btcfwd).mean() / ((nb.fwd - nb.btcfwd).std() / np.sqrt(len(nb))),
                                           corr_btc=np.corrcoef(nb.fwd, nb.btcfwd)[0, 1]))
    out["skew"] = pd.Series(dict(skew=stats.skew(a.ex), sd=a.ex.std(), share_pos=(a.ex > 0).mean(),
                                 trim_mean_5=stats.trim_mean(a.ex, 0.05)))
    return out
