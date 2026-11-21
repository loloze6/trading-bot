def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=26
    rows=[];drift={};usual={}
    for c,ws in data["bars"].items():
        rets=[]
        for w,b in ws.items():
            cl=b["close"].values
            for i in range(0,len(cl)-H,H): rets.append(cl[i+H]/cl[i]-1)
        drift[c]=np.mean(rets);usual[c]=np.std(rets)
        for w,b in ws.items():
            b=b.reset_index(drop=True);cl=b["close"].values;f=b["forecast"].fillna(0).values
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            for s in range(0,len(b),H):
                e=min(s+H,len(b))
                idx=[i for i in range(s,e) if f[i]<=-2]
                if not idx: continue
                i=idx[0]
                if i+H>=len(cl): continue
                fr=cl[i+H]/cl[i]-1
                r26=cl[i]/cl[i-26]-1 if i>=26 else np.nan
                r10=cl[i]/cl[i-10]-1 if i>=10 else np.nan
                hi=b["high"].values[max(0,i-52):i+1].max();lo=b["low"].values[max(0,i-52):i+1].min()
                pos=(cl[i]-lo)/(hi-lo) if hi>lo else np.nan
                vol=np.std(np.diff(np.log(cl[max(0,i-20):i+1]))) if i>=10 else np.nan
                rows.append(dict(coin=c,w=w,year=yr[i],tot=-fr,unus=-(fr-drift[c]),r26=r26,r10=r10,pos=pos,vol=vol,fc=f[i]))
    d=pd.DataFrame(rows)
    out={"n":len(d),"mean_tot":d.tot.mean(),"mean_unus":d.unus.mean()}
    def grp(col,q=3):
        x=d.dropna(subset=[col]).copy();x["g"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        return x.groupby("g").agg(n=("unus","size"),lo=(col,"min"),hi=(col,"max"),unus=("unus","mean"),tot=("tot","mean"),t=("unus",lambda v:v.mean()/(v.std()/np.sqrt(len(v)))))
    out["by_r26"]=grp("r26");out["by_r10"]=grp("r10");out["by_pos"]=grp("pos");out["by_vol"]=grp("vol")
    out["by_year"]=d.groupby("year").agg(n=("unus","size"),unus=("unus","mean"),tot=("tot","mean"))
    out["by_coin"]=d.groupby("coin").agg(n=("unus","size"),unus=("unus","mean"),tot=("tot","mean"))
    # book daily
    dd=[]
    for c,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy();x["coin"]=c;x["w"]=w;x["year"]=pd.to_datetime(x["day"]).dt.year;dd.append(x)
    D=pd.concat(dd)
    out["book_by_year"]=D.groupby("year").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","size"))
    out["corr_tot_r26"]=d[["tot","r26","r10","pos","vol"]].corr().loc["tot"]
    return out
