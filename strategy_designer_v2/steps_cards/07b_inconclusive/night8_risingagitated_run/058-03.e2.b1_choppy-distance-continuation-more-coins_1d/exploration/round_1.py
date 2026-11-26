import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    # drift per coin per horizon on grid
    def drift(coin, h):
        r = []
        for w, df in bars[coin].items():
            c = df["close"].values
            for i in range(0, len(c) - h, h):
                r.append(c[i + h] / c[i] - 1)
        return np.mean(r) if r else np.nan, np.std(r) if r else np.nan
    rows = []
    for h in [3, 5, 10, 20]:
        for coin in bars:
            d, sd = drift(coin, h)
            for w, df in bars[coin].items():
                c = df["close"].values; f = df["forecast"].values
                ts = pd.to_datetime(df["timestamp"]).values
                ret1 = df["close"].pct_change().values
                vol10 = pd.Series(ret1).rolling(10).std().values
                vol30 = pd.Series(ret1).rolling(30).std().values
                for i in range(0, len(c) - h, h):
                    if f[i] == 0 or np.isnan(f[i]): continue
                    r = c[i + h] / c[i] - 1
                    rows.append(dict(h=h, coin=coin, w=w, ts=ts[i], f=f[i],
                                     prod=f[i] / 10 * (r - d), sx=np.sign(f[i]) * (r - d),
                                     z=np.sign(f[i]) * (r - d) / sd,
                                     ag=vol10[i] / vol30[i] if vol30[i] > 0 else np.nan,
                                     year=pd.Timestamp(ts[i]).year))
    D = pd.DataFrame(rows)
    def summ(g):
        byd = g.groupby("ts")["prod"].sum()
        m = g["prod"].mean(); n = len(g)
        dev = (g["prod"] - m).groupby(g["ts"]).sum()
        J = len(dev); se = np.sqrt((dev**2).sum() * J / (J - 1)) / n if J > 1 else np.nan
        return pd.Series(dict(n=n, days=J, mean_prod=m, t=m / se if se else np.nan,
                              mean_sx=g["sx"].mean(), mean_z=g["z"].mean()))
    out = {}
    out["by_horizon"] = D.groupby("h").apply(summ)
    D10 = D[D.h == 10].copy()
    D10["side"] = np.where(D10.f > 0, "long", "short")
    out["h10_by_side"] = D10.groupby("side").apply(summ)
    D10["fq"] = pd.qcut(D10.f.abs(), 4, labels=["q1", "q2", "q3", "q4"])
    out["h10_by_absf_quartile"] = D10.groupby("fq").apply(summ)
    out["h10_by_side_quart"] = D10.groupby(["side", "fq"]).apply(summ)
    out["h10_by_coin"] = D10.groupby("coin").apply(summ)
    out["h10_by_window"] = D10.groupby("w").apply(summ)
    out["h10_by_year"] = D10.groupby("year").apply(summ)
    D10["agq"] = pd.qcut(D10.ag, 2, labels=["calm10", "agit10"])
    out["h10_by_recentvol"] = D10.groupby("agq").apply(summ)
    D20 = D[D.h == 20].copy(); D20["side"] = np.where(D20.f > 0, "long", "short")
    out["h20_by_side"] = D20.groupby("side").apply(summ)
    return out
