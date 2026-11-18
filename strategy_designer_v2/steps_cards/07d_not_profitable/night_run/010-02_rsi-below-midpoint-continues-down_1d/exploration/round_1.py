def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted(set(w for c in coins for w in days[c].keys()), key=lambda x:int(x[1:]))
    # daily book series: mean over coins per day, within window
    rows=[]
    for w in wins:
        frames=[]
        for c in coins:
            if w in days[c]:
                d=days[c][w][["day","book_return","coin_return","close"]].copy()
                b=bars[c][w].copy()
                b["day"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
                pos=b.groupby("day")["postRebalance_current_allocation"].last()
                d["day"]=pd.to_datetime(d["day"])
                d["pos"]=d["day"].map(pos)
                d["ret14"]=d["close"]/d["close"].shift(14)-1
                d["ret28"]=d["close"]/d["close"].shift(28)-1
                d["vol14"]=d["coin_return"].rolling(14).std()
                d["coin"]=c
                frames.append(d)
        f=pd.concat(frames)
        f["win"]=w
        rows.append(f)
    allc=pd.concat(rows)
    allc["pos_prev"]=allc.groupby(["coin","win"])["pos"].shift(1)
    book=allc.groupby(["win","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).reset_index()
    book["wn"]=book["win"].str[1:].astype(int)
    book=book.sort_values(["wn","day"]).dropna(subset=["br"])
    eq=(1+book["br"]).cumprod(); dd=eq/eq.cummax()-1
    book["dd"]=dd.values
    out["overall"]=pd.Series({"mean":book.br.mean(),"sd":book.br.std(),"n":len(book),"maxdd":dd.min(),
        "yearly":eq.iloc[-1]**(365/len(book))-1})
    # per window
    pw=book.groupby("wn").apply(lambda g: pd.Series({"book":(1+g.br).prod()-1,"hold":(1+g.cr).prod()-1,
        "maxdd_in":((1+g.br).cumprod()/(1+g.br).cumprod().cummax()-1).min(),"n":len(g),"year":pd.to_datetime(g.day).dt.year.iloc[0]}))
    out["per_window"]=pw
    # deepest episode
    trough=dd.values.argmin(); peak=np.argmax(eq.values[:trough+1])
    ep=book.iloc[peak:trough+1]
    out["deepest_ep"]=pd.Series({"days":len(ep),"windows":str(sorted(ep.wn.unique())),"book":(1+ep.br).prod()-1,"coin":(1+ep.cr).prod()-1})
    # position sign during losing days, by coin's state
    a=allc.dropna(subset=["book_return","pos_prev"]).copy()
    a["side"]=np.sign(a.pos_prev)
    a["trend"]=pd.cut(a.ret28,[-9,-0.15,-0.05,0.05,0.15,9])
    out["by_side_trend"]=a.groupby(["side","trend"]).book_return.agg(["mean","count","std"])
    a["volq"]=a.groupby("coin").vol14.transform(lambda s: pd.qcut(s,4,labels=False))
    out["by_side_vol"]=a.groupby(["side","volq"]).book_return.agg(["mean","count","std"])
    out["by_side"]=a.groupby("side").book_return.agg(["mean","count","std"])
    # worst 5% book days
    thr=a.book_return.quantile(0.05)
    w5=a[a.book_return<=thr]
    out["worst5_profile"]=w5.groupby("side").agg(n=("book_return","size"),mean=("book_return","mean"),ret28=("ret28","mean"),ret14=("ret14","mean"),coinret=("coin_return","mean"))
    return out
