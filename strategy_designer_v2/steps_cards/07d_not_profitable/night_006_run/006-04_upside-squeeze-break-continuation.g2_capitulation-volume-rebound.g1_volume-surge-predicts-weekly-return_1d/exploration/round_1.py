def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # pooled bar-level gain by position side
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            r = b["close"].shift(-1)/b["close"]-1
            a = b["postRebalance_current_allocation"]
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            f = b["forecast"]
            # 5d trailing return & 30d trailing vol for state
            r5 = b["close"]/b["close"].shift(5)-1
            r30 = b["close"]/b["close"].shift(30)-1
            fwd7 = b["close"].shift(-7)/b["close"]-1
            df = pd.DataFrame({"coin":c,"w":w,"pos":b.index,"r":r,"a":a,"g":a*r,"fee":fee,"f":f,"r5":r5,"r30":r30,"fwd7":fwd7})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["side"] = np.sign(D["a"])
    coinmean = D.groupby("coin")["r"].mean()
    D["mkt"] = D["a"]*D["coin"].map(coinmean)
    D["timing"] = D["g"]-D["mkt"]
    out["by_side"] = D.groupby("side").agg(n=("g","size"),mean_gain=("g","mean"),mean_abs_a=("a",lambda x: x.abs().mean()),mean_r=("r","mean"),mkt=("mkt","mean"),timing=("timing","mean"),fee=("fee","mean"))
    out["by_coin"] = D.groupby("coin").agg(gain=("g","mean"),mkt=("mkt","mean"),timing=("timing","mean"),fee=("fee","mean"),long_share=("side",lambda x:(x>0).mean()),coin_r=("r","mean"))
    # forecast quintiles vs fwd7, non-overlapping
    S = D[D["pos"]%7==0].dropna(subset=["f","fwd7"]).copy()
    S["ex"] = S["fwd7"]-S["coin"].map(S.groupby("coin")["fwd7"].mean())
    S["fq"] = pd.qcut(S["f"],5,labels=False)
    out["fq_fwd7"] = S.groupby("fq").agg(n=("ex","size"),f=("f","mean"),ex=("ex","mean"),raw=("fwd7","mean"),sd=("fwd7","std"))
    # conditional on r5 sign
    S["r5s"] = np.sign(S["r5"])
    S["fpos"] = S["f"]>0
    out["f_by_r5sign"] = S.groupby(["r5s","fpos"]).agg(n=("ex","size"),ex=("ex","mean"),raw=("fwd7","mean"))
    S["r30t"] = pd.qcut(S["r30"],3,labels=False)
    out["f_by_r30tercile"] = S.groupby(["r30t","fpos"]).agg(n=("ex","size"),ex=("ex","mean"))
    # book daily
    bk=[]
    for c in days:
        for w,d in days[c].items():
            dd=d[["day","book_return","coin_return"]].copy(); dd["w"]=w; dd["coin"]=c; bk.append(dd)
    B=pd.concat(bk).dropna()
    P=B.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    out["book_sum"]=pd.Series({"book_mean":P.book_return.mean(),"hold_mean":P.coin_return.mean(),"book_sh":P.book_return.mean()/P.book_return.std()*np.sqrt(365),"hold_sh":P.coin_return.mean()/P.coin_return.std()*np.sqrt(365),"fee_per_bar":D.fee.mean(),"gross_bar":D.g.mean()})
    P["wn"]=P.w.str[1:].astype(int)
    out["by_window"]=P.groupby("wn").agg(book=("book_return","mean"),hold=("coin_return","mean"))
    return out
