def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            allr.append(b["close"].astype(float).pct_change().dropna())
        mu=pd.concat(allr).mean(); sd=pd.concat(allr).std()
        allv=pd.concat([b["close"].astype(float).pct_change().rolling(30).std() for b in ws.values()]).median()
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r0=c.pct_change(); nx=c.shift(-1)/c-1; nx2=c.shift(-2)/c-1
            run=np.zeros(len(c),int); loss=np.full(len(c),np.nan); cnt=0
            for i in range(1,len(c)):
                run[i]=cnt
                if cnt>0: loss[i]=c[i-1]/c[i-1-cnt]-1
                cnt = cnt+1 if r0[i]<0 else 0
            vol30=r0.rolling(30).std(); ret30=c/c.shift(30)-1
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
               "r0":r0,"u":nx-mu,"u2":nx2-2*mu,"run":run,"loss":loss,"vol30":vol30,"ret30":ret30,
               "agit":vol30>allv,"reg":b["regime"],"yr":pd.to_datetime(b["timestamp"]).dt.year,
               "sd":sd,"w_":w})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    def ct(s,days):
        x=pd.DataFrame({"v":s.values,"d":days.values}).dropna()
        if len(x)<5: return (len(x),np.nan,np.nan,0)
        m=x.v.mean(); g=(x.v-m).groupby(x.d).sum(); n=len(x); Dn=len(g)
        se=np.sqrt((g**2).sum()*Dn/(Dn-1))/n
        return (n,m,m/se,Dn)
    def tab(groups,col="u"):
        out={}
        for k,sub in groups:
            n,m,t,dn=ct(sub[col],sub["day"]); out[k]={"n":n,"days":dn,"mean":m,"t":t}
        return pd.DataFrame(out).T
    res={}
    up=D[(D.r0>0)&(D.run>=1)].copy()
    up["depth"]=-up.loss/up.vol30
    up["dq"]=pd.qcut(up.depth,4,labels=False)
    res["all breaks run>=1 by depth/vol30 quartile"]=pd.concat([tab(up.groupby("dq")),tab(up.groupby("dq"),"u2").add_suffix("_2d")],axis=1)
    up["tr"]=np.where(up.ret30>0.05,"rise",np.where(up.ret30<-0.05,"fall","chop"))
    up["prof"]=up.tr+"_"+np.where(up.agit,"ag","calm")
    res["breaks top depth quartile by proxy profile"]=tab(up[up.dq==3].groupby("prof"))
    res["breaks bottom depth quartile by proxy profile"]=tab(up[up.dq==0].groupby("prof"))
    res["top quartile by regime"]=tab(up[up.dq==3].groupby("reg"))
    res["top quartile by year"]=tab(up[up.dq==3].groupby("yr"))
    up["bq"]=pd.qcut(up.r0/up.vol30,3,labels=False)
    res["top depth quartile by bounce tercile"]=tab(up[up.dq==3].groupby("bq"))
    # control: any day after deep fall (not only up close)
    D["l3"]=D.groupby(["coin","w"]).r0.transform(lambda s:(1+s).rolling(3).apply(np.prod,raw=True)-1)
    a=D.dropna(subset=["l3","vol30"]).copy(); a["z"]=a.l3/a.vol30
    a["up"]=a.r0>0
    a["zq"]=pd.qcut(a.z,5,labels=False)
    res["all days by 3d ret/vol30 quintile x upclose"]=tab(a.groupby(["zq","up"]))
    # correlation-type slope t
    x=up.dropna(subset=["depth","u"])
    res["corr depth vs u"]=float(np.corrcoef(x.depth,x.u)[0,1]); res["n"]=len(x)
    return res
