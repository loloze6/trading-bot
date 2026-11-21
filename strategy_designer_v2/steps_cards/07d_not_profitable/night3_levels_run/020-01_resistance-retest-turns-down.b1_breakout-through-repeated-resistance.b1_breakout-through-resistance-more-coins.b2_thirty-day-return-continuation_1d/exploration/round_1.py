def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    # book daily returns: mean over coins per day, per window
    recs = []
    for c, ws in days.items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["win"] = w
            recs.append(dd)
    D = pd.concat(recs)
    D["wn"] = D["win"].str[1:].astype(int)
    g = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("coin", "count")).reset_index()
    g = g.dropna(subset=["book"]).sort_values(["wn", "day"]).reset_index(drop=True)
    eq = (1 + g["book"]).cumprod()
    peak = eq.cummax(); ddn = eq / peak - 1
    g["dd"] = ddn.values
    trough = ddn.idxmin()
    pk = eq[:trough + 1].idxmax()
    span = g.loc[pk:trough]
    out = {}
    out["deepest fall"] = pd.Series({"depth": ddn.min(), "days": trough - pk, "start_win": g.loc[pk, "wn"], "end_win": g.loc[trough, "wn"],
                                     "book_sum": span["book"].sum(), "coin_sum": span["coin"].sum()})
    # per window
    pw = g.groupby("wn").apply(lambda x: pd.Series({
        "book_chain": (1 + x["book"]).prod() - 1, "coin_chain": (1 + x["coin"]).prod() - 1,
        "book_maxdd": ((1 + x["book"]).cumprod() / (1 + x["book"]).cumprod().cummax() - 1).min(),
        "ncoins": x["n"].mean()}))
    out["per window"] = pw
    # bar level gains
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.copy()
            cl = b["close"]
            r1 = cl.shift(-1) / cl - 1
            a = b["postRebalance_current_allocation"]
            ret30 = cl / cl.shift(30) - 1
            vol = cl.pct_change().rolling(30).std()
            ret10p = cl / cl.shift(10) - 1
            x = pd.DataFrame({"gain": a * r1, "a": a, "f": b["forecast"], "r1": r1, "ret30": ret30, "vol": vol,
                              "ret10p": ret10p, "wn": int(w[1:]), "coin": c})
            rows.append(x)
    B = pd.concat(rows).dropna(subset=["gain"])
    B["side"] = np.sign(B["a"])
    out["by side"] = B.groupby("side")["gain"].agg(["count", "mean", "sum", "std"])
    B["fq"] = pd.qcut(B["f"], 5, labels=False, duplicates="drop")
    out["by forecast quintile"] = B.groupby("fq").agg(f=("f", "mean"), a=("a", "mean"), gain=("gain", "mean"), r1=("r1", "mean"), n=("gain", "count"))
    B["vq"] = B.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["by side x vol tercile"] = B.groupby(["side", "vq"]).agg(gain=("gain", "mean"), r1=("r1", "mean"), absa=("a", lambda s: s.abs().mean()), n=("gain", "count"))
    # in the deepest fall: which windows, held what
    wins = set(span["wn"])
    S = B[B["wn"].isin(wins)]
    out["in fall windows by side"] = S.groupby("side").agg(gain=("gain", "sum"), r1=("r1", "mean"), n=("gain", "count"))
    # conflict: 30d long signal but last 10d falling
    B["rev"] = np.sign(B["ret10p"]) != np.sign(B["ret30"])
    out["by side x 10d disagrees"] = B.groupby(["side", "rev"]).agg(gain=("gain", "mean"), r1=("r1", "mean"), n=("gain", "count"))
    # worst 20 book days: composition
    worst = g.nsmallest(30, "book")
    out["worst30 days"] = pd.Series({"mean_book": worst["book"].mean(), "mean_coin": worst["coin"].mean(),
                                    "share coin down": (worst["coin"] < 0).mean(), "share coin up": (worst["coin"] > 0).mean()})
    return out
