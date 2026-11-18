def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].values; o=b["open"].values; l=b["low"].values; h=b["high"].values; v=b["volume"].values
            n = len(b)
            r1 = pd.Series(c).pct_change()
            sd = r1.rolling(20).std()
            z = r1/sd
            vmed = pd.Series(v).shift(1).rolling(20).median()
            vr = pd.Series(v)/vmed
            rng = h-l
            wick = np.where(rng>0,(np.minimum(o,c)-l)/np.where(rng>0,rng,1),np.nan)
            ret20 = pd.Series(c).pct_change(20)
            ma50 = pd.Series(c).rolling(50,min_periods=20).mean()
            for t in range(n):
                f = {}
                for hh in (1,3,5,10):
                    f["f%d"%hh] = c[t+hh]/c[t]-1 if t+hh<n else np.nan
                rows.append(dict(coin=coin,w=w,t=t,z=z.iloc[t],vr=vr.iloc[t],wick=wick[t],
                    drop=(o[t]-l[t])/o[t] if o[t] else np.nan,ret20=ret20.iloc[t],
                    abovema=float(c[t]>ma50.iloc[t]) if not np.isnan(ma50.iloc[t]) else np.nan,
                    reg=b["regime"].iloc[t],fc=b["forecast"].iloc[t],
                    alloc=b["postRebalance_current_allocation"].iloc[t],**f))
    d = pd.DataFrame(rows)
    # coin mean returns on non-overlapping grids
    for hh in (1,3,5,10):
        mm = d[d.t%hh==0].groupby("coin")["f%d"%hh].mean()
        d["x%d"%hh] = d["f%d"%hh]-d.coin.map(mm)
    fl = d[(d.reg=="mean_reversion")]
    out = {}
    def summ(g):
        res={}
        for hh in (1,3,5,10):
            s=g["x%d"%hh].dropna()
            res["n%d"%hh]=len(s); res["mx%d"%hh]=s.mean(); res["t%d"%hh]=s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
        return pd.Series(res)
    out["flush_all"]=summ(fl).to_frame().T
    out["flush_fc_pos_share"]=float((fl.fc>0).mean())
    out["flush_mean_alloc"]=float(fl.alloc.mean())
    fl = fl.copy(); fl["dq"]=pd.qcut(fl["drop"],3,labels=False)
    out["by_drop_tercile"]=fl.groupby("dq").apply(summ)
    out["by_trend_ret20"]=fl.groupby(fl.ret20>0).apply(summ)
    out["by_abovema50"]=fl.groupby("abovema").apply(summ)
    out["by_coin"]=fl.groupby("coin").apply(summ)
    # broader: sharp falls z<=-2 any
    sharp = d[d.z<=-2]
    out["sharp_all"]=summ(sharp).to_frame().T
    out["sharp_volburst"]=sharp.groupby(sharp.vr>=2).apply(summ)
    out["sharp_wick"]=sharp.groupby(sharp.wick>=0.3).apply(summ)
    out["sharp_by_ret20pos"]=sharp.groupby(sharp.ret20>0).apply(summ)
    # broader graded: z<=-1.5
    s15=d[d.z<=-1.5]
    out["z15_by_wick_tercile"]=s15.groupby(pd.qcut(s15.wick,3,labels=False)).apply(summ)
    # book
    br=[]
    for coin in days:
        for w,dd in days[coin].items():
            br.append(dd.assign(coin=coin))
    D=pd.concat(br)
    inpos = d.groupby("coin").apply(lambda g:(g.alloc.abs()>0.01).mean())
    out["share_bars_in_position"]=inpos
    out["book_mean_daily"]=float(D.book_return.mean())
    out["held_days_alloc_mean"]=float(d.loc[d.alloc.abs()>0.01,"alloc"].mean())
    return out
