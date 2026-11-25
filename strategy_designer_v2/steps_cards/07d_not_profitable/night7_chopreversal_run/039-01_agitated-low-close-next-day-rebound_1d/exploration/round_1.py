def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    dayrows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            rng=(b.high-b.low).replace(0,np.nan)
            b["cl"]=(b.high-b.close)/rng
            b["r1"]=b.close.shift(-1)/b.close-1
            b["r3"]=b.close.shift(-3)/b.close-1
            b["ret1d"]=b.close/b.close.shift(1)-1
            b["tr20"]=b.close/b.close.shift(20)-1
            b["pos"]=b.postRebalance_current_allocation
            b["gross"]=b.pos*b.r1
            b["net"]=b.postRebalance_total_value.shift(-1)/b.postRebalance_total_value-1
            b["turn"]=(b.postRebalance_current_allocation-b.previous_allocation).abs()
            b["agit"]=b.regime!="chop"
            b["coin"]=coin; b["w"]=w; b["i"]=np.arange(len(b))
            rows.append(b[["coin","w","i","timestamp","cl","r1","r3","ret1d","tr20","pos","gross","net","turn","agit","forecast"]])
        for w,d in data["days"][coin].items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dayrows.append(d)
    A=pd.concat(rows,ignore_index=True)
    mu=A.r1.mean(); A["x1"]=A.r1-mu
    out={}
    act=A[A.pos.abs()>1e-9].copy()
    act["side"]=np.where(act.pos>0,"long","short")
    def agg(g):
        return pd.Series({"n":len(g),"gross_mean":g.gross.mean(),"net_mean":g.net.mean(),"turn_mean":g.turn.mean(),
                          "sig_ret":(np.sign(g.pos)*g.x1).mean(),"t":stats.ttest_1samp(np.sign(g.pos)*g.x1,0,nan_policy='omit').statistic})
    out["by_side"]=act.groupby("side").apply(agg)
    act["clbin"]=pd.cut(act.cl,[-0.01,0.1,0.25,0.5,0.75,0.9,1.01])
    out["by_cl_bin"]=act.groupby(["clbin"]).apply(agg)
    # all agitated bars, next-day excess by cl bin, and calm
    A["clbin"]=pd.cut(A.cl,[-0.01,0.1,0.25,0.5,0.75,0.9,1.01])
    out["x1_by_cl_agit"]=A.groupby(["agit","clbin"]).x1.agg(["count","mean"]).unstack(0)
    # 3-day
    A["x3"]=A.r3-A.r3.mean()
    out["x3_by_cl_agit"]=A[A.agit].groupby("clbin").x3.agg(["count","mean"])
    # trend context
    A["trb"]=pd.cut(A.tr20,[-9,-0.1,0,0.1,9])
    A["d1b"]=pd.cut(A.ret1d,[-9,-0.03,0,0.03,9])
    act=act.merge(A[["coin","w","i","trb","d1b"]],on=["coin","w","i"])
    out["by_side_trend20"]=act.groupby(["side","trb"]).apply(agg)
    out["by_side_day1"]=act.groupby(["side","d1b"]).apply(agg)
    out["by_window"]=act.groupby("w").apply(agg)
    # book daily
    D=pd.concat(dayrows,ignore_index=True)
    bk=D.groupby(["w","day"]).book_return.mean().dropna()
    cn=D.groupby(["w","day"]).coin_return.mean().dropna()
    v=(1+bk).cumprod(); dd=v/v.cummax()-1
    out["deepest_fall"]=dd.min()
    trough=dd.idxmin(); peak=v.loc[:trough].idxmax()
    seg=bk.loc[peak:trough]
    out["fall_info"]=pd.Series({"days":len(seg),"win_peak":peak[0],"win_trough":trough[0],"coin_ret_in_fall":(1+cn.loc[peak:trough]).prod()-1})
    out["book_by_window"]=pd.DataFrame({"book_sum":bk.groupby(level=0).sum(),"coin_sum":cn.groupby(level=0).sum()})
    out["fee_drag_per_bar"]=(act.gross.mean()-act.net.mean())
    return out
