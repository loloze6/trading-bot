def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    coin = list(data["bars"].keys())[0]
    B = data["bars"][coin]; D = data["days"][coin]
    rows = []; drows = []
    for w in sorted(B.keys(), key=lambda s: int(s[1:])):
        b = B[w].copy().reset_index(drop=True)
        c = b["close"]
        b["w"] = w
        b["r1"] = c.shift(-1)/c - 1
        b["ret"] = c.pct_change()
        b["vol30"] = b["ret"].rolling(30).std()
        b["vol5"] = b["ret"].rolling(5).std()
        b["vr"] = b["vol5"]/b["vol30"]
        b["z"] = b["ret"]/b["vol30"]
        b["r60"] = c/c.shift(60) - 1
        b["r20"] = c/c.shift(20) - 1
        b["pos"] = b["postRebalance_current_allocation"]
        b["gain"] = b["pos"]*b["r1"]
        b["fee"] = b["total_portfolio_value"] - b["postRebalance_total_value"]
        b["feefrac"] = b["fee"]/b["total_portfolio_value"]
        b["turn"] = (b["pos"]-b["previous_allocation"]).abs()
        b["year"] = pd.to_datetime(b["timestamp"]).dt.year
        rows.append(b)
        d = D[w].copy(); d["w"] = w; drows.append(d)
    A = pd.concat(rows, ignore_index=True)
    Dd = pd.concat(drows, ignore_index=True).dropna(subset=["book_return"])
    out = {}
    # drawdown chain
    v = (1+Dd["book_return"]).cumprod().values
    peak = np.maximum.accumulate(v); dd = v/peak-1
    Dd["dd"] = dd
    # find top episodes
    eps = []; i = 0; n = len(dd)
    while i < n:
        if dd[i] < 0:
            j = i
            while j < n and dd[j] < 0: j += 1
            k = i + np.argmin(dd[i:j])
            eps.append((dd[k], i, k, j, Dd["w"].iloc[i], Dd["w"].iloc[k], k-i))
            i = j
        else: i += 1
    E = pd.DataFrame(eps, columns=["depth","start","trough","end","w_start","w_trough","days_to_trough"]).sort_values("depth").head(6)
    out["deepest falls"] = E[["depth","w_start","w_trough","days_to_trough"]]
    out["max dd"] = float(dd.min())
    # per window
    out["per window"] = Dd.groupby("w").agg(book=("book_return","mean"), coin=("coin_return","mean"), sd=("book_return","std"), n=("book_return","size"), mindd=("dd","min"))
    # side
    A2 = A.dropna(subset=["r1"])
    A2["side"] = np.sign(A2["pos"])
    out["by side"] = A2.groupby("side").agg(n=("gain","size"), mean_gain=("gain","mean"), sd=("gain","std"), mean_r1=("r1","mean"), abspos=("pos", lambda x: x.abs().mean()))
    out["fees"] = pd.Series({"mean feefrac/bar": A2["feefrac"].mean(), "mean gain/bar": A2["gain"].mean(), "mean turnover": A2["turn"].mean(), "mean abs pos": A2["pos"].abs().mean()})
    # quantile groupings (gain per bar)
    for col in ["vr","z","r60","r20","vol30"]:
        q = pd.qcut(A2[col], 5, duplicates="drop")
        g = A2.groupby(q).agg(n=("gain","size"), gain=("gain","mean"), sd=("gain","std"), fee=("feefrac","mean"), abspos=("pos", lambda x: x.abs().mean()))
        g["t"] = g["gain"]/(g["sd"]/np.sqrt(g["n"]))
        g.index = g.index.astype(str)
        out["by "+col] = g
    # absz quintile
    q = pd.qcut(A2["z"].abs(), 5)
    g = A2.groupby(q).agg(n=("gain","size"), gain=("gain","mean"), sd=("gain","std"), fee=("feefrac","mean"))
    g.index = g.index.astype(str); out["by |z|"] = g
    # trend-alignment: fading against 60d trend vs with
    A2["fade_vs_trend"] = np.sign(A2["pos"])*np.sign(A2["r60"])
    g = A2.groupby("fade_vs_trend").agg(n=("gain","size"), gain=("gain","mean"), sd=("gain","std"))
    out["pos sign x r60 sign"] = g
    out["by year"] = A2.groupby("year").agg(n=("gain","size"), gain=("gain","mean"), sd=("gain","std"), fee=("feefrac","mean"))
    return out
