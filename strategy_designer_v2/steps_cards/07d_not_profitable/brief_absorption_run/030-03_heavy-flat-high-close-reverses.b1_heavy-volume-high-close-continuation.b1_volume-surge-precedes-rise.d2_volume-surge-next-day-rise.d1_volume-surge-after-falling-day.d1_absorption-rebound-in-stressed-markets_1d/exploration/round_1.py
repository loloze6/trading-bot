def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["w"] = w; b["coin"] = coin
            b["wn"] = int(w[1:])
            b["pos"] = np.arange(len(b))
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            lr = np.log(b["close"]).diff()
            b["vr"] = lr.rolling(20).std() / lr.rolling(120, min_periods=40).std()
            b["dayret"] = b["close"] / b["close"].shift(1) - 1
            b["gain"] = b["postRebalance_current_allocation"] * b["r1"]
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["r1"].mean()
    B["ex"] = B["r1"] - B["coin"].map(mu)
    B["held"] = B["postRebalance_current_allocation"].abs() > 1e-6
    B["fpos"] = B["forecast"] > 0
    out["state counts"] = B.groupby(["fpos", "held"]).agg(n=("r1", "size"), alloc=("postRebalance_current_allocation", "mean"), ex=("ex", "mean"), gain=("gain", "mean"))
    # book daily
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["w"] = w; d["wn"] = int(w[1:]); d["coin"] = coin; D.append(d)
    D = pd.concat(D)
    P = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna().sort_index()
    v = (1 + P["br"]).cumprod()
    dd = v / v.cummax() - 1
    P["dd"] = dd.values
    out["maxdd"] = float(dd.min())
    # drawdown by window: min dd and window return
    out["by window"] = P.groupby(level=0).agg(book=("br", lambda x: (1 + x).prod() - 1), coin=("cr", lambda x: (1 + x).prod() - 1), mindd=("dd", "min"))
    # deepest episode: from peak to trough
    i_tr = int(np.argmin(dd.values))
    i_pk = int(np.argmax(v.values[:i_tr + 1]))
    seg = P.iloc[i_pk:i_tr + 1]
    out["episode"] = pd.Series({"start_window": seg.index[0][0], "end_window": seg.index[-1][0], "days": len(seg), "book": float((1 + seg["br"]).prod() - 1), "coins": float((1 + seg["cr"]).prod() - 1)})
    # conditional analysis on signal cases
    S = B[B["fpos"]].dropna(subset=["ex", "ret20", "vr"]).copy()
    S["r20q"] = pd.qcut(S["ret20"], 4, labels=False)
    S["vrq"] = pd.qcut(S["vr"], 4, labels=False)
    out["signal by ret20 quartile"] = S.groupby("r20q").agg(n=("ex", "size"), ex=("ex", "mean"), r1=("r1", "mean"), gain=("gain", "mean"), sd=("r1", "std"), ret20=("ret20", "mean"))
    out["signal by volratio quartile"] = S.groupby("vrq").agg(n=("ex", "size"), ex=("ex", "mean"), gain=("gain", "mean"), sd=("r1", "std"), vr=("vr", "mean"))
    NS = B[~B["fpos"]].dropna(subset=["ex", "ret20"]).copy()
    NS["r20q"] = pd.cut(NS["ret20"], [-np.inf] + list(S["ret20"].quantile([.25, .5, .75])) + [np.inf], labels=False)
    out["nonsignal by ret20 quartile"] = NS.groupby("r20q").agg(n=("ex", "size"), ex=("ex", "mean"), held=("held", "mean"), gain=("gain", "mean"))
    # gain by year from held days
    B["year"] = pd.to_datetime(B["timestamp"]).dt.year
    out["gain by fpos/held"] = B.groupby(["fpos", "held"])["gain"].sum()
    out["forecast desc on held"] = B.loc[B["held"], "forecast"].describe()
    return out
