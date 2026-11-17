def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; grid=[]; days=[]
    for coin,ws in data["bars"].items():
        allc=[]
        for w,b in ws.items():
            c=b["close"].values
            r1=np.r_[c[1:]/c[:-1]-1,np.nan]
            allc.append(pd.Series(c))
        # coin mean 7-bar ret over all windows (grid)
        g7=[]
        for w,b in ws.items():
            c=b["close"].values
            for i in range(0,len(c)-7,7): g7.append(c[i+7]/c[i]-1)
        m7=np.mean(g7)
        m1=np.nanmean(np.concatenate([b["close"].pct_change().values for b in ws.values()]))
        for w,b in ws.items():
            c=b["close"].values
            n=len(c)
            r1=np.r_[c[1:]/c[:-1]-1,np.nan]
            ret14=pd.Series(c).pct_change(14).values
            ret60=pd.Series(c).pct_change(60).values
            fs=b.get("debug_info.components.fall_short.last_history_value")
            s=-fs.values if fs is not None else np.full(n,np.nan)
            pos=b["postRebalance_current_allocation"].values
            df=pd.DataFrame({"coin":coin,"w":w,"s":s,"pos":pos,"r1":r1,"gain":pos*r1,"mkt":pos*m1,"fc":b["forecast"].values,"ret60":ret60,"z":b["debug_info.components.fall_short.last_history_value"].values})
            rows.append(df)
            for i in range(0,n-7,7):
                grid.append((coin,s[i],b["forecast"].values[i],c[i+7]/c[i]-1-m7,ret60[i]))
    d=pd.concat(rows)
    G=pd.DataFrame(grid,columns=["coin","s","fc","ex","ret60"])
    d["zb"]=pd.cut(d["z"],[-30,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,30])
    out={}
    out["by_z_bar"]=d.groupby("zb").agg(n=("gain","size"),pos=("pos","mean"),gain_bp=("gain",lambda x:x.mean()*1e4),r1_bp=("r1",lambda x:x.mean()*1e4),mkt_bp=("mkt",lambda x:x.mean()*1e4))
    G["zb"]=pd.cut(-G["s"],[-30,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,30])
    out["grid_by_z"]=G.groupby("zb")["ex"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["s_quantiles"]=d["s"].describe()
    out["fc_quantiles"]=d["fc"].describe()
    d["side"]=np.sign(d["pos"].round(3))
    out["by_side"]=d.groupby("side").agg(n=("gain","size"),gain_bp=("gain",lambda x:x.mean()*1e4),mkt_bp=("mkt",lambda x:x.mean()*1e4),abspos=("pos",lambda x:x.abs().mean()))
    d["trend"]=pd.cut(d["ret60"],[-10,-0.2,0,0.2,0.5,100])
    out["short_by_60d"]=d[d.side<0].groupby("trend").agg(n=("gain","size"),gain_bp=("gain",lambda x:x.mean()*1e4),r1_bp=("r1",lambda x:x.mean()*1e4))
    out["all_by_60d"]=d.groupby("trend").agg(n=("gain","size"),r1_bp=("r1",lambda x:x.mean()*1e4))
    G["tr"]=pd.cut(G["ret60"],[-10,-0.2,0,0.2,0.5,100])
    Gf=G[G.fc<0]
    out["grid_short_by_60d"]=Gf.groupby("tr")["ex"].agg(["count","mean"])
    # book
    bk=[];hd=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            bk.append(dd[["day","book_return","coin_return"]].assign(w=w))
    D=pd.concat(bk).groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book"]=pd.Series({"book_mean_bp":D.book_return.mean()*1e4,"hold_mean_bp":D.coin_return.mean()*1e4,"book_sh":D.book_return.mean()/D.book_return.std()*np.sqrt(365),"hold_sh":D.coin_return.mean()/D.coin_return.std()*np.sqrt(365),"mkt_gain_bp":d["mkt"].mean()*1e4,"total_gain_bp":d["gain"].mean()*1e4,"frac_flat":(d.side==0).mean()})
    return out
