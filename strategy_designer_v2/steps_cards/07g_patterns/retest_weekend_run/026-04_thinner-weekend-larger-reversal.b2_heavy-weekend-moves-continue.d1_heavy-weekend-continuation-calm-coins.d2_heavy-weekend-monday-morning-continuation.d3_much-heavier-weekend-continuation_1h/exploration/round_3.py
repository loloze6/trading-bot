def explore(data):
    import numpy as np, pandas as pd
    out = {}
    G = []; H = []
    for coin, wins in data["bars"].items():
        r24 = []; r1 = []
        for w, b in wins.items():
            c = b["close"].values
            r24 += list(c[24::24] / c[:-24:24][:len(c[24::24])] - 1)
            r1 += list(c[1:] / c[:-1] - 1)
        sd24, m24 = np.std(r24), np.mean(r24); sd1 = np.std(r1); m1 = np.mean(r1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); c = b["close"].values; n = len(c)
            lr = np.r_[np.nan, np.log(c[1:] / c[:-1])]
            vol24 = pd.Series(lr).rolling(24).std().values
            vol720 = pd.Series(lr).rolling(720, min_periods=240).std().values
            for i in range(24, n - 24, 24):
                G.append(dict(coin=coin, w=w, p=(c[i]/c[i-24]-1)/sd24,
                              fraw=c[i+24]/c[i]-1-m24, f=(c[i+24]/c[i]-1-m24)/sd24,
                              vr=vol24[i]/vol720[i] if vol720[i] > 0 else np.nan))
            hr = ts.dt.hour.values
            for i in np.where(hr == 20)[0]:
                if i < 21 or i + 2 >= n: continue
                H.append(dict(coin=coin, w=w, f=(c[i+2]/c[i]-1-2*m1)/sd1, fraw=c[i+2]/c[i]-1-2*m1,
                              vr=vol24[i]/vol720[i] if vol720[i] > 0 else np.nan))
    G = pd.DataFrame(G); H = pd.DataFrame(H)
    def tt(x):
        x = x.dropna(); return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)})
    G["s"] = -np.sign(G.p) * G.f; G["sraw"] = -np.sign(G.p) * G.fraw
    G["ab"] = pd.qcut(G.p.abs(), [0, .8, .9, .95, .98, 1], labels=False)
    out["24h reversal t by |p| bucket (0-80,80-90,90-95,95-98,98-100)"] = G.groupby("ab").s.apply(tt).unstack().round(3)
    out["24h reversal raw pct by bucket"] = G.groupby("ab").sraw.apply(lambda x: 100*x.mean()).round(3)
    G["wn"] = G.w.str[1:].astype(int)
    T = G[G.ab >= 2]
    out["tail(top10%) reversal by window group"] = T.groupby(pd.cut(T.wn, [0,6,12,18,24])).s.apply(tt).unstack().round(3)
    H["vq"] = pd.qcut(H.vr, 5, labels=False)
    out["21-22h excess by vol ratio quintile, t"] = H.groupby("vq").f.apply(tt).unstack().round(3)
    out["21-22h raw pct by vol quintile"] = H.groupby("vq").fraw.apply(lambda x: 100*x.mean()).round(4)
    H["wn"] = H.w.str[1:].astype(int)
    out["21-22h by window group"] = H.groupby(pd.cut(H.wn, [0,6,12,18,24])).f.apply(tt).unstack().round(3)
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D).dropna(subset=["book_return"])
    bd = D.groupby(["w", "day"]).book_return.mean()
    q = bd.quantile([0.01, 0.99])
    out["book day share of total from top/bottom 1% days"] = pd.Series({
        "sum_all": bd.sum(), "sum_top1": bd[bd >= q[0.99]].sum(), "sum_bot1": bd[bd <= q[0.01]].sum(), "n": len(bd)}).round(4)
    return out
