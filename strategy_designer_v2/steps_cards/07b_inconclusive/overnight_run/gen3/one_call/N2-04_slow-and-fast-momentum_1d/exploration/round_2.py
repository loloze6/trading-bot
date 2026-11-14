import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allfwd = []
        for w, df in wins.items():
            c = df["close"].values
            if len(c) > 20:
                allfwd.append(c[20:] / c[:-20] - 1)
        cmean = np.concatenate(allfwd).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n - 20, 20):
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, i=i,
                                 f=df["forecast"].iloc[i], fwd=c[i + 20] / c[i] - 1,
                                 ex=c[i + 20] / c[i] - 1 - cmean,
                                 r20=c[i] / c[i - 20] - 1 if i >= 20 else np.nan,
                                 r60=c[i] / c[i - 60] - 1 if i >= 60 else np.nan))
    d = pd.DataFrame(rows)
    btc = d[d.coin == "BTCUSD"][["win", "i", "fwd", "r20", "r60"]].rename(
        columns={"fwd": "btcfwd", "r20": "btcr20", "r60": "btcr60"})
    m = d.merge(btc, on=["win", "i"], how="left")
    m["active"] = m.f > 0
    m["btc60up"] = m.btcr60 > 0
    m["btcboth"] = (m.btcr60 > 0) & (m.btcr20 > 0)

    def summ(g):
        x = g["ex"]
        n = len(x)
        return pd.Series(dict(n=n, mean=x.mean(), med=x.median(),
                              trim5=stats.trim_mean(x, 0.05) if n > 5 else np.nan,
                              t=x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan,
                              hit=(g["fwd"] > 0).mean()))
    out = {}
    mm = m.dropna(subset=["btcr60"])
    out["active_x_btc60"] = mm.groupby(["active", "btc60up"]).apply(summ)
    out["active_x_btcboth"] = mm.groupby(["active", "btcboth"]).apply(summ)
    a = mm[mm.active & mm.btc60up]
    out["act_btcup_by_coin"] = a.groupby("coin").apply(summ)
    out["act_btcup_by_year"] = a.groupby("year").apply(summ)
    # alt relative to BTC when active & btc up
    nb = a[a.coin != "BTCUSD"]
    rel = nb.fwd - nb.btcfwd
    out["alt_rel_btc_btcup"] = pd.Series(dict(n=len(rel), mean=rel.mean(), med=rel.median(),
                                              t=rel.mean() / (rel.std() / np.sqrt(len(rel)))))
    # coin r60 stronger than btc r60
    act = mm[mm.active].copy()
    act["stronger"] = act.r60 > act.btcr60
    out["act_alts_stronger_than_btc"] = act[act.coin != "BTCUSD"].groupby(["btc60up", "stronger"]).apply(summ)
    # by window count of active btcup positive
    wm = a.groupby("win")["ex"].mean()
    out["act_btcup_windows"] = pd.Series(dict(nwin=len(wm), share_pos=(wm > 0).mean(),
                                              t=wm.mean() / (wm.std() / np.sqrt(len(wm)))))
    return out
