def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for coin in data["bars"]:
        for w, b in data["bars"][coin].items():
            b = b.copy()
            b["nret"] = b["close"].shift(-1)/b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gross"] = b["pos"]*b["nret"]
            b["fee"] = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["turn"] = (b["pos"]-b["previous_allocation"]).abs()
            b["ret"] = b["close"]/b["close"].shift(1)-1
            b["vol20"] = b["ret"].rolling(20).std()
            b["move"] = b["ret"]/b["vol20"].shift(1)
            fr = b.get("debug_info.components.fade.last_history_value")
            lr = b.get("debug_info.components.lowvol_move.last_history_value")
            b["ratio"] = (lr/fr) if fr is not None and lr is not None else np.nan
            b["coin"] = coin; b["w"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    cm = B.groupby("coin")["nret"].transform("mean")
    B["timing"] = B["pos"]*(B["nret"]-cm)
    B["beta"] = B["pos"]*cm
    out["overall"] = pd.Series({"gross_mean": B["gross"].mean(), "fee_mean": B["fee"].mean(),
        "timing": B["timing"].mean(), "beta": B["beta"].mean(), "mean_pos": B["pos"].mean(),
        "mean_abs_pos": B["pos"].abs().mean(), "turn_mean": B["turn"].mean(),
        "share_long": (B["pos"]>0).mean(), "coin_mean_ret": B["nret"].mean()})
    B["side"] = np.sign(B["pos"])
    out["by_side"] = B.groupby(["coin","side"]).agg(n=("gross","size"), gross=("gross","mean"), timing=("timing","mean"), nret=("nret","mean"))
    B["mq"] = pd.qcut(B["move"], 5, labels=False, duplicates="drop")
    out["by_move_q"] = B.groupby("mq").agg(n=("gross","size"), move=("move","mean"), nret=("nret","mean"), pos=("pos","mean"), gross=("gross","mean"), fee=("fee","mean"))
    out["ratio_desc"] = B["ratio"].describe()
    B["vq"] = B.groupby("coin")["sizing_realised_vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    g = B.groupby(["vq", np.sign(B["move"])])
    def tt(x):
        x = x.dropna(); return x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
    out["vol_x_movesign"] = g.agg(n=("nret","size"), nret=("nret","mean"), gross=("gross","mean"), pos=("pos","mean")).assign(t_nret=g["nret"].apply(tt))
    out["by_year"] = B.groupby("year").agg(gross=("gross","mean"), fee=("fee","mean"), beta=("beta","mean"), timing=("timing","mean"), nret=("nret","mean"), pos=("pos","mean"))
    D = pd.concat([d.assign(coin=c, w=w) for c in data["days"] for w, d in data["days"][c].items()])
    day = D.groupby(["w","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).dropna()
    out["days"] = pd.Series({"book_mean": day.br.mean(), "book_sh": day.br.mean()/day.br.std()*np.sqrt(365),
        "hold_mean": day.cr.mean(), "hold_sh": day.cr.mean()/day.cr.std()*np.sqrt(365), "n": len(day)})
    # deepest falls: chained book
    wins = sorted(day.index.get_level_values(0).unique(), key=lambda s:int(s[1:]))
    eq = (1+pd.concat([day.loc[w,"br"] for w in wins]).values).cumprod()
    dd = eq/np.maximum.accumulate(eq)-1
    out["maxdd"] = float(dd.min())
    out["by_window"] = day.groupby(level=0).agg(br=("br","mean"), cr=("cr","mean")).assign(diff=lambda x: x.br-x.cr).loc[wins]
    return out
