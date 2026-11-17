def explore(data):
    import pandas as pd, numpy as np
    days = data["days"]; bars = data["bars"]
    out = {}
    rows = []
    for c in days:
        for w, d in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            last = b.groupby("day").last()
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.merge(last[["postRebalance_current_allocation", "forecast"]].shift(1).rename(
                columns={"postRebalance_current_allocation": "pos", "forecast": "fc"}), left_on="day", right_index=True, how="left")
            cl = dd["close"]
            dd["r90"] = cl / cl.shift(90) - 1
            dd["r60"] = cl / cl.shift(60) - 1
            dd["r30"] = cl / cl.shift(30) - 1
            dd["vol20"] = dd["coin_return"].rolling(20).std()
            dd["coin"] = c; dd["wn"] = int(w[1:])
            rows.append(dd)
    D = pd.concat(rows).dropna(subset=["book_return"])
    D["pos"] = D["pos"].fillna(0)
    mu = D["coin_return"].mean()
    out["coin_mean_daily"] = float(mu)
    D["mkt_part"] = D["pos"] * mu
    out["book_mean"] = float(D["book_return"].mean())
    out["market_part"] = float(D["mkt_part"].mean())
    out["by_coin_side"] = D.groupby(["coin", np.sign(D["pos"])])["book_return"].agg(["mean", "std", "count"]).round(5)
    def stats(col):
        P = D.groupby(["wn", "day"])[col].mean().reset_index().sort_values(["wn", "day"])
        r = P[col]
        eq = (1 + r).cumprod(); mdd = float((eq / eq.cummax() - 1).min())
        yr = float(eq.iloc[-1] ** (365 / len(r)) - 1)
        return {"sharpe": round(float(r.mean() / r.std() * np.sqrt(365)), 3), "yearly": round(yr, 3), "maxdd": round(mdd, 3), "calmar": round(yr / -mdd, 3)}
    # counterfactuals
    D["long_only"] = np.where(D["pos"] > 0, D["book_return"], 0.0)
    D["short_only"] = np.where(D["pos"] < 0, D["book_return"], 0.0)
    # shorts only when coin's own 90d return negative
    D["short_if_r90neg"] = np.where(D["pos"] > 0, D["book_return"], np.where((D["pos"] < 0) & (D["r90"] < 0), D["book_return"], 0.0))
    D["long_if_r90pos_short_if_neg"] = np.where(((D["pos"] > 0) & (D["r90"] > 0)) | ((D["pos"] < 0) & (D["r90"] < 0)), D["book_return"], 0.0)
    D["hold"] = D["coin_return"]
    out["cf"] = pd.DataFrame({k: stats(k) for k in ["book_return", "long_only", "short_only", "short_if_r90neg", "long_if_r90pos_short_if_neg", "hold"]}).T
    # side by r90 sign and by r90 tercile
    g = D.dropna(subset=["r90"]).copy()
    g["side"] = np.sign(g["pos"])
    g["r90_up"] = g["r90"] > 0
    out["side_by_r90sign"] = g.groupby(["side", "r90_up"])["book_return"].agg(["mean", "std", "count"]).round(5)
    g["r90_q"] = pd.qcut(g["r90"], 5, labels=False)
    out["side_by_r90q"] = g.groupby(["side", "r90_q"])["book_return"].agg(["mean", "count"]).round(5)
    # deepest fall episodes of the book chain: share of losses from long vs short
    P = D.groupby(["wn", "day"]).agg(br=("book_return", "mean")).reset_index().sort_values(["wn", "day"])
    L = D.assign(lc=np.where(D["pos"] > 0, D["book_return"], 0) / 2, sc=np.where(D["pos"] < 0, D["book_return"], 0) / 2)
    LS = L.groupby(["wn", "day"])[["lc", "sc"]].sum().reset_index().sort_values(["wn", "day"])
    P = P.merge(LS, on=["wn", "day"])
    eq = (1 + P["br"]).cumprod(); peak = eq.cummax()
    P["dd"] = eq / peak - 1
    i_min = int(P["dd"].values.argmin()); i_pk = int((eq.iloc[:i_min + 1]).values.argmax())
    seg = P.iloc[i_pk + 1:i_min + 1]
    out["deepest_fall"] = {"windows": f"w{seg.wn.min()}-w{seg.wn.max()}", "days": len(seg), "sum_long": round(float(seg.lc.sum()), 4), "sum_short": round(float(seg.sc.sum()), 4)}
    return out
