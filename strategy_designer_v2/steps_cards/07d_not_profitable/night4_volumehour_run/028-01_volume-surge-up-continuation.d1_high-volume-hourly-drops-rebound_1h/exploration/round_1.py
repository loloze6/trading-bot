import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    # ---- book daily, pooled over coins
    frames = []
    for c in days:
        for w, d in days[c].items():
            x = d[["day","book_return","coin_return"]].copy(); x["w"]=w; x["coin"]=c
            frames.append(x)
    D = pd.concat(frames)
    wn = lambda s: int(str(s)[1:])
    P = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    P["wn"]=P["w"].map(wn); P=P.sort_values(["wn","day"]).dropna()
    sh = lambda r: r.mean()/r.std()*np.sqrt(365)
    out["sharpe book/hold"] = f"{sh(P.book_return):.3f} / {sh(P.coin_return):.3f}; mean {P.book_return.mean():.5f} / {P.coin_return.mean():.5f}"
    # per window
    pw = P.groupby("wn").agg(book=("book_return","sum"), coin=("coin_return","sum"), n=("book_return","size"))
    out["per window summed returns"] = pw.round(4)
    # drawdown chain
    eq = (1+P.book_return).cumprod().values
    peak = np.maximum.accumulate(eq); dd = eq/peak-1
    P["dd"]=dd
    i_trough = int(np.argmin(dd)); i_peak = int(np.argmax(eq[:i_trough+1]))
    seg = P.iloc[i_peak+1:i_trough+1]
    out["deepest fall"] = f"depth {dd[i_trough]:.3f}, days {len(seg)}, windows {seg.wn.min()}-{seg.wn.max()}, coin chained {(1+seg.coin_return).prod()-1:.3f}, book chained {(1+seg.book_return).prod()-1:.3f}"
    # ---- bar-level: allocation, timing
    B=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True).copy()
            b["ret1"]=b.close.shift(-1)/b.close-1
            b["r24"]=b.close.shift(-24)/b.close-1
            b["past7"]=b.close/b.close.shift(168)-1
            b["past30"]=b.close/b.close.shift(720)-1
            b["past1"]=b.close/b.close.shift(24)-1
            lr=np.log(b.close).diff()
            b["vol7"]=lr.rolling(168).std()
            b["pos"]=np.arange(len(b)); b["cell"]=b.pos//24
            b["coin"]=c; b["w"]=w
            B.append(b)
    B=pd.concat(B, ignore_index=True)
    a=B.postRebalance_current_allocation
    out["allocation"] = f"share bars long {(a>0.001).mean():.3f}, short {(a<-0.001).mean():.3f}, mean alloc {a.mean():.3f}, mean alloc when long {a[a>0.001].mean():.3f}"
    g=B.dropna(subset=["ret1"])
    mu = g.groupby("coin").ret1.mean()
    gain = (g.postRebalance_current_allocation*g.ret1).mean()
    mkt = (g.postRebalance_current_allocation*g.coin.map(mu)).mean()
    out["bar gain: total / market / timing"] = f"{gain:.2e} / {mkt:.2e} / {gain-mkt:.2e}"
    # ---- cases
    grid = B[B.pos%24==0].dropna(subset=["r24"])
    drift = grid.groupby("coin").r24.mean(); sd = grid.groupby("coin").r24.std()
    out["drift24 / sd24"] = pd.DataFrame({"drift":drift,"sd":sd})
    B["df"]=B.groupby(["coin","w"]).forecast.diff()
    cs = B[(B.forecast>=2)&(B.df>0)].dropna(subset=["r24"])
    cs = cs.groupby(["coin","w","cell"]).head(1).copy()
    cs["ex"]=cs.r24-cs.coin.map(drift)
    def summ(gr):
        return pd.Series({"n":len(gr),"mean_ex":gr.ex.mean(),"t":gr.ex.mean()/(gr.ex.std()/np.sqrt(len(gr))) if len(gr)>2 else np.nan,"mean_total":gr.r24.mean()})
    out["cases all"] = summ(cs)
    cs["fq"]=pd.qcut(cs.forecast.rank(method="first"),5,labels=False)
    out["cases by forecast quintile"]=cs.groupby("fq").apply(summ).round(5)
    for col in ["past1","past7","past30","vol7"]:
        cc=cs.dropna(subset=[col]).copy(); cc["q"]=pd.qcut(cc[col].rank(method="first"),5,labels=False)
        out[f"cases by {col} quintile"]=cc.groupby("q").apply(lambda gr: pd.concat([summ(gr),pd.Series({"med":gr[col].median()})])).round(5)
    out["cases by coin"]=cs.groupby("coin").apply(summ).round(5)
    # trades
    T=pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    out["trades"]=f"n {len(T)}, mean gross {T.profit_loss_percent.mean():.4f}, mean net {T.net_profit_loss_percent.mean():.4f}, mean dur h {T.duration_minutes.mean()/60:.1f}, long share {(T.side=='LONG').mean():.3f}"
    return out
