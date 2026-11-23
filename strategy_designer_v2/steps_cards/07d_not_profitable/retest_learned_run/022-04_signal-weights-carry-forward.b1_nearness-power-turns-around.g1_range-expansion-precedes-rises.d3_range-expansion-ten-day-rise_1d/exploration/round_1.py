def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    # book daily returns: per window, per day mean across coins
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    P = D.groupby(["wn","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).reset_index().sort_values(["wn","day"])
    P = P.dropna(subset=["br"])
    P["v"] = (1+P["br"]).cumprod()
    P["peak"] = P["v"].cummax(); P["dd"] = P["v"]/P["peak"]-1
    P["hv"] = (1+P["cr"].fillna(0)).cumprod(); P["hdd"] = P["hv"]/P["hv"].cummax()-1
    out["book max dd"] = float(P["dd"].min()); out["hold max dd"] = float(P["hdd"].min())
    # per window: book return, hold return, min dd within window chain
    pw = P.groupby("wn").agg(book=("br", lambda x: (1+x).prod()-1), hold=("cr", lambda x: (1+x.fillna(0)).prod()-1), mindd=("dd","min"), n=("br","size"))
    out["per window"] = pw.round(3)
    # bar-level features
    B = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            b["coin"]=c; b["wn"]=int(w[1:])
            b["ret20"] = b["close"]/b["close"].shift(20)-1
            rng = (b["high"]-b["low"])/b["close"]
            b["rr"] = rng / rng.rolling(30).mean()
            b["clv"] = (b["close"]-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)  # close location
            b["dayret"] = b["close"]/b["close"].shift(1)-1
            b["vol30"] = b["dayret"].rolling(30).std()
            b["vol90"] = b["dayret"].rolling(90).std()
            b["f10"] = b["close"].shift(-10)/b["close"]-1
            b["pos"] = np.arange(len(b))
            b["gain"] = b["postRebalance_current_allocation"]*(b["close"].shift(-1)/b["close"]-1)
            b["ma100"] = b["close"]/b["close"].rolling(100,min_periods=50).mean()-1
            B.append(b)
    B = pd.concat(B, ignore_index=True)
    mu = B.groupby("coin").apply(lambda g: g[g["pos"]%10==0]["f10"].mean())
    B["x10"] = B["f10"] - B["coin"].map(mu)
    G = B[(B["pos"]%10==0)].dropna(subset=["x10"])
    act = G[G["forecast"]>0]
    def summ(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    # in-regime cases split by close location (down-closing wide bar vs up)
    act = act.copy()
    act["rrq"] = pd.qcut(act["rr"], 3, labels=["lo","mid","hi"])
    act["clvb"] = np.where(act["clv"]<0.5,"close low","close high")
    out["active: rr tercile x close loc, x10"] = act.groupby(["rrq","clvb"])["x10"].apply(summ).unstack().round(4)
    act["r20q"] = pd.qcut(act["ret20"], 3, labels=["weak","mid","strong"])
    out["active: ret20 tercile x rr tercile, x10"] = act.groupby(["r20q","rrq"])["x10"].apply(summ).unstack().round(4)
    act["vq"] = pd.qcut(act["vol30"]/act["vol90"], 3, labels=["volfall","volmid","volrise"])
    out["active: vol30/vol90 tercile, x10"] = act.groupby("vq")["x10"].apply(summ).unstack().round(4)
    act["mab"] = np.where(act["ma100"]>0,"above ma100","below ma100")
    out["active: ma100 side, x10"] = act.groupby("mab")["x10"].apply(summ).unstack().round(4)
    # book gain per coin
    out["gain by coin (mean daily pos gain)"] = B.groupby("coin")["gain"].mean().round(5)
    # deepest drawdown periods: top 3 episodes, window range
    P["inDD"] = P["dd"]<-0.15
    P["ep"] = (P["dd"]==0).cumsum()
    ep = P.groupby("ep").agg(mindd=("dd","min"), w0=("wn","min"), w1=("wn","max"), n=("dd","size"), holdret=("cr", lambda x:(1+x.fillna(0)).prod()-1), bookret=("br",lambda x:(1+x).prod()-1)).sort_values("mindd").head(5)
    out["deepest episodes"] = ep.round(3)
    return out
