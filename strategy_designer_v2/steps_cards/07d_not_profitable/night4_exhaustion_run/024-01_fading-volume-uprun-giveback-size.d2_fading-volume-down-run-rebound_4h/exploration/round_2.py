import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    days=data["days"]; bars=data["bars"]
    coins=list(days.keys())
    wins=sorted({w for c in coins for w in days[c]}, key=lambda s:int(s[1:]))
    rows=[]
    for w in wins:
        fr=[]
        for c in coins:
            if w in days[c]:
                d=days[c][w][["day","book_return","coin_return"]].copy(); fr.append(d)
        d=pd.concat(fr).groupby("day")[["book_return","coin_return"]].mean().reset_index()
        d["win"]=w; rows.append(d)
    B=pd.concat(rows,ignore_index=True).dropna().reset_index(drop=True)
    B["equity"]=(1+B["book_return"]).cumprod()
    B["ddn"]=B["equity"]/B["equity"].cummax()-1
    perw=B.groupby("win",sort=False).agg(book=("book_return",lambda x:(1+x).prod()-1),hold=("coin_return",lambda x:(1+x).prod()-1),days=("book_return","size"))
    perw["book_minus_hold"]=perw["book"]-perw["hold"]
    trough=int(B["ddn"].idxmin()); peak=int(B["equity"].iloc[:trough+1].idxmax())
    ep=B.iloc[peak:trough+1]
    epi={"days":len(ep),"depth":B["ddn"].min(),"book":(1+ep["book_return"]).prod()-1,"hold":(1+ep["coin_return"]).prod()-1,"first_win":ep["win"].iloc[0],"last_win":ep["win"].iloc[-1]}
    # worst 5% book days vs coin
    q=B["book_return"].quantile(0.05)
    worst={"worst5pct_book_mean":B.loc[B["book_return"]<=q,"book_return"].mean(),"worst5pct_coin_mean":B.loc[B["book_return"]<=q,"coin_return"].mean(),
           "corr_book_hold":B["book_return"].corr(B["coin_return"]),"book_sd":B["book_return"].std(),"hold_sd":B["coin_return"].std()}
    br=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"]
            r1=cl.shift(-1)/cl-1
            al=b["postRebalance_current_allocation"]
            lr=np.log(cl).diff()
            br.append(pd.DataFrame({"coin":c,"win":w,"g":al*r1,"alloc":al,
                "p30":cl/cl.shift(180)-1,"p7":cl/cl.shift(42)-1,
                "vol_ratio":lr.rolling(42).std()/lr.rolling(180).std(),
                "f18":cl.shift(-18)/cl-1,"grid":(np.arange(len(b))%18==0),"fc":b["forecast"],"r1":r1}))
    R=pd.concat(br,ignore_index=True)
    drift=R[R["grid"]].groupby("coin")["f18"].mean()
    R["u18"]=R["f18"]-R["coin"].map(drift)
    R["q30"]=pd.qcut(R["p30"],5,labels=False)
    R["q7"]=pd.qcut(R["p7"],5,labels=False)
    R["qv"]=pd.qcut(R["vol_ratio"],5,labels=False)
    act=R[R["alloc"].abs()>0]
    def gt(col):
        o=act.groupby(col).agg(n=("g","size"),gain_mean=("g","mean"),gain_sd=("g","std"),alloc=("alloc","mean"))
        o["t"]=o["gain_mean"]/(o["gain_sd"]/np.sqrt(o["n"])); return o
    cs=R[R["grid"]&(R["fc"]>=2)].dropna(subset=["u18"])
    def tab(col):
        o=cs.groupby(col)["u18"].agg(["size","mean","std"]); o["t"]=o["mean"]/(o["std"]/np.sqrt(o["size"])); return o
    # position held in deepest-fall windows vs elsewhere
    epw=set(B.iloc[peak:trough+1]["win"])
    R["in_ep"]=R["win"].isin(epw)
    pos=R.groupby("in_ep").agg(share_in=("alloc",lambda x:(x.abs()>0).mean()),mean_alloc=("alloc","mean"),gain=("g","mean"),p30=("p30","mean"))
    return {"perwindow":perw,"deepest_episode":pd.Series(epi),"worst_days":pd.Series(worst),
            "gain_by_p30q":gt("q30"),"gain_by_p7q":gt("q7"),"gain_by_volratio_q":gt("qv"),
            "cases_u18_by_p30q":tab("q30"),"cases_u18_by_p7q":tab("q7"),"cases_u18_by_volratio_q":tab("qv"),
            "pos_in_episode_windows":pos}
