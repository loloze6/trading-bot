def explore(data):
    import pandas as pd, numpy as np
    out = {}
    T = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; vol = b["volume"]
            r1 = cl.pct_change()
            fwd5 = cl.shift(-5) / cl - 1
            ret60 = cl / cl.shift(60) - 1
            ret10 = cl / cl.shift(10) - 1
            vr = np.log(vol.rolling(30).mean() / vol.shift(30).rolling(30).mean())
            alloc = b["postRebalance_current_allocation"].fillna(0)
            # age of position in bars
            age = np.zeros(len(b)); a = 0
            for i in range(len(b)):
                a = a + 1 if alloc[i] > 0 else 0
                age[i] = a
            fc = b["forecast"].fillna(0)
            for i in range(0, len(b) - 5, 5):
                T.append(dict(coin=c, wn=int(w[1:]), alloc=alloc[i], age=age[i], fc=fc[i],
                              fwd5=fwd5[i], ret60=ret60[i], ret10=ret10[i], vr=vr[i]))
    G = pd.DataFrame(T)
    G["unus"] = G["fwd5"] - G.groupby("coin")["fwd5"].transform("mean")
    inp = G[G["alloc"] > 0].copy()
    inp["ageb"] = pd.cut(inp["age"], [0, 5, 10, 20, 1000])
    def agg(x):
        return x.groupby(level=0) if False else None
    out["inpos_by_age"] = inp.groupby("ageb")["fwd5"].agg(["size", "mean", "std", "min",
        lambda s: (s < 0).mean()]).round(4)
    out["inpos_by_age_w14"] = inp[inp.wn == 14].groupby("ageb")["fwd5"].agg(["size", "mean"]).round(4)
    out["w14_inpos_features"] = inp[inp.wn == 14][["ret60", "ret10", "vr", "fc", "fwd5"]].describe().round(3)
    out["other_inpos_features"] = inp[inp.wn != 14][["ret60", "ret10", "vr", "fc", "fwd5"]].describe().round(3)
    # condition alone vs with signal: deep 60-day fall
    fall = G[G["ret60"] < -0.10].copy()
    fall["deep60"] = fall["ret60"] < -0.30
    fall["sig"] = (fall["vr"] > 0) & (fall["ret10"] < 0)
    out["deep60_by_sig"] = fall.groupby(["deep60", "sig"])["fwd5"].agg(["size", "mean", "std"]).round(4)
    # fresh signal only: age<=5
    fr = inp[inp.age <= 5]
    fr = fr.copy(); fr["d60"] = pd.qcut(fr["ret60"], 3, labels=False)
    out["fresh_by_ret60"] = fr.groupby("d60").agg(lo=("ret60", "min"), hi=("ret60", "max"),
                                                  n=("fwd5", "size"), mean=("fwd5", "mean")).round(4)
    out["by_window_age"] = inp.assign(old=inp.age > 5).groupby(["wn", "old"])["fwd5"].agg(["size", "sum"]).round(3).unstack()
    return out
