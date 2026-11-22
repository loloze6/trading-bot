import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    days=data["days"]; bars=data["bars"]
    coins=list(days.keys())
    wins=sorted({w for c in coins for w in days[c]}, key=lambda s:int(s[1:]))
    # book daily
    rows=[]
    for w in wins:
        fr=[]
        for c in coins:
            if w in days[c]:
                d=days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; fr.append(d)
        d=pd.concat(fr).groupby("day")[["book_return","coin_return"]].mean().reset_index()
        d["w"]=w; rows.append(d)
    B=pd.concat(rows,ignore_index=True).dropna()
    B["eq"]=(1+B.book_return).cumprod(); B["dd"]=B.eq/B.eq.cummax()-1
    B["heq"]=(1+B.coin_return).cumprod()
    perw=B.groupby("w",sort=False).agg(book=("book_return",lambda x:(1+x).prod()-1),hold=("coin_return",lambda x:(1+x).prod()-1),mindd=("dd","min"))
    # deepest fall episode
    trough=B.dd.idxmin(); peak=B.eq[:trough+1].idxmax()
    ep=B.loc[peak:trough]
    epi={"days":len(ep),"depth":B.dd.min(),"book":(1+ep.book_return).prod()-1,"hold":(1+ep.coin_return).prod()-1,"windows":",".join(ep.w.unique())}
    # bar-level: position gain by coin's prior 30-day return and 7-day return quintiles
    br=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            r1=b.close.shift(-1)/b.close-1
            g=b.postRebalance_current_allocation*r1
            p30=b.close/b.close.shift(180)-1
            p7=b.close/b.close.shift(42)-1
            f18=b.close.shift(-18)/b.close-1
            grid=(np.arange(len(b))%18==0)
            br.append(pd.DataFrame({"coin":c,"w":w,"g":g,"alloc":b.postRebalance_current_allocation,"p30":p30,"p7":p7,"f18":f18,"grid":grid,"fc":b.forecast,"r1":r1}))
    R=pd.concat(br,ignore_index=True)
    drift=R[R.grid].groupby("coin").f18.mean()
    R["u18"]=R.f18-R.coin.map(drift)
    R["q30"]=pd.qcut(R.p30,5,labels=False)
    R["q7"]=pd.qcut(R.p7,5,labels=False)
    act=R[R.alloc.abs()>0]
    g30=act.groupby("q30").agg(n=("g","size"),gain_mean=("g","mean"),alloc=("alloc","mean"),p30=("p30","mean"))
    g7=act.groupby("q7").agg(n=("g","size"),gain_mean=("g","mean"),alloc=("alloc","mean"),p7=("p7","mean"))
    cs=R[R.grid&(R.fc>=2)].dropna(subset=["u18"])
    def tab(col):
        o=cs.groupby(col).u18.agg(["size","mean","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["size"])); return o
    # exposure stats
    exp={"share_bars_in_pos":(R.alloc.abs()>0).mean(),"mean_alloc_when_in":act.alloc.mean(),"max_alloc":R.alloc.max(),
         "corr_book_hold_daily":B.book_return.corr(B.coin_return),
         "book_sd":B.book_return.std(),"hold_sd":B.coin_return.std()}
    return {"perwindow":perw,"deepest_episode":pd.Series(epi),"exposure":pd.Series(exp),
            "gain_by_p30q":g30,"gain_by_p7q":g7,"cases_u18_by_p30q":tab("q30"),"cases_u18_by_p7q":tab("q7")}
