def explore(data):
    import pandas as pd, numpy as np
    days = data["days"]; bars = data["bars"]
    out = {}
    # portfolio daily returns: mean over coins per day, per window
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
            dd["r30"] = cl / cl.shift(30) - 1
            dd["r7"] = cl / cl.shift(7) - 1
            dd["vol20"] = dd["coin_return"].rolling(20).std()
            dd["peak_dd"] = cl / cl.rolling(60, min_periods=1).max() - 1
            dd["coin"] = c; dd["window"] = w; dd["wn"] = int(w[1:])
            rows.append(dd)
    D = pd.concat(rows)
    P = D.groupby(["wn", "day"])["book_return"].mean().dropna().reset_index().sort_values(["wn", "day"])
    eq = (1 + P["book_return"]).cumprod()
    dd = eq / eq.cummax() - 1
    P["dd"] = dd.values
    P["year"] = pd.to_datetime(P["day"]).dt.year
    out["max_dd"] = float(dd.min())
    out["yearly_ret"] = float(eq.iloc[-1] ** (365 / len(P)) - 1)
    out["per_window"] = P.groupby("wn").agg(sum_ret=("book_return", "sum"), min_dd=("dd", "min"), n=("book_return", "size")).round(4)
    # worst window-level drawdowns per coin
    D["eqc"] = D.groupby(["coin", "wn"])["book_return"].transform(lambda s: (1 + s.fillna(0)).cumprod())
    D["ddc"] = D["eqc"] / D.groupby(["coin", "wn"])["eqc"].cummax() - 1
    # losing days decomposition by state
    D["side"] = np.sign(D["pos"]).map({1: "long", -1: "short", 0: "flat"})
    D["r7_q"] = pd.qcut(D["r7"], 5, labels=False)
    D["vol_q"] = pd.qcut(D["vol20"], 4, labels=False)
    g = D.dropna(subset=["book_return", "side"])
    out["by_side"] = g.groupby("side")["book_return"].agg(["mean", "std", "count"]).round(5)
    out["by_side_r7q"] = g.groupby(["side", "r7_q"])["book_return"].agg(["mean", "count"]).round(5)
    out["by_side_volq"] = g.groupby(["side", "vol_q"])["book_return"].agg(["mean", "std", "count"]).round(5)
    # days in bottom 5% of book returns: state
    thr = g["book_return"].quantile(0.05)
    worst = g[g["book_return"] <= thr]
    out["worst_days_state"] = worst.groupby("side").agg(n=("book_return", "size"), mean_ret=("book_return", "mean"),
        mean_r7=("r7", "mean"), mean_r30=("r30", "mean"), mean_pos=("pos", "mean"), coin_ret=("coin_return", "mean")).round(4)
    out["all_days_state"] = g.groupby("side").agg(mean_r7=("r7", "mean"), mean_r30=("r30", "mean"), mean_pos=("pos", "mean"), absfc=("fc", lambda s: s.abs().mean())).round(4)
    # mismatch: position sign vs r7 sign
    g2 = g.dropna(subset=["r7"]).copy()
    g2["agree"] = np.sign(g2["pos"]) == np.sign(g2["r7"])
    out["by_agree_r7"] = g2.groupby(["side", "agree"])["book_return"].agg(["mean", "std", "count"]).round(5)
    return out
