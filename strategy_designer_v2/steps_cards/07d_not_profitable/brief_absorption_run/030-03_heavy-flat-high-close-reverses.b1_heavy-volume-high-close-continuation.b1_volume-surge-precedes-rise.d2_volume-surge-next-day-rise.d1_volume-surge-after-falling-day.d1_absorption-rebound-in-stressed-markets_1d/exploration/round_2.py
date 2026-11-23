def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["w"] = w; b["coin"] = coin; b["wn"] = int(w[1:])
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["r3f"] = b["close"].shift(-3) / b["close"] - 1
            b["ret5"] = b["close"] / b["close"].shift(5) - 1
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            lr = np.log(b["close"]).diff()
            b["vr"] = lr.rolling(20).std() / lr.rolling(120, min_periods=40).std()
            b["dayret"] = b["close"] / b["close"].shift(1) - 1
            b["prevsig"] = (b["forecast"].shift(1) > 0)
            b["clv"] = (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            b["gain"] = b["postRebalance_current_allocation"] * b["r1"]
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["r1"].mean()
    B["ex"] = B["r1"] - B["coin"].map(mu)
    B["fpos"] = B["forecast"] > 0
    # episode in w16: locate deepest fall days
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["wn"] = int(w[1:]); d["coin"] = coin; D.append(d)
    D = pd.concat(D)
    P = D.groupby(["wn", "day"]).agg(br=("book_return", "mean")).dropna().sort_index()
    v = (1 + P["br"]).cumprod(); dd = v / v.cummax() - 1
    i_tr = int(np.argmin(dd.values)); i_pk = int(np.argmax(v.values[:i_tr + 1]))
    seg = P.iloc[i_pk:i_tr + 1]
    days = set(pd.to_datetime(seg.index.get_level_values(1)).floor("D"))
    E = B[(B["wn"] == 16) & (B["day"].isin(days))]
    out["episode per coin"] = E.groupby("coin").agg(n=("r1", "size"), sig=("fpos", "mean"), alloc=("postRebalance_current_allocation", "mean"), gain=("gain", "sum"), coinret=("dayret", lambda x: (1 + x).prod() - 1), vr=("vr", "mean"), ret20_start=("ret20", "first"))
    E2 = E.copy(); E2["k"] = np.arange(len(E2)) % 1
    out["episode signal state"] = E.groupby(["fpos", "prevsig"]).agg(n=("r1", "size"), r1=("r1", "mean"), gain=("gain", "sum"), alloc=("postRebalance_current_allocation", "mean"))
    S = B[B["fpos"]].dropna(subset=["ex"]).copy()
    # consecutive down days
    out["signal by prev signal"] = S.groupby("prevsig").agg(n=("ex", "size"), ex=("ex", "mean"), sd=("r1", "std"), worst=("r1", lambda x: x.quantile(0.05)), gain=("gain", "mean"))
    S5 = S.dropna(subset=["ret5"]).copy()
    S5["q"] = pd.qcut(S5["ret5"], 5, labels=False)
    out["signal by 5d return quintile"] = S5.groupby("q").agg(n=("ex", "size"), ret5=("ret5", "mean"), ex=("ex", "mean"), sd=("r1", "std"), q05=("r1", lambda x: x.quantile(0.05)), gain=("gain", "mean"))
    # condition alone: ret5 deep fall without signal (up days)
    NS = B[~B["fpos"]].dropna(subset=["ex", "ret5"]).copy()
    cuts = list(S5["ret5"].quantile([.2, .4, .6, .8]))
    NS["q"] = pd.cut(NS["ret5"], [-np.inf] + cuts + [np.inf], labels=False)
    out["nonsignal by same 5d bins"] = NS.groupby("q").agg(n=("ex", "size"), ex=("ex", "mean"))
    # close location of the down day
    Sc = S.dropna(subset=["clv"]).copy()
    Sc["q"] = pd.qcut(Sc["clv"], 3, labels=False)
    out["signal by close location tercile"] = Sc.groupby("q").agg(n=("ex", "size"), clv=("clv", "mean"), ex=("ex", "mean"), sd=("r1", "std"), q05=("r1", lambda x: x.quantile(0.05)), gain=("gain", "mean"))
    NC = B[(~B["fpos"]) & (B["dayret"] < 0)].dropna(subset=["clv", "ex"]).copy()
    NC["q"] = pd.cut(NC["clv"], [-np.inf] + list(Sc["clv"].quantile([1/3, 2/3])) + [np.inf], labels=False)
    out["down days without signal by clv"] = NC.groupby("q").agg(n=("ex", "size"), ex=("ex", "mean"))
    # 3 day horizon, non-overlapping grid approx
    out["signal 3d fwd by vr quartile"] = S.dropna(subset=["vr", "r3f"]).assign(q=lambda x: pd.qcut(x["vr"], 4, labels=False)).groupby("q").agg(n=("r3f", "size"), r3=("r3f", "mean"), r1=("r1", "mean"))
    # forecast tercile vs drawdown contributions: gain from top-capped forecast
    S["fq"] = pd.qcut(S["forecast"].rank(method="first"), 3, labels=False)
    out["signal by forecast tercile"] = S.groupby("fq").agg(n=("ex", "size"), f=("forecast", "mean"), ex=("ex", "mean"), sd=("r1", "std"), q05=("r1", lambda x: x.quantile(0.05)), alloc=("postRebalance_current_allocation", "mean"), gain=("gain", "mean"))
    return out
