def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy(); c=b["close"]
            b["r1"]=c.shift(-1)/c-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["dpos"]=(b["pos"]-b["previous_allocation"]).abs()
            b["gross"]=b["pos"]*b["r1"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["ret"]=c/c.shift(1)-1
            b["z"]=b["ret"]/b["ret"].rolling(20).std()
            b["tr20"]=c/c.shift(20)-1
            b["tr20z"]=b["tr20"]/(b["ret"].rolling(20).std()*np.sqrt(20))
            b["coin"]=coin; b["w"]=w
            rows.append(b)
    d=pd.concat(rows).dropna(subset=["r1"])
    d["mu"]=d["coin"].map(d.groupby("coin")["ret"].mean())
    d["ex"]=d["r1"]-d["mu"]
    out={}
    out["turnover"]=pd.Series({"mean_abs_trade":d["dpos"].mean(),"mean_abspos":d["pos"].abs().mean(),
        "fee_per_turn":d["fee"].sum()/d["dpos"].sum(),"share_sign_flip":(np.sign(d["pos"])!=np.sign(d["previous_allocation"])).mean()})
    out["by_window"]=d.groupby("w").apply(lambda g: pd.Series({"gross":g["gross"].mean(),"net":(g["gross"]-g["fee"]).mean(),
        "coin_r":g["ret"].mean(),"short_gross":g.loc[g.pos<0,"gross"].mean(),"long_gross":g.loc[g.pos>0,"gross"].mean()}))
    dz=d.dropna(subset=["z","tr20z"]).copy()
    dz["tq"]=pd.qcut(dz["tr20z"],4)
    dz["zs"]=np.where(dz["z"]>0,"up","dn")
    out["ex_by_trend_q_side"]=dz.groupby(["tq","zs"]).apply(lambda g: pd.Series({"n":len(g),"mean_ex":g["ex"].mean(),
        "t":g["ex"].mean()/g["ex"].std()*np.sqrt(len(g)),"corr_z_ex":np.corrcoef(g["z"],g["ex"])[0,1]}))
    # graded: z*ex slope inside up/down trend
    for k,g in dz.groupby(np.where(dz["tr20z"]>0,"up","dn")):
        s=-g["z"]*g["ex"]
        out["rev_prod_"+k]=pd.Series({"n":len(g),"mean":s.mean(),"t":s.mean()/s.std()*np.sqrt(len(g))})
    # 3-day grid non-overlapping, 3-day z
    res=[]
    for (coin,w),g in d.groupby(["coin","w"]):
        g=g.reset_index(drop=True); c=g["close"]
        idx=np.arange(0,len(g)-3,3)
        sd=g["ret"].rolling(20).std()
        z3=(c/c.shift(3)-1)/(sd*np.sqrt(3))
        f3=c.shift(-3)/c-1
        res.append(pd.DataFrame({"z3":z3.iloc[idx].values,"f3":f3.iloc[idx].values-3*g["mu"].iloc[0],"tr":g["tr20z"].iloc[idx].values}))
    r=pd.concat(res).dropna()
    r["zq"]=pd.qcut(r["z3"],4)
    out["f3_by_z3_trend"]=r.groupby([np.where(r.tr>0,"up","dn"),"zq"]).apply(lambda g: pd.Series({"n":len(g),"mean_f3":g["f3"].mean(),"t":g["f3"].mean()/g["f3"].std()*np.sqrt(len(g))}))
    return out
