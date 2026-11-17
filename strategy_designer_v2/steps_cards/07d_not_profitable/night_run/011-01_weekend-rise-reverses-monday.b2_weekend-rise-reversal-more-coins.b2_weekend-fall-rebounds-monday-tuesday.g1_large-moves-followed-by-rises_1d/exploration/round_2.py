def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"]=D["w"].str[1:].astype(int)
    P = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().reset_index().sort_values(["wn","day"]).reset_index(drop=True)
    eq=(1+P.book_return).cumprod(); P["dd"]=eq/eq.cummax()-1
    # identify worst drawdown episode
    trough=P.dd.idxmin(); peak=eq[:trough+1].idxmax()
    out["worst dd: windows, days, book cum, hold cum"]=str((P.wn[peak],P.wn[trough],trough-peak,
        float((1+P.book_return[peak+1:trough+1]).prod()-1),float((1+P.coin_return[peak+1:trough+1]).prod()-1)))
    # book return on days with deep coin falls
    P["hq"]=pd.qcut(P.coin_return,5,labels=False)
    out["book by hold-day quintile"]=P.groupby("hq").agg(n=("book_return","size"),book=("book_return","mean"),hold=("coin_return","mean")).round(5)
    # per-bar
    recs=[]
    for c, ws in data["bars"].items():
        for w, b_ in ws.items():
            s=b_["close"].reset_index(drop=True); cl=s.values
            r1=s.pct_change().values
            al=b_["postRebalance_current_allocation"].values
            nxt=np.r_[cl[1:]/cl[:-1]-1, np.nan]
            fwd2=np.r_[cl[2:]/cl[:-2]-1,[np.nan,np.nan]]
            ma=(s/s.rolling(50,min_periods=20).mean()-1).values
            r10=(s/s.shift(10)-1).values
            sd=pd.Series(r1).rolling(60,min_periods=20).std().values
            recs.append(pd.DataFrame(dict(coin=c,w=w,pos=np.arange(len(cl)),r1=r1,z=r1/sd,f=b_["forecast"].values,al=al,gain=al*nxt,nxt=nxt,fwd2=fwd2,ma=ma,r10=r10)))
    B=pd.concat(recs)
    B["mn"]=B.groupby("coin").nxt.transform("mean")
    B["mkt"]=B.al*B.mn; B["timing"]=B.gain-B.mkt
    out["gain split mean (gain,market,timing)"]=str(np.round([B.gain.mean(),B.mkt.mean(),B.timing.mean()],6))
    g=B[B.pos%2==0].dropna(subset=["fwd2","ma","z"]).copy()
    g["exc2"]=g.fwd2-g.groupby("coin").fwd2.transform("mean")
    # signed z: exc2 by z bins
    g["zb"]=pd.cut(g.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    out["exc2 by signed z"]=g.groupby("zb").agg(n=("exc2","size"),exc2=("exc2","mean"),t=("exc2",lambda x:x.mean()/x.std()*np.sqrt(len(x)))).round(5)
    g["tr"]=pd.qcut(g.ma,3,labels=["down","mid","up"])
    g["dir"]=np.where(g.r1<0,"fall","rise")
    big=g[g.z.abs()>1]
    out["big moves exc2 by dir x trend"]=big.groupby(["dir","tr"]).agg(n=("exc2","size"),exc2=("exc2","mean"),t=("exc2",lambda x:x.mean()/x.std()*np.sqrt(len(x)))).round(5)
    # slope of exc2 on -z (fall size graded) among falls, and on z among rises
    res={}
    for k,gg in g.groupby("dir"):
        sl=stats.linregress(gg.z.abs(),gg.exc2); res[k]=(len(gg),sl.slope,sl.slope/sl.stderr)
    out["slope exc2 on |z| by dir"]=pd.DataFrame(res,index=["n","slope","t"]).T
    # gain when book in down trend and held
    B["tr"]=pd.qcut(B.ma,3,labels=["down","mid","up"])
    B["dir"]=np.where(B.r1<0,"fall","rise")
    out["gain by trend x dir (held bars)"]=B[B.al>0.3].groupby(["tr","dir"]).agg(n=("gain","size"),alloc=("al","mean"),gain=("gain","mean"),sd=("gain","std")).round(5)
    return out
