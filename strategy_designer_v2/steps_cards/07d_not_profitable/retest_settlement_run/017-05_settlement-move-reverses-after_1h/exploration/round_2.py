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
            g=np.full(n,np.nan); g[:-1]=b["postRebalance_current_allocation"].values[:-1]*r1[1:]
            dd={"coin":coin,"w":w,"endh":endh,"pre":pre,"tr24":tr24,"vol1":vol1,
                "fc":b["forecast"].values,"alloc":b["postRebalance_current_allocation"].values,"gain":g}
            for h in (2,8,16):
                r=np.full(n,np.nan); r[:-h]=c[h:]/c[:-h]-1; dd[f"f{h}"]=r
            df=pd.DataFrame(dd); df["pos"]=np.arange(n); rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    d["z"]=d.pre/(d.vol1*np.sqrt(2)); d["z24"]=d.tr24/(d.vol1*np.sqrt(24))
    d["side"]=-np.sign(d.pre); d["sett"]=d.endh%8==0
    out={}
    # book gross gain by |forecast| bucket of the settlement bar
    s=d[d.sett&d.z.notna()&(d.side!=0)].copy()
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()],ignore_index=True)
    tr["afc"]=tr.entry_forecast.abs()
    tr["b"]=pd.cut(tr.afc,[-0.01,2,5,10,15,19.99,20])
    out["trades_by_absfc"]=tr.groupby("b",observed=True).agg(n=("afc","size"),pl=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur=("duration_minutes","mean"))
    out["trades_by_side"]=tr.groupby("side").agg(n=("afc","size"),pl=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"))
    # against-trend graded by 24h trend strength
    s["ag"]=np.sign(s.pre)!=np.sign(s.tr24)
    s["az"]=s.z.abs()
    s_top=s[(s.az>s.az.quantile(.5))&(s.az<s.az.quantile(.99))]
    s_top=s_top.assign(t24b=pd.qcut(s_top.z24.abs(),[0,.33,.66,.9,1],labels=["lo","mid","hi","top10"]))
    out["settle_mid_absz_by_against_x_trend"]=s_top.groupby(["ag","t24b"],observed=True).apply(lambda y:pd.Series({"tot2":(y.side*y.f2).mean()*1e4,"tot8":(y.side*y.f8).mean()*1e4,"tot16":(y.side*y.f16).mean()*1e4,"t8":stats.ttest_1samp((y.side*y.f8).dropna(),0).statistic,"n":len(y)}))
    # condition alone: non-settlement grid, same buckets
    o=d[(~d.sett)&d.z.notna()&(d.side!=0)&(d.pos%8==4)].copy()
    o["ag"]=np.sign(o.pre)!=np.sign(o.tr24); o["az"]=o.z.abs()
    o_top=o[(o.az>o.az.quantile(.5))&(o.az<o.az.quantile(.99))]
    o_top=o_top.assign(t24b=pd.qcut(o_top.z24.abs(),[0,.33,.66,.9,1],labels=["lo","mid","hi","top10"]))
    out["other_mid_absz_by_against_x_trend"]=o_top.groupby(["ag","t24b"],observed=True).apply(lambda y:pd.Series({"tot2":(y.side*y.f2).mean()*1e4,"tot8":(y.side*y.f8).mean()*1e4,"tot16":(y.side*y.f16).mean()*1e4,"n":len(y)}))
    # against-trend at settlement by hour
    out["settle_against_by_hour"]=s_top[s_top.ag].groupby("endh").apply(lambda y:pd.Series({"tot2":(y.side*y.f2).mean()*1e4,"tot8":(y.side*y.f8).mean()*1e4,"n":len(y)}))
    # book's gross gain: settlement window vs other bars
    d["hrs"]=d.endh%8
    out["book_gain_by_hours_after_settle_bp"]=d.groupby("hrs").agg(gain=("gain",lambda x:x.mean()*1e4),absalloc=("alloc",lambda x:x.abs().mean()))
    return out
