def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    # book by coin
    rows = []
    for c in bars:
        d = pd.concat([days[c][w].assign(w=w) for w in days[c]])
        br = d["book_return"].dropna(); cr = d["coin_return"].dropna()
        tr = pd.concat([trades[c][w] for w in trades[c] if len(trades[c][w])]) if any(len(trades[c][w]) for w in trades[c]) else pd.DataFrame()
        rows.append(dict(coin=c, book_mean_bps=br.mean()*1e4, book_sharpe=br.mean()/br.std()*np.sqrt(365),
                         coin_mean_bps=cr.mean()*1e4, n_trades=len(tr),
                         trade_gross=tr["profit_loss_percent"].mean() if len(tr) else np.nan,
                         trade_net=tr["net_profit_loss_percent"].mean() if len(tr) else np.nan))
    out["by_coin"] = pd.DataFrame(rows)
    # market part vs timing
    mk = []; tot = []
    for c in bars:
        allc = pd.concat([bars[c][w]["close"].pct_change() for w in bars[c]]).mean()
        for w in bars[c]:
            b = bars[c][w]
            pos = b["postRebalance_current_allocation"].fillna(0)
            g = pos * (b["close"].shift(-1)/b["close"]-1)
            mk.append((pos*allc).sum()); tot.append(g.sum())
    out["gross_sum_total_vs_market"] = pd.Series({"total": np.sum(tot), "market_part": np.sum(mk)})
    # cases recomputed: every 120-bar grid cell, first bar meeting the condition
    recs = []
    for c in bars:
        fw = []
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True); cl = b["close"]
            r24 = cl/cl.shift(24)-1
            mab = r24.abs().rolling(720, min_periods=300).mean()
            surge = r24/mab
            p7 = cl.shift(24)/cl.shift(192)-1
            vol = cl.pct_change().rolling(720, min_periods=300).std()*np.sqrt(168)
            p7s = p7/vol
            r30 = cl/cl.shift(720)-1
            fwd = cl.shift(-120)/cl-1
            fwd24 = cl.shift(-24)/cl-1
            for g0 in range(0, len(b), 120):
                fw.append(fwd.iloc[g0] if g0 < len(b) else np.nan)
                seg = range(g0, min(g0+120, len(b)))
                cond = (surge.iloc[list(seg)] >= 3) & (p7.iloc[list(seg)] < 0)
                if cond.any():
                    i = cond.idxmax()
                    recs.append(dict(coin=c, w=w, surge=surge[i], p7s=p7s[i], p7=p7[i], r30=r30[i], fwd=fwd[i], fwd24=fwd24[i], r24=r24[i]))
        drift = np.nanmean(fw)
        for r in recs:
            if r["coin"] == c: r["drift"] = drift
    df = pd.DataFrame(recs).dropna(subset=["fwd"])
    df["unus"] = df["fwd"] - df["drift"]
    def summ(g):
        x = g["fwd"]; u = g["unus"]
        return pd.Series(dict(n=len(g), fwd_mean_pct=x.mean()*100, unus_mean_pct=u.mean()*100,
                              t_unus=u.mean()/(u.std()/np.sqrt(len(g))) if len(g)>2 else np.nan, fwd24_pct=g["fwd24"].mean()*100))
    out["all_cases"] = summ(df)
    df["p7q"] = pd.qcut(df["p7s"], 4, labels=["deepest","q2","q3","shallow"])
    out["by_fall_depth"] = df.groupby("p7q").apply(summ)
    df["sq"] = pd.qcut(df["surge"], 3, labels=["small","mid","big"])
    out["by_surge"] = df.groupby("sq").apply(summ)
    df["r30s"] = np.sign(df["r30"])
    out["by_30d_sign"] = df.groupby("r30s").apply(summ)
    df["r30q"] = pd.qcut(df["r30"], 4, labels=["r30_low","q2","q3","r30_high"])
    out["by_30d_q"] = df.groupby("r30q").apply(summ)
    out["by_coin_cases"] = df.groupby("coin").apply(summ)
    df["yr"] = None
    return out
