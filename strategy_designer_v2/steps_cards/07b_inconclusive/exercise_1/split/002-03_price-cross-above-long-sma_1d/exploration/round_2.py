def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        mu = pd.concat([df["close"].pct_change().dropna() for df in wins.values()]).mean()
        for w, df in wins.items():
            d = df[["timestamp","close","forecast","postRebalance_current_allocation"]].copy().reset_index(drop=True)
            d["fwd"] = d["close"].shift(-20)/d["close"] - 1
            d["exc"] = d["fwd"] - 20*mu
            d["coin"] = coin; d["win"] = w
            d["year"] = pd.to_datetime(d["timestamp"]).dt.year
            d["i"] = np.arange(len(d))
            d["dist"] = df["debug_info.components.above_ma.last_history_value"].values
            on = (d["forecast"]>0).astype(int)
            grp = (on.diff().fillna(0)!=0).cumsum()
            d["age"] = on.groupby(grp).cumcount()
            d["age"] = np.where(on==1, d["age"], -1)
            d["past20"] = d["close"]/d["close"].shift(20)-1
            d["dist_chg"] = d["dist"]-d["dist"].shift(10)
            rows.append(d)
    a = pd.concat(rows).dropna(subset=["fwd"])
    a["alloc"] = a["postRebalance_current_allocation"]
    a["contrib"] = a["alloc"]*a["exc"]
    a["blk"] = a["i"]//20
    def t(x):
        x = x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std(ddof=1)*np.sqrt(len(x)) if len(x)>1 else np.nan,"median":x.median(),"hit":(x>0).mean()})
    out = {}
    on = a[a["forecast"]>0].copy()
    on["age_b"] = pd.cut(on["age"],[-1,10,30,60,120,10000])
    out["on_by_age_since_cross"] = on.groupby("age_b")["exc"].apply(t).unstack()
    # BTC-based market regime: BTC dist>0 at same timestamp
    btc = a[a["coin"]=="BTCUSD"][["timestamp","dist","fwd"]].rename(columns={"dist":"btc_dist","fwd":"btc_fwd"})
    m = on.merge(btc, on="timestamp", how="left")
    m["btc_up"] = m["btc_dist"]>0
    out["on_by_btc_above_sma"] = m.groupby("btc_up")["exc"].apply(t).unstack()
    m["rel"] = m["fwd"]-m["btc_fwd"]
    out["on_alts_minus_btc_fwd"] = t(m[m["coin"]!="BTCUSD"]["rel"]).to_frame().T
    out["on_by_dist_rising"] = on.groupby(on["dist_chg"]>0)["exc"].apply(t).unstack()
    out["on_by_past20_sign"] = on.groupby(on["past20"]>0)["exc"].apply(t).unstack()
    blocks = a.groupby(["coin","win","blk"]).agg(c=("contrib","sum"),alloc=("alloc","mean")).reset_index()
    nb = blocks[blocks["alloc"]!=0]["c"]
    lo, hi = nb.quantile([.01,.99])
    out["block_t_winsor1pct"] = t(nb.clip(lo,hi)).to_frame().T
    out["block_t_drop_top5"] = t(nb.sort_values().iloc[:-5]).to_frame().T
    out["block_t_excl_ZEC"] = t(blocks[(blocks["alloc"]!=0)&(blocks["coin"]!="ZECUSD")]["c"]).to_frame().T
    # top forecast only, fresh vs old
    top = on[on["forecast"]>=15]
    out["top_fc_by_age"] = top.groupby(pd.cut(top["age"],[-1,30,120,10000]))["exc"].apply(t).unstack()
    return out
