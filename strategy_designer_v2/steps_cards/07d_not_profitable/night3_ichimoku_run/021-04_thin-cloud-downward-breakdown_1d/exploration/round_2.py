def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=26
    out={}
    # book decomposition: market part vs timing
    drift_d={}
    for c,ws in data["days"].items():
        drift_d[c]=pd.concat([x["coin_return"] for x in ws.values()]).mean()
    bk=[];mk=[];alloc_share=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            a=b["postRebalance_current_allocation"].fillna(0).values
            cl=b["close"].values
            g=a[:-1]*(cl[1:]/cl[:-1]-1)
            bk.append(g.mean()); mk.append((a[:-1]*drift_d[c]).mean()); alloc_share.append((a!=0).mean())
    out["gain_vs_market_part"]=pd.Series({"pos_gain_mean":np.mean(bk),"market_part":np.mean(mk),"timing":np.mean(bk)-np.mean(mk),"share_bars_in":np.mean(alloc_share)})
    # cloud from prices; state at grid points, forward 26
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True);h=b["high"];l=b["low"];cl=b["close"]
            ten=(h.rolling(9).max()+l.rolling(9).min())/2;kij=(h.rolling(26).max()+l.rolling(26).min())/2
            sa=((ten+kij)/2).shift(26);sb=((h.rolling(52).max()+l.rolling(52).min())/2).shift(26)
            top=np.maximum(sa,sb);bot=np.minimum(sa,sb);width=(top-bot)/cl
            above=cl>top;below=cl<bot
            r26=cl/cl.shift(26)-1
            vol=np.log(cl).diff().rolling(20).std()
            cv=cl.values
            for i in range(0,len(b)-H,H):
                if np.isnan(top.iloc[i]): continue
                st="above" if above.iloc[i] else ("below" if below.iloc[i] else "inside")
                rows.append(dict(coin=c,st=st,fr=cv[i+H]/cv[i]-1,dist=(cv[i]-(top.iloc[i]+bot.iloc[i])/2)/cv[i],width=width.iloc[i],r26=r26.iloc[i],vol=vol.iloc[i]))
    d=pd.DataFrame(rows)
    dr=d.groupby("coin").fr.transform("mean");d["un"]=d.fr-dr
    out["by_state"]=d.groupby("st").agg(n=("un","size"),un=("un","mean"),tot=("fr","mean"),t=("un",lambda v:v.mean()/(v.std()/np.sqrt(len(v)))))
    def q(x,col,k=4):
        x=x.dropna(subset=[col]).copy();x["g"]=pd.qcut(x[col],k,labels=False,duplicates="drop")
        return x.groupby("g").agg(n=("un","size"),lo=(col,"min"),hi=(col,"max"),un=("un","mean"),tot=("fr","mean"),t=("un",lambda v:v.mean()/(v.std()/np.sqrt(len(v)))))
    out["all_by_r26"]=q(d,"r26")
    out["below_by_r26"]=q(d[d.st=="below"],"r26",3)
    out["below_by_vol"]=q(d[d.st=="below"],"vol",3)
    out["all_by_dist"]=q(d,"dist")
    out["above_by_width"]=q(d[d.st=="above"],"width",3)
    return out
