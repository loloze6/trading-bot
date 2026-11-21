def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 26
    cases = []
    barrows = []
    col_sf = "debug_info.components.slow_fall.last_history_value"
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
            r7 = cl / cl.shift(7) - 1
            sf = b[col_sf] if col_sf in b.columns else pd.Series(np.nan, index=b.index)
            alloc = b["postRebalance_current_allocation"]
            g = cl.shift(-1) / cl - 1
            barrows.append(pd.DataFrame(dict(alloc=alloc, gain=alloc * g, reg=b["regime"], r26=r26, dist=dist)))
            for i in range(0, len(b) - H, H):
                if b.loc[i, "regime"] != "trending":
                    continue
                cases.append(dict(fwd=cl[i + H] / cl[i] - 1, sf=sf[i], dist=dist[i], thick=thick[i],
                                  r26=r26[i], r7=r7[i]))
    C = pd.DataFrame(cases)
    B = pd.concat(barrows).dropna(subset=["gain"])
    out["gain_by_regime"] = B.groupby("reg").agg(n=("gain", "size"), alloc=("alloc", "mean"),
                                                  gain_bps=("gain", lambda x: x.mean() * 1e4))
    S = B[B.alloc < 0].dropna(subset=["r26"])
    q = pd.qcut(S.r26, 4, labels=False)
    gg = S.groupby(q).agg(n=("gain", "size"), gain_bps=("gain", lambda x: x.mean() * 1e4))
    gg["lo"] = S.groupby(q).r26.min(); gg["hi"] = S.groupby(q).r26.max()
    out["short_bar_gain_by_r26"] = gg
    for col in ["dist", "thick", "r7"]:
        x = C.dropna(subset=[col])
        qq = pd.qcut(x[col], 4, labels=False, duplicates="drop")
        t = x.groupby(qq)["fwd"].agg(["size", "mean", "median"])
        t["lo"] = x.groupby(qq)[col].min(); t["hi"] = x.groupby(qq)[col].max()
        out["fwd_by_" + col] = t
    x = C.dropna(subset=["sf", "r26"]).copy()
    x["sfh"] = (x.sf > x.sf.median()).astype(int)
    x["r26h"] = (x.r26 > x.r26.median()).astype(int)
    out["fwd_sf_x_r26"] = x.groupby(["sfh", "r26h"])["fwd"].agg(["size", "mean", "median"])
    out["corr_sf_r26"] = float(x.sf.corr(x.r26))
    top = x[x.sfh == 1]; bot = x[x.sfh == 0]
    out["slow_minus_fast_raw"] = f"{top.fwd.mean()-bot.fwd.mean():.4f} t {stats.ttest_ind(top.fwd, bot.fwd, equal_var=False).statistic:.2f} n {len(top)}/{len(bot)}"
    y = C.dropna(subset=["dist", "r26"]).copy()
    y["deep"] = (y.dist < y.dist.median()).astype(int)
    y["r26h"] = (y.r26 > y.r26.median()).astype(int)
    out["fwd_dist_x_r26"] = y.groupby(["deep", "r26h"])["fwd"].agg(["size", "mean", "median"])
    return out
