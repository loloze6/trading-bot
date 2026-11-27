def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h=b["high"]; l=b["low"]; v=b["volume"]
            r1 = c.pct_change()
            rng = (h-l)/c.shift(1)
            width = rng / rng.rolling(20, min_periods=20).mean()
            sd20 = r1.rolling(20, min_periods=20).std()
            sd30 = r1.rolling(30, min_periods=30).std()
            agit = sd30 / sd30.rolling(60, min_periods=30).median()
            df = pd.DataFrame({"coin":coin,"win":w,"ts":pd.to_datetime(b["timestamp"]),
                "r1":r1,"nxt":c.shift(-1)/c-1,"nxt2":c.shift(-2)/c-1,"nxt3":c.shift(-3)/c-1,
                "d2":c.shift(-2)/c.shift(-1)-1,
                "width":width,"z1":r1/sd20.shift(1),"tr60":c/c.shift(60)-1,
                "falling":(b["regime"]!="chop"),"agit":agit,
                "vr":v/v.rolling(20,min_periods=20).mean(),
                "clv":(c-l)/(h-l),"alloc":b["postRebalance_current_allocation"]})
            df["pos"]=np.arange(len(df))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["day"]=D["ts"].dt.floor("D"); D["year"]=D["ts"].dt.year
    for col in ["nxt","nxt2","nxt3","d2"]:
        dr = D.groupby("coin")[col].mean()
        D["u_"+col]=D[col]-D["coin"].map(dr)
    def T(mask,col="u_nxt"):
        x=D.loc[mask,[col,"day"]].dropna()
        n=len(x)
        if n<10: return pd.Series({"mean":np.nan,"n":n,"days":0,"t":np.nan})
        m=x[col].mean()
        g=x.groupby("day")[col].agg(["sum","size"])
        se=np.sqrt(((g["sum"]-m*g["size"])**2).sum())/n
        return pd.Series({"mean":m,"n":n,"days":len(g),"t":m/se})
    D["trend"]=np.where(D.falling,"falling",np.where(D.tr60>0.10,"rising",np.where(D.tr60.notna(),"choppy","na")))
    D["ag"]=np.where(D.agit>1,"agit",np.where(D.agit.notna(),"calm","na"))
    out={}
    # wide down & wide up by trend x agitation
    D["wq"]=pd.qcut(D["width"],5,labels=False)
    tab=[]
    for tr in ["falling","choppy","rising"]:
        for ag in ["agit","calm"]:
            for side,sm in [("up",D.r1>0),("down",D.r1<0)]:
                for q in [0,4]:
                    m=(D.trend==tr)&(D.ag==ag)&sm&(D.wq==q)
                    s=T(m); s["tr"]=tr; s["ag"]=ag; s["side"]=side; s["wq"]=q
                    tab.append(s)
    out["width_by_profile"]=pd.DataFrame(tab)
    # falling wide up days: later horizons
    m=(D.trend=="falling")&(D.r1>0)&(D.wq>=3)
    out["falling_wideup_horizons"]=pd.DataFrame({k:T(m,"u_"+k) for k in ["nxt","d2","nxt2","nxt3"]}).T
    # falling up days by volume ratio tercile
    D["vq"]=pd.qcut(D["vr"],3,labels=False)
    tab=[]
    for q in range(3):
        for side,sm in [("up",D.r1>0),("down",D.r1<0)]:
            s=T((D.trend=="falling")&sm&(D.vq==q)); s["vq"]=q; s["side"]=side; tab.append(s)
    out["falling_by_volume"]=pd.DataFrame(tab)
    # choppy/rising: down days by z1 in deciles graded?
    D["zq"]=pd.qcut(D["z1"],5,labels=False)
    tab=[]
    for tr in ["choppy","rising"]:
        for q in range(5):
            s=T((D.trend==tr)&(D.zq==q)); s["tr"]=tr; s["zq"]=q; tab.append(s)
    out["z1_choppy_rising"]=pd.DataFrame(tab)
    # book: largest gains/losses context
    pos=D[D.alloc.abs()>1e-9].copy(); pos["g"]=pos.alloc*pos.nxt
    pos["gq"]=pd.qcut(pos.g,5,labels=False)
    out["book_quintiles"]=pos.groupby("gq")[["g","width","z1","clv","vr","agit","tr60"]].mean()
    out["book_by_agit"]=pos.groupby("ag")["g"].agg(["count","mean"])
    out["book_by_width_half"]=pos.groupby(pos.width>pos.width.median())["g"].agg(["count","mean"])
    return out
