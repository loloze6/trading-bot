def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    wins = sorted(data["days"][coins[0]].keys(), key=lambda w: int(w[1:]))
    # book daily
    bk = []
    for w in wins:
        frames = []
        for c in coins:
            if w in data["days"][c]:
                d = data["days"][c][w][["day","book_return","coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        f = pd.concat(frames)
        g = f.groupby("day")[["book_return","coin_return"]].mean().reset_index()
        g["w"] = w
        bk.append(g)
    bk = pd.concat(bk, ignore_index=True)
    bk = bk.dropna(subset=["book_return"])
    v = (1+bk["book_return"]).cumprod()
    dd = v/v.cummax()-1
    bk["dd"] = dd.values
    # deepest fall episode
    trough = dd.idxmin()
    peak = v.loc[:trough].idxmax()
    out["deepest_fall"] = pd.Series({"depth": dd.min(), "days": trough-peak,
        "window_peak": bk.loc[peak,"w"], "window_trough": bk.loc[trough,"w"],
        "coin_ret_during": (1+bk.loc[peak+1:trough,"coin_return"]).prod()-1,
        "book_ret_during": (1+bk.loc[peak+1:trough,"book_return"]).prod()-1})
    pw = bk.groupby("w").agg(book_mean=("book_return","mean"), coin_mean=("coin_return","mean"),
                             book_sum=("book_return","sum"), coin_sum=("coin_return","sum"), mindd=("dd","min"))
    out["per_window"] = pw
    # bar-level
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            r = b["close"].pct_change()
            b["r1"] = r
            b["nxt"] = b["close"].shift(-1)/b["close"]-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["nxt"]
            b["sma50"] = b["close"]/b["close"].rolling(50, min_periods=30).mean()-1
            b["ret20"] = b["close"]/b["close"].shift(20)-1
            b["ret5"] = b["close"]/b["close"].shift(5)-1
            b["vol20"] = r.rolling(20).std()
            b["z"] = r/b["vol20"].shift(1)
            b["fee"] = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["coin"] = c; b["w"] = w
            rows.append(b[["coin","w","forecast","pos","nxt","gain","sma50","ret20","ret5","vol20","z","fee","r1"]])
    B = pd.concat(rows, ignore_index=True)
    act = B[B["pos"].abs()>1e-9].dropna(subset=["nxt"])
    mu = B.groupby("coin")["nxt"].mean()
    act = act.assign(ex=act["nxt"]-act["coin"].map(mu))
    out["totals"] = pd.Series({"mean_gain_per_bar_all": B["gain"].mean(), "mean_fee_per_bar": B["fee"].mean(),
        "share_bars_in": len(act)/B["nxt"].notna().sum(), "mean_pos_when_in": act["pos"].mean(),
        "gain_when_in": act["gain"].mean(), "nxt_when_in": act["nxt"].mean(), "coin_mean_all": B["nxt"].mean()})
    def grp(col, q=5):
        x = act.dropna(subset=[col])
        k = pd.qcut(x[col], q, duplicates="drop")
        return x.groupby(k).agg(n=("gain","size"), gain=("gain","mean"), nxt=("nxt","mean"),
            t_nxt=("nxt", lambda s: s.mean()/s.std()*np.sqrt(len(s))), pos=("pos","mean"))
    out["by_sma50"] = grp("sma50")
    out["by_ret20"] = grp("ret20")
    out["by_vol20"] = grp("vol20")
    out["by_z"] = grp("z")
    out["by_coin"] = act.groupby("coin").agg(n=("gain","size"), gain=("gain","mean"), nxt=("nxt","mean"))
    return out
