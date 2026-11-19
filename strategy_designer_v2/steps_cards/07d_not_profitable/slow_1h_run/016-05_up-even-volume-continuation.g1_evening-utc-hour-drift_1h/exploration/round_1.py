def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t):
                d = t.copy(); d["coin"] = c; d["w"] = w; tr.append(d)
    tr = pd.concat(tr)
    tr["fee_cost"] = tr["profit_loss_percent"] - tr["net_profit_loss_percent"]
    out["trades_by_coin"] = tr.groupby("coin").agg(n=("side","size"),
        gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"),
        fee=("fee_cost","mean"), commission=("total_commission","mean"),
        dur=("duration_minutes","mean"))
    out["trades_all"] = pd.Series({"n":len(tr),"gross_mean":tr.profit_loss_percent.mean(),
        "net_mean":tr.net_profit_loss_percent.mean(),"fee_mean":tr.fee_cost.mean(),
        "gross_t":stats.ttest_1samp(tr.profit_loss_percent,0).statistic,
        "share_long":(tr.side=="LONG").mean()})
    # per-bar position gain, gross, on active bars; and the 20-22 return by vol quintile
    rows = []; blk = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            r1 = b.close.shift(-1)/b.close-1
            pos = b.postRebalance_current_allocation
            ts = pd.to_datetime(b.timestamp)
            rows.append(pd.DataFrame({"coin":c,"hour":ts.dt.hour,"gain":pos*r1,"pos":pos,"r1":r1,
                                      "turn":(b.postRebalance_current_allocation-b.previous_allocation).abs()}))
            # 20-22 block: from close of 19:00 bar to close of 21:00 bar
            i19 = np.where(ts.dt.hour==19)[0]
            i19 = i19[i19+2 < len(b)]
            ok = (ts.iloc[i19+2].values - ts.iloc[i19].values) == np.timedelta64(2,'h')
            i19 = i19[ok]
            ret = b.close.values[i19+2]/b.close.values[i19]-1
            r1h = np.log(b.close).diff()
            vol = r1h.rolling(168).std().values[i19]
            blk.append(pd.DataFrame({"coin":c,"ret":ret,"vol":vol,"pos":b.postRebalance_current_allocation.values[i19+1]}))
    R = pd.concat(rows).dropna()
    B = pd.concat(blk).dropna()
    out["gain_by_hour"] = R.groupby("hour").agg(gain=("gain","mean"),pos=("pos","mean"),
                                                r1=("r1","mean"),turn=("turn","mean"))
    B["q"] = B.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,5,labels=False))
    out["block_by_volq"] = B.groupby("q").agg(n=("ret","size"),ret=("ret","mean"),
        pos=("pos","mean"),t=("ret",lambda s: s.mean()/s.std()*np.sqrt(len(s))))
    out["block_by_coin"] = B.groupby("coin").agg(n=("ret","size"),ret=("ret","mean"),
        t=("ret",lambda s: s.mean()/s.std()*np.sqrt(len(s))),pos=("pos","mean"))
    D = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            D.append(d.assign(coin=c, w=w))
    D = pd.concat(D)
    out["daily"] = D.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    return out
