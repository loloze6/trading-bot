def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; trades=data["trades"]
    out={}
    hr_rows=[]; ev=[]; book=[]; g24=[]; trd=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"]); b["hour"]=ts.dt.hour.values
            cl=b["close"].values.astype(float)
            r1=np.r_[cl[1:]/cl[:-1]-1,np.nan]
            b["r1"]=r1
            r2=np.full(len(cl),np.nan); r2[:-2]=cl[2:]/cl[:-2]-1
            r24=np.full(len(cl),np.nan); r24[24:]=cl[24:]/cl[:-24]-1
            lr=pd.Series(np.log(cl)).diff()
            vol=lr.rolling(168).std()*np.sqrt(24)
            vs=r24/vol.values
            maxabs=lr.abs().rolling(24).max().values
            sumabs=lr.abs().rolling(24).sum().values
            conc=maxabs/sumabs
            f24=np.full(len(cl),np.nan); f24[:-24]=cl[24:]/cl[:-24]-1
            hr_rows.append(pd.DataFrame({"coin":c,"hour":b["hour"],"r1":r1}))
            m=(b["hour"].values==20)
            ev.append(pd.DataFrame({"coin":c,"win":w,"vs":vs[m],"r2":r2[m],"fc":b["forecast"].values[m]}))
            pos=b["postRebalance_current_allocation"].values.astype(float)
            book.append(pd.DataFrame({"coin":c,"hour":b["hour"],"g":pos*r1,"pos":pos,
                 "fee":(b["total_portfolio_value"].shift(-1)*0+ (b["postRebalance_total_value"]-b["total_portfolio_value"])/b["total_portfolio_value"]).values}))
            idx=np.arange(24,len(cl),24)
            g24.append(pd.DataFrame({"coin":c,"vs":vs[idx],"conc":conc[idx],"f24":f24[idx]}))
            t=trades[c].get(w) if hasattr(trades[c],"get") else None
            if t is not None and len(t): trd.append(t.assign(coin=c))
    H=pd.concat(hr_rows).dropna()
    gh=H.groupby("hour")["r1"].agg(["mean","std","count"]); gh["t"]=gh["mean"]/(gh["std"]/np.sqrt(gh["count"]))
    out["hourly_ret"]=gh[["mean","t","count"]]
    E=pd.concat(ev).dropna(subset=["vs","r2"])
    E["q"]=pd.qcut(E["vs"],10,labels=False)
    eq=E.groupby("q").agg(vs=("vs","mean"),r2=("r2","mean"),sd=("r2","std"),n=("r2","count"))
    eq["t"]=eq["r2"]/(eq["sd"]/np.sqrt(eq["n"])); out["r2_after21_by_vs_decile"]=eq
    out["r2_after21_by_coin_fall"]=E[E.vs<0].groupby("coin")["r2"].agg(["mean","count"])
    B=pd.concat(book)
    out["book_gain_fee_by_hour"]=B.groupby("hour").agg(g=("g","sum"),fee=("fee","sum"),pos=("pos","mean")).loc[lambda d:(d.pos.abs()>1e-4)|(d.fee.abs()>1e-6)]
    out["book_total_gain_fee"]=pd.Series({"gain":B["g"].sum(),"fee":B["fee"].sum()})
    if trd:
        T=pd.concat(trd)
        out["trades"]=T.groupby("coin").agg(n=("side","count"),pl=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur=("duration_minutes","mean"),comm=("total_commission","mean"))
    G=pd.concat(g24).dropna()
    G["vq"]=pd.qcut(G["vs"],5,labels=False); G["cq"]=pd.qcut(G["conc"],3,labels=False)
    G["sf"]=np.sign(G["vs"])*G["f24"]
    out["next24_by_vs_q_conc"]=G.pivot_table(index="vq",columns="cq",values="f24",aggfunc="mean")
    out["next24_counts"]=G.pivot_table(index="vq",columns="cq",values="f24",aggfunc="count")
    return out
