def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            r1=b["close"].shift(-1)/b["close"]-1
            pos=b["postRebalance_current_allocation"]
            gross=pos*r1
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            turn=(pos-b["previous_allocation"]).abs()
            f=b["forecast"]
            lr=np.log(b["close"]).diff()
            v24=lr.rolling(24).std()
            vrel=v24/v24.rolling(720,min_periods=100).mean()
            # forward returns at several horizons
            d=pd.DataFrame({"coin":c,"win":w,"gross":gross,"fee":fee,"turn":turn,"f":f,"pos":pos,
                            "r1":r1,"vrel":vrel,"hour":pd.to_datetime(b["timestamp"]).dt.hour,"lr":lr})
            for h in [2,4,8,24]:
                d[f"r{h}"]=b["close"].shift(-h)/b["close"]-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    out["per_bar"]=pd.Series({"gross_mean":D.gross.mean(),"fee_mean":D.fee.mean(),"turn_mean":D.turn.mean(),
        "fee_per_turn":D.fee.sum()/D.turn.sum(),"abs_pos_mean":D.pos.abs().mean(),
        "gross_per_day":D.gross.mean()*24,"fee_per_day":D.fee.mean()*24})
    D["q"]=pd.qcut(D.f.abs().rank(method="first"),5,labels=False)
    out["by_absf_quintile"]=D.groupby("q").agg(gross=("gross","mean"),fee=("fee","mean"),turn=("turn","mean"),abspos=("pos",lambda x:x.abs().mean()))
    D["vq"]=pd.qcut(D.vrel,5,labels=False)
    out["by_vol_quintile"]=D.groupby("vq").agg(gross=("gross","mean"),fee=("fee","mean"),abspos=("pos",lambda x:x.abs().mean()))
    # sign of forecast times forward return over horizons, normalized by abs pos, nonoverlap
    res={}
    for h in [1,2,4,8,24]:
        col="r1" if h==1 else f"r{h}"
        sub=D.groupby(["coin","win"],group_keys=False).apply(lambda g:g.iloc[::h])
        x=(np.sign(sub.f)*sub[col]).dropna()
        res[h]=pd.Series({"mean":x.mean(),"per_hour":x.mean()/h,"t":x.mean()/x.std()*np.sqrt(len(x)),"n":len(x)})
    out["sign_f_x_fwd"]=pd.DataFrame(res).T
    # strong moves: top decile abs f, forward returns signed
    top=D[D.f.abs()>=D.f.abs().quantile(0.9)]
    out["top_decile_signed_fwd"]=pd.Series({h:(np.sign(top.f)*top["r1" if h==1 else f"r{h}"]).mean() for h in [1,2,4,8,24]})
    dd=pd.concat([x.assign(coin=c,win=w) for c,ws in data["days"].items() for w,x in ws.items()])
    out["daily"]=pd.Series({"book_mean":dd.book_return.mean(),"coin_mean":dd.coin_return.mean()})
    out["coin_gross_fee"]=D.groupby("coin").agg(gross=("gross","mean"),fee=("fee","mean"))
    return out
