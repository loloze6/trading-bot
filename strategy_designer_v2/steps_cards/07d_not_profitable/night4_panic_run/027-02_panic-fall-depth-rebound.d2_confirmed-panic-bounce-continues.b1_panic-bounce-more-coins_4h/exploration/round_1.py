import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]; drift={}; usual={}
    H=84
    for coin,ws in data["bars"].items():
        g=[]
        for w,b in ws.items():
            c=b["close"].values
            g+=list(c[H::H]/c[:-H:H]-1) if len(c)>H else []
        g=np.array(g); drift[coin]=np.nanmean(g) if len(g) else np.nan; usual[coin]=np.nanstd(g) if len(g) else np.nan
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            h=b["high"];l=b["low"];c=b["close"]
            r6=h.rolling(6).max()-l.rolling(6).min()
            base=r6.rolling(180,min_periods=30).mean()
            mult=(r6/base).shift(6)
            fall=(c.shift(6)/c.shift(12)-1)
            bounce=c/c.shift(6)-1
            prior=c.shift(6)/c.shift(186)-1
            n=len(c)
            for k in [6,18,42,84]:
                b[f"f{k}"]=c.shift(-k)/c-1
            panic=(mult>=3)&(fall<0)
            b["cell"]=np.arange(n)//H
            d=pd.DataFrame({"panic":panic,"mult":mult,"fall":fall,"bounce":bounce,"prior":prior,
                "f6":b.f6,"f18":b.f18,"f42":b.f42,"f84":b.f84,"cell":b.cell,"reg":b["regime"],
                "fc":b["forecast"],"alloc":b["postRebalance_current_allocation"]})
            d=d[d.panic]
            d=d.groupby("cell").head(1)
            d["coin"]=coin;d["w"]=w
            rows.append(d)
    D=pd.concat(rows)
    D["dr"]=D.coin.map(drift);D["us"]=D.coin.map(usual)
    D["ex"]=D.f84-D.dr
    D=D.dropna(subset=["ex","bounce"])
    out={}
    out["n_cases"]=len(D)
    def summ(G):
        return G.agg(n=("ex","size"),ex84=("ex","mean"),tot84=("f84","mean"),f6=("f6","mean"),f18=("f18","mean"),f42=("f42","mean"),fc_pos=("fc",lambda x:(x>0).mean()))
    D["bq"]=pd.qcut(D.bounce,5,labels=False)
    out["by_bounce_q"]=summ(D.groupby("bq"))
    D["fq"]=pd.qcut(D.fall,5,labels=False)
    out["by_fall_q(0=deepest)"]=summ(D.groupby("fq"))
    D["pq"]=pd.qcut(D.prior,5,labels=False)
    out["by_prior30d_q(0=most down)"]=summ(D.groupby("pq"))
    D["mq"]=pd.qcut(D["mult"],4,labels=False)
    out["by_mult_q"]=summ(D.groupby("mq"))
    D["yr"]=0
    def tt(x,y):
        s=stats.linregress(x,y);return pd.Series({"slope":s.slope,"t":s.slope/s.stderr,"n":len(x)})
    out["slopes_ex84"]=pd.DataFrame({k:tt(D[k].values,D.ex.values) for k in ["bounce","fall","prior","mult"] if D[k].notna().all()} )
    Dp=D.dropna(subset=["prior"])
    out["slope_prior"]=tt(Dp.prior.values,Dp.ex.values)
    # book days
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            b=data["bars"][coin][w]
            al=b.groupby(pd.to_datetime(b.timestamp).dt.floor("D"))["postRebalance_current_allocation"].last().abs()
            x=x.copy();x["inpos"]=al.reindex(pd.to_datetime(x.day)).values>0.01 if True else None
            x["coin"]=coin;x["w"]=w;dd.append(x)
    X=pd.concat(dd)
    X["yr"]=pd.to_datetime(X.day).dt.year
    out["days_inpos_share"]=X.inpos.mean()
    out["book_by_inpos"]=X.groupby("inpos").agg(n=("book_return","size"),book=("book_return","mean"),coin=("coin_return","mean"))
    out["book_by_year"]=X.groupby("yr").agg(book=("book_return","mean"),coin=("coin_return","mean"),inpos=("inpos","mean"))
    return out
