def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; grid=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            b["nr"]=b.close.shift(-1)/b.close-1
            b["al"]=b.postRebalance_current_allocation
            b["g"]=b.al*b.nr
            b["r30"]=b.close/b.close.shift(30)-1
            b["f7"]=b.close.shift(-7)/b.close-1
            b["nh"]=b["debug_info.components.near_high.last_history_value"]
            b["coin"]=c; b["w"]=w
            rows.append(b[["coin","w","regime","forecast","al","nr","g","r30","f7","nh","volume"]])
            grid.append(b.iloc[::7][["coin","w","regime","forecast","al","f7","nh","r30"]])
    B=pd.concat(rows); G=pd.concat(grid)
    B["side"]=np.sign(B.al).map({1:"long",-1:"short",0:"flat"})
    out={}
    out["by_regime_side"]=B.groupby(["regime","side"]).agg(n=("g","size"),mean_g=("g","mean"),mean_nr=("nr","mean"),mean_al=("al","mean"))
    t=B[B.regime=="trending"].dropna(subset=["forecast","g"])
    t["fq"]=pd.qcut(t.forecast,5,labels=False,duplicates="drop")
    out["trend_by_fq"]=t.groupby("fq").agg(n=("g","size"),f=("forecast","mean"),al=("al","mean"),g=("g","mean"),nr=("nr","mean"))
    gt=G[G.regime=="trending"].dropna(subset=["f7","nh"])
    gt["nq"]=pd.qcut(gt.nh,5,labels=False,duplicates="drop")
    gt["rq"]=pd.qcut(gt.r30,5,labels=False,duplicates="drop")
    out["grid_by_near"]=gt.groupby("nq").agg(n=("f7","size"),nh=("nh","mean"),f7=("f7","mean"))
    out["grid_by_r30"]=gt.groupby("rq").agg(n=("f7","size"),r30=("r30","mean"),f7=("f7","mean"))
    gu=G[G.regime!="trending"].dropna(subset=["f7"])
    out["grid_nontrend_f7"]=pd.Series({"n":len(gu),"f7":gu.f7.mean(),"trend_f7":gt.f7.mean()})
    # book daily
    D=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=c; d["w"]=w; D.append(d)
    D=pd.concat(D)
    D["wn"]=D.w.str[1:].astype(int)
    bk=D.groupby(["wn","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna().reset_index().sort_values(["wn","day"])
    eq=(1+bk.br).cumprod(); dd=eq/eq.cummax()-1
    bk["dd"]=dd.values
    out["book"]=pd.Series({"mean":bk.br.mean(),"sd":bk.br.std(),"cr_mean":bk.cr.mean(),"maxdd":dd.min(),"n":len(bk)})
    out["book_by_window"]=bk.groupby("wn").agg(br=("br","mean"),cr=("cr","mean"),mindd=("dd","min"))
    return out
