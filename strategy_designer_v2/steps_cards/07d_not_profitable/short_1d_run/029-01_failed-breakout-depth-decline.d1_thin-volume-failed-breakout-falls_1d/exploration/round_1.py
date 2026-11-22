import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars=data["bars"]; days=data["days"]; trades=data["trades"]
    out={}
    # book per coin
    rows=[]
    for c in bars:
        br=[];cr=[];al=[];
        for w,df in days[c].items():
            br.append(df["book_return"].dropna()); cr.append(df["coin_return"].dropna())
        for w,df in bars[c].items():
            al.append(df["postRebalance_current_allocation"])
        br=pd.concat(br);cr=pd.concat(cr);al=pd.concat(al)
        tr=pd.concat([t for t in trades[c].values() if len(t)]) if any(len(t) for t in trades[c].values()) else pd.DataFrame()
        rows.append(dict(coin=c,book_mean=br.mean(),coin_mean=cr.mean(),share_in=(al.abs()>1e-6).mean(),
                         mean_abs_alloc_when_in=al[al.abs()>1e-6].abs().mean(),ntr=len(tr),
                         tr_net_mean=tr["net_profit_loss_percent"].mean() if len(tr) else np.nan,
                         tr_gross_mean=tr["profit_loss_percent"].mean() if len(tr) else np.nan,
                         win=(tr["net_profit_loss_percent"]>0).mean() if len(tr) else np.nan,
                         dur_days=tr["duration_minutes"].mean()/1440 if len(tr) else np.nan))
    out["per_coin_book"]=pd.DataFrame(rows)
    # forecast distribution on active bars
    f=pd.concat([df["forecast"] for c in bars for df in bars[c].values()])
    out["forecast_nonzero_desc"]=f[f!=0].describe()
    out["forecast_nonzero_rounded_counts"]=f[f!=0].round(0).value_counts().head(15)
    # situation from prices: all failed breakouts, features
    H=5
    recs=[]; drift={}
    for c in bars:
        g=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            for i in range(0,len(cl)-H,H): g.append(cl[i+H]/cl[i]-1)
        drift[c]=np.mean(g); sd=np.std(g)
        for w,df in bars[c].items():
            cl=df["close"].values; v=df["volume"].values; n=len(cl); fc=df["forecast"].values
            ts=pd.to_datetime(df["timestamp"])
            ph=pd.Series(cl).shift(1).rolling(20).max().values
            vm=pd.Series(v).rolling(20).mean().values
            bo=cl>ph
            used=set()
            for t in range(25,n-H):
                js=[j for j in range(t-3,t) if j>=21 and bo[j]]
                if not js or bo[t]: continue
                j=js[-1]
                if cl[t]>=ph[j]: continue
                if any(cl[k]<ph[j] for k in range(j+1,t)): continue  # first failure bar only
                cell=t//H
                if cell in used: continue
                used.add(cell)
                fwd=cl[t+H]/cl[t]-1
                recs.append(dict(coin=c,win=w,year=ts.iloc[t].year,thin=max(0,1-v[j]/vm[j]) if vm[j]>0 else np.nan,
                    short_unusual=-(fwd-drift[c]),short_total=-fwd,strength=-(fwd-drift[c])/sd,
                    ret20=cl[t]/cl[t-20]-1, ret60=cl[t]/cl[max(0,t-60)]-1,
                    depth=cl[t]/ph[j]-1, bosize=cl[j]/ph[j]-1, fc=fc[t]))
    R=pd.DataFrame(recs)
    R["thin_pos"]=R["thin"]>0
    def summ(g):
        x=g["short_unusual"]
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,total=g["short_total"].mean()))
    out["all_failed_by_thin"]=R.groupby("thin_pos").apply(summ)
    out["by_coin"]=R.groupby("coin").apply(summ)
    out["by_year"]=R.groupby("year").apply(summ)
    for col in ["ret20","ret60","depth","bosize","thin"]:
        R[col+"_q"]=pd.qcut(R[col].rank(method="first"),4,labels=False)
        out["by_"+col+"_quartile"]=R.groupby(col+"_q").apply(summ).join(R.groupby(col+"_q")[col].mean())
    out["thin_only_by_ret60_q"]=R[R.thin_pos].groupby("ret60_q").apply(summ)
    return out
