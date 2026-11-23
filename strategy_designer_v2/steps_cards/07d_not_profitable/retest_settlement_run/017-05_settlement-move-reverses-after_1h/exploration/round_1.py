import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; n=len(c)
            ts=pd.to_datetime(b["timestamp"])
            endh=((ts+pd.Timedelta(hours=1)).dt.hour).values
            # drift per horizon from grid
            for i in range(2,n):
                pass
            pre=np.full(n,np.nan); pre[2:]=c[2:]/c[:-2]-1
            tr24=np.full(n,np.nan); tr24[24:]=c[24:]/c[:-24]-1
            f={}
            for h in (1,2,4,8,16):
                r=np.full(n,np.nan); r[:-h]=c[h:]/c[:-h]-1; f[h]=r
            # usual 2h vol rolling
            r1=np.full(n,np.nan); r1[1:]=c[1:]/c[:-1]-1
            vol2=pd.Series(r1).rolling(60,min_periods=20).std().values*np.sqrt(2)
            df=pd.DataFrame({"coin":coin,"w":w,"endh":endh,"pre":pre,"tr24":tr24,"vol2":vol2,
                             "fc":b["forecast"].values,**{f"f{h}":f[h] for h in f}})
            df["pos"]=np.arange(n)
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    # drift per coin per h (non-overlapping grid)
    for h in (1,2,4,8,16):
        dr=d[d.pos%h==0].groupby("coin")[f"f{h}"].mean()
        d[f"u{h}"]=d[f"f{h}"]-d.coin.map(dr)
    d["z"]=d.pre/d.vol2
    d["side"]=-np.sign(d.pre)
    d["sett"]=d.endh%8==0
    out={}
    s=d[d.sett&d.z.notna()&(d.side!=0)].copy()
    o=d[(~d.sett)&d.z.notna()&(d.side!=0)&(d.pos%8==0)].copy()  # non-settlement grid
    for nm,x in (("settle",s),("other",o)):
        x["zb"]=pd.qcut(x.z.abs(),[0,.5,.8,.9,.95,.99,1],labels=["0-50","50-80","80-90","90-95","95-99","99+"])
        g={}
        for h in (1,2,4,8,16):
            g[f"tot{h}_bp"]=x.groupby("zb",observed=True).apply(lambda y:(y.side*y[f"f{h}"]).mean()*1e4)
        g["n"]=x.groupby("zb",observed=True).size()
        out[nm+"_by_absz_bp"]=pd.DataFrame(g)
    # settle by hour
    s["hr"]=s.endh
    out["settle_by_hour_2h_bp"]=s.groupby("hr").apply(lambda y:pd.Series({"tot2":(y.side*y.f2).mean()*1e4,"t":stats.ttest_1samp(y.side*y.u2,0,nan_policy='omit').statistic,"n":len(y)}))
    # trend alignment: pre against 24h trend
    s["against"]=np.sign(s.pre)!=np.sign(s.tr24)
    big=s[s.z.abs()>s.z.abs().quantile(.8)]
    out["settle_top20_by_against_trend_bp"]=big.groupby("against").apply(lambda y:pd.Series({"tot2":(y.side*y.f2).mean()*1e4,"tot8":(y.side*y.f8).mean()*1e4,"n":len(y)}))
    out["settle_by_coin_2h_bp"]=s.groupby("coin").apply(lambda y:(y.side*y.f2).mean()*1e4)
    # book: trades
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()],ignore_index=True)
    out["trades"]=pd.Series({"n":len(tr),"mean_pl_pct":tr.profit_loss_percent.mean(),"mean_net_pct":tr.net_profit_loss_percent.mean(),"med_dur_min":tr.duration_minutes.median(),"mean_dur_min":tr.duration_minutes.mean()})
    al=pd.concat([b[["postRebalance_current_allocation"]] for ws in data["bars"].values() for b in ws.values()])
    out["alloc"]=pd.Series({"share_nonzero":(al.iloc[:,0].abs()>1e-6).mean(),"mean_abs":al.iloc[:,0].abs().mean()})
    return out
