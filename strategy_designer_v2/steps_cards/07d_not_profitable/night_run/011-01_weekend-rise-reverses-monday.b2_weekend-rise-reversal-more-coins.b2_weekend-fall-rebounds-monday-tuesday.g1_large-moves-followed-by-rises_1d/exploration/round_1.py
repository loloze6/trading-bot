def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily pooled
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"]=D["w"].str[1:].astype(int)
    P = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().reset_index().sort_values(["wn","day"])
    def stats_(r):
        eq=(1+r).cumprod(); dd=eq/eq.cummax()-1
        yr=eq.iloc[-1]**(365/len(r))-1
        return r.mean()/r.std()*np.sqrt(365), yr, dd.min()
    b=stats_(P.book_return); h=stats_(P.coin_return)
    out["book sharpe,yr,mdd"]=str(np.round(b,4)); out["hold sharpe,yr,mdd"]=str(np.round(h,4))
    eq=(1+P.book_return).cumprod(); P["dd"]=eq/eq.cummax()-1
    P["year"]=pd.to_datetime(P.day).dt.year
    out["by window"]=P.groupby("wn").agg(n=("book_return","size"),book=("book_return","mean"),hold=("coin_return","mean"),mindd=("dd","min")).round(5)
    # per bar analysis: next 2-day return by prior move sign and trend
    recs=[]
    for c, ws in data["bars"].items():
        for w, b_ in ws.items():
            cl=b_["close"].values
            r1=pd.Series(cl).pct_change().values
            f=b_["forecast"].values
            al=b_["postRebalance_current_allocation"].values
            nxt=np.r_[cl[1:]/cl[:-1]-1, np.nan]
            fwd2=np.r_[cl[2:]/cl[:-2]-1,[np.nan,np.nan]]
            s=pd.Series(cl)
            r20=(s/s.shift(20)-1).values
            vol=pd.Series(r1).rolling(60,min_periods=20).std().values
            ma=(s/s.rolling(50,min_periods=20).mean()-1).values
            recs.append(pd.DataFrame(dict(coin=c,w=w,pos=np.arange(len(cl)),r1=r1,f=f,al=al,gain=al*nxt,nxt=nxt,fwd2=fwd2,r20=r20,ma=ma,vol=vol)))
    B=pd.concat(recs)
    B["exc_nxt"]=B.nxt-B.groupby("coin").nxt.transform("mean")
    B["dir"]=np.sign(B.r1)
    B["fq"]=pd.qcut(B.f.rank(method="first"),5,labels=False)
    out["gain by fq x dir"]=B.groupby(["fq","dir"]).agg(n=("gain","size"),alloc=("al","mean"),gain=("gain","mean"),exc_nxt=("exc_nxt","mean")).round(5)
    B["tr"]=pd.qcut(B.ma,5,labels=False)
    out["by trend q (price/50d ma)"]=B.groupby("tr").agg(n=("gain","size"),alloc=("al","mean"),gain=("gain","mean"),nxt=("nxt","mean"),exc=("exc_nxt","mean")).round(5)
    g=B[B.pos%2==0].dropna(subset=["fwd2","ma"])
    g["exc2"]=g.fwd2-g.groupby("coin").fwd2.transform("mean")
    g["tr"]=pd.qcut(g.ma,3,labels=False)
    res={}
    for t,gg in g.groupby("tr"):
        sl=stats.linregress(gg.f,gg.exc2); res[t]=(len(gg),sl.slope,sl.slope/sl.stderr)
    out["slope f->exc2 by trend tercile (n,slope,t)"]=pd.DataFrame(res,index=["n","slope","t"]).T
    res={}
    for t,gg in g.groupby(np.sign(g.r1)):
        sl=stats.linregress(gg.f,gg.exc2); res[t]=(len(gg),sl.slope,sl.slope/sl.stderr)
    out["slope by dir"]=pd.DataFrame(res,index=["n","slope","t"]).T
    out["mean alloc"]=float(B.al.mean())
    return out
