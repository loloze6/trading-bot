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
            pre=np.full(n,np.nan); pre[2:]=c[2:]/c[:-2]-1
            tr24=np.full(n,np.nan); tr24[24:]=c[24:]/c[:-24]-1
            r1=np.full(n,np.nan); r1[1:]=c[1:]/c[:-1]-1
            vol1=pd.Series(r1).rolling(60,min_periods=20).std().values
            dd={"coin":coin,"w":w,"endh":endh,"pre":pre,"tr24":tr24,"vol1":vol1}
            for h in (2,8,16,24):
                r=np.full(n,np.nan); r[:-h]=c[h:]/c[:-h]-1; dd[f"f{h}"]=r
            df=pd.DataFrame(dd); df["pos"]=np.arange(n); rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    for h in (2,8,16,24):
        dr=d[d.pos%h==0].groupby("coin")[f"f{h}"].mean()
        d[f"u{h}"]=d[f"f{h}"]-d.coin.map(dr)
    d["z"]=d.pre/(d.vol1*np.sqrt(2))
    d["side"]=-np.sign(d.pre); d["sett"]=d.endh%8==0
    d=d[d.z.notna()&(d.side!=0)]
    out={}
    def tab(x):
        x=x.copy(); x["zb"]=pd.qcut(x.z.abs(),[0,.5,.8,.95,.99,1],labels=["0-50","50-80","80-95","95-99","99+"])
        def f(y):
            r={}
            for h in (2,8,16,24):
                v=(y.side*y[f"f{h}"]).dropna(); r[f"tot{h}"]=v.mean()*1e4
                u=(y.side*y[f"u{h}"]).dropna(); r[f"unu{h}"]=u.mean()*1e4
            r["t8"]=stats.ttest_1samp((y.side*y.u8).dropna(),0).statistic; r["n"]=len(y); return pd.Series(r)
        return x.groupby(["side","zb"],observed=True).apply(f)
    s=d[d.sett]
    out["settle_all_hours_by_side_absz"]=tab(s)
    out["settle_h0_16_by_side_absz"]=tab(s[s.endh!=8])
    o=d[(~d.sett)&(d.pos%8==4)]
    out["other_by_side_absz"]=tab(o)
    # by year at settlement, long side, h0/16, |z| 50-99
    s2=s[(s.endh!=8)&(s.side>0)].copy(); q=s.z.abs().quantile([.5,.99]).values
    s2=s2[(s2.z.abs()>q[0])&(s2.z.abs()<q[1])]
    tsy=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            tsy.append(pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"yr":pd.to_datetime(b.timestamp).dt.year.values}))
    s2=s2.merge(pd.concat(tsy),on=["coin","w","pos"])
    out["long_h0_16_mid_by_year"]=s2.groupby("yr").apply(lambda y:pd.Series({"tot8":(y.f8).mean()*1e4,"unu8":y.u8.mean()*1e4,"n":len(y)}))
    return out
