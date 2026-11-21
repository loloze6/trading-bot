def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 26
    cases = []
    barrows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; hi = b["high"]; lo = b["low"]
            ten = (hi.rolling(9).max() + lo.rolling(9).min()) / 2
            kij = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            sa = ((ten + kij) / 2).shift(26)
            sb = ((hi.rolling(52).max() + lo.rolling(52).min()) / 2).shift(26)
            low_edge = np.minimum(sa, sb); up_edge = np.maximum(sa, sb)
            dist = cl / low_edge - 1
            thick = (up_edge - low_edge) / cl
            r26 = cl / cl.shift(26) - 1
            sf = b["debug_info.components.slow_fall.last_history_value"]
            pp = b["debug_info.components.slow_fall.post_pipeline_value"]
            alloc = b["postRebalance_current_allocation"]
            g = cl.shift(-1) / cl - 1
            barrows.append(pd.DataFrame(dict(sf=sf, pp=pp, alloc=alloc, gain=alloc * g, reg=b["regime"])))
            for i in range(0, len(b) - H, H):
                if b.loc[i, "regime"] != "trending":
                    continue
                cases.append(dict(fwd=cl[i + H] / cl[i] - 1, sf=sf[i], pp=pp[i], alloc=alloc[i],
                                  dist=dist[i], thick=thick[i], r26=r26[i],
                                  year=pd.to_datetime(b.loc[i, "timestamp"]).year))
    C = pd.DataFrame(cases)
    B = pd.concat(barrows)
    A = B[B.reg == "trending"].dropna(subset=["sf", "pp"])
    out["corr_sf_pp_alloc"] = f"corr(sf,pp) {A.sf.corr(A.pp):.2f} corr(sf,alloc) {A.sf.corr(A.alloc):.2f} n {len(A)}"
    A["q"] = pd.qcut(A.sf, 4, labels=False)
    out["bars_by_sf_q"] = A.groupby("q").agg(n=("sf", "size"), pp=("pp", "mean"), alloc=("alloc", "mean"),
                                              gain_bps=("gain", lambda x: x.mean() * 1e4))
    Bh = B.dropna(subset=["gain"])
    out["gain_by_regime"] = Bh.groupby("reg").agg(n=("gain", "size"), alloc=("alloc", "mean"),
                                                   gain_bps=("gain", lambda x: x.mean() * 1e4))
    for col in ["dist", "thick", "pp"]:
        x = C.dropna(subset=[col])
        q = pd.qcut(x[col], 4, labels=False, duplicates="drop")
        gg = x.groupby(q)["fwd"].agg(["size", "mean", "median"])
        gg["lo"] = x.groupby(q)[col].min(); gg["hi"] = x.groupby(q)[col].max()
        out["fwd_by_" + col] = gg
    x = C.dropna(subset=["sf", "r26"])
    x["sfh"] = (x.sf > x.sf.median()).astype(int)
    x["r26h"] = (x.r26 > x.r26.median()).astype(int)
    out["fwd_sf_x_r26"] = x.groupby(["sfh", "r26h"])["fwd"].agg(["size", "mean", "median"])
    top = x[x.sfh == 1]; bot = x[x.sfh == 0]
    out["slow_minus_fast"] = f"{top.fwd.mean()-bot.fwd.mean():.4f} t {stats.ttest_ind(top.fwd, bot.fwd, equal_var=False).statistic:.2f}"
    x["sfq"] = pd.qcut(x.sf, 2, labels=False)
    out["fwd_sf_by_year"] = x.groupby(["year", "sfh"])["fwd"].agg(["size", "mean"]).unstack()
    return out
