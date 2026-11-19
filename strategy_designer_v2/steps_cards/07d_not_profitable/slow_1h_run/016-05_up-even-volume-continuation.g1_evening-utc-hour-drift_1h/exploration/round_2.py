def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []; blk = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b.timestamp)
            fee = (b.total_portfolio_value - b.postRebalance_total_value)/b.total_portfolio_value
            turn = (b.postRebalance_current_allocation - b.previous_allocation).abs()
            r1 = b.close.shift(-1)/b.close-1
            rows.append(pd.DataFrame({"fee":fee,"turn":turn,"gain":b.postRebalance_current_allocation*r1}))
            i19 = np.where(ts.dt.hour==19)[0]; i19 = i19[i19+2 < len(b)]
            ok = (ts.iloc[i19+2].values - ts.iloc[i19].values) == np.timedelta64(2,'h'); i19 = i19[ok]
            ret = b.close.values[i19+2]/b.close.values[i19]-1
            lr = np.log(b.close).diff()
            vol = lr.rolling(168).std().values[i19]
            vrel = (lr.rolling(168).std()/lr.rolling(168).std().rolling(720, min_periods=168).mean()).values[i19]
            blk.append(pd.DataFrame({"coin":c,"w":w,"year":ts.dt.year.values[i19],"ret":ret,"vol":vol,"vrel":vrel,
                                     "pos":b.postRebalance_current_allocation.values[i19+1]}))
    R = pd.concat(rows).dropna()
    act = R[R.turn>1e-4]
    out["fee_per_turnover"] = pd.Series({"fee_sum/turn_sum": act.fee.sum()/act.turn.sum(),
        "gain_sum": R.gain.sum(), "fee_sum": R.fee.sum(), "turn_per_trade_mean": act.turn.mean()})
    B = pd.concat(blk).dropna()
    B["d"] = B.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,10,labels=False))
    f = lambda s: s.mean()/s.std()*np.sqrt(len(s))
    out["block_by_voldecile"] = B.groupby("d").agg(n=("ret","size"),ret=("ret","mean"),t=("ret",f),
        pos=("pos","mean"),vol=("vol","mean"))
    B["rq"] = pd.qcut(B.vrel,5,labels=False)
    out["block_by_relvol_q"] = B.groupby("rq").agg(n=("ret","size"),ret=("ret","mean"),t=("ret",f),pos=("pos","mean"))
    out["block_by_year"] = B.groupby("year").agg(n=("ret","size"),ret=("ret","mean"),t=("ret",f))
    B["retvol"] = B.ret/B.vol
    out["ret_in_vol_units"] = B.groupby("d").agg(rv=("retvol","mean"),t=("retvol",f))
    return out
