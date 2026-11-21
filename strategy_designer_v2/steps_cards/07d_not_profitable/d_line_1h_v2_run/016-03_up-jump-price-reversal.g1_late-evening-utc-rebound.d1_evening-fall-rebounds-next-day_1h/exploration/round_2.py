import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows); D["wn"]=D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().sort_index()
    eq=(1+B.book_return).cumprod(); dd=eq/eq.cummax()-1
    B["dd"]=dd.values
    # deepest drawdown episode: from peak to trough
    trough=np.argmin(dd.values); peak=np.argmax(eq.values[:trough+1])
    ep=B.iloc[peak:trough+1]
    out["dd_episode"]=pd.Series({"days":len(ep),"book_sum":ep.book_return.sum(),"hold_sum":ep.coin_return.sum(),
        "windows":str(sorted(set(ep.index.get_level_values(0))))})
    # book in worst coin days
    B["hq"]=pd.qcut(B.coin_return,5,labels=False)
    out["book_by_hold_quint"]=B.groupby("hq").agg(hold=("coin_return","mean"),book=("book_return","mean"),n=("book_return","size"))
    # signal bars with vol relative to own coin
    S=[]
    for c, ws in data["bars"].items():
        mu=[]
        for w,b in ws.items():
            cl=b.close.values; a=cl[24::24]; mu.append(a/cl[:-24:24][:len(a)]-1)
        mu=np.nanmean(np.concatenate(mu))
        for w,b in ws.items():
            b=b.reset_index(drop=True); ts=pd.to_datetime(b.timestamp); cl=b.close
            lr=np.log(cl).diff()
            v24=lr.rolling(24).std(); v720=lr.rolling(720).std()
            nxt=(b.postRebalance_current_allocation.shift(0)*(cl.shift(-1)/cl-1))
            g24=nxt[::-1].rolling(24).sum()[::-1]  # position gain next 24 bars
            s=pd.DataFrame({"coin":c,"fc":b.forecast,"alloc":b.postRebalance_current_allocation,
               "ex":cl.shift(-24)/cl-1-mu,"vratio":v24/v720,"v720":v720,
               "p7":cl/cl.shift(168)-1,"p24":cl/cl.shift(24)-1,"g24":g24})[ts.dt.hour==19]
            S.append(s)
    S=pd.concat(S).dropna(subset=["ex","vratio"])
    L=S[S.fc>0].copy()
    for k in ["vratio","v720"]:
        L["q"]=L.groupby("coin")[k].transform(lambda x: pd.qcut(x,4,labels=False))
        g=L.groupby("q").agg(ex=("ex","mean"),sd=("ex","std"),n=("ex","size"),alloc=("alloc","mean"),g24=("g24","mean"))
        g["t"]=g.ex/(g.sd/np.sqrt(g.n))
        g["slope_t"]=[stats.linregress(L[L.q==q].fc,L[L.q==q].ex).slope/stats.linregress(L[L.q==q].fc,L[L.q==q].ex).stderr for q in g.index]
        out["long_by_coinq_"+k]=g
    # fall size relative to own vol: p24 / (v24*sqrt24)
    L["z"]=-L.p24/(L.v720*np.sqrt(24))
    L["zq"]=pd.qcut(L.z,5,labels=False)
    out["long_by_fall_in_vol"]=L.groupby("zq").agg(z=("z","mean"),ex=("ex","mean"),fc=("fc","mean"),n=("ex","size"))
    # vratio x fall: slope of ex on z in high vratio half vs low
    L["hv"]=L.groupby("coin")["vratio"].transform(lambda x: x>x.median())
    for h in [False,True]:
        x=L[L.hv==h]; r=stats.linregress(x.z,x.ex)
        out[f"z_slope_highvratio_{h}"]=f"slope {r.slope:.5f} t {r.slope/r.stderr:.2f} n {len(x)} meanex {x.ex.mean():.5f}"
    return out
