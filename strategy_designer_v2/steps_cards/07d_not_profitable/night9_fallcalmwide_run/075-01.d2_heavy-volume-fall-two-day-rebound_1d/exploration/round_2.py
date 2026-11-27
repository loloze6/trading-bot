def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars=data["bars"]; out={}
    cs=[]; sims=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b.close; r1=cl.pct_change(); vol=b.volume
            vr=vol/vol.shift(1).rolling(20).mean()
            lvr=np.log(vr); z=(lvr-lvr.rolling(60,min_periods=20).mean())/lvr.rolling(60,min_periods=20).std()
            f2=cl.shift(-2)/cl-1
            p20=cl/cl.shift(20)-1; p60=cl/cl.shift(60)-1
            sd30=r1.rolling(30).std()
            df=pd.DataFrame({"r1":r1,"vr":vr,"z":z,"f2":f2,"p20":p20,"p60":p60,"fc":b.forecast,
                             "alloc":b.postRebalance_current_allocation,"sd30":sd30})
            df["coin"]=c; df["wn"]=int(w[1:]); df["pos"]=np.arange(len(df))
            # simulated books: hold 2 bars after signal, gross daily ret, cost 0.22% per round trip
            nr=cl.shift(-1)/cl-1
            for name,sig in {"all_down":(r1<0)&(df.fc>0),"down_fc_top":(r1<0)&(df.fc>=12),"down_fc_15":(r1<0)&(df.fc>=15)}.items():
                s=sig.fillna(False).values; pos=np.zeros(len(s))
                for i in range(len(s)):
                    if s[i]:
                        pos[i]=1
                        if i+1<len(s): pos[i+1]=1
                ent=np.diff(np.r_[0,pos])>0
                g=pos*nr.fillna(0).values-ent*0.0022
                sims.append(pd.DataFrame({"name":name,"wn":int(w[1:]),"pos":np.arange(len(s)),"g":g,"inpos":pos}))
            cs.append(df)
    A=pd.concat(cs)
    C=A[A.pos%2==0].dropna(subset=["f2","r1"]).copy()
    C["ex2"]=C.f2-C.groupby("coin").f2.transform("mean")
    dn=C[(C.r1<0)&(C.fc>0)].copy()
    dn["fb"]=pd.cut(dn.fc,[0,7,10,12,15,21],labels=["<7","7-10","10-12","12-15","15+"])
    out["down_by_forecast_band"]=dn.groupby("fb").agg(n=("ex2","size"),f2=("f2","mean"),ex2=("ex2","mean"),
        t=("ex2",lambda x:x.mean()/x.std()*np.sqrt(len(x)))).round(4)
    up=C[(C.r1>=0)].copy()
    lvr_fc_up=up.groupby(pd.cut(up.z,[-9,-1,0,0.5,1.5,9])).agg(n=("ex2","size"),f2=("f2","mean"),ex2=("ex2","mean")).round(4)
    out["up_days_by_vol_z (condition without signal)"]=lvr_fc_up
    dn["fb2"]=dn.fc>=12
    dn["tr60"]=pd.cut(dn.p60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    out["down_tr60_x_heavy"]=dn.groupby(["tr60","fb2"]).agg(n=("ex2","size"),ex2=("ex2","mean")).unstack().round(4)
    dn["tr20"]=pd.cut(dn.p20,[-9,-0.15,-0.03,0.03,0.15,9])
    out["down_tr20_x_heavy"]=dn.groupby(["tr20","fb2"]).agg(n=("ex2","size"),ex2=("ex2","mean")).unstack().round(4)
    out["down_window_x_heavy"]=dn.groupby(["wn","fb2"]).ex2.mean().unstack().round(4)
    S=pd.concat(sims)
    Bk=S.groupby(["name","wn","pos"]).agg(g=("g","mean"),ip=("inpos","mean")).reset_index().sort_values(["name","wn","pos"])
    res={}
    for n,gg in Bk.groupby("name"):
        x=gg.g.values; v=np.cumprod(1+x); mdd=(v/np.maximum.accumulate(v)-1).min()
        yr=v[-1]**(365/len(x))-1
        res[n]={"mean":x.mean(),"sharpe":x.mean()/x.std()*np.sqrt(365),"yr":yr,"mdd":mdd,"calmar":yr/-mdd,"inpos":gg.ip.mean()}
    out["sim_books_unsized"]=pd.DataFrame(res).T.round(4)
    return out
