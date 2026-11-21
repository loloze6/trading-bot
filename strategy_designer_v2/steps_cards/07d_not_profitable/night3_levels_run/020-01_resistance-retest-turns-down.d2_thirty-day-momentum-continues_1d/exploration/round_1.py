import pandas as pd, numpy as np

def explore(data):
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted(set(w for c in coins for w in days[c]), key=lambda s:int(s[1:]))
    # book daily: mean over coins per day within window
    rows=[]
    for w in wins:
        dfs=[]
        for c in coins:
            if w in days[c]:
                d=days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; dfs.append(d)
        d=pd.concat(dfs)
        g=d.groupby("day")[["book_return","coin_return"]].mean().dropna().sort_index()
        g["w"]=w; rows.append(g.reset_index())
    B=pd.concat(rows,ignore_index=True)
    B["eq"]=(1+B.book_return).cumprod(); B["peak"]=B.eq.cummax(); B["dd"]=B.eq/B.peak-1
    B["heq"]=(1+B.coin_return).cumprod()
    # deepest fall episode
    tr=B.dd.idxmin(); pk=B.loc[:tr,"eq"].idxmax()
    ep=B.loc[pk+1:tr]
    # top falls per window
    wstat=B.groupby("w",sort=False).agg(book_sum=("book_return","sum"),hold_sum=("coin_return","sum"),
        min_dd=("dd","min"),n=("book_return","size"))
    # per-bar position gains
    P=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            r=b.close.shift(-1)/b.close-1
            a=b.postRebalance_current_allocation
            r30=b.close/b.close.shift(30)-1
            lr=np.log(b.close).diff()
            vol20=lr.rolling(20).std()
            vol60=lr.rolling(60,min_periods=30).std()
            r5=b.close/b.close.shift(5)-1
            P.append(pd.DataFrame({"coin":c,"w":w,"a":a,"r":r,"g":a*r,"f":b.forecast,
               "r30":r30,"volratio":vol20/vol60,"vol20":vol20,"r5":r5,"in_ep":False}).dropna(subset=["g"]))
    P=pd.concat(P,ignore_index=True)
    P["side"]=np.sign(P.a)
    side=P.groupby("side").g.agg(["mean","sum","count"])
    P["fq"]=pd.qcut(P.f,5,labels=False,duplicates="drop")
    fq=P.groupby("fq").agg(g=("g","mean"),r=("r","mean"),a=("a","mean"),n=("g","size"))
    P["vq"]=pd.qcut(P.volratio,4,labels=False)
    vq=P.groupby(["vq","side"]).g.agg(["mean","count"]).unstack()
    P["v20q"]=pd.qcut(P.vol20,4,labels=False)
    v20=P.groupby(["v20q","side"]).g.agg(["mean","sum","count"]).unstack()
    # sorting by reversal: r5 against position
    P["r5_with"]=np.sign(P.a)*P.r5
    P["r5q"]=pd.qcut(P.r5_with,5,labels=False)
    r5q=P.groupby("r5q").g.agg(["mean","sum","count"])
    return {"episode": pd.Series({"len_days":len(ep),"depth":B.dd.min(),"book_sum":ep.book_return.sum(),
             "hold_sum":ep.coin_return.sum(),"windows":",".join(ep.w.unique()),
             "yearly":(B.eq.iloc[-1])**(365/len(B))-1}),
            "windows":wstat,"side":side,"fq":fq,"volratio_side":vq,"vol20_side":v20,"r5_against_pos":r5q}
