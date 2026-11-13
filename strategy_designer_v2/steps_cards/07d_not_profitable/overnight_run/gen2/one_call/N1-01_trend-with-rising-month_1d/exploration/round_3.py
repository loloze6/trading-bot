def explore(data):
    import numpy as np, pandas as pd
    out = {}
    tt = lambda s: s.mean()/s.std()*np.sqrt(len(s)) if len(s)>2 else np.nan
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            cl = b.close
            b["ret"] = cl.pct_change()
            b["nret"] = b["ret"].shift(-1)
            b["vol20"] = b["ret"].rolling(20, min_periods=10).std()
            b["mom20"] = cl.pct_change(20); b["mom60"] = cl.pct_change(60)
            b["pos"] = b["postRebalance_current_allocation"].astype(float)
            bv = b["postRebalance_total_value"].astype(float)
            b["bret_next"] = bv.shift(-1)/bv - 1
            b["active"] = (b.forecast > 0).astype(int)
            b["run"] = (b.active.diff().fillna(0) != 0).cumsum()
            b["runlen"] = b.groupby("run").active.transform("size")
            b["fwd20"] = cl.shift(-20)/cl - 1
            b["coin"] = c; b["win"] = w
            rows.append(b[["coin","win","ret","nret","vol20","mom20","mom60","pos","bret_next","active","run","runlen","fwd20","forecast"]])
    B = pd.concat(rows, ignore_index=True)
    B["vq"] = B.groupby("coin").vol20.transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    A = B[B.active == 1].copy()
    # daily book return when active, by state
    out["active_day_book_by_mom60_vq"] = A.groupby([A.mom60 > 0, "vq"]).bret_next.agg(["size","mean","std"])
    # drawdown share: loss days when active, coin down big
    A["cdn"] = pd.cut(A.nret, [-1, -0.08, -0.03, 0, 0.03, 0.08, 10])
    out["active_book_by_next_coin_ret"] = A.groupby("cdn", observed=True).bret_next.agg(["size","mean","sum"])
    # active spells by length: sum of book return
    S = A.groupby(["coin","win","run"]).agg(L=("active","size"), br=("bret_next", lambda s: (1+s.fillna(0)).prod()-1),
                                            m60=("mom60","first"), vq=("vq","first"))
    out["spells_by_len"] = S.groupby(pd.cut(S.L, [0,3,7,20,60,1e4])).br.agg(["size","mean","sum"])
    out["spells_by_entry_mom60"] = S.groupby(pd.cut(S.m60, [-1,0,0.3,100])).br.agg(["size","mean","median",lambda s:(s>0).mean()])
    out["spells_by_entry_vq"] = S.groupby("vq").br.agg(["size","mean","median",lambda s:(s>0).mean()])
    # Calmar proxy if only mom60>0 active days
    def calmar(r):
        r = r.fillna(0); v = (1+r).cumprod(); dd = (v/v.cummax()-1).min(); return r.mean()*365, dd
    res = {}
    for name, mask in {"all": B.active==1, "mom60pos": (B.active==1)&(B.mom60>0),
                       "lowmidvol": (B.active==1)&(B.vq<2)}.items():
        ms, dds = [], []
        for (c,w), g in B.groupby(["coin","win"]):
            r = g.bret_next.where(mask.loc[g.index], 0)
            m, d = calmar(r); ms.append(m); dds.append(d)
        res[name] = {"ann_mean": np.mean(ms), "mean_window_dd": np.mean(dds), "worst_dd": np.min(dds)}
    out["filter_proxy"] = pd.DataFrame(res).T
    # nonoverlapping fwd20 by mom60 sign x vol tercile, active
    NO = B.groupby(["coin","win"], group_keys=False).apply(lambda d: d.iloc[::20])
    NO = NO[NO.fwd20.notna()].copy()
    NO["ex"] = NO.fwd20 - NO.groupby("coin").fwd20.transform("mean")
    NA = NO[NO.active==1]
    out["nonovl_active_mom60_vq"] = NA.groupby([NA.mom60>0, "vq"]).ex.agg(["size","mean",tt])
    return out
