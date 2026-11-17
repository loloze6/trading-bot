def explore(data):
    import pandas as pd, numpy as np
    out = {}
    coins = list(data["days"].keys())
    # build per-day table with position from bars
    rows = []
    for c in coins:
        for w, d in data["days"][c].items():
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            last = b.groupby("day").last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"])
            dd = dd.set_index("day")
            dd["pos_prev"] = last["postRebalance_current_allocation"].shift(1).reindex(dd.index)
            dd["fc_prev"] = last["forecast"].shift(1).reindex(dd.index)
            dd["reg_prev"] = last["regime"].shift(1).reindex(dd.index)
            cl = dd["close"]
            dd["ret30_prev"] = (cl / cl.shift(30) - 1).shift(1)
            dd["ret7_prev"] = (cl / cl.shift(7) - 1).shift(1)
            r = dd["coin_return"]
            dd["vol30_prev"] = r.rolling(30).std().shift(1)
            dd["coin"] = c; dd["window"] = w
            rows.append(dd.reset_index())
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    # book combined
    B = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index().sort_values(["wn", "day"])
    B = B.dropna()
    def stats(x):
        eq = (1 + x).cumprod(); dd_ = eq / eq.cummax() - 1
        yr = eq.iloc[-1] ** (365 / len(x)) - 1
        return pd.Series({"mean": x.mean(), "sharpe": x.mean() / x.std() * np.sqrt(365), "yearly": yr, "maxdd": dd_.min(), "calmar": yr / -dd_.min()})
    out["book_vs_hold"] = pd.DataFrame({"book": stats(B["book"]), "hold": stats(B["hold"])})
    # drawdown episodes of book
    eq = (1 + B["book"]).cumprod().values
    peak = np.maximum.accumulate(eq); ddv = eq / peak - 1
    B["dd"] = ddv
    # identify episode: from peak to trough
    trough = int(np.argmin(ddv)); pk = int(np.argmax(eq[:trough + 1]))
    seg = B.iloc[pk + 1:trough + 1]
    out["deepest_dd"] = pd.Series({"depth": ddv[trough], "days": len(seg), "windows": str(sorted(seg["wn"].unique())), "book_sum": seg["book"].sum(), "hold_sum": seg["hold"].sum()})
    segD = D.merge(seg[["wn", "day"]], on=["wn", "day"])
    out["deepest_dd_by_coin"] = segD.groupby("coin").agg(n=("book_return", "size"), book_sum=("book_return", "sum"), coin_sum=("coin_return", "sum"), mean_pos=("pos_prev", "mean"), share_long=("pos_prev", lambda s: (s > 0).mean()), share_short=("pos_prev", lambda s: (s < 0).mean()))
    # book return by position side
    D["side"] = np.sign(D["pos_prev"]).map({1: "long", -1: "short", 0: "flat"})
    out["by_side"] = D.groupby(["coin", "side"]).agg(n=("book_return", "size"), mean_book=("book_return", "mean"), mean_coin=("coin_return", "mean"), sum_book=("book_return", "sum"))
    # by year
    D["year"] = D["day"].dt.year
    out["by_year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), share_long=("pos_prev", lambda s: (s > 0).mean()), share_short=("pos_prev", lambda s: (s < 0).mean()))
    # worst 5% days of book per coin: what context
    D["bad"] = D["book_return"] <= D.groupby("coin")["book_return"].transform(lambda s: s.quantile(0.05))
    out["bad_days_context"] = D.groupby("bad").agg(n=("book_return", "size"), side_long=("pos_prev", lambda s: (s > 0).mean()), side_short=("pos_prev", lambda s: (s < 0).mean()), abs_pos=("pos_prev", lambda s: s.abs().mean()), ret30=("ret30_prev", "mean"), ret7=("ret7_prev", "mean"), vol30=("vol30_prev", "mean"), coin_ret=("coin_return", "mean"))
    # short side book by prior 30d return tercile
    S = D[D["pos_prev"] < 0].dropna(subset=["ret30_prev"])
    S["t"] = pd.qcut(S["ret30_prev"], 3, labels=["low", "mid", "high"])
    out["short_by_ret30"] = S.groupby("t").agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    L = D[D["pos_prev"] > 0].dropna(subset=["ret30_prev"])
    L["t"] = pd.qcut(L["ret30_prev"], 3, labels=["low", "mid", "high"])
    out["long_by_ret30"] = L.groupby("t").agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["coins"] = str(coins)
    return out
