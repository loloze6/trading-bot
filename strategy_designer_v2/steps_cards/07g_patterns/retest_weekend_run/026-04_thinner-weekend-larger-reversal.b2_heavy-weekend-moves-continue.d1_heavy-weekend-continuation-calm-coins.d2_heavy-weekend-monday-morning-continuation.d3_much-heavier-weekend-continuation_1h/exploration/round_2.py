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
        sd24, m24 = np.std(r24), np.mean(r24)
        sd1 = np.std(r1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            n = len(c)
            lr = np.r_[np.nan, np.log(c[1:] / c[:-1])]
            vol24 = pd.Series(lr).rolling(24).std().values
            vol720 = pd.Series(lr).rolling(720, min_periods=240).std().values
            for i in range(24, n - 48, 24):
                G.append(dict(coin=coin, y=ts.iloc[i].year, p=(c[i]/c[i-24]-1)/sd24,
                              praw=c[i]/c[i-24]-1,
                              f=(c[i+24]/c[i]-1 - m24)/sd24, fraw=c[i+24]/c[i]-1 - m24,
                              f12=(c[i+12]/c[i]-1)/sd24, f48=(c[i+48]/c[i]-1-2*m24)/sd24,
                              vr=vol24[i]/vol720[i] if vol720[i] > 0 else np.nan))
            hr = ts.dt.hour.values
            idx = np.where(hr == 20)[0]
            for i in idx:
                if i < 21 or i + 2 >= n:
                    continue
                H.append(dict(coin=coin, y=ts.iloc[i].year, wd=ts.iloc[i].weekday(),
                              f=(c[i+2]/c[i]-1)/sd1, fraw=c[i+2]/c[i]-1,
                              day=(c[i]/c[i-20]-1)/sd24,
                              vr=vol24[i]/vol720[i] if vol720[i] > 0 else np.nan))
    G = pd.DataFrame(G); H = pd.DataFrame(H)
    def tt(x):
        x = x.dropna(); return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)})
    G["s"] = -np.sign(G.p) * G.f      # reversal, signed
    G["sraw"] = -np.sign(G.p) * G.fraw
    G["s12"] = -np.sign(G.p) * G.f12; G["s48"] = -np.sign(G.p) * G.f48
    G["ab"] = pd.qcut(G.p.abs(), [0, .5, .8, .9, .95, .98, 1], labels=False)
    out["24h reversal by |past 24h| bucket (0-50,50-80,80-90,90-95,95-98,98-100%)"] = G.groupby("ab").agg(
        p=("p", lambda x: x.abs().mean()), s=("s", "mean"), sraw_pct=("sraw", lambda x: 100*x.mean()),
        s12=("s12", "mean"), s48=("s48", "mean"), n=("s", "size")).round(3)
    for side, d in [("falls", G[G.p < 0]), ("rises", G[G.p > 0])]:
        d = d.copy(); d["q"] = pd.qcut(d.p.abs(), 5, labels=False)
        out[f"{side}: reversal by |p| quintile"] = d.groupby("q").s.apply(tt).unstack().round(3)
    T = G[G.ab >= 3]
    out["tail (top10% |p|) reversal by year"] = T.groupby("y").s.apply(tt).unstack().round(3)
    out["tail reversal by coin"] = T.groupby("coin").s.apply(tt).unstack().round(3)
    T = T.copy(); T["vq"] = pd.qcut(T.vr, 3, labels=False)
    out["tail reversal by vol ratio tercile"] = T.groupby("vq").agg(vr=("vr","mean"), s=("s","mean"), n=("s","size")).round(3)
    out["hours 21-22 by year"] = H.groupby("y").f.apply(tt).unstack().round(3)
    out["hours 21-22 by coin"] = H.groupby("coin").f.apply(tt).unstack().round(3)
    out["hours 21-22 by weekday"] = H.groupby("wd").f.apply(tt).unstack().round(3)
    H["dq"] = pd.qcut(H.day, 5, labels=False)
    out["hours 21-22 by day-so-far quintile"] = H.groupby("dq").agg(day=("day","mean"), f=("f","mean"), raw_pct=("fraw", lambda x: 100*x.mean()), n=("f","size")).round(4)
    H["vq"] = pd.qcut(H.vr, 5, labels=False)
    out["hours 21-22 by vol ratio quintile"] = H.groupby("vq").agg(vr=("vr","mean"), f=("f","mean"), raw_pct=("fraw", lambda x: 100*x.mean()), n=("f","size")).round(4)
    out["hours 21-22 raw mean pct overall"] = float(100*H.fraw.mean())
    return out
