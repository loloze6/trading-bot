def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            a = b["postRebalance_current_allocation"]
            r1 = c.shift(-1)/c - 1
            g = a*r1
            ret20 = c/c.shift(20)-1
            hi20 = c.rolling(20).max()
            dist = c/hi20-1
            vr = b["volume"]/b["volume"].rolling(30).mean()
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            df = pd.DataFrame({"coin":coin,"w":w,"a":a,"g":g,"r1":r1,"f":b["forecast"],
                               "ret20":ret20,"dist":dist,"vr":vr,"fee":fee,
                               "yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(df)
        for w, d in data["days"][coin].items():
            dd = d[["book_return","coin_return"]].copy(); dd["w"]=w; dd["coin"]=coin
            dd["i"]=range(len(dd)); daily.append(dd)
    B = pd.concat(rows, ignore_index=True)
    D = pd.concat(daily, ignore_index=True)
    # book daily: mean over coins per (w, i)
    bk = D.groupby(["w","i"])[["book_return","coin_return"]].mean().reset_index()
    bk["wn"]=bk["w"].str[1:].astype(int)
    bk = bk.sort_values(["wn","i"])
    eq = (1+bk["book_return"].fillna(0)).cumprod()
    dd = eq/eq.cummax()-1
    bk["dd"]=dd.values
    out["book_overall"] = pd.Series({"mean":bk.book_return.mean(),"coin_mean":bk.coin_return.mean(),
                                     "maxdd":dd.min(),"n":bk.book_return.count()})
    out["by_window"] = bk.groupby("wn").agg(book=("book_return","mean"),coin=("coin_return","mean"),
                                            mindd=("dd","min")).round(5)
    B["side"]=np.sign(B["a"])
    B["absa"]=B["a"].abs()
    out["by_side"]=B.groupby("side").agg(n=("g","size"),meang=("g","mean"),sumg=("g","sum"),
                                         r1=("r1","mean"),absa=("absa","mean"),fee=("fee","sum"))
    B["ret20q"]=pd.qcut(B["ret20"],5,labels=False)
    out["by_ret20q_side"]=B.groupby(["ret20q","side"]).agg(n=("g","size"),meang=("g","mean"),r1=("r1","mean")).round(5)
    B["fq"]=pd.qcut(B["f"],5,labels=False,duplicates="drop")
    out["by_fq"]=B.groupby("fq").agg(n=("g","size"),f=("f","mean"),a=("a","mean"),meang=("g","mean"),r1=("r1","mean")).round(5)
    out["fee_total_vs_gain"]=pd.Series({"fee_mean_per_bar":B.fee.mean(),"gain_mean_per_bar":B.g.mean()})
    out["by_year"]=B.groupby("yr").agg(g=("g","mean"),r1=("r1","mean"),a=("a","mean"))
    return out
