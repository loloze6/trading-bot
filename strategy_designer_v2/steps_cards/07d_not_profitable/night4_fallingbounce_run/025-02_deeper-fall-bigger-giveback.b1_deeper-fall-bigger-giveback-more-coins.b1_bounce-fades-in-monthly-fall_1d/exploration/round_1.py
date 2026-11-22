import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(20).std()
            z=r/sd
            r30=c/c.shift(30)-1; r90=c/c.shift(90)-1
            f1=c.shift(-1)/c-1; f3=c.shift(-3)/c-1; f5=c.shift(-5)/c-1
            df=pd.DataFrame({"coin":coin,"w":w,"z":z,"r30":r30,"r90":r90,"f1":f1,"f3":f3,"f5":f5,
                             "pos":b["postRebalance_current_allocation"].astype(float),
                             "fc":b["forecast"].astype(float),"pos_i":np.arange(len(b)),
                             "year":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
    d=pd.concat(rows)
    drift=d.groupby("coin")["f1"].mean()
    d["a1"]=d["f1"]-d["coin"].map(drift)
    d["a3"]=d["f3"]-3*d["coin"].map(drift)
    d["a5"]=d["f5"]-5*d["coin"].map(drift)
    out={}
    d["zb"]=pd.cut(d["z"],[-99,-2,-1,0,1,1.5,2,3,99])
    d["reg"]=np.where((d.r90<0)&(d.r30<0),"both_neg",np.where((d.r90<0),"r90neg_r30pos",np.where(d.r30<0,"r90pos_r30neg","both_pos")))
    def agg(g,col):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out["a1 by reg x zbin"]=d.groupby(["reg","zb"],observed=True).apply(lambda g:agg(g,"a1")).round(3)
    # 3-day on grid
    g3=d[d.pos_i%3==0]
    out["a3 grid by reg x zbin"]=g3.groupby(["reg","zb"],observed=True).apply(lambda g:agg(g,"a3")).round(3)
    act=d[d.fc!=0]
    out["active counts"]=pd.Series({"bars":len(d),"active":len(act),"held_nonzero":(d.pos.abs()>1e-6).sum(),
       "mean_pos_active":act.pos.mean(),"a1_active":100*act.a1.mean(),"a3_active":100*act.a3.mean(),"a5_active":100*act.a5.mean()})
    out["active by year"]=act.groupby("year").apply(lambda g:agg(g,"a1")).round(3)
    # days of book
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            dd.append(x.assign(coin=coin,w=w))
    dd=pd.concat(dd)
    bd=dd.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book days"]=pd.Series({"days":len(bd),"book_mean%":100*bd.book_return.mean(),"hold_mean%":100*bd.coin_return.mean(),
        "nonzero_book_days":(bd.book_return.abs()>1e-9).sum()})
    return out
