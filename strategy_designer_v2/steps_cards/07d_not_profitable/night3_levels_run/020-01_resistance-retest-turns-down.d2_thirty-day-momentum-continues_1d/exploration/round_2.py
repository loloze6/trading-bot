import pandas as pd, numpy as np

def calmar(x):
    x=np.asarray(x); eq=np.cumprod(1+x); pk=np.maximum.accumulate(eq); dd=(eq/pk-1).min()
    yr=eq[-1]**(365/len(x))-1
    return pd.Series({"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd) if dd<0 else np.nan,
                      "sharpe":x.mean()/x.std()*np.sqrt(365),"mean":x.mean()})

def explore(data):
    days=data["days"]; bars=data["bars"]; coins=list(days.keys())
    wins=sorted(set(w for c in coins for w in days[c]), key=lambda s:int(s[1:]))
    rows=[]
    for w in wins:
        dfs=[]
        for c in coins:
            if w in days[c]:
                d=days[c][w][["day","book_return","coin_return"]].copy(); dfs.append(d)
        g=pd.concat(dfs).groupby("day")[["book_return","coin_return"]].mean().dropna().sort_index()
        g["w"]=w; rows.append(g.reset_index())
    B=pd.concat(rows,ignore_index=True)
    B["EQ"]=(1+B["book_return"]).cumprod(); B["PK"]=B["EQ"].cummax(); B["DD"]=B["EQ"]/B["PK"]-1
    # episodes of drawdown
    B["epi"]=(B["DD"]==0).cumsum()
    ep=B[B.DD<0].groupby("epi").agg(depth=("DD","min"),length=("DD","size"),hold_sum=("coin_return","sum"),
        book_sum=("book_return","sum"),wfirst=("w","first"),wlast=("w","last"))
    ep=ep.sort_values("depth").head(6)
    worst_epis=list(ep.index[:3])
    dayset={}
    for e in worst_epis:
        sub=B[B.epi==e]; tr=sub.DD.idxmin(); dayset[e]=set(zip(B.loc[sub.index[0]:tr,"w"],B.loc[sub.index[0]:tr,"day"]))
    P=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            day=pd.to_datetime(b.timestamp).dt.floor("D")
            r=b.close.shift(-1)/b.close-1; a=b.postRebalance_current_allocation
            lr=np.log(b.close).diff()
            P.append(pd.DataFrame({"coin":c,"w":w,"day":day,"a":a,"r":r,"g":a*r,"f":b.forecast,
              "r30":b.close/b.close.shift(30)-1,"r5":b.close/b.close.shift(5)-1,
              "r10":b.close/b.close.shift(10)-1,
              "vol20":lr.rolling(20).std(),"volratio":lr.rolling(10).std()/lr.rolling(60,min_periods=30).std(),
              "dd60":b.close/b.close.rolling(60,min_periods=20).max()-1}).dropna(subset=["g"]))
    P=pd.concat(P,ignore_index=True)
    P["side"]=np.sign(P.a)
    # which day is in episode
    out={}
    for k,e in enumerate(worst_epis):
        ds=dayset[e]
        m=pd.Series([ (w,pd.Timestamp(d).floor("D")) in {(a,pd.Timestamp(b).floor("D")) for a,b in ds} for w,d in zip(P.w,P.day)],index=P.index) if k==0 else None
        if k==0:
            E=P[m]
            out["ep1_by_coin_side"]=E.groupby(["coin","side"]).agg(g_sum=("g","sum"),r_sum=("r","sum"),n=("g","size"),a=("a","mean"),r30=("r30","mean")).round(4)
    P["side_lbl"]=P.side.map({1:"long",-1:"short",0:"flat"})
    out["episodes"]=ep
    out["side"]=P.groupby("side_lbl").g.agg(["mean","sum","count"])
    P["r30q"]=pd.qcut(P.r30,6,labels=False)
    out["r30q"]=P.groupby("r30q").agg(r30=("r30","mean"),g=("g","mean"),r=("r","mean"),a=("a","mean"),n=("g","size"),gstd=("g","std"))
    P["vrq"]=pd.qcut(P.volratio,4,labels=False)
    out["volratio_side"]=P.groupby(["vrq","side_lbl"]).g.mean().unstack()
    P["r5w"]=P.side*P.r5; P["r5q"]=pd.qcut(P.r5w,5,labels=False)
    out["r5_with_pos"]=P.groupby("r5q").agg(r5w=("r5w","mean"),g=("g","mean"),gstd=("g","std"),n=("g","size"))
    P["ddq"]=pd.qcut(P.dd60,5,labels=False)
    out["dd60_side"]=P.groupby(["ddq","side_lbl"]).g.mean().unstack()
    # variants: daily mean of g across coins
    def book(mask):
        Q=P.copy(); Q.loc[~mask,"g"]=0
        return Q.groupby(["w","day"],sort=False).g.mean()
    order=lambda s: s.reindex(sorted(s.index,key=lambda t:(int(t[0][1:]),t[1])))
    V={"all":P.g==P.g,"long_only":P.side>=0,"no_hi_volratio":P.volratio<P.volratio.quantile(.75),
       "short_only":P.side<=0,"r5_not_against":P.r5w>P.r5w.quantile(.2)}
    out["variants_precost"]=pd.DataFrame({k:calmar(order(book(m)).values) for k,m in V.items()}).T
    out["book_actual"]=calmar(B.book_return.values)
    out["hold"]=calmar(B.coin_return.values)
    return out
