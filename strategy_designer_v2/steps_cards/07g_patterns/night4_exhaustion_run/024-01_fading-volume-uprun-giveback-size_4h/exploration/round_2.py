def explore(data):
    import numpy as np, pandas as pd
    H=18
    ev=[]; grid=[]; hr=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float); v=df["volume"].astype(float)
            r=c.pct_change()
            sd=r.rolling(180,min_periods=60).std()
            sg=np.sign(r.fillna(0)).values
            s=np.zeros(len(df))
            for i in range(1,len(df)):
                if sg[i]>0: s[i]=s[i-1]+1 if s[i-1]>0 else 1
                elif sg[i]<0: s[i]=s[i-1]-1 if s[i-1]<0 else -1
            g4=((c/c.shift(4)-1)/sd).values
            g18=((c/c.shift(18)-1)/sd).values
            fade=(v.rolling(2).mean()/v.rolling(4).mean()).values
            vrel=(v/v.rolling(180,min_periods=60).mean()).values
            fwd=(c.shift(-H)/c-1).values
            fc=df["forecast"].astype(float).values
            pfc=np.r_[0,fc[:-1]]
            n=len(df)
            d=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(n),"cell":np.arange(n)//H,"streak":s,"g4":g4,"g18":g18,
                            "fade":fade,"vrel":vrel,"sd":sd.values,"fwd":fwd,"fc":fc,"entry":(fc<0)&(pfc>=0)})
            ev.append(d)
            grid.append(d.iloc[::H])
            ts=pd.to_datetime(df["timestamp"])
            hr.append(pd.DataFrame({"coin":coin,"hour":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r1":r.shift(-1).values,"sd":sd.values}))
    A=pd.concat(ev,ignore_index=True); G=pd.concat(grid,ignore_index=True).dropna(subset=["fwd"])
    drift=G.groupby("coin")["fwd"].mean(); usual=G.groupby("coin")["fwd"].std()
    A["ex"]=A["fwd"]-A["coin"].map(drift); A["z"]=A["ex"]/A["coin"].map(usual)
    G["ex"]=G["fwd"]-G["coin"].map(drift); G["z"]=G["ex"]/G["coin"].map(usual)
    def summ(x,sign=1):
        x=x.dropna(subset=["z"])
        z=sign*x["z"]; e=sign*x["ex"]
        n=len(z)
        return pd.Series({"n":n,"mean_ex%":100*e.mean() if n else np.nan,"strength":z.mean() if n else np.nan,
                          "t":z.mean()/(z.std()/np.sqrt(n)) if n>2 else np.nan})
    def cases(mask):
        x=A[mask & A["fwd"].notna()]
        return x.groupby(["coin","w","cell"]).head(1)
    out={}
    conds={
     "up4_fade":(A["streak"]>=4)&(A["fade"]<1),
     "up4_risevol":(A["streak"]>=4)&(A["fade"]>=1),
     "dn4_fade":(A["streak"]<=-4)&(A["fade"]<1),
     "dn4_risevol":(A["streak"]<=-4)&(A["fade"]>=1),
     "up6":(A["streak"]>=6),"dn6":(A["streak"]<=-6),
     "short_entries":A["entry"],
    }
    tab={}
    for k,m in conds.items():
        tab[k]=summ(cases(m))  # signed in UP direction (raw excess, positive = coin rose more than drift)
    out["events_raw_excess_up_positive"]=pd.DataFrame(tab).T
    # graded by g4 within up4 and dn4 streaks
    gr={}
    for k,m in [("up4",A["streak"]>=4),("dn4",A["streak"]<=-4)]:
        x=cases(m).copy()
        x["q"]=pd.qcut(x["g4"].abs(),3,labels=["lo","mid","hi"])
        for q,g in x.groupby("q",observed=True):
            gr[f"{k}_{q}"]=summ(g)
    out["streak_by_gain_tercile_raw"]=pd.DataFrame(gr).T
    # grid-based: past 18-bar scaled move quintiles, vol level, vrel
    for k in ["g18","g4","sd","vrel"]:
        G[k+"q"]=G.groupby("coin")[k].transform(lambda x: pd.qcut(x,5,labels=False,duplicates="drop"))
        out[k+"_quintile_grid_raw"]=G.groupby(k+"q").apply(lambda g: summ(g))
    # g18 extremes split by vol level
    G["hiv"]=(G["sdq"]>=3).map({True:"hivol",False:"lovol"})
    out["g18_ext_by_vol"]=G[G["g18q"].isin([0,4])].groupby(["hiv","g18q"]).apply(lambda g: summ(g))
    out["coin_drift_%"]=pd.DataFrame({"drift%":100*drift,"usual%":100*usual})
    Hh=pd.concat(hr,ignore_index=True).dropna()
    Hh["z1"]=Hh["r1"]/Hh["sd"]
    for k in ["hour","wd"]:
        q=Hh.groupby(k)["z1"].agg(["count","mean","std"]); q["t"]=q["mean"]/(q["std"]/np.sqrt(q["count"]))
        out[k+"_next_bar_z"]=q
    D=pd.concat([d.assign(coin=c,w=w) for c,ws in data["days"].items() for w,d in ws.items()],ignore_index=True)
    out["book_by_coin_%"]=D.groupby("coin")[["book_return","coin_return"]].mean()*100
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()],ignore_index=True)
    out["trades_by_coin"]=T.groupby(["coin","side"])["net_profit_loss_percent"].agg(["count","mean","median"])
    T["dur_h"]=T["duration_minutes"]/60
    out["trade_dur"]=T["dur_h"].describe()
    return out
