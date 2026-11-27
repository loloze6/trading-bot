def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # book daily returns, mean across coins per day per window
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["w","day"]).agg(book=("book_return","mean"), hold=("coin_return","mean")).reset_index()
    B = B.dropna()
    def sh(x): return x.mean()/x.std()*np.sqrt(365) if x.std()>0 else np.nan
    pw = B.groupby("w").agg(n=("book","size"), book_sum=("book","sum"), book_sh=("book",sh), hold_sum=("hold","sum"), worst_day=("book","min"))
    out["per_window"] = pw.round(4)
    # leave one out
    lo = {w: sh(B[B.w!=w].book) for w in B.w.unique()}
    out["loo_sharpe"] = pd.Series(lo).round(3)
    # cases
    cs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b.close.values; n=len(b)
            r1 = b.close.pct_change()
            ret5 = b.close/b.close.shift(5)-1
            ret60 = b.close/b.close.shift(60)-1
            ret20 = b.close/b.close.shift(20)-1
            ret10 = b.close/b.close.shift(10)-1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            loc = (b.close-b.low)/(b.high-b.low)
            rng = (b.high-b.low)/b.close
            rngrel = rng/rng.rolling(20).mean()
            alloc = b.postRebalance_current_allocation
            for i in range(0, n, 5):
                cell = b.iloc[i:i+5]
                idx = cell.index[cell.forecast<0]
                if len(idx)==0: continue
                j = idx[0]
                rec = dict(coin=c, w=w, f=b.forecast[j], ret5=ret5[j], ret60=ret60[j], ret20=ret20[j], ret10=ret10[j],
                           vol20=vol20[j], vrat=vol20[j]/vol60[j], loc=loc[j], r1=r1[j], rngrel=rngrel[j], alloc=alloc[j])
                for h in [1,2,3,5,10]:
                    rec[f"f{h}"] = cl[j+h]/cl[j]-1 if j+h<n else np.nan
                cs.append(rec)
    C = pd.DataFrame(cs)
    for h in [1,2,3,5,10]: C[f"s{h}"] = -C[f"f{h}"]
    def summ(g):
        x=g.s5.dropna()
        return pd.Series(dict(n=len(x), s1=g.s1.mean(), s2=g.s2.mean(), s3=g.s3.mean(), s5=x.mean(), t5=x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan, s10=g.s10.mean(), hit5=(x>0).mean()))
    out["all_cases"] = summ(C).round(4)
    out["by_window"] = C.groupby("w").apply(summ).round(4)
    out["by_coin"] = C.groupby("coin").apply(summ).round(4)
    for col in ["f","ret5","ret60","ret20","vol20","vrat","loc","r1","rngrel"]:
        q = pd.qcut(C[col], 4, labels=False, duplicates="drop")
        g = C.groupby(q).apply(summ)
        g["mid"] = C.groupby(q)[col].median()
        out[f"by_{col}_q"] = g.round(4)
    return out
