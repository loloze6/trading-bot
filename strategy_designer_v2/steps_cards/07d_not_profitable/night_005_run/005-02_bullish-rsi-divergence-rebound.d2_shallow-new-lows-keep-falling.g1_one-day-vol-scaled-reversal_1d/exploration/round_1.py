def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy(); c=b["close"]
            b["r1"]=c.shift(-1)/c-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["gross"]=b["pos"]*b["r1"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["ret"]=c/c.shift(1)-1
            b["z"]=b["ret"]/b["ret"].rolling(20).std()
            b["tr20"]=c/c.shift(20)-1
            b["coin"]=coin; b["w"]=w
            rows.append(b)
    d=pd.concat(rows).dropna(subset=["r1"])
    d["mu"]=d["coin"].map(d.groupby("coin")["ret"].mean())
    d["ex"]=d["r1"]-d["mu"]
    d["mkt"]=d["pos"]*d["mu"]
    d["side"]=np.sign(d["pos"])
    d["trs"]=np.where(d["tr20"]>0,"tr20_up","tr20_dn")
    def agg(g):
        return pd.Series({"n":len(g),"gross":g["gross"].mean(),"fee":g["fee"].mean(),
                          "net":(g["gross"]-g["fee"]).mean(),"mkt":g["mkt"].mean(),
                          "meanpos":g["pos"].mean(),"abspos":g["pos"].abs().mean(),
                          "t_gross":g["gross"].mean()/g["gross"].std()*np.sqrt(len(g))})
    out={}
    out["all"]=agg(d).to_frame().T
    out["by_side"]=d.groupby("side").apply(agg)
    out["by_side_trend"]=d.groupby(["side","trs"]).apply(agg)
    out["by_coin_side"]=d.groupby(["coin","side"]).apply(agg)
    dz=d.dropna(subset=["z"]).copy()
    dz["zq"]=pd.qcut(dz["z"],6)
    out["ex_by_z"]=dz.groupby("zq").apply(lambda g: pd.Series({"n":len(g),"mean_ex":g["ex"].mean(),
        "t":g["ex"].mean()/g["ex"].std()*np.sqrt(len(g)),"gross":g["gross"].mean(),"fee":g["fee"].mean()}))
    out["ex_by_z_trend"]=dz.groupby(["trs",pd.cut(dz["z"],[-99,-1,0,1,99])]).apply(lambda g: pd.Series({"n":len(g),
        "mean_ex":g["ex"].mean(),"t":g["ex"].mean()/g["ex"].std()*np.sqrt(len(g))}))
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; dd.append(x)
    dd=pd.concat(dd).dropna(subset=["book_return"])
    out["days"]=dd.groupby("coin")[["book_return","coin_return"]].agg(["mean","std"])
    return out
