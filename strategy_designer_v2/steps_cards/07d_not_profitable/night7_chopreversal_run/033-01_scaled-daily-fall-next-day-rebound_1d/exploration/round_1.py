def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    days_rows = []
    for coin, wins in data["bars"].items():
        # coin-wide median of 30d swing (descriptive)
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            b["ret"] = r
            b["nxt"] = c.shift(-1) / c - 1
            b["sd30"] = r.rolling(30, min_periods=20).std()
            b["z"] = r / b["sd30"].shift(0)
            b["tr60"] = c / c.shift(60) - 1
            b["ret5"] = c / c.shift(5) - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["coin"] = coin; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b[["coin","win","year","ret","nxt","sd30","z","tr60","ret5","forecast","pos"]])
        for w, d in data["days"][coin].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=coin; dd["win"]=w
            days_rows.append(dd)
    B = pd.concat(rows, ignore_index=True)
    drift = B.groupby("coin")["nxt"].mean()
    B["drift"] = B["coin"].map(drift)
    B["ex"] = B["nxt"] - B["drift"]
    med = B.groupby("coin")["sd30"].median()
    B["agit"] = np.where(B["sd30"] > B["coin"].map(med), "agit", "calm")
    B["trend"] = pd.cut(B["tr60"], [-np.inf,-0.10,0.10,np.inf], labels=["fall","chop","rise"])
    B["sig"] = B["forecast"] > 0
    B["gain"] = B["pos"] * B["nxt"]
    def st(x):
        x = x.dropna(); n=len(x)
        return pd.Series({"n":n,"mean%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    S = B[B.sig]
    out["sig by z bucket (ex next day)"] = S.groupby(pd.cut(S["z"],[-np.inf,-3,-2,-1.5,-1,-0.5,0]))["ex"].apply(st).unstack()
    out["sig by trend"] = S.groupby("trend")["ex"].apply(st).unstack()
    out["nosig by trend"] = B[~B.sig].groupby("trend")["ex"].apply(st).unstack()
    out["sig by agit"] = S.groupby("agit")["ex"].apply(st).unstack()
    out["nosig by agit"] = B[~B.sig].groupby("agit")["ex"].apply(st).unstack()
    out["sig by trend x agit"] = S.groupby(["trend","agit"])["ex"].apply(st).unstack()
    out["nosig by trend x agit"] = B[~B.sig].groupby(["trend","agit"])["ex"].apply(st).unstack()
    out["book gain by trend x agit (pos*nxt, %sum, n held)"] = B[B.pos.abs()>0].groupby(["trend","agit"]).agg(sum_pct=("gain",lambda x:x.sum()*100), mean_pct=("gain",lambda x:x.mean()*100), n=("gain","size"), meanpos=("pos","mean"))
    out["held when no signal: share of held bars"] = float(((B.pos.abs()>0)&(~B.sig)).sum()/(B.pos.abs()>0).sum())
    out["held no-signal gain mean%"] = float(B[(B.pos.abs()>0)&(~B.sig)]["gain"].mean()*100)
    out["held signal gain mean%"] = float(B[(B.pos.abs()>0)&(B.sig)]["gain"].mean()*100)
    out["pos by z bucket"] = S.groupby(pd.cut(S["z"],[-np.inf,-3,-2,-1.5,-1,-0.5,0]))["pos"].mean()
    out["sig by ret5 (prior 5d) bucket"] = S.groupby(pd.cut(S["ret5"],[-np.inf,-0.15,-0.05,0,0.05,np.inf]))["ex"].apply(st).unstack()
    # book daily, drawdowns
    D = pd.concat(days_rows, ignore_index=True)
    bk = D.groupby(["win","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).reset_index()
    bk["wn"] = bk["win"].str[1:].astype(int)
    bk = bk.sort_values(["wn","day"]).dropna(subset=["br"])
    eq = (1+bk["br"]).cumprod(); dd = eq/eq.cummax()-1
    bk["dd"]=dd.values
    out["deepest dd"] = float(dd.min())
    out["per window: book sum%, coin sum%, min dd in window"] = bk.groupby("win").agg(book=("br",lambda x:x.sum()*100), coin=("cr",lambda x:x.sum()*100), mindd=("dd","min"), wn=("wn","first")).sort_values("wn")
    return out
