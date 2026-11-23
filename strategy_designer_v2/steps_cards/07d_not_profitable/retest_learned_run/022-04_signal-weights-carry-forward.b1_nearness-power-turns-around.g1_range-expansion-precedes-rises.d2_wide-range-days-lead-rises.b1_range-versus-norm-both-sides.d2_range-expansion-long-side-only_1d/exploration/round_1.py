import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # book daily returns: mean across coins per (window, day)
    rows = []
    for c in coins:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    wins = sorted(D["w"].unique(), key=lambda s: int(s[1:]))
    B = D.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    B["wi"] = B["w"].map({w:i for i,w in enumerate(wins)})
    B = B.sort_values(["wi","day"]).dropna(subset=["book_return"])
    v = (1+B["book_return"]).cumprod().values
    peak = np.maximum.accumulate(v); dd = v/peak-1
    B["dd"] = dd
    i_min = int(np.argmin(dd))
    i_peak = int(np.argmax(v[:i_min+1]))
    out["deepest fall"] = pd.Series({"depth": dd[i_min], "peak_window": B.iloc[i_peak]["w"], "trough_window": B.iloc[i_min]["w"],
        "days": i_min-i_peak, "book_ret_in_fall": v[i_min]/v[i_peak]-1,
        "coin_ret_in_fall": (1+B.iloc[i_peak+1:i_min+1]["coin_return"]).prod()-1})
    # per window book vs coin
    pw = B.groupby("w").agg(book=("book_return", lambda x:(1+x).prod()-1), coin=("coin_return", lambda x:(1+x).prod()-1), mindd=("dd","min"))
    pw = pw.reindex(wins)
    out["per window"] = pw
    # grid analysis per bar with features
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; hi=b["high"]; lo=b["low"]; op=b["open"]
            rng = (hi-lo)/cl
            r1 = cl/cl.shift(1)-1
            r30 = cl/cl.shift(30)-1
            fwd = cl.shift(-3)/cl-1
            fwd1 = cl.shift(-1)/cl-1
            # day position: close location in range
            cpos = (cl-lo)/(hi-lo)
            ma = cl.rolling(50, min_periods=20).mean()
            df = pd.DataFrame({"f":b["forecast"], "fwd":fwd, "r1":r1, "r30":r30, "cpos":cpos,
                               "above_ma": (cl>ma).astype(float).where(ma.notna()),
                               "alloc":b["postRebalance_current_allocation"], "fwd1":fwd1})
            df["coin"]=c; df["w"]=w; df["pos"]=np.arange(len(df))
            recs.append(df)
    G = pd.concat(recs)
    drift = G[G["pos"]%3==0].groupby("coin")["fwd"].mean()
    G["ex"] = G["fwd"] - G["coin"].map(drift)
    g = G[(G["pos"]%3==0)].dropna(subset=["fwd"])
    def summ(x):
        if len(x)<3: return pd.Series({"n":len(x)})
        return pd.Series({"n":len(x),"mean_fwd":x["fwd"].mean(),"mean_ex":x["ex"].mean(),"t_ex":stats.ttest_1samp(x["ex"],0).statistic})
    sig = g["f"]>0
    out["signal vs none"] = pd.DataFrame({"sig":summ(g[sig]),"nosig":summ(g[~sig])})
    # split by day direction
    res = {}
    for name, cond in [("down day", g["r1"]<0), ("up day", g["r1"]>=0),
                       ("r30<0", g["r30"]<0), ("r30>=0", g["r30"]>=0),
                       ("above ma50", g["above_ma"]==1), ("below ma50", g["above_ma"]==0),
                       ("close low in range", g["cpos"]<0.5), ("close high in range", g["cpos"]>=0.5)]:
        res[name+"|sig"] = summ(g[sig & cond])
        res[name+"|nosig"] = summ(g[~sig & cond])
    out["splits"] = pd.DataFrame(res).T
    # signal strength buckets
    gs = g[sig].copy()
    gs["fq"] = pd.qcut(gs["f"], 4, labels=False, duplicates="drop")
    out["by forecast quartile"] = gs.groupby("fq").apply(summ)
    # book daily return grouped by held conditions: contribution of day types
    G["gain"] = G["alloc"]*G["fwd1"]
    G["r30neg"] = G["r30"]<0
    out["bar gain by r30 sign, held"] = G[G["alloc"]>0].groupby("r30neg")["gain"].agg(["count","mean","std","sum"])
    out["bar gain by above ma, held"] = G[G["alloc"]>0].groupby("above_ma")["gain"].agg(["count","mean","std","sum"])
    return out
