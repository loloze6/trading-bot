def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted(set(w for c in coins for w in days[c].keys()), key=lambda s:int(s[1:]))
    # book daily returns
    rows=[]
    for w in wins:
        dfs=[]
        for c in coins:
            if w in days[c]:
                d=days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; dfs.append(d)
        d=pd.concat(dfs)
        g=d.groupby("day")[["book_return","coin_return"]].mean().dropna()
        g["w"]=w; rows.append(g)
    book=pd.concat(rows).reset_index()
    v=(1+book.book_return).cumprod(); dd=v/v.cummax()-1
    book["dd"]=dd.values
    # deepest fall location
    i_trough=int(np.argmin(dd.values)); peak=int(np.argmax(v.values[:i_trough+1]))
    out["deepest_fall"]=pd.Series({"depth":dd.min(),"peak_window":book.w[peak],"trough_window":book.w[i_trough],"days":i_trough-peak,
        "book_ret_in_fall":v.values[i_trough]/v.values[peak]-1,
        "hold_ret_in_fall":float(np.prod(1+book.coin_return.values[peak+1:i_trough+1])-1)})
    wsum=book.groupby("w").agg(book=("book_return",lambda x:np.prod(1+x)-1),hold=("coin_return",lambda x:np.prod(1+x)-1),mindd=("dd","min"))
    out["per_window"]=wsum.reindex(wins)
    # bar-level: per coin features
    recs=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy()
            r=b.close.pct_change()
            b["r"]=r
            b["nxt"]=b.close.shift(-1)/b.close-1
            b["r20"]=b.close/b.close.shift(20)-1
            b["r5"]=b.close/b.close.shift(5)-1
            b["vol20"]=r.rolling(20).std()
            b["vol60"]=r.rolling(60,min_periods=20).std()
            b["z"]=r/b.vol20.shift(1)
            b["coin"]=c; b["w"]=w
            b["gain"]=b.postRebalance_current_allocation*b.nxt
            recs.append(b[["coin","w","forecast","r","nxt","r20","r5","vol20","vol60","z","gain","postRebalance_current_allocation"]])
    B=pd.concat(recs).dropna(subset=["nxt"])
    mu=B.groupby("coin").nxt.mean(); B["ex"]=B.nxt-B.coin.map(mu)
    B["sig"]=B.forecast>0
    B["r20q"]=pd.qcut(B.r20,5,labels=False)
    B["volq"]=pd.qcut(B.vol20/B.vol60,5,labels=False)
    def tab(key):
        g=B.dropna(subset=[key]).groupby([key,"sig"]).agg(n=("ex","size"),mean_ex=("ex","mean"),mean_nxt=("nxt","mean"),sd=("ex","std"),gain=("gain","mean"))
        g["t"]=g.mean_ex/(g.sd/np.sqrt(g.n)); return g.drop(columns="sd")
    out["by_r20_quintile"]=tab("r20q")
    out["by_volratio_quintile"]=tab("volq")
    B["fq"]=pd.cut(B.forecast,[-0.1,0.001,5,10,15,20.1])
    out["by_forecast"]=B.groupby("fq").agg(n=("ex","size"),mean_ex=("ex","mean"),gain=("gain","mean"),alloc=("postRebalance_current_allocation","mean"))
    out["r20_edges"]=pd.Series(pd.qcut(B.r20,5,retbins=True)[1])
    # holding share on loss days
    out["alloc_when_sig_vs_not"]=B.groupby("sig").postRebalance_current_allocation.agg(["mean","count"])
    return out
