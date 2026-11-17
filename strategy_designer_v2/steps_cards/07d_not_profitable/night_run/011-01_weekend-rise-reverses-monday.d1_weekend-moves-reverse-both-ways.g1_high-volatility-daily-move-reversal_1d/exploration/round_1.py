def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns, holding daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    bk = D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    def sharpe(x): return x.mean()/x.std()*np.sqrt(365)
    out["book_vs_hold"] = pd.DataFrame({"mean":[bk.book_return.mean(), bk.coin_return.mean()],
        "sharpe":[sharpe(bk.book_return), sharpe(bk.coin_return)]}, index=["book","hold"])
    # per window
    wk = bk.groupby(level=0).agg(book=("book_return","sum"), hold=("coin_return","sum"), n=("book_return","size"))
    wk["idx"] = wk.index.str[1:].astype(int)
    out["by_window_summed"] = wk.sort_values("idx").drop(columns="idx").round(4)
    # per bar analysis
    br = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["r1"] = b.close.shift(-1)/b.close - 1
            b["r0"] = b.close/b.close.shift(1) - 1
            vol = b.r0.rolling(20).std()
            b["z"] = b.r0/vol
            b["r5p"] = b.close/b.close.shift(5)-1
            b["r20p"] = b.close/b.close.shift(20)-1
            b["coin"]=c; b["w"]=w
            b["dow"]=pd.to_datetime(b.timestamp).dt.dayofweek
            br.append(b)
    B = pd.concat(br, ignore_index=True)
    cm = B.groupby("coin").r0.mean()
    B["mu"] = B.coin.map(cm)
    a = B.postRebalance_current_allocation
    B["g"] = a*B.r1
    B["mkt"] = a*B.mu
    B["timing"] = a*(B.r1-B.mu)
    B["fee"] = (B.total_portfolio_value - B.postRebalance_total_value)/B.total_portfolio_value
    out["regime_share_gain"] = B.groupby("regime").agg(n=("g","size"), gain=("g","mean"), mkt=("mkt","mean"),
        timing=("timing","mean"), fee=("fee","mean"), absalloc=("postRebalance_current_allocation", lambda x: x.abs().mean()))
    out["overall_gain_parts"] = pd.Series({"gain":B.g.mean(),"mkt":B.mkt.mean(),"timing":B.timing.mean(),"fee":B.fee.mean(),
        "mean_alloc":a.mean()})
    act = B[B.regime=="mean_reversion"].copy()
    act["side"] = np.sign(act.postRebalance_current_allocation)
    out["by_side"] = act.groupby("side").agg(n=("g","size"), gain=("g","mean"), timing=("timing","mean"), r1=("r1","mean"))
    act["zq"] = pd.qcut(act.z, 6, duplicates="drop")
    out["by_zbucket"] = act.groupby("zq").agg(n=("g","size"), r1_minus_mu=("timing", "size"), next=("r1","mean"), gain=("g","mean"), alloc=("postRebalance_current_allocation","mean"))
    act["r20q"] = pd.qcut(act.r20p, 5)
    out["by_r20_trend"] = act.groupby("r20q").agg(n=("g","size"), gain=("g","mean"), timing=("timing","mean"), alloc=("postRebalance_current_allocation","mean"), next=("r1","mean"))
    out["by_coin"] = act.groupby("coin").agg(gain=("g","mean"), timing=("timing","mean"), fee=("fee","mean"))
    out["by_dow"] = act.groupby("dow").agg(n=("g","size"), gain=("g","mean"), timing=("timing","mean"))
    return out
