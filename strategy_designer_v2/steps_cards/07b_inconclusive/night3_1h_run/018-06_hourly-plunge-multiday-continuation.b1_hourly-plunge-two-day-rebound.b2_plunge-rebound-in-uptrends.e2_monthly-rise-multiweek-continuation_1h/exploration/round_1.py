import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    H = {168: None, 336: None, 672: None}
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            # 30d return recomputed
            r30 = pd.Series(c).pct_change(720).values
            for h in H:
                for t in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, f=f[t], r30=r30[t], yr=yr[t],
                                     ret=c[t + h] / c[t] - 1))
    d = pd.DataFrame(rows)
    d["mean_c"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["mean_c"]
    out = {}

    def wm(g):
        g = g[g.f > 0]
        if len(g) < 3:
            return pd.Series(dict(n=len(g), wmean=np.nan, t=np.nan, mean_ex=np.nan))
        v = g.f * g.ex / g.f.mean()
        return pd.Series(dict(n=len(g), wmean=v.mean(), t=v.mean() / (v.std() / np.sqrt(len(v))),
                              mean_ex=g.ex.mean()))

    out["by_h"] = d.groupby("h").apply(wm)
    d3 = d[d.h == 336]
    out["by_coin"] = d3.groupby("coin").apply(wm)
    out["by_year"] = d3.groupby("yr").apply(wm)
    win_num = d3.win.str[1:].astype(int)
    d3 = d3.assign(fold=pd.cut(win_num, [0, 6, 12, 18, 24], labels=list("ABCD")))
    out["by_fold"] = d3.groupby("fold").apply(wm)
    pos = d3[d3.f > 0].copy()
    pos["fq"] = pd.qcut(pos.f.rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_fq"] = pos.groupby("fq").agg(n=("ex", "size"), f=("f", "mean"), mean_ex=("ex", "mean"),
                                         sd=("ex", "std"), r30=("r30", "mean"))
    zero = d3[d3.f <= 0]
    out["zero_cells"] = pd.Series(dict(n=len(zero), mean_ex=zero.ex.mean(),
                                       t=zero.ex.mean() / (zero.ex.std() / np.sqrt(len(zero)))))
    # raw 30d return graded, all cells
    a = d3.dropna(subset=["r30"])
    a = a.assign(rq=pd.qcut(a.r30.rank(method="first"), 5, labels=[f"r{i}" for i in range(1, 6)]))
    out["by_r30_quint_all"] = a.groupby("rq").agg(n=("ex", "size"), r30=("r30", "mean"),
                                                   mean_ex=("ex", "mean"), sd=("ex", "std"))
    # median-weighted contribution check: share of weighted gain from top 5% cells
    v = pos.f * pos.ex
    out["top_share"] = pd.Series(dict(sum_all=v.sum(), sum_excl_top10=v.sort_values().iloc[:-10].sum(),
                                      mean_ex_trim=stats.trim_mean(pos.ex, 0.05)))
    return out
