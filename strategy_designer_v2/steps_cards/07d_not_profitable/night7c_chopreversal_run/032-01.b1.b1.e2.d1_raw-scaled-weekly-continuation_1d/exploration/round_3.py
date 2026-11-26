def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"].astype(float)
            b["r1"] = cl.shift(-1)/cl - 1
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            b["gain"] = b["alloc"]*b["r1"]
            b["fwd7"] = cl.shift(-7)/cl - 1
            b["fwd14"] = cl.shift(-14)/cl - 1
            b["ret7"] = cl/cl.shift(7) - 1
            b["ret30"] = cl/cl.shift(30) - 1
            d = cl.diff().abs()
            b["er"] = (cl - cl.shift(30)).abs()/d.rolling(30).sum()
            lr = np.log(cl).diff()
            b["vol30"] = lr.rolling(30).std()
            b["scaled"] = b["ret7"]/(b["vol30"]*np.sqrt(7))
            b["grid"] = (np.arange(len(b)) % 7 == 0)
            b["grid14"] = (np.arange(len(b)) % 14 == 0)
            b["coin"] = c; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    drift = B[B.grid].groupby("coin")["fwd7"].mean()
    drift14 = B[B.grid14].groupby("coin")["fwd14"].mean()
    B["ex7"] = B["fwd7"] - B["coin"].map(drift)
    B["ex14"] = B["fwd14"] - B["coin"].map(drift14)
    def agg(g, col="ex7"):
        x = g[col].dropna(); n=len(x); s=x.std()
        return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(s/np.sqrt(n)) if n>2 and s>0 else np.nan})
    out = {}
    R = B[B.grid & (B["er"]<=0.3) & B["scaled"].notna() & B["ret30"].notna() & B["fwd7"].notna()].copy()
    R["s7"]=np.sign(R["scaled"]); R["s30"]=np.sign(R["ret30"])
    R["agree"]=(R.s7==R.s30).astype(int)
    # condition alone: follow 30d sign, in regime, split by agree
    R["d30"]=R.s30*R.ex7
    out["follow30_inreg_by_agree"]=R.groupby("agree").apply(lambda g: agg(g.assign(ex7=g.d30)))
    out["follow30_inreg_all"]=agg(R.assign(ex7=R.d30))
    # signal: follow 7d sign, by agree and |scaled| quartile (graded?)
    R["d7"]=R.s7*R.ex7
    R["sq"]=pd.qcut(R["scaled"].abs(),3,labels=False,duplicates="drop")
    out["follow7_by_agree_sq"]=R.groupby(["agree","sq"]).apply(lambda g: agg(g.assign(ex7=g.d7)))
    out["follow7_agree_by_side"]=R[R.agree==1].groupby("s7").apply(lambda g: agg(g.assign(ex7=g.d7)))
    out["follow7_agree_by_year"]=R[R.agree==1].groupby("year").apply(lambda g: agg(g.assign(ex7=g.d7)))
    # graded strength by scaled * agree: product
    # 14-day horizon on agree cases
    R14 = B[B.grid14 & (B["er"]<=0.3) & B["scaled"].notna() & B["ret30"].notna() & B["fwd14"].notna()].copy()
    R14["agree"]=(np.sign(R14.scaled)==np.sign(R14.ret30)).astype(int)
    R14["d"]=np.sign(R14.scaled)*R14.ex14
    out["follow7_14d_by_agree"]=R14.groupby("agree").apply(lambda g: agg(g.assign(ex7=g.d)))
    # book bar gain split by agreement of position with 30d return, in held bars
    H=B[B.alloc!=0].copy()
    H["agreepos"]=(np.sign(H.alloc)==np.sign(H.ret30)).astype(int)
    H["side"]=np.where(H.alloc>0,"long","short")
    out["book_gain_by_agreepos_side"]=H.groupby(["agreepos","side"])["gain"].agg(["count","mean","std"])
    return out
