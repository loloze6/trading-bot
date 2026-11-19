def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    grid = []; flips = []; seg = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            fc = b["forecast"].fillna(0).values
            raw = b["debug_info.components.grind.last_history_value"].values
            on = fc > 0
            # spells of being on
            ch = np.diff(on.astype(int))
            nstart = (ch == 1).sum()
            spells = []
            cnt = 0
            for v in on:
                if v: cnt += 1
                elif cnt: spells.append(cnt); cnt = 0
            if cnt: spells.append(cnt)
            flips.append((c, w, nstart, np.mean(spells) if spells else np.nan, on.mean(),
                          np.mean(np.abs(np.diff(fc)))))
            hr = pd.Series(cl).pct_change().values
            lr = np.log(pd.Series(cl)).diff().values
            for i in range(72, n-72, 72):
                past = cl[i]/cl[i-72]-1; fwd = cl[i+72]/cl[i]-1
                past1 = cl[i]/cl[i-24]-1
                # fraction of past 72h with positive hourly return
                h = hr[i-71:i+1]
                pos_frac = (h > 0).mean()
                # efficiency: net log move / sum abs
                eff = lr[i-71:i+1].sum()/np.abs(lr[i-71:i+1]).sum()
                past7 = cl[i]/cl[max(i-168,0)]-1
                grid.append((c, w, past, fwd, raw[i], fc[i], pos_frac, eff, past7))
    F = pd.DataFrame(flips, columns=["coin","w","starts","mean_spell_h","share_on","mean_abs_dfc"])
    out["spells"] = F[["starts","mean_spell_h","share_on","mean_abs_dfc"]].describe().loc[["mean","50%"]]
    G = pd.DataFrame(grid, columns=["coin","w","past","fwd","raw","fc","posfrac","eff","past7"])
    G["ex"] = G["fwd"] - G["coin"].map(G.groupby("coin")["fwd"].mean())
    def tt(x): return x.mean()/x.std()*np.sqrt(len(x))
    up = G[G["past"]>0].copy()
    # regress ex on past and raw
    import numpy.linalg as la
    res = {}
    for cols in [["past"], ["raw"], ["past","raw"], ["eff"], ["past","eff"], ["posfrac"]]:
        d = up.dropna(subset=cols+["ex"])
        X = np.column_stack([np.ones(len(d))]+[d[k].values for k in cols]); y = d["ex"].values
        bta, *_ = la.lstsq(X, y, rcond=None); e = y - X@bta
        s2 = e@e/(len(y)-X.shape[1]); se = np.sqrt(np.diag(s2*la.inv(X.T@X)))
        res["+".join(cols)] = {"n": len(d), **{f"t_{k}": bta[j+1]/se[j+1] for j, k in enumerate(cols)}}
    out["up_regs"] = pd.DataFrame(res).T
    # all bars: eff (signed) quintiles
    G["eq"] = pd.qcut(G["eff"], 5, labels=False)
    out["all_by_eff_q"] = G.groupby("eq").agg(n=("ex","size"), eff=("eff","mean"), past=("past","mean"), ex=("ex","mean"), t=("ex", tt))
    G["p7"] = pd.qcut(G["past7"], 5, labels=False)
    out["all_by_7d_q"] = G.groupby("p7").agg(n=("ex","size"), past7=("past7","mean"), ex=("ex","mean"), t=("ex", tt))
    # forecast on grid vs ex among up
    up["fq"] = pd.qcut(up["fc"].rank(method="first"), 4, labels=False)
    out["up_by_fc_q"] = up.groupby("fq").agg(n=("ex","size"), fc=("fc","mean"), raw=("raw","mean"), past=("past","mean"), ex=("ex","mean"), t=("ex", tt))
    # daily book: worst days share
    D = pd.concat([d.assign(coin=c, w=w) for c, ws in data["days"].items() for w, d in ws.items()])
    book = D.groupby(["w","day"])["book_return"].mean().dropna()
    out["book_daily_dist"] = pd.Series({"mean": book.mean(), "share_pos": (book>0).mean(), "sum_worst5pct": book[book<book.quantile(0.05)].sum(), "sum_all": book.sum()})
    return out
