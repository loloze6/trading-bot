def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        allr=pd.concat([pd.Series(df["close"].astype(float).values).pct_change() for df in ws.values()])
        cm=allr.mean()
        for w,df in ws.items():
            c=df["close"].astype(float).reset_index(drop=True)
            d=pd.DataFrame()
            d["r1"]=c.pct_change()
            d["vol"]=d["r1"].rolling(24).std()
            d["z"]=d["r1"]/d["vol"]
            d["nx"]=c.shift(-1)/c-1-cm
            d["r4"]=c.pct_change(4)
            d["z4"]=d["r4"]/(d["vol"]*2)
            d["nx4"]=c.shift(-4)/c-1-4*cm
            d["r24"]=c.pct_change(24)
            d["z24"]=d["r24"]/(d["vol"]*np.sqrt(24))
            d["nx24"]=c.shift(-24)/c-1-24*cm
            d["vol_rel"]=d["vol"]/d["vol"].rolling(720,min_periods=200).median()
            d["pos"]=np.arange(len(d))
            ts=pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            d["hour"]=ts.dt.hour; d["year"]=ts.dt.year
            d["coin"]=coin; d["win"]=w
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D=D[np.isfinite(D.z)]
    out={}
    def sl(g,x,y):
        g=g[[x,y]].dropna()
        if len(g)<100: return pd.Series({"n":len(g),"slope_bp":np.nan,"t":np.nan})
        r=stats.linregress(-g[x].clip(-6,6),g[y])
        return pd.Series({"n":len(g),"slope_bp":r.slope*1e4,"t":r.slope/r.stderr})
    D["vb"]=pd.qcut(D.vol_rel,5,labels=False)
    # asymmetry by vol quintile: mean next return after down vs up big moves
    big=D[D.z.abs()>1]
    a=big.assign(side=np.where(big.z<0,"down","up")).groupby(["vb","side"]).nx.agg(["mean","std","count"])
    a["mean_bp"]=a["mean"]*1e4; a["t"]=a["mean"]/a["std"]*np.sqrt(a["count"])
    out["big_move_side_by_vol"]=a[["mean_bp","t","count"]]
    # 4h non-overlapping
    g4=D[D.pos%4==0]
    out["h4_by_vol"]=g4.groupby("vb").apply(lambda g:sl(g,"z4","nx4"))
    g24=D[D.pos%24==0]
    out["h24_by_vol"]=g24.groupby("vb").apply(lambda g:sl(g,"z24","nx24"))
    # hour pattern stability: halves
    D["half"]=np.where(D.year<=2021,"early","late")
    hb=D.groupby(["half","hour"]).apply(lambda g:sl(g,"z","nx")["t"]).unstack(0)
    out["hour_t_by_half"]=hb
    out["hour_t_corr_halves"]=float(hb.corr().iloc[0,1])
    # vol regime by coin
    out["coin_by_vol_top"]=D[D.vb==4].groupby("coin").apply(lambda g:sl(g,"z","nx"))
    out["vol_top_by_year"]=D[D.vb==4].groupby("year").apply(lambda g:sl(g,"z","nx"))
    # costs: book daily vs gross
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            tr.append(t[["profit_loss_percent","net_profit_loss_percent","duration_minutes"]])
    T=pd.concat(tr)
    out["trades"]=T.describe().loc[["count","mean","50%"]]
    return out
