def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # portfolio daily returns
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    wnum = lambda w: int(w[1:])
    P = D.groupby(["w","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).reset_index()
    P["wn"]=P.w.map(wnum); P=P.sort_values(["wn","day"]).dropna(subset=["br"])
    eq=(1+P.br).cumprod(); dd=eq/eq.cummax()-1; P["dd"]=dd.values
    out["dd_by_window"]=P.groupby("w").agg(min_dd=("dd","min"), book_sum=("br","sum"), coin_sum=("cr","sum"), n=("br","size")).sort_values("min_dd")
    # per-window max drawdown within window
    def wdd(s):
        e=(1+s).cumprod(); return (e/e.cummax()-1).min()
    out["within_window_dd"]=P.groupby("w").br.apply(wdd).sort_values()
    # bar-level features
    B=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.copy(); b["coin"]=c; b["w"]=w
            cl=b.close; r=cl.pct_change()
            b["er"]=(cl-cl.shift(30)).abs()/cl.diff().abs().rolling(30).sum()
            b["p7"]=cl/cl.shift(7)-1; b["p30"]=cl/cl.shift(30)-1
            b["vol30"]=r.rolling(30).std()
            b["f7"]=cl.shift(-7)/cl-1
            b["r1"]=cl.shift(-1)/cl-1
            b["pos"]=b.postRebalance_current_allocation
            b["gain"]=b.pos*b.r1
            b["i"]=np.arange(len(b))
            B.append(b)
    B=pd.concat(B)
    B["side"]=np.sign(B.pos)
    B["inreg"]=B.regime=="mean_reversion"
    out["gain_by_side_regime"]=B.groupby(["side","inreg"]).gain.agg(["mean","sum","count"])
    # vol30 terciles by coin
    B["volq"]=B.groupby("coin").vol30.transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    B["side_p30"]=np.sign(B.p30)
    out["gain_by_side_volq"]=B[B.side!=0].groupby(["side","volq"]).gain.agg(["mean","sum","count"])
    # grid cases
    drift=B[B.i%7==0].groupby("coin").f7.mean()
    G=B[(B.i%7==0)&B.inreg&B.forecast.notna()&(B.forecast!=0)].copy()
    G["ex"]=np.sign(G.forecast)*(G.f7-G.coin.map(drift))
    G["fq"]=pd.qcut(G.forecast.abs(),3,labels=False,duplicates="drop")
    G["erq"]=pd.qcut(G.er,3,labels=False,duplicates="drop")
    def agg(g):
        return pd.Series({"mean":g.ex.mean(),"t":g.ex.mean()/(g.ex.std()/np.sqrt(len(g))),"n":len(g)})
    out["grid_by_side"]=G.groupby(np.sign(G.forecast)).apply(agg)
    out["grid_by_absfq"]=G.groupby("fq").apply(agg)
    out["grid_by_volq"]=G.groupby("volq").apply(agg)
    out["grid_by_erq"]=G.groupby("erq").apply(agg)
    # deepest fall: top 30 worst portfolio days and states
    worst=P.nsmallest(30,"br")[["w","day"]]
    m=B.copy(); m["day"]=pd.to_datetime(m.timestamp).dt.floor("D")
    worst["day"]=pd.to_datetime(worst.day)
    mm=m.merge(worst,on=["w","day"])
    out["worst_days_state"]=pd.Series({"n_coinbars":len(mm),"share_long":(mm.side>0).mean(),"share_short":(mm.side<0).mean(),
        "share_inreg":mm.inreg.mean(),"mean_gain":mm.gain.mean(),"mean_absalloc":mm.pos.abs().mean(),"all_absalloc":B.pos.abs().mean(),
        "volq_mean_worst":mm.volq.mean(),"coin_r1_mean":mm.r1.mean()})
    # holding outside regime: share of position bars where regime not active
    out["pos_bars_inreg_share"]=B[B.side!=0].inreg.mean()
    out["trades_by_side"]=pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()]).groupby("side").net_profit_loss_percent.agg(["mean","sum","count"])
    return out
