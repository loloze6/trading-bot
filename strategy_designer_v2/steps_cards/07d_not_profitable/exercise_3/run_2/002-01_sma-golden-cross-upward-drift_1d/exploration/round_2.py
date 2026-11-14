def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; blocks = []
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
            dd["coin"] = coin; dd["w"] = w
            # drawdown of book within window
            v = dd["book_value"]
            dd["dd"] = v / v.cummax() - 1
            rows.append(dd)
            cl = b["close"].values; fc = b["forecast"].values
            for i in range(0, len(b) - 10, 10):
                r10 = cl[i+10]/cl[i]-1
                past = cl[i]/cl[i-20]-1 if i >= 20 else np.nan
                past60 = cl[i]/cl[i-60]-1 if i >= 60 else np.nan
                blocks.append((coin, w, fc[i], r10, past, past60))
    D = pd.concat(rows).dropna(subset=["book_return"])
    tt = lambda x: x.mean()/x.std()*np.sqrt(len(x))
    L = D[D.alloc_prev > 0].copy()
    L["sgn"] = np.where(L.ret20_prev > 0, "past20 up", "past20 down")
    out["long days by past20 sign"] = L.groupby("sgn").agg(n=("book_return","size"), book=("book_return","mean"), coin=("coin_return","mean"), t_coin=("coin_return", tt), sd_book=("book_return","std"))
    F = D[(D.fc_prev == 0)].copy()
    F["sgn"] = np.where(F.ret20_prev > 0, "past20 up", "past20 down")
    out["flat days coin by past20 sign"] = F.groupby("sgn").agg(n=("coin_return","size"), coin=("coin_return","mean"), t=("coin_return", tt))
    # deep drawdown days (book dd < -20%) 
    deep = D[D.dd < -0.2]
    out["deep dd days profile"] = pd.Series({"n": len(deep), "share long": (deep.alloc_prev>0).mean(), "mean prior20": deep.ret20_prev.mean(), "share prior20<0": (deep.ret20_prev<0).mean(), "mean fc": deep.fc_prev.mean(), "all-days share prior20<0 when long": (L.ret20_prev<0).mean()})
    out["max dd by coin"] = D.groupby("coin").dd.min()
    # hypothetical: book returns only when past20 up (else 0) -> sharpe, mean, calmar-ish
    D["book_f"] = np.where(D.ret20_prev > 0, D.book_return, 0.0)
    res = {}
    for col in ["book_return", "book_f", "coin_return"]:
        x = D[col]
        res[col] = {"mean": x.mean(), "sharpe": x.mean()/x.std()*np.sqrt(365)}
    out["hypothetical filter"] = pd.DataFrame(res)
    B = pd.DataFrame(blocks, columns=["coin","w","fc","r10","past","past60"])
    B["r10x"] = B.r10 - B.groupby("coin").r10.transform("mean")
    act = B[B.fc > 0].dropna(subset=["past"])
    sl = np.polyfit(act.past.clip(-0.5,1), act.r10x, 1)
    from scipy import stats
    r = stats.linregress(act.past.clip(-0.5,1), act.r10x)
    out["active blocks: r10x on past20 (clipped)"] = pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(act)})
    allb = B.dropna(subset=["past"])
    r2 = stats.linregress(allb.past.clip(-0.5,1), allb.r10x)
    out["all blocks: r10x on past20"] = pd.Series({"slope": r2.slope, "t": r2.slope/r2.stderr, "n": len(allb)})
    fl = B[B.fc == 0].dropna(subset=["past"])
    r3 = stats.linregress(fl.past.clip(-0.5,1), fl.r10x)
    out["flat blocks: r10x on past20"] = pd.Series({"slope": r3.slope, "t": r3.slope/r3.stderr, "n": len(fl)})
    return out
