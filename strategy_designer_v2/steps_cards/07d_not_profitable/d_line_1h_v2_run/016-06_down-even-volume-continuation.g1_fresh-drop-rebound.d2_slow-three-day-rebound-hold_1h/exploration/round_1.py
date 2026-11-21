def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns, pooled
    rows = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            d = d.copy(); d["coin"] = c; d["win"] = w
            rows.append(d[["coin","win","book_return","coin_return"]])
    D = pd.concat(rows)
    bw = D.groupby("win")[["book_return","coin_return"]].mean()
    bw["book_sh"] = D.groupby("win")["book_return"].apply(lambda x: x.mean()/x.std()*np.sqrt(365))
    out["by_window_mean_daily"] = bw.reindex(sorted(bw.index, key=lambda s:int(s[1:])))
    out["by_coin_mean_daily"] = D.groupby("coin")[["book_return","coin_return"]].mean()

    # grid analysis
    G = []; T = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            al = b["postRebalance_current_allocation"].fillna(0).values
            pnl = np.zeros(n); pnl[:-1] = al[:-1]*(cl[1:]/cl[:-1]-1)
            fee = (b["total_portfolio_value"]-b["postRebalance_total_value"]).clip(lower=0).values/b["total_portfolio_value"].values
            T.append(pd.DataFrame({"coin":c,"win":w,"gross":pnl.sum(),"fee":np.nansum(fee),"active":(np.abs(al)>0).mean()},index=[0]))
            s = pd.Series(cl)
            r72p = s/s.shift(72)-1; r24p = s/s.shift(24)-1; r720p = s/s.shift(720)-1
            lr = np.log(s).diff()
            vol24 = lr.rolling(24).std(); vol720 = lr.rolling(720).std()
            # jumpiness: max abs hourly ret over 24 / abs 24h ret
            mx24 = lr.abs().rolling(24).max()
            vr = b["volume"]/b["volume"].rolling(720,min_periods=100).mean()
            vr24 = vr.rolling(24).mean()
            f24 = s.shift(-24)/s-1; f72 = s.shift(-72)/s-1
            idx = np.arange(0, n, 72)
            g = pd.DataFrame({"coin":c,"win":w,"fc":b["forecast"].values[idx],"alloc":al[idx],
                              "r72p":r72p.values[idx],"r24p":r24p.values[idx],"r720p":r720p.values[idx],
                              "volratio":(vol24/vol720).values[idx],"jump":(mx24/(r24p.abs()+1e-9)).values[idx],
                              "vr24":vr24.values[idx],"f24":f24.values[idx],"f72":f72.values[idx]})
            G.append(g)
    T = pd.concat(T); G = pd.concat(G)
    out["fees_vs_gross_by_coin"] = T.groupby("coin")[["gross","fee","active"]].agg({"gross":"sum","fee":"sum","active":"mean"})
    G["m72"] = G.groupby("coin")["f72"].transform("mean")
    G["m24"] = G.groupby("coin")["f24"].transform("mean")
    G["ex72"] = G["f72"]-G["m72"]; G["ex24"] = G["f24"]-G["m24"]
    G["ex2472"] = G["ex72"]-G["ex24"]
    A = G[G.fc>0].dropna(subset=["ex72"])
    def summ(g):
        return pd.Series({"n":len(g),"ex72":g.ex72.mean(),"t72":stats.ttest_1samp(g.ex72,0).statistic if len(g)>2 else np.nan,
                          "ex24":g.ex24.mean(),"ex24_72":g.ex2472.mean(),"raw72":g.f72.mean()})
    A["fq"] = pd.qcut(A.fc, 4, labels=False, duplicates="drop")
    out["active_by_fc_quart"] = A.groupby("fq").apply(summ)
    A["trend30"] = pd.qcut(A.r720p, 4, labels=False)
    out["active_by_30d_trend_quart"] = A.groupby("trend30").apply(summ)
    A["volq"] = pd.qcut(A.volratio, 4, labels=False)
    out["active_by_vol24_over_vol30_quart"] = A.groupby("volq").apply(summ)
    A["jq"] = pd.qcut(A.jump, 4, labels=False)
    out["active_by_jumpiness_quart"] = A.groupby("jq").apply(summ)
    A["vq"] = pd.qcut(A.vr24, 4, labels=False)
    out["active_by_volume_ratio_quart"] = A.groupby("vq").apply(summ)
    A["d3"] = pd.qcut(A.r72p, 4, labels=False)
    out["active_by_3d_fall_quart(0=deepest)"] = A.groupby("d3").apply(summ)
    out["inactive_grid_mean_ex72"] = G[(G.fc<=0)].ex72.mean()
    return out
