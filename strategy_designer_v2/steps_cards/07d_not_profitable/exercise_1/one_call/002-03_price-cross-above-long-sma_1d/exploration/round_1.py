def explore(data):
    import pandas as pd, numpy as np
    rows=[]; trs=[]; dys=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            b["r1"]=b["close"].shift(-1)/b["close"]-1
            b["r20"]=b["close"].shift(-20)/b["close"]-1
            b["past20"]=b["close"]/b["close"].shift(20)-1
            lr=np.log(b["close"]).diff()
            b["vol20"]=lr.rolling(20).std()
            b["alloc"]=b["postRebalance_current_allocation"]
            b["raw"]=b["debug_info.components.above_ma.last_history_value"]
            b["coin"]=c; b["w"]=w
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["bv_r"]=b["postRebalance_total_value"].shift(-1)/b["postRebalance_total_value"]-1
            rows.append(b[["coin","w","year","forecast","alloc","raw","r1","r20","past20","vol20","bv_r"]])
            t=data["trades"][c][w].copy(); t["coin"]=c; trs.append(t)
    B=pd.concat(rows); B=B.dropna(subset=["r1"])
    B["gross"]=B["alloc"]*B["r1"]
    T=pd.concat(trs)
    out={}
    out["alloc_desc"]=B["alloc"].describe()
    B["on"]=B["forecast"]>0
    on=B[B["on"]].copy()
    on["fq"]=pd.qcut(on["forecast"].rank(method="first"),5,labels=False)
    out["by_fq"]=on.groupby("fq").agg(n=("r1","size"),fc=("forecast","mean"),raw=("raw","mean"),r1=("r1","mean"),r20=("r20","mean"),alloc=("alloc","mean"),gross=("gross","mean"))
    on["rq"]=pd.qcut(on["raw"].rank(method="first"),5,labels=False)
    out["by_rawq"]=on.groupby("rq").agg(n=("r1","size"),raw=("raw","mean"),fc=("forecast","mean"),r1=("r1","mean"),r20=("r20","mean"))
    out["on_vs_off"]=B.groupby("on").agg(n=("r1","size"),r1=("r1","mean"),sd=("r1","std"),r20=("r20","mean"))
    out["gross_vs_book"]=pd.Series({"gross_mean":B["gross"].mean(),"book_mean":B["bv_r"].mean(),"coin_mean":B["r1"].mean()})
    out["trades"]=pd.Series({"n":len(T),"days_mean":T["duration_minutes"].mean()/1440,"days_med":T["duration_minutes"].median()/1440,
        "pl_gross_mean":T["profit_loss_percent"].mean(),"pl_net_mean":T["net_profit_loss_percent"].mean(),
        "comm_sum":T["total_commission"].sum(),"long_share":(T["side"]=="LONG").mean(),"win":(T["profit_loss_percent"]>0).mean()})
    T["dq"]=pd.qcut(T["duration_minutes"].rank(method="first"),4,labels=False)
    out["trades_by_dur"]=T.groupby("dq").agg(n=("side","size"),days=("duration_minutes",lambda x:x.mean()/1440),g=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"))
    on["vq"]=pd.qcut(on["vol20"].rank(method="first"),3,labels=False)
    out["on_by_vol"]=on.groupby("vq").agg(n=("r1","size"),vol=("vol20","mean"),gross=("gross","mean"),r1=("r1","mean"))
    on["up"]=on["past20"]>0
    out["on_by_past20"]=on.groupby("up").agg(n=("r1","size"),gross=("gross","mean"),r1=("r1","mean"),r20=("r20","mean"))
    out["by_year"]=B.groupby("year").agg(n=("r1","size"),onsh=("on","mean"),gross=("gross","mean"),coin=("r1","mean"),book=("bv_r","mean"))
    out["by_coin"]=B.groupby("coin").agg(onsh=("on","mean"),gross=("gross","mean"),coin=("r1","mean"),book=("bv_r","mean"))
    return out
