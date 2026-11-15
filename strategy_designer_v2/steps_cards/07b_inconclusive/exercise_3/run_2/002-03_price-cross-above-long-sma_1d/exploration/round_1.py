def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]
    bars=data["bars"]
    # pooled mean daily return per coin
    mu={}
    for c in bars:
        rs=[]
        for w,df in bars[c].items():
            r=df["close"].pct_change().dropna(); rs.append(r)
        mu[c]=pd.concat(rs).mean()
    for c in bars:
        for w,df in bars[c].items():
            df=df.reset_index(drop=True)
            cl=df["close"].values; n=len(df)
            dist=df["debug_info.components.above_ma.last_history_value"].values
            fc=df["forecast"].values; al=df["postRebalance_current_allocation"].values
            ts=pd.to_datetime(df["timestamp"])
            for h in [5,10,20,40,60]:
                for i in range(0,n-h,h):
                    rows.append(dict(coin=c,w=w,h=h,year=ts.iloc[i].year,fc=fc[i],dist=dist[i],al=al[i],
                                     ex=cl[i+h]/cl[i]-1-h*mu[c]))
    d=pd.DataFrame(rows)
    out={}
    def summ(g):
        return pd.Series(dict(n=len(g),mean=g.ex.mean(),t=g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,
                              win=(g.ex>0).mean(),med=g.ex.median()))
    d["state"]=np.where(d.fc>0,"fc>0",np.where(d.dist>0,"above_fc0",np.where(d.dist<=0,"below","na")))
    out["by_h_state"]=d.groupby(["h","state"]).apply(summ)
    d20=d[d.h==20]
    pos=d20[d20.fc>0].copy()
    pos["fq"]=pd.qcut(pos.fc,4,labels=False,duplicates="drop")
    out["h20_fc_quartile"]=pos.groupby("fq").apply(summ)
    d20b=d20[d20.dist.notna()].copy()
    d20b["dq"]=pd.qcut(d20b.dist,6,labels=False,duplicates="drop")
    out["h20_rawdist_sextile"]=d20b.groupby("dq").apply(lambda g: pd.concat([summ(g),pd.Series(dict(dmean=g.dist.mean()))]))
    out["h20_pos_by_coin"]=pos.groupby("coin").apply(summ)
    out["h20_pos_by_year"]=pos.groupby("year").apply(summ)
    out["h20_below_by_coin"]=d20[d20.state=="below"].groupby("coin").apply(summ)
    d60=d[(d.h==60)&d.dist.notna()].copy()
    d60["dq"]=pd.qcut(d60.dist,6,labels=False,duplicates="drop")
    out["h60_rawdist_sextile"]=d60.groupby("dq").apply(summ)
    return out
