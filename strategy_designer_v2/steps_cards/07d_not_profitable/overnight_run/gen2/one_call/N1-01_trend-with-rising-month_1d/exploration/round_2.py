def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            cl = b.close
            b["ret"] = cl.pct_change()
            b["vol20"] = b["ret"].rolling(20, min_periods=10).std()
            b["mom20"] = cl.pct_change(20)
            b["mom60"] = cl.pct_change(60)
            b["fwd20"] = cl.shift(-20) / cl - 1
            # raw dist if available
            dcol = [x for x in b.columns if "dist" in x and "last_history" in x]
            b["dist"] = b[dcol[0]] if dcol else np.nan
            b["coin"] = c; b["win"] = w
            b["active"] = (b.forecast > 0).astype(int)
            b["flip"] = b["active"].diff().abs()
            rows.append(b[["coin","win","ts","close","forecast","ret","vol20","mom20","mom60","fwd20","dist","active","flip"]])
    B = pd.concat(rows, ignore_index=True)
    out["dist_cols_found"] = str([x for x in data["bars"]["BTCUSD"]["w1"].columns if "components" in x][:6])
    # trades joined with entry state
    tr = []
    for c, ws in data["trades"].items():
        for w, df in ws.items():
            if df is None or len(df) == 0: continue
            d = df.copy(); d["coin"] = c; d["win"] = w
            bb = B[(B.coin == c) & (B.win == w)].set_index("ts")
            et = pd.to_datetime(d.entry_time)
            idx = bb.index.get_indexer(et, method="pad")
            for k in ["vol20","mom20","mom60","dist"]:
                d[k] = np.where(idx >= 0, bb[k].values[np.clip(idx,0,None)], np.nan)
            d = d.sort_values("entry_time")
            gap = (pd.to_datetime(d.entry_time) - pd.to_datetime(d.exit_time).shift(1)).dt.total_seconds()/86400
            d["gap"] = gap.values
            tr.append(d)
    T = pd.concat(tr, ignore_index=True)
    T["vq"] = T.groupby("coin").vol20.transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    g = lambda x: x.agg(n=("profit_loss_percent","size"), gross=("profit_loss_percent","mean"),
                        med=("profit_loss_percent","median"), win=("profit_loss_percent", lambda s:(s>0).mean()))
    out["tr_by_entry_vol_q"] = g(T.groupby("vq"))
    out["tr_by_entry_mom20"] = g(T.groupby(pd.cut(T.mom20, [-1, 0.05, 0.15, 0.3, 0.6, 100])))
    out["tr_by_entry_mom60"] = g(T.groupby(pd.cut(T.mom60, [-1, -0.1, 0, 0.2, 0.5, 100])))
    out["tr_by_entry_dist"] = g(T.groupby(pd.cut(T.dist, [-1, 0.1, 0.3, 0.6, 1.0, 100])))
    out["tr_by_entry_forecast"] = g(T.groupby(pd.qcut(T.entry_forecast, 4, duplicates="drop")))
    out["tr_by_gap_since_last"] = g(T.groupby(pd.cut(T.gap, [-1, 2, 5, 15, 1e4])))
    out["active_share_flips"] = pd.Series({"active_share": B.active.mean(),
        "flips_per_100bars": B.flip.mean()*100})
    # non-overlapping fwd20 at active bars by mom60 sign and dist bins
    NO = B.groupby(["coin","win"], group_keys=False).apply(lambda d: d.iloc[::20])
    NO = NO[NO.fwd20.notna()].copy()
    NO["ex"] = NO.fwd20 - NO.groupby("coin").fwd20.transform("mean")
    A = NO[NO.active == 1]
    tt = lambda s: s.mean()/s.std()*np.sqrt(len(s)) if len(s)>2 else np.nan
    out["nonovl_active_by_mom60"] = A.groupby(pd.cut(A.mom60, [-1, 0, 0.3, 100])).ex.agg(["size","mean",tt])
    out["nonovl_active_by_dist"] = A.groupby(pd.cut(A.dist, [-1, 0.2, 0.5, 1.0, 100])).ex.agg(["size","mean",tt])
    out["nonovl_active_by_volq"] = A.groupby(A.groupby("coin").vol20.transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))).ex.agg(["size","mean",tt])
    out["nonovl_all_by_mom60_sign"] = NO.groupby([NO.active, NO.mom60 > 0]).ex.agg(["size","mean",tt])
    return out
