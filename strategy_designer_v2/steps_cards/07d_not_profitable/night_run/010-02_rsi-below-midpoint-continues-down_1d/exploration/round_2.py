def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted(set(w for c in coins for w in days[c].keys()), key=lambda x:int(x[1:]))
    frames=[]
    for c in coins:
        for w in wins:
            if w not in days[c]: continue
            b=bars[c][w].copy().reset_index(drop=True)
            b["coin"]=c; b["win"]=w; b["wn"]=int(w[1:])
            b["ret"]=b.close.pct_change()
            b["ret7p"]=b.close/b.close.shift(7)-1
            b["ret28"]=b.close/b.close.shift(28)-1
            b["ret60"]=b.close/b.close.shift(60)-1
            b["fwd1"]=b.close.shift(-1)/b.close-1
            b["fwd7"]=b.close.shift(-7)/b.close-1
            b["pos"]=b.postRebalance_current_allocation
            b["pnl"]=b.pos*b.fwd1
            b["grid"]=(np.arange(len(b))%7==0)
            frames.append(b)
    a=pd.concat(frames,ignore_index=True)
    a["mean7"]=a[a.grid].groupby("coin").fwd7.transform("mean")
    m7=a[a.grid].groupby("coin").fwd7.mean()
    a["ex7"]=a.fwd7-a.coin.map(m7)
    a["fc"]=a.forecast
    # agreement of forecast sign with 28-day trend
    a["agree28"]=np.sign(a.fc)==np.sign(a.ret28)
    g=a[a.grid].dropna(subset=["ex7","fc","ret28"])
    res={}
    for k,s in g.groupby("agree28"):
        r=stats.linregress(s.fc,s.ex7); res[str(k)]=pd.Series({"n":len(s),"slope":r.slope,"t":r.slope/r.stderr,"mean_signed_ex7":(np.sign(s.fc)*s.ex7).mean()})
    out["slope_by_agree28"]=pd.DataFrame(res).T
    # interaction: fc x ret28 and fc graded by trend size
    g["fc_x_r28"]=np.sign(g.fc)*g.ret28
    g["q"]=pd.qcut(g.fc_x_r28,5,labels=False)
    out["signed_ex7_by_alignment_quintile"]=g.groupby("q").apply(lambda s: pd.Series({"n":len(s),"mean_fc_x_r28":s.fc_x_r28.mean(),"signed_ex7":(np.sign(s.fc)*s.ex7).mean(),"t":stats.ttest_1samp(np.sign(s.fc)*s.ex7,0).statistic}))
    # daily pnl by agree28 using longer trend 60
    d=a.dropna(subset=["pnl","ret28"])
    d["al28"]=np.sign(d.pos)*d.ret28
    d["q28"]=pd.qcut(d.al28,5,labels=False)
    out["daily_pnl_by_alignment28_q"]=d.groupby("q28").agg(n=("pnl","size"),al=("al28","mean"),pnl=("pnl","mean"),sd=("pnl","std"))
    d2=a.dropna(subset=["pnl","ret60"])
    d2["al60"]=np.sign(d2.pos)*d2.ret60
    d2["q60"]=pd.qcut(d2.al60,5,labels=False)
    out["daily_pnl_by_alignment60_q"]=d2.groupby("q60").agg(n=("pnl","size"),al=("al60","mean"),pnl=("pnl","mean"))
    # deepest episode windows 2-6: pnl by side and coin
    e=a[a.wn.between(2,6)].dropna(subset=["pnl"])
    out["ep_by_coin_side"]=e.groupby(["coin",np.sign(e.pos)]).agg(n=("pnl","size"),pnl=("pnl","mean"),sum=("pnl","sum"))
    out["ep_by_window"]=e.groupby("wn").agg(pnl_sum=("pnl","sum"),short_share=("pos",lambda s:(s<0).mean()),r28=("ret28","mean"))
    # mean abs position and forecast
    out["pos_stats"]=pd.Series({"mean_abs_pos":a.pos.abs().mean(),"short_share":(a.pos<0).mean(),"corr_fc_ret28":a[["fc","ret28"]].corr().iloc[0,1]})
    return out
