import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close","forecast","postRebalance_current_allocation"]].copy().reset_index(drop=True)
            c = d["close"].values
            r1 = pd.Series(c).pct_change()
            d["r1"] = r1
            d["r5"] = pd.Series(c).pct_change(5)
            d["r20"] = pd.Series(c).pct_change(20)
            d["vol20"] = r1.rolling(20).std()
            d["vol60"] = r1.rolling(60).std()
            s = np.sign(r1.fillna(0).values); st = np.zeros(len(s))
            for i in range(1, len(s)):
                st[i] = st[i-1]+s[i] if (s[i]!=0 and np.sign(st[i-1])==s[i]) else s[i]
            d["streak"] = st
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["day"] = pd.to_datetime(d["timestamp"]).dt.floor("D")
            d["pos"] = np.arange(len(d))
            for h in (1,2,3,5,10):
                d[f"f{h}"] = pd.Series(c).shift(-h)/pd.Series(c) - 1
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["z1"] = A["r1"]/A["vol60"]
    A["volrank"] = A.groupby("coin")["vol60"].rank(pct=True)
    out = {}
    def stat(h, key, B):
        g = B[(B["pos"] % h == 0) & B[f"f{h}"].notna() & B[key].notna()].copy()
        mu = A[(A["pos"] % h == 0)].groupby("coin")[f"f{h}"].mean()
        sd = A[(A["pos"] % h == 0)].groupby("coin")[f"f{h}"].std()
        g["ex"] = g[f"f{h}"] - g["coin"].map(mu)
        g["str"] = g["ex"]/g["coin"].map(sd)
        res = []
        for k, gg in g.groupby(key):
            m = gg["ex"].mean()
            dev = (gg["ex"]-m).groupby(gg["day"]).sum()
            se = np.sqrt((dev**2).sum())/len(gg)
            res.append((k, len(gg), gg["day"].nunique(), m*100, m/se if se>0 else np.nan, gg["str"].mean()))
        return pd.DataFrame(res, columns=[key,"n","days","ex%","t","strength"]).set_index(key)
    A["zbin"] = pd.cut(A["z1"], [-np.inf,-2.5,-1.5,-0.75,0,0.75,1.5,2.5,np.inf])
    A["stk"] = A["streak"].clip(-5,5)
    A["r5z"] = pd.cut(A["r5"]/(A["vol60"]*np.sqrt(5)), [-np.inf,-2,-1,0,1,2,np.inf])
    A["r20z"] = pd.cut(A["r20"]/(A["vol60"]*np.sqrt(20)), [-np.inf,-2,-1,0,1,2,np.inf])
    A["vq"] = pd.cut(A["volrank"], [0,.33,.67,1])
    for h in (1,2,5):
        out[f"z1 bin h{h}"] = stat(h,"zbin",A)
        out[f"streak h{h}"] = stat(h,"stk",A)
    for h in (2,5,10):
        out[f"r5z h{h}"] = stat(h,"r5z",A)
        out[f"r20z h{h}"] = stat(h,"r20z",A)
    out["vol tercile h5"] = stat(5,"vq",A)
    out["weekday h1"] = stat(1,"wd",A)
    # book
    D = pd.concat([df.assign(coin=c, win=w) for c, ws in data["days"].items() for w, df in ws.items()])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    bk["wd"] = pd.to_datetime(bk.index.get_level_values(1)).weekday
    out["book by weekday"] = bk.groupby("wd").agg(n=("book_return","size"), book=("book_return","mean"), hold=("coin_return","mean"))
    out["book by year"] = bk.groupby(pd.to_datetime(bk.index.get_level_values(1)).year).agg(book=("book_return","mean"), hold=("coin_return","mean"), n=("book_return","size"))
    return out
