import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 10
    # coin drift per coin on 10-bar grid
    rows = []
    book_rows = []
    for coin, wins in data["bars"].items():
        g_all = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            # past features
            ret30 = pd.Series(c).pct_change(30).values
            ret90 = pd.Series(c).pct_change(90).values
            ma50 = pd.Series(c).rolling(50, min_periods=30).mean().values
            vol20 = pd.Series(c).pct_change().rolling(20, min_periods=10).std().values
            for i in range(0, n - H, H):
                g_all.append(dict(coin=coin, w=w, f=b["forecast"].iloc[i],
                                  raw=b.get("debug_info.components.support_above.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                                  r=c[i+H]/c[i]-1, r30=ret30[i], r90=ret90[i],
                                  ma=c[i]/ma50[i]-1 if ma50[i]==ma50[i] else np.nan, vol=vol20[i],
                                  alloc=b["postRebalance_current_allocation"].iloc[i]))
        g = pd.DataFrame(g_all)
        g["drift"] = g["r"].mean()
        rows.append(g)
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            book_rows.append(d)
    G = pd.concat(rows)
    G["adj_short"] = -(G["r"] - G["drift"])
    G["short_r"] = -G["r"]
    S = G[G["f"] < 0].copy()
    N = G[G["f"] >= 0].copy()
    out["active vs flat: mean 10d return, n"] = pd.DataFrame({
        "active_mean_r": [S["r"].mean()], "flat_mean_r": [N["r"].mean()],
        "n_active": [len(S)], "n_flat": [len(N)],
        "welch_t": [stats.ttest_ind(S["r"], N["r"], equal_var=False).statistic]})
    S["fq"] = pd.qcut(S["f"].abs().rank(method="first"), 4, labels=["q1small","q2","q3","q4large"])
    out["by |forecast| quartile: drift-adj short gain"] = S.groupby("fq")["adj_short"].agg(["mean","count",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    out["by coin"] = S.groupby("coin")["adj_short"].agg(["mean","count"])
    S["trend"] = pd.qcut(S["r90"].rank(method="first"), 4, labels=["down90","q2","q3","up90"])
    out["by prior 90d return quartile"] = S.groupby("trend").agg(adj=("adj_short","mean"), raw_short=("short_r","mean"), r90=("r90","mean"), n=("r","count"))
    S["t30"] = pd.qcut(S["r30"].rank(method="first"), 4, labels=["down30","q2","q3","up30"])
    out["by prior 30d return quartile"] = S.groupby("t30").agg(adj=("adj_short","mean"), r30=("r30","mean"), n=("r","count"))
    S["vq"] = pd.qcut(S["vol"].rank(method="first"), 3, labels=["lowvol","mid","highvol"])
    out["by 20d vol tercile"] = S.groupby("vq").agg(adj=("adj_short","mean"), n=("r","count"))
    G["t30"] = pd.qcut(G["r30"].rank(method="first"), 4, labels=["down30","q2","q3","up30"])
    out["all grid bars by 30d ret: mean 10d r"] = G.groupby("t30").agg(r=("r","mean"), n=("r","count"))
    B = pd.concat(book_rows)
    daily = B.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book by window"] = daily.groupby(level=0).agg(book=("book_return","mean"), coin=("coin_return","mean"), n=("book_return","count"))
    out["share of grid bars active"] = len(S)/len(G)
    return out
