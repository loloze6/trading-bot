import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # book daily
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().sort_index()
    def stats_(r):
        eq=(1+r).cumprod(); dd=(eq/eq.cummax()-1).min()
        return pd.Series({"mean":r.mean(),"sharpe":r.mean()/r.std()*np.sqrt(365),"maxdd":dd,"n":len(r)})
    out["book_vs_hold"]=pd.DataFrame({"book":stats_(B.book_return),"hold":stats_(B.coin_return)})
    out["by_window"]=B.groupby(level=0).agg(book=("book_return","sum"),hold=("coin_return","sum"))
    out["by_coin"]=D.groupby("coin")[["book_return","coin_return"]].mean()
    # trades
    tr=[]
    for c, ws in data["trades"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=c; tr.append(t)
    T=pd.concat(tr)
    out["trades"]=pd.Series({"n":len(T),"gross_mean":T.profit_loss_percent.mean(),"net_mean":T.net_profit_loss_percent.mean(),
        "comm_mean":T.total_commission.mean(),"dur_h_mean":T.duration_minutes.mean()/60,"win_net":(T.net_profit_loss_percent>0).mean()})
    # signal bars
    S=[]
    for c, ws in data["bars"].items():
        mu=[]
        for w,b in ws.items():
            cl=b.close.values; mu.append(cl[24::24][:]/cl[:-24:24][:len(cl[24::24])]-1)
        mu=np.nanmean(np.concatenate(mu))
        for w,b in ws.items():
            b=b.reset_index(drop=True); ts=pd.to_datetime(b.timestamp)
            cl=b.close
            f24=cl.shift(-24)/cl-1
            p24=cl/cl.shift(24)-1; p7=cl/cl.shift(168)-1; p30=cl/cl.shift(720)-1
            lr=np.log(cl).diff()
            vol=lr.rolling(168).std()
            # jumpiness: max abs hourly over 24h / abs sum
            mx=lr.abs().rolling(24).max(); sm=lr.abs().rolling(24).sum()
            m=(ts.dt.hour==19)
            s=pd.DataFrame({"coin":c,"w":w,"fc":b.forecast,"alloc":b.postRebalance_current_allocation,
              "ex":f24-mu,"p24":p24,"p7":p7,"p30":p30,"vol":vol,"jump":mx/sm,"year":ts.dt.year})[m]
            S.append(s)
    S=pd.concat(S).dropna(subset=["ex"])
    L=S[S.fc>0].copy()
    out["n_long"]=len(L)
    L["fbin"]=pd.qcut(L.fc,5,labels=False,duplicates="drop")
    out["by_fc_quint"]=L.groupby("fbin").agg(fc=("fc","mean"),ex=("ex","mean"),alloc=("alloc","mean"),n=("ex","size"))
    for k in ["p7","p30","vol","jump"]:
        x=L.dropna(subset=[k]).copy(); x["q"]=pd.qcut(x[k],4,labels=False)
        g=x.groupby("q").agg(lo=(k,"min"),hi=(k,"max"),ex=("ex","mean"),sd=("ex","std"),n=("ex","size"))
        g["t"]=g.ex/(g.sd/np.sqrt(g.n))
        # slope of ex on fc within quartile
        g["slope_t"]=[stats.linregress(x[x.q==q].fc,x[x.q==q].ex).rvalue*np.sqrt((len(x[x.q==q])-2)/(1-stats.linregress(x[x.q==q].fc,x[x.q==q].ex).rvalue**2)) for q in g.index]
        out["long_by_"+k]=g
    out["long_by_year"]=L.groupby("year").agg(ex=("ex","mean"),n=("ex","size"))
    out["long_by_coin"]=L.groupby("coin").agg(ex=("ex","mean"),n=("ex","size"))
    return out
