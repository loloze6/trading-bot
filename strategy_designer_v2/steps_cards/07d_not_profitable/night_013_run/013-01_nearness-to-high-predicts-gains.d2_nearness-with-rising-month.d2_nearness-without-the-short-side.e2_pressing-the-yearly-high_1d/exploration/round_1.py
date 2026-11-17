import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars, days = data["bars"], data["days"]
    # book daily
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            al = b.groupby("day")["postRebalance_current_allocation"].last()
            dd["alloc_prev"] = dd["day"].map(lambda x: np.nan).values
            dd = dd.merge(al.rename("alloc").reset_index(), on="day", how="left") if dd["day"].dtype==al.index.dtype else dd.assign(alloc=al.reindex(pd.to_datetime(dd["day"])).values)
            dd["alloc_prev"] = dd["alloc"].shift(1)
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    port = D.groupby(["wn","day"]).agg(book=("book_return","mean"), coin=("coin_return","mean"), alloc=("alloc_prev","mean")).reset_index().sort_values(["wn","day"])
    p = port.dropna(subset=["book"])
    out["book_vs_hold"] = pd.DataFrame({"mean":[p.book.mean(),p.coin.mean()],"sd":[p.book.std(),p.coin.std()],
        "sharpe":[p.book.mean()/p.book.std()*np.sqrt(365),p.coin.mean()/p.coin.std()*np.sqrt(365)]},index=["book","hold"])
    out["mean_alloc_held"] = D["alloc_prev"].mean()
    # market vs timing per coin
    mt = []
    for c, g in D.groupby("coin"):
        g = g.dropna(subset=["book_return","alloc_prev"])
        mu = g.coin_return.mean()
        mt.append([c, g.book_return.mean(), (g.alloc_prev*mu).mean(), g.alloc_prev.mean(), mu, g.coin_return.mean()/g.coin_return.std()*np.sqrt(365), g.book_return.mean()/g.book_return.std()*np.sqrt(365)])
    out["per_coin"] = pd.DataFrame(mt, columns=["coin","book_mean","market_part","alloc","coin_mu","hold_sh","book_sh"]).set_index("coin")
    # drawdowns of chained book
    v = (1+p.book.fillna(0)).cumprod().values
    dd = v/np.maximum.accumulate(v)-1
    i = dd.argmin(); pk = np.argmax(v[:i+1])
    out["deepest_dd"] = pd.DataFrame({"dd":[dd[i]],"win_from":[p.wn.iloc[pk]],"win_to":[p.wn.iloc[i]],"days":[i-pk],
        "coin_ret_chain":[np.prod(1+p.coin.iloc[pk+1:i+1].fillna(0))-1],"alloc_in":[p.alloc.iloc[pk+1:i+1].mean()]})
    yr = (v[-1])**(365/len(v))-1
    out["yearly_ret"] = yr
    # by window book vs coin
    pw = p.groupby("wn").agg(book=("book","sum"),coin=("coin","sum"),alloc=("alloc","mean"))
    out["by_window_sum"] = pw.round(3)
    # grid: forecast quintile, 7d fwd, alloc, dist
    G = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            fwd = b.close.shift(-7)/b.close-1
            r28 = b.close/b.close.shift(28)-1
            idx = np.arange(0,len(b),7)
            g = pd.DataFrame({"f":b.forecast.iloc[idx].values,"fwd":fwd.iloc[idx].values,"al":b.postRebalance_current_allocation.iloc[idx].values,
                "dist":b["debug_info.components.dist_high.last_history_value"].iloc[idx].values,"r28":r28.iloc[idx].values,"coin":c})
            G.append(g)
    G = pd.concat(G).dropna(subset=["fwd","f"])
    G["exc"] = G.fwd - G.groupby("coin").fwd.transform("mean")
    G["fq"] = pd.qcut(G.f.rank(method="first"),5,labels=False)
    def summ(gg, key):
        t = gg.groupby(key).agg(n=("exc","size"),fwd=("fwd","mean"),exc=("exc","mean"),sd=("exc","std"),al=("al","mean"),f=("f","mean"),dist=("dist","mean"))
        t["t"] = t.exc/(t.sd/np.sqrt(t.n)); return t.drop(columns="sd").round(4)
    out["by_fq"] = summ(G,"fq")
    G["dq"] = pd.qcut(G.dist.rank(method="first"),5,labels=False)
    out["by_rawdist_q"] = summ(G.dropna(subset=["dist"]),"dq")
    G["mq"] = pd.qcut(G.r28.rank(method="first"),5,labels=False)
    out["by_r28_q"] = summ(G.dropna(subset=["r28"]),"mq")
    out["fq_x_r28"] = G.dropna(subset=["r28"]).pivot_table(index="fq",columns="mq",values="exc",aggfunc="mean").round(4)
    return out
