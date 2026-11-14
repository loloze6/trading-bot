def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    blocks = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            b = data["bars"][coin][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            bl = b.groupby("day").last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day")
            dd["alloc_prev"] = bl["postRebalance_current_allocation"].reindex(dd.index).shift(1)
            dd["fc_prev"] = bl["forecast"].reindex(dd.index).shift(1)
            c = bl["close"].reindex(dd.index)
            dd["ret20_prev"] = (c / c.shift(20) - 1).shift(1)
            dd["spread_prev"] = bl["debug_info.components.sma_cross.last_history_value"].reindex(dd.index).shift(1)
            dd["coin"] = coin; dd["w"] = w
            rows.append(dd)
            # blocks of 10 bars
            cl = b["close"].values; fc = b["forecast"].values
            sp = b["debug_info.components.sma_cross.last_history_value"].values if "debug_info.components.sma_cross.last_history_value" in b else np.full(len(b), np.nan)
            for i in range(0, len(b) - 10, 10):
                r10 = cl[i+10]/cl[i]-1
                past = cl[i]/cl[i-20]-1 if i >= 20 else np.nan
                blocks.append((coin, w, fc[i], sp[i], r10, past))
    D = pd.concat(rows)
    D = D.dropna(subset=["book_return"])
    out["book vs coin daily mean/std"] = pd.DataFrame({
        "book": [D.book_return.mean(), D.book_return.std()],
        "coin": [D.coin_return.mean(), D.coin_return.std()]}, index=["mean", "std"])
    D["fcb"] = pd.cut(D.fc_prev, [-0.1, 0.001, 5, 10, 15, 20.1])
    out["daily by forecast bucket"] = D.groupby("fcb", observed=True).agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"), alloc=("alloc_prev", "mean"))
    D["spb"] = pd.qcut(D.spread_prev, 5, duplicates="drop")
    out["daily by raw spread quintile"] = D.groupby("spb", observed=True).agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"), alloc=("alloc_prev", "mean"))
    D["pastb"] = pd.qcut(D.ret20_prev, 5, duplicates="drop")
    long = D[D.alloc_prev > 0]
    out["long days by prior 20d return quintile"] = long.groupby("pastb", observed=True).agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"), t=("coin_return", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    out["by coin"] = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), sb=("book_return", lambda x: x.mean()/x.std()*np.sqrt(365)), sc=("coin_return", lambda x: x.mean()/x.std()*np.sqrt(365)), longshare=("alloc_prev", lambda x: (x > 0).mean()))
    out["by window"] = D.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    # worst book days
    W = D.nsmallest(100, "book_return")
    out["worst 100 book days"] = pd.Series({"mean book": W.book_return.mean(), "mean alloc": W.alloc_prev.mean(), "mean fc": W.fc_prev.mean(), "mean prior20": W.ret20_prev.mean(), "all-long prior20": long.ret20_prev.mean(), "share fc>15": (W.fc_prev > 15).mean(), "all long share fc>15": (long.fc_prev > 15).mean()})
    B = pd.DataFrame(blocks, columns=["coin", "w", "fc", "sp", "r10", "past"])
    B["r10x"] = B.r10 - B.groupby("coin").r10.transform("mean")
    act = B[B.fc > 0].copy()
    act["spq"] = pd.qcut(act.sp, 4, duplicates="drop")
    out["blocks active by raw spread quartile"] = act.groupby("spq", observed=True).r10x.agg(["size", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    act["pq"] = pd.qcut(act.past, 4, duplicates="drop")
    out["blocks active by past20 quartile"] = act.groupby("pq", observed=True).r10x.agg(["size", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["blocks flat"] = B[B.fc == 0].r10x.agg(["size", "mean"])
    return out
