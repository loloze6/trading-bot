def explore(data):
    import pandas as pd, numpy as np
    rows=[]; dayrows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            df=pd.DataFrame({"r":r,"nxt":c.shift(-1)/c-1,
                "a":b["postRebalance_current_allocation"].fillna(0),"f":b["forecast"],
                "zr":r/r.rolling(20).std(),"vol20":r.rolling(20).std(),
                "ret20":c/c.shift(20)-1,"ret5":c/c.shift(5)-1,
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday})
            df["gain"]=df.a*df.nxt; rows.append(df)
        for w,d in data["days"][coin].items():
            dd=d[["day","book_return","coin_return"]].copy(); dd["w"]=w; dayrows.append(dd)
    B=pd.concat(rows,ignore_index=True); D=pd.concat(dayrows,ignore_index=True)
    out={}
    act=B[B.a>0.001].dropna(subset=["nxt"])
    out["active"]=f"{len(act)} of {B.nxt.notna().sum()}, alloc {act.a.mean():.3f}, share f==0 {(act.f==0).mean():.3f}"
    bk=D.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna().reset_index()
    bk["wn"]=bk.w.str[1:].astype(int); bk=bk.sort_values(["wn","day"])
    eq=(1+bk.br).cumprod(); dd=eq/eq.cummax()-1
    out["book/hold/maxDD"]=f"{bk.br.mean():.5f} {bk.cr.mean():.5f} {dd.min():.3f}"
    out["by window"]=bk.groupby("wn").agg(book=("br",lambda x:(1+x).prod()-1),hold=("cr",lambda x:(1+x).prod()-1)).round(3)
    def g(col,q=5):
        x=act.copy(); x["b"]=pd.qcut(x[col],q,duplicates="drop")
        return x.groupby("b",observed=True).agg(n=("gain","size"),gain=("gain","mean"),nxt=("nxt","mean"),
            t=("nxt",lambda s:s.mean()/s.std()*np.sqrt(len(s))),alloc=("a","mean")).round(4)
    for c in ["f","zr","ret20","ret5","vol20"]: out["by "+c]=g(c)
    out["weekday"]=act.groupby("wd").agg(n=("gain","size"),gain=("gain","mean"),nxt=("nxt","mean")).round(4)
    T=pd.concat([t for wins in data["trades"].values() for t in wins.values()])
    out["trades"]=f"n {len(T)} pl {T.profit_loss_percent.mean():.4f} net {T.net_profit_loss_percent.mean():.4f}"
    return out
