import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["day"] = b["ts"].dt.floor("D")
            b["ret1"] = b["close"].pct_change()
            b["next"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["next"]
            b["ret90"] = b["close"] / b["close"].shift(90) - 1
            b["ret30"] = b["close"] / b["close"].shift(30) - 1
            b["vol20"] = b["ret1"].rolling(20).std()
            b["vol20_rel"] = b["vol20"] / b["ret1"].rolling(120, min_periods=60).std()
            b["coin"] = coin; b["w"] = w
            b["wn"] = int(w[1:])
            b["side"] = np.sign(b["pos"].fillna(0))
            rows.append(b[["coin","w","wn","day","ts","ret1","next","pos","gain","regime","side","ret90","ret30","vol20","vol20_rel","postRebalance_total_value"]])
    B = pd.concat(rows)
    B["bv_ret"] = B.groupby(["coin","w"])["postRebalance_total_value"].pct_change()
    # book daily: mean over coins of book return per day, by window
    book = B.dropna(subset=["bv_ret"]).groupby(["wn","day"])["bv_ret"].mean().sort_index()
    eq = (1+book).cumprod()
    dd = eq/eq.cummax()-1
    out["book_summary"] = pd.Series({"mean": book.mean(), "sd": book.std(), "n": len(book),
        "sharpe": book.mean()/book.std()*np.sqrt(365), "maxdd": dd.min(),
        "yearly": eq.iloc[-1]**(365/len(book))-1})
    # gain split by side and regime (per-bar position gains, averaged like the book: per day mean over coins)
    B["gain_long"] = B["gain"].where(B["side"]>0, 0)
    B["gain_short"] = B["gain"].where(B["side"]<0, 0)
    g = B.dropna(subset=["next"]).groupby(["wn","day"])[["gain","gain_long","gain_short"]].mean()
    out["gain_by_side"] = pd.DataFrame({"mean": g.mean(), "t": g.mean()/(g.std()/np.sqrt(len(g)))})
    # chain each side separately: drawdown
    res = {}
    for c in ["gain","gain_long","gain_short"]:
        e = (1+g[c]).cumprod(); d = e/e.cummax()-1
        res[c] = {"maxdd": d.min(), "yearly": e.iloc[-1]**(365/len(e))-1, "sharpe": g[c].mean()/g[c].std()*np.sqrt(365)}
    out["side_chains"] = pd.DataFrame(res).T
    # drawdown episodes: top 5 by depth
    ddf = pd.DataFrame({"dd": dd.values}, index=book.index)
    ddf["inDD"] = ddf["dd"] < 0
    ddf["ep"] = (~ddf["inDD"]).cumsum()
    eps = ddf[ddf["inDD"]].groupby("ep").agg(depth=("dd","min"), length=("dd","size"))
    top = eps.sort_values("depth").head(6)
    # mark bars in top drawdown episodes (from peak to trough)
    ddf["top"] = ddf["ep"].isin(top.index)
    idx = ddf[ddf["top"]].index
    Bi = B.set_index(["wn","day"])
    inn = Bi.index.isin(idx)
    sub = Bi[inn]; rest = Bi[~inn]
    def prof(x):
        return pd.Series({"share_long": (x["side"]>0).mean(), "share_short": (x["side"]<0).mean(),
            "gain_long_mean": x.loc[x["side"]>0,"gain"].mean(), "gain_short_mean": x.loc[x["side"]<0,"gain"].mean(),
            "coin_ret_mean": x["next"].mean(), "ret90_mean": x["ret90"].mean(), "ret30_mean": x["ret30"].mean(),
            "vol20_rel": x["vol20_rel"].mean(), "share_mr_regime": (x["regime"]=="mean_reversion").mean()})
    out["in_top_dd_vs_rest"] = pd.DataFrame({"in_dd": prof(sub), "rest": prof(rest)})
    top["wins"] = [",".join(sorted(set("w"+str(i[0]) for i in ddf[ddf["ep"]==e].index))) for e in top.index]
    out["top_dd_episodes"] = top
    # per year book
    yr = book.groupby([book.index.get_level_values(1).year]).agg(["mean","std","count"])
    out["book_by_year"] = yr
    # gain per position by regime and by 30d return tercile within regime
    A = B[(B["side"]!=0)].dropna(subset=["next","ret30","vol20_rel"])
    A["r30q"] = A.groupby("side")["ret30"].transform(lambda s: pd.qcut(s,4,labels=False))
    out["gain_by_side_r30q"] = A.groupby(["side","r30q"])["gain"].agg(["mean","count"])
    A["vq"] = A.groupby("side")["vol20_rel"].transform(lambda s: pd.qcut(s,4,labels=False))
    out["gain_by_side_volq"] = A.groupby(["side","vq"])["gain"].agg(["mean","std","count"])
    return out
