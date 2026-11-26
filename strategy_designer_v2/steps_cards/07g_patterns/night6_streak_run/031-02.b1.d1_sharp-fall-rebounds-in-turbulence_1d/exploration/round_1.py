def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            mabs=r.abs().rolling(60,min_periods=20).mean()
            sc=r/mabs
            turb=r.rolling(10,min_periods=8).std()/r.rolling(60,min_periods=20).std()
            # streak signed
            s=np.sign(r.fillna(0)).values; st=np.zeros(len(s))
            for i in range(len(s)):
                if s[i]==0: st[i]=0
                elif i>0 and np.sign(st[i-1])==s[i]: st[i]=st[i-1]+s[i]
                else: st[i]=s[i]
            r5=c.pct_change(5)/(r.rolling(60,min_periods=20).std()*np.sqrt(5))
            vol60=r.rolling(60,min_periods=20).std()
            f1=c.shift(-1)/c-1; f2=c.shift(-2)/c-1; f5=c.shift(-5)/c-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"sc":sc,"turb":turb,"st":st,"r5":r5,
                             "vol60":vol60,"f1":f1,"f2":f2,"f5":f5,"wd":ts.dt.weekday,"yr":ts.dt.year,
                             "alloc":b["postRebalance_current_allocation"].astype(float),"fc":b["forecast"].astype(float)})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    out={}
    def grid(h,col):
        g=D[D.pos%h==0].copy()
        m=g.groupby("coin")[col].mean()
        g["ex"]=g[col]-g.coin.map(m)
        return g.dropna(subset=["ex"])
    def summ(g,key):
        a=g.groupby(key)["ex"].agg(["mean","count","std"])
        a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
        a["mean"]*=100
        return a[["mean","count","t"]].round(3)
    g2=grid(2,"f2")
    g2=g2.dropna(subset=["sc","turb"])
    g2["scb"]=pd.cut(g2.sc,[-99,-2,-1,-0.3,0.3,1,2,99])
    g2["tb"]=np.where(g2.turb>1,"turb","calm")
    out["f2 excess by scaled ret x turb"]=summ(g2,["tb","scb"])
    g2["stb"]=g2.st.clip(-5,5)
    out["f2 excess by streak"]=summ(g2,"stb")
    g5=grid(5,"f5").dropna(subset=["r5","turb"])
    g5["r5b"]=pd.cut(g5.r5,[-99,-2,-1,0,1,2,99])
    g5["tb"]=np.where(g5.turb>1,"turb","calm")
    out["f5 excess by 5d z x turb"]=summ(g5,["tb","r5b"])
    g1=grid(1,"f1")
    out["f1 excess by weekday"]=summ(g1,"wd")
    g2["vq"]=g2.groupby("coin")["vol60"].transform(lambda x: pd.qcut(x,4,labels=False,duplicates="drop"))
    out["f2 excess by vol60 quartile"]=summ(g2,"vq")
    # turbulence ratio level within falls
    gf=g2[g2.sc<0].copy()
    gf["tbq"]=pd.cut(gf.turb,[0,0.7,0.9,1.1,1.4,9])
    out["f2 excess on down days by turb ratio"]=summ(gf,"tbq")
    gu=g2[g2.sc>0].copy(); gu["tbq"]=pd.cut(gu.turb,[0,0.7,0.9,1.1,1.4,9])
    out["f2 excess on up days by turb ratio"]=summ(gu,"tbq")
    # book by coin/year
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            x=d.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    DD=pd.concat(dd); DD["yr"]=pd.to_datetime(DD["day"]).dt.year
    out["book by coin"]=DD.groupby("coin").agg(br=("book_return","mean"),cr=("coin_return","mean")).mul(1e4).round(2)
    out["book by year"]=DD.groupby("yr").agg(br=("book_return","mean"),cr=("coin_return","mean")).mul(1e4).round(2)
    return out
