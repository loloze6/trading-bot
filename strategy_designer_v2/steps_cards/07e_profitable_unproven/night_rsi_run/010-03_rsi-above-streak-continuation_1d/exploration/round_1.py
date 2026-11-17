def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    # coin mean daily return over all windows
    cmean = {}
    for c in coins:
        r = pd.concat([d["coin_return"] for d in data["days"][c].values()]).dropna()
        cmean[c] = r.mean()
    # book daily: mean of coins per day within window
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["nr"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["g"] = b["pos"] * b["nr"]
            b["mkt"] = b["pos"] * cmean[c]
            b["coin"] = c; b["w"] = w
            b["year"] = b["ts"].dt.year
            b["streak"] = b["debug_info.components.rsi_age.last_history_value"]
            rows.append(b)
    B = pd.concat(rows)
    B = B.dropna(subset=["nr"])
    B["timing"] = B["g"] - B["mkt"]
    out["per_coin"] = B.groupby("coin").agg(gain=("g","mean"), mkt=("mkt","mean"), timing=("timing","mean"), pos=("pos","mean"), inpos=("pos", lambda x:(x>0).mean()))
    out["per_year"] = B.groupby("year").agg(gain=("g","mean"), mkt=("mkt","mean"), timing=("timing","mean"), n=("g","size"))
    out["per_window"] = B.groupby("w").agg(gain=("g","mean"), timing=("timing","mean"), coin_ret=("nr","mean"))
    # gain by streak bucket (raw value)
    B["sb"] = pd.cut(B["streak"], [-1e9,0,5,10,20,40,1e9])
    out["by_streak"] = B.groupby("sb").agg(n=("nr","size"), nextret=("nr","mean"), pos=("pos","mean"), gain=("g","mean"))
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in coins for t in data["trades"][c].values()])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top5_sum": p.head(5).sum(), "top10_sum": p.head(10).sum(), "win": (p>0).mean(), "mean_dur_days": T["duration_minutes"].mean()/1440})
    # forward returns at various horizons by in/out (non-overlap grid)
    res = []
    for h in [1,3,7,14,30]:
        for c in coins:
            for w, b in data["bars"][c].items():
                cl = b["close"].values; f = b["forecast"].values
                for i in range(0, len(cl)-h, h):
                    res.append((h, c, f[i] > 0, cl[i+h]/cl[i]-1))
    R = pd.DataFrame(res, columns=["h","coin","on","r"])
    tab = []
    for h, g in R.groupby("h"):
        a = g[g.on]["r"]; bb = g[~g.on]["r"]
        t = stats.ttest_ind(a, bb, equal_var=False).statistic
        tab.append((h, a.mean(), bb.mean(), len(a), len(bb), t))
    out["on_vs_off_h"] = pd.DataFrame(tab, columns=["h","on","off","n_on","n_off","t"])
    return out
