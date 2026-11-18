def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(20,min_periods=20).std()
            vr=b["volume"]/b["volume"].rolling(30,min_periods=30).mean()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            wick=(np.minimum(b["open"],c)-b["low"])/rng
            d=pd.DataFrame({"coin":coin,"w":w,"z":r/sd,"vr":vr,"wick":wick,"sd":sd,
                            "yr":pd.to_datetime(b["timestamp"]).dt.year,
                            "pos":b["postRebalance_current_allocation"]})
            for L in [5,10,20,30]:
                d[f"m{L}"]=(c/c.shift(L)-1)/(sd*np.sqrt(L))
            for h in [3,7]:
                d[f"f{h}"]=c.shift(-h)/c-1
            d3=d.iloc[::3].copy(); d3["h"]=3
            d7=d.iloc[::7].copy(); d7["h"]=7
            rows.append((d3,d7))
    D3=pd.concat([a for a,_ in rows]).dropna(subset=["f3"])
    D7=pd.concat([b for _,b in rows]).dropna(subset=["f7"])
    D3["ex"]=D3["f3"]-D3.groupby("coin")["f3"].transform("mean")
    D7["ex"]=D7["f7"]-D7.groupby("coin")["f7"].transform("mean")
    def tab(g):
        x=g["ex"].dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    def slope(g,col):
        g=g.dropna(subset=[col,"ex"]); x=g[col]; y=g["ex"]
        if len(g)<10: return pd.Series({"n":len(g),"b":np.nan,"t":np.nan})
        X=np.c_[np.ones(len(x)),x]; bb,res,_,_=np.linalg.lstsq(X,y,rcond=None)
        e=y-X@bb; s2=(e**2).sum()/(len(y)-2); se=np.sqrt(s2*np.linalg.inv(X.T@X)[1,1])
        return pd.Series({"n":len(g),"b":bb[1],"t":bb[1]/se})
    out={}
    out["mom_slope_3d"]=pd.DataFrame({L:slope(D3,f"m{L}") for L in [5,10,20,30]}).T
    out["mom_slope_7d"]=pd.DataFrame({L:slope(D7,f"m{L}") for L in [5,10,20,30]}).T
    for L in [10,20]:
        R=D7.dropna(subset=[f"m{L}"]).copy(); R["q"]=pd.qcut(R[f"m{L}"],5,labels=False)
        out[f"m{L}_quint_7d"]=R.groupby("q").apply(tab)
    out["m20_slope_7d_by_coin"]=D7.groupby("coin").apply(lambda g: slope(g,"m20"))
    out["m20_slope_7d_by_year"]=D7.groupby("yr").apply(lambda g: slope(g,"m20"))
    # volume ratio regardless of sign, and abs z
    D3["az"]=D3["z"].abs()
    out["vr_slope_all_3d"]=slope(D3,"vr").to_frame().T
    F=D3[D3["z"]<-1].copy()
    out["fall_vr_slope_3d_by_coin"]=F.groupby("coin").apply(lambda g: slope(g,"vr"))
    out["fall_vr_slope_3d_by_year"]=F.groupby("yr").apply(lambda g: slope(g,"vr"))
    F7=D7[D7["z"]<-1]
    out["fall_vr_slope_7d"]=slope(F7,"vr").to_frame().T
    out["fall_wick_slope_3d"]=slope(F,"wick").to_frame().T
    U=D3[D3["z"]>1]
    out["rise_vr_slope_3d"]=slope(U,"vr").to_frame().T
    out["absz_slope_3d"]=slope(D3,"az").to_frame().T
    # book: largest days and the position/forecast context
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; dd.append(d)
    B=pd.concat(dd).dropna(subset=["book_return"])
    q=B["book_return"].quantile([0.01,0.99])
    out["book_tail_days_coinret"]=pd.DataFrame({
        "worst1%_mean_book":[B[B.book_return<=q[0.01]].book_return.mean()],
        "worst1%_mean_coin":[B[B.book_return<=q[0.01]].coin_return.mean()],
        "best1%_mean_book":[B[B.book_return>=q[0.99]].book_return.mean()],
        "best1%_mean_coin":[B[B.book_return>=q[0.99]].coin_return.mean()],
        "share_days_invested":[(B.book_return!=0).mean()]})
    return out
