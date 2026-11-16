def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily returns per coin/window, averaged across coins per day
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day","book_return","coin_return"]].copy()
            t["coin"] = c; t["win"] = w
            rows.append(t)
    D = pd.concat(rows)
    D["wn"] = D["win"].str[1:].astype(int)
    port = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    out["port_mean"] = port[["book_return","coin_return"]].agg(["mean","std","count"])
    # by window
    bw = port.groupby("wn").agg(book=("book_return","mean"), coin=("coin_return","mean"), n=("book_return","count"))
    out["by_window"] = bw
    # drawdown of chained book
    v = (1+port["book_return"].fillna(0)).cumprod().values
    peak = np.maximum.accumulate(v); dd = v/peak-1
    out["maxdd"] = float(dd.min())
    i = int(dd.argmin()); j = int(np.argmax(v[:i+1]))
    out["dd_peak_trough_windows"] = f"{port['wn'].iloc[j]} -> {port['wn'].iloc[i]}, days {i-j}"
    # bar-level: position, gain, forecast buckets, fees
    br = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            b["ret1"] = b["close"].shift(-1)/b["close"]-1
            b["gain"] = b["postRebalance_current_allocation"]*b["ret1"]
            b["fee"] = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["r20"] = b["close"]/b["close"].shift(20)-1
            hi = b["high"].rolling(20).max(); lo=b["low"].rolling(20).min()
            b["c5"] = b["close"].shift(-5)/b["close"]-1
            b["vol20"] = b["close"].pct_change().rolling(20).std()
            b["coin"]=c; b["win"]=w
            br.append(b[["coin","win","forecast","regime","postRebalance_current_allocation","ret1","gain","fee","r20","c5","vol20"]])
    B = pd.concat(br)
    out["gain_vs_fee_per_bar"] = pd.Series({"gain_mean": B["gain"].mean(), "fee_mean": B["fee"].mean(), "share_in": (B["postRebalance_current_allocation"].abs()>0.01).mean(), "mean_alloc_when_in": B.loc[B["postRebalance_current_allocation"].abs()>0.01,"postRebalance_current_allocation"].mean()})
    act = B[B["forecast"]>0].copy()
    act["fq"] = pd.qcut(act["forecast"], 5, labels=False, duplicates="drop")
    out["by_forecast_q"] = act.groupby("fq").agg(f=("forecast","mean"), alloc=("postRebalance_current_allocation","mean"), gain=("gain","mean"), ret1=("ret1","mean"), n=("gain","count"))
    # gain in state: r20 quintiles while active
    act["rq"] = pd.qcut(act["r20"], 5, labels=False)
    out["by_r20_q_active"] = act.groupby("rq").agg(r20=("r20","mean"), gain=("gain","mean"), ret1=("ret1","mean"), alloc=("postRebalance_current_allocation","mean"), n=("gain","count"))
    act["vq"] = pd.qcut(act["vol20"], 5, labels=False)
    out["by_vol_q_active"] = act.groupby("vq").agg(vol=("vol20","mean"), gain=("gain","mean"), ret1=("ret1","mean"), alloc=("postRebalance_current_allocation","mean"), n=("gain","count"))
    # coin mean daily return overall and beta part
    out["coin_mean_ret1_all"] = float(B["ret1"].mean())
    out["by_coin"] = B.groupby("coin").agg(gain=("gain","mean"), fee=("fee","mean"), ret1=("ret1","mean"), alloc=("postRebalance_current_allocation","mean"))
    return out
