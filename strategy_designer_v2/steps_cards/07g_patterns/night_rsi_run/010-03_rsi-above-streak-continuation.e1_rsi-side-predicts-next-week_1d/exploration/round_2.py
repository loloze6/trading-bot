def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            dd = dd.copy().reset_index(drop=True); dd["coin"]=coin; dd["w"]=w
            r = dd["coin_return"]
            dd["prev1"] = r.shift(1)
            dd["prev3"] = (1+r).rolling(3).apply(np.prod, raw=True).shift(1) - 1
            dd["vol20"] = r.rolling(20).std().shift(1)
            dd["absprev_z"] = dd["prev1"].abs() / dd["vol20"]
            dd["next1"] = r.shift(-1)
            dd["pos"] = np.arange(len(dd))
            dl.append(dd)
    D = pd.concat(dl, ignore_index=True)
    D = D.dropna(subset=["coin_return","prev1"])
    def tt(a, b):
        t, p = stats.ttest_ind(a, b, equal_var=False); return t
    # 1-day reversal, by coin and year, independent daily cases
    res = []
    for coin, g in D.groupby("coin"):
        q = pd.qcut(g["prev1"], 5, labels=False)
        lo = g.loc[q==0,"coin_return"]; hi = g.loc[q==4,"coin_return"]
        sl, ic, rr, p, se = stats.linregress(g["prev1"]/g["prev1"].std(), g["coin_return"])
        res.append(dict(coin=coin, n=len(g), lo=lo.mean(), hi=hi.mean(), lo_minus_hi=lo.mean()-hi.mean(), welch_t=tt(lo,hi), slope_t=sl/se))
    out["1d reversal by coin"] = pd.DataFrame(res)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    res = []
    for yr, g in D.groupby("yr"):
        sl, ic, rr, p, se = stats.linregress(g["prev1"], g["coin_return"])
        res.append(dict(yr=yr, n=len(g), slope=sl, t=sl/se))
    out["1d slope next on prev by year"] = pd.DataFrame(res)
    # standardised prev move: size of move in vol units
    g = D.dropna(subset=["vol20"]).copy()
    g["z"] = g["prev1"]/g["vol20"]
    g["zb"] = pd.cut(g["z"], [-99,-2,-1,0,1,2,99])
    out["next day coin by prev z bucket"] = g.groupby("zb").agg(n=("coin_return","size"), m=("coin_return","mean"), sd=("coin_return","std")).assign(t=lambda x: x.m/(x.sd/np.sqrt(x.n)))
    g["vq"] = g.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,3,labels=False))
    res=[]
    for vq, h in g.groupby("vq"):
        sl, ic, rr, p, se = stats.linregress(h["z"], h["coin_return"])
        res.append(dict(vq=vq, n=len(h), slope_per_z=sl, t=sl/se))
    out["reversal slope by vol tercile"] = pd.DataFrame(res)
    # 3-day past -> next 3 days, non-overlapping grid
    rows=[]
    for (coin,w), h in D.groupby(["coin","w"]):
        pass
    gl=[]
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            c = dd["close"].values
            for i in range(3, len(c)-3, 3):
                gl.append(dict(coin=coin, past=c[i]/c[i-3]-1, fwd=c[i+3]/c[i]-1))
    G = pd.DataFrame(gl)
    sl, ic, rr, p, se = stats.linregress(G["past"], G["fwd"])
    out["3d past->3d fwd slope, t, n"] = f"slope {sl:.4f} t {sl/se:.2f} n {len(G)}"
    # weekday t-stats coin return
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    m_all = D["coin_return"].mean()
    res=[]
    for wd, h in D.groupby("wd"):
        o = D.loc[D.wd!=wd,"coin_return"]
        res.append(dict(wd=wd, n=len(h), coin=h["coin_return"].mean(), welch_t_vs_rest=tt(h["coin_return"].dropna(), o.dropna()), book=h["book_return"].mean()))
    out["weekday coin t"] = pd.DataFrame(res)
    # book's largest days: what coin did before and after
    B = D.dropna(subset=["book_return"]).copy()
    B["bq"] = pd.qcut(B["book_return"], 10, labels=False)
    out["around book decile"] = B.groupby("bq").agg(n=("book_return","size"), book=("book_return","mean"), coin_prev=("prev1","mean"), coin_next=("next1","mean"))
    return out
