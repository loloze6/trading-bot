import numpy as np, pandas as pd

def explore(data):
    out = {}
    days = data["days"]; bars = data["bars"]; trades = data["trades"]
    # book daily returns: per window, per day mean over coins
    wins = sorted({w for c in days for w in days[c]}, key=lambda s: int(s[1:]))
    chain = []
    for w in wins:
        parts = []
        for c in days:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c
                parts.append(d)
        df = pd.concat(parts)
        g = df.groupby("day")[["book_return","coin_return"]].mean().sort_index()
        g["window"]=w
        chain.append(g)
    ch = pd.concat(chain).dropna(subset=["book_return"]).reset_index(drop=True)
    eq = (1+ch["book_return"]).cumprod()
    dd = eq/eq.cummax()-1
    out["max_dd"] = float(dd.min())
    tr = dd.idxmin(); pk = eq[:tr+1].idxmax()
    out["dd_peak_window"] = ch.loc[pk,"window"]; out["dd_trough_window"]=ch.loc[tr,"window"]
    out["dd_len_days"] = int(tr-pk)
    seg = ch.loc[pk+1:tr]
    out["dd_by_window"] = seg.groupby("window").agg(book=("book_return","sum"),coin=("coin_return","sum"),n=("book_return","size"))
    # per-window book summary
    pw = ch.groupby("window").agg(book=("book_return","sum"),coin=("coin_return","sum"))
    pw["mdd"] = ch.groupby("window")["book_return"].apply(lambda r: float(((1+r).cumprod()/(1+r).cumprod().cummax()-1).min()))
    out["per_window"] = pw.reindex(wins)
    # per coin contribution during drawdown
    rows=[]
    for c in days:
        for w in seg["window"].unique():
            if w in days[c]:
                d=days[c][w]; d=d[d["day"].isin(seg.loc[seg.window==w].index.map(lambda i: None))] if False else d
    # trades features
    recs=[]
    for c in trades:
        for w,t in trades[c].items():
            if t is None or len(t)==0: continue
            b = bars[c][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            lr = np.log(b["close"]).diff()
            for _,r in t.iterrows():
                et = pd.to_datetime(r["entry_time"]); xt=pd.to_datetime(r["exit_time"])
                i = ts.searchsorted(et, side="right")-1
                j = ts.searchsorted(xt, side="right")-1
                if i<0: continue
                vol20 = lr.iloc[max(1,i-19):i+1].std()*np.sqrt(365)
                ret20 = b["close"].iloc[i]/b["close"].iloc[max(0,i-20)]-1
                ret5 = b["close"].iloc[i]/b["close"].iloc[max(0,i-5)]-1
                hi = b["high"].iloc[max(0,i-60):i+1].max(); lo=b["low"].iloc[max(0,i-60):i+1].min()
                pos60 = (b["close"].iloc[i]-lo)/(hi-lo) if hi>lo else np.nan
                path = b["close"].iloc[i:j+1]/b["close"].iloc[i]-1
                alloc = b["postRebalance_current_allocation"].iloc[i]
                recs.append(dict(coin=c,window=w,pnl=r["net_profit_loss_percent"],alloc=alloc,
                    fc=r["entry_forecast"],vol20=vol20,ret20=ret20,ret5=ret5,pos60=pos60,
                    mae=path.min(),dur=r["duration_minutes"]/1440,side=r["side"]))
    T=pd.DataFrame(recs)
    T["contrib"]=T["pnl"]*T["alloc"].abs()
    out["n_trades"]=len(T)
    out["trades_desc"]=T[["pnl","alloc","fc","vol20","ret20","ret5","pos60","mae","dur","contrib"]].describe().T
    out["corr_with_pnl"]=T[["alloc","fc","vol20","ret20","ret5","pos60"]].corrwith(T["pnl"],method="spearman")
    out["corr_with_mae"]=T[["alloc","fc","vol20","ret20","ret5","pos60"]].corrwith(T["mae"],method="spearman")
    for col in ["vol20","ret20","ret5","pos60","alloc"]:
        q=pd.qcut(T[col],4,labels=False,duplicates="drop")
        out["q_"+col]=T.groupby(q).agg(n=("pnl","size"),pnl=("pnl","mean"),mae=("mae","mean"),contrib=("contrib","mean"),lo=(col,"min"),hi=(col,"max"))
    out["dd_window_trades"]=T[T.window.isin(seg["window"].unique())].groupby(["window"]).agg(n=("pnl","size"),pnl=("pnl","mean"),contrib=("contrib","sum"),alloc=("alloc","mean"),vol20=("vol20","mean"),ret20=("ret20","mean"))
    out["worst10"]=T.nsmallest(10,"contrib")[["coin","window","pnl","alloc","vol20","ret20","ret5","pos60","mae"]].reset_index(drop=True)
    return out
