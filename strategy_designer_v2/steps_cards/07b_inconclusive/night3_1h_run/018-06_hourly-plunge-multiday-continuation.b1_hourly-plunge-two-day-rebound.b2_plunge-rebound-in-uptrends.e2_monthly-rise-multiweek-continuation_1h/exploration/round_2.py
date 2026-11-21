import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    h = 336
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            s = pd.Series(c)
            r30 = s.pct_change(720).values
            r7 = s.pct_change(168).values
            ma = s.rolling(2400, min_periods=1200).mean().values
            r90 = s.pct_change(2160).values
            for t in range(0, n - h, h):
                rows.append(dict(coin=coin, win=w, f=f[t], r30=r30[t], r7=r7[t], yr=yr[t],
                                 above=(c[t] / ma[t] - 1) if not np.isnan(ma[t]) else np.nan,
                                 r90=r90[t], ret=c[t + h] / c[t] - 1))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby("coin")["ret"].transform("mean")
    pos = d[d.f > 0].copy()
    out = {}
    v = pos.f * pos.ex / pos.f.mean()
    pos["v"] = v
    top = pos.sort_values("v", ascending=False).head(10)
    out["top10_by_coin"] = top.groupby("coin").agg(n=("v", "size"), v=("v", "sum"), ex=("ex", "mean"))
    out["top10_by_year"] = top.groupby("yr").agg(n=("v", "size"), v=("v", "sum"))
    bot = pos.sort_values("v").head(10)
    out["bot10_sum"] = pd.Series(dict(top10_v=top.v.sum(), bot10_v=bot.v.sum(), all_v=v.sum(),
                                      n=len(pos), share_pos_ex=(pos.ex > 0).mean(),
                                      median_ex=pos.ex.median(),
                                      wilcoxon_p=stats.wilcoxon(v).pvalue))
    # regime: long-term trend (price vs ~100-day mean)
    pr = pos.dropna(subset=["above"])
    pr = pr.assign(reg=np.where(pr.above > 0, "above100d", "below100d"))
    def wm(g):
        vv = g.f * g.ex / g.f.mean()
        return pd.Series(dict(n=len(g), wmean=vv.mean(), t=vv.mean() / (vv.std() / np.sqrt(len(vv))),
                              med_ex=g.ex.median(), share_pos=(g.ex > 0).mean()))
    out["by_trend_regime"] = pr.groupby("reg").apply(wm)
    p9 = pos.dropna(subset=["r90"]).assign(reg=lambda x: np.where(x.r90 > 0, "r90pos", "r90neg"))
    out["by_r90"] = p9.groupby("reg").apply(wm)
    p7 = pos.dropna(subset=["r7"]).assign(reg=lambda x: np.where(x.r7 > 0, "r7pos", "r7neg"))
    out["by_r7"] = p7.groupby("reg").apply(wm)
    # slope within trend regime
    res = {}
    for name, g in pr.groupby("reg"):
        sl = stats.linregress(g.f, g.ex)
        res[name] = dict(slope=sl.slope, t=sl.slope / sl.stderr, n=len(g))
    out["slope_by_regime"] = pd.DataFrame(res).T
    # winsorised wmean
    exw = pos.ex.clip(pos.ex.quantile(0.02), pos.ex.quantile(0.98))
    vw = pos.f * exw / pos.f.mean()
    out["winsor"] = pd.Series(dict(wmean=vw.mean(), t=vw.mean() / (vw.std() / np.sqrt(len(vw)))))
    return out
