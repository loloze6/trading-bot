def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns: per window, mean over coins by day
    dd = []
    for c, ws in data["days"].items():
        for w, df in ws.items():
            d = df[["day","book_return","coin_return"]].copy(); d["coin"]=c; d["w"]=w
            dd.append(d)
    dd = pd.concat(dd)
    dd["wn"] = dd["w"].str[1:].astype(int)
    port = dd.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().sort_index()
    eq = (1+port["book_return"]).cumprod()
    dda = eq/eq.cummax()-1
    port["dd"]=dda.values
    perw = port.groupby(level=0).agg(book_mean=("book_return","mean"), coin_mean=("coin_return","mean"), mindd=("dd","min"), n=("book_return","size"))
    perw["book_cum"]=port.groupby(level=0)["book_return"].apply(lambda s:(1+s).prod()-1)
    perw["coin_cum"]=port.groupby(level=0)["coin_return"].apply(lambda s:(1+s).prod()-1)
    # in-window drawdown
    perw["inwin_dd"]=port.groupby(level=0)["book_return"].apply(lambda s:((1+s).cumprod()/(1+s).cumprod().cummax()-1).min())
    out["per_window"]=perw.round(4)
    yr = eq.iloc[-1]**(365/len(eq))-1
    out["overall"]=pd.Series({"yearly":yr,"maxdd":dda.min(),"calmar":yr/-dda.min(),"days":len(eq)})
    # deepest fall location
    i = int(np.argmin(dda.values)); peak = int(np.argmax(eq.values[:i+1]))
    seg = port.iloc[peak:i+1]
    out["deepest_fall"]=pd.Series({"peak_window":seg.index[0][0],"trough_window":seg.index[-1][0],"days":len(seg),"book_cum":(1+seg.book_return).prod()-1,"coin_cum":(1+seg.coin_return).prod()-1})
    # cases: entries from allocation 0 -> >0
    rows=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; hi=b["high"].values; lo=b["low"].values
            pa=b["previous_allocation"].fillna(0).values; a=b["postRebalance_current_allocation"].fillna(0).values
            n=len(b)
            r180=pd.Series(cl).pct_change(180).values
            r42=pd.Series(cl).pct_change(42).values
            rng=pd.Series((hi-lo)/cl)
            volratio=(rng.rolling(42).mean()/rng.rolling(360).mean()).values
            ma=pd.Series(cl).rolling(300).mean().values
            for t in range(n-18):
                if pa[t]<=1e-9 and a[t]>1e-9:
                    rows.append(dict(coin=c,w=w,f=b["forecast"].iloc[t],fwd=cl[t+18]/cl[t]-1,
                        r180=r180[t],r42=r42[t],vr=volratio[t],abovema=cl[t]/ma[t]-1 if ma[t]==ma[t] else np.nan,
                        maxdd=(lo[t+1:t+19].min()/cl[t]-1)))
    cs=pd.DataFrame(rows)
    out["n_entries"]=len(cs)
    def g(col):
        x=cs.dropna(subset=[col]).copy(); x["q"]=pd.qcut(x[col],4,labels=False,duplicates="drop")
        r=x.groupby("q").agg(n=("fwd","size"),lo=(col,"min"),hi=(col,"max"),fwd=("fwd","mean"),worst_path=("maxdd","mean"),share_neg=("fwd",lambda s:(s<0).mean()))
        r["t"]=x.groupby("q")["fwd"].apply(lambda s:s.mean()/s.std()*np.sqrt(len(s)))
        return r.round(4)
    for col in ["r180","r42","vr","abovema","f"]:
        out["by_"+col]=g(col)
    return out
