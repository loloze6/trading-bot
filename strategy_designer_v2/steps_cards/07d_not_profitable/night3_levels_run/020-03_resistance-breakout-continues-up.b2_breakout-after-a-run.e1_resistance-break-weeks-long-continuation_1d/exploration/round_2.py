def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted(days[coins[0]].keys(), key=lambda w: int(w[1:]))
    # per coin per day: state at previous day's close, book and coin return
    rows=[]
    for c in coins:
        for w in bars[c]:
            b=bars[c][w].copy(); b["ts"]=pd.to_datetime(b.timestamp)
            cl=b.close
            b["ma50"]=cl/cl.rolling(50).mean()-1
            b["r20"]=cl/cl.shift(20)-1
            b["r10"]=cl/cl.shift(10)-1
            b["vol20"]=np.log(cl).diff().rolling(20).std()*np.sqrt(365)
            b["volratio"]=np.log(cl).diff().rolling(10).std()/np.log(cl).diff().rolling(60,min_periods=30).std()
            b["alloc"]=b.postRebalance_current_allocation
            b["g"]=b.alloc*(cl.shift(-1)/cl-1)
            b["cr"]=cl.shift(-1)/cl-1
            b["coin"]=c; b["w"]=w
            rows.append(b[["coin","w","ma50","r20","r10","vol20","volratio","alloc","g","cr"]])
    B=pd.concat(rows,ignore_index=True).dropna(subset=["g"])
    inpos=B[B.alloc>0.01]
    out["share_in_pos"]=float((B.alloc>0.01).mean())
    out["alloc_desc"]=inpos.alloc.describe().round(3)
    def tab(k,q=4):
        x=inpos.dropna(subset=[k])
        qq=pd.qcut(x[k],q,duplicates="drop")
        r=x.groupby(qq).agg(n=("g","size"),mean_gain_bps=("g",lambda s:s.mean()*1e4),
            coin_bps=("cr",lambda s:s.mean()*1e4),sd_gain_bps=("g",lambda s:s.std()*1e4),
            worst1pct_bps=("g",lambda s:s.quantile(0.01)*1e4),alloc=("alloc","mean"))
        r["gain_over_sd"]=r.mean_gain_bps/r.sd_gain_bps
        return r.round(3)
    for k in ["ma50","r20","r10","vol20","volratio"]:
        out["inpos_by_"+k]=tab(k)
    # 20-day non-overlapping forward returns in position by ma50 state with t
    res=[]
    for (c,w),g in B.groupby(["coin","w"]):
        g=g.reset_index(drop=True)
        for i in range(0,len(g)-20,20):
            if g.alloc.iloc[i]>0.01 and not np.isnan(g.ma50.iloc[i]):
                res.append((g.ma50.iloc[i], g.g.iloc[i:i+20].sum(), g.cr.iloc[i:i+20].sum()))
    R=pd.DataFrame(res,columns=["ma50","g20","c20"])
    R["above"]=R.ma50>0
    out["grid20_by_above_ma50"]=R.groupby("above").agg(n=("g20","size"),g20=("g20","mean"),sd=("g20","std"),c20=("c20","mean"),worst=("g20","min")).round(4)
    out["t_above_minus_below"]=float(stats.ttest_ind(R[R.above].g20,R[~R.above].g20,equal_var=False).statistic)
    # book drawdown days: mean coin-state of positions
    ch=[]
    for w in wins:
        f=B[B.w==w].copy()
    # concurrency: how many coins in position on the same days
    dd=[]
    for w in wins:
        f=pd.concat([days[c][w].assign(coin=c) for c in coins if w in days[c]])
        dd.append(f.groupby("day").agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna())
    D=pd.concat(dd)
    D["q"]=pd.qcut(D.cr,10,labels=False)
    out["book_by_market_decile"]=D.groupby("q").agg(br=("br",lambda s:s.mean()*1e4),cr=("cr",lambda s:s.mean()*1e4),n=("br","size")).round(1)
    out["worst_book_days_share_of_loss"]=float(D.br.nsmallest(40).sum()/D.br[D.br<0].sum())
    return out
