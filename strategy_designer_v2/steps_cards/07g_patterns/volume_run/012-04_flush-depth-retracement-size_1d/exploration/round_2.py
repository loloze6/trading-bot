import pandas as pd, numpy as np
from scipy import stats

def prep(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            d=df.reset_index(drop=True).copy()
            c=d["close"]; r1=c.pct_change()
            vol=r1.rolling(20,min_periods=20).std()
            d["r1"]=r1; d["z"]=r1/vol
            d["vr"]=d["volume"]/d["volume"].shift(1).rolling(20,min_periods=20).mean()
            rng=(d["high"]-d["low"]).replace(0,np.nan)
            d["wick"]=(np.minimum(d["open"],c)-d["low"])/rng
            d["r5"]=c/c.shift(5)-1
            d["f3"]=c.shift(-3)/c-1
            d["f1"]=c.shift(-1)/c-1
            d["pos"]=np.arange(len(d))
            d["coin"]=coin; d["win"]=w
            ts=pd.to_datetime(d["timestamp"])
            d["wd"]=ts.dt.dayofweek; d["yr"]=ts.dt.year
            rows.append(d)
    return pd.concat(rows,ignore_index=True)

def summ(df,key):
    o=df.groupby(key)["ex"].agg(["mean","std","count"])
    o["t"]=o["mean"]/(o["std"]/np.sqrt(o["count"]))
    return o.drop(columns="std")

def reg(x,y):
    m=~(np.isnan(x)|np.isnan(y))
    r=stats.linregress(x[m],y[m]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":m.sum()})

def explore(data):
    A=prep(data)
    out={}
    g3=A[A.pos%3==0].dropna(subset=["f3"]).copy()
    g3["ex"]=g3["f3"]-g3.groupby("coin")["f3"].transform("mean")
    G=g3.dropna(subset=["vr","z"]).copy()
    G["lvr"]=np.log(G.vr)
    # volume ratio graded, split by sign of bar return
    G["dir"]=np.where(G.z<0,"down","up")
    out["slope_ex3_on_logvr_by_dir"]=G.groupby("dir").apply(lambda d: reg(d.lvr.values,d.ex.values))
    out["slope_ex3_on_logvr_by_coin"]=G.groupby("coin").apply(lambda d: reg(d.lvr.values,d.ex.values))
    G["half"]=np.where(G.yr<=2021,"2018-21","2022-25")
    out["slope_ex3_on_logvr_by_half"]=G.groupby("half").apply(lambda d: reg(d.lvr.values,d.ex.values))
    G["vrq"]=G.groupby("coin")["vr"].transform(lambda s: pd.qcut(s,5,labels=False))
    G["k"]=G["dir"]+"_vq"+G["vrq"].astype(str)
    out["ex3_by_dir_vrquint"]=summ(G,"k")
    # among down bars z<=-1: slope on log vr
    dn=G[G.z<=-1]
    out["down_z_le_-1_slope_logvr"]=reg(dn.lvr.values,dn.ex.values).to_frame().T
    # r5 graded
    out["slope_ex3_on_r5_by_coin"]=G.groupby("coin").apply(lambda d: reg(d.r5.values,d.ex.values))
    # weekday 1-day
    g1=A.dropna(subset=["f1"]).copy()
    g1["ex"]=g1["f1"]-g1.groupby("coin")["f1"].transform("mean")
    g1["thfr"]=g1.wd.isin([3,4])
    p=g1.groupby(["coin","thfr"])["ex"].mean().unstack()
    out["thfr_minus_other_by_coin"]=p[True]-p[False]
    g1["half"]=np.where(g1.yr<=2021,"2018-21","2022-25")
    p2=g1.groupby(["half","thfr"])["ex"].agg(["mean","count"]).unstack()
    out["thfr_by_half"]=p2
    a=g1[g1.thfr].ex; b=g1[~g1.thfr].ex
    out["thfr_welch_t"]=float(stats.ttest_ind(a,b,equal_var=False).statistic)
    # book: days around largest gains/losses
    days=[]
    for coin,wins in data["days"].items():
        for w,dd in wins.items():
            x=dd.copy().reset_index(drop=True); x["coin"]=coin; x["win"]=w
            x["next3"]=x["coin_return"].shift(-1).rolling(1).mean()
            days.append(x)
    D=pd.concat(days).dropna(subset=["book_return"])
    act=D[D.book_return!=0]
    out["book_active_days"]=pd.Series({"n":len(act),"mean":act.book_return.mean(),"t":act.book_return.mean()/(act.book_return.std()/np.sqrt(len(act))),"share_pos":(act.book_return>0).mean()})
    return out
