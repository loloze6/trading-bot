import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = 7
    out = {}
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i+H]/c[i]-1)
        mu = np.mean(allr)
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].values
            reg = df["regime"].astype(str).values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for off in range(H):
                for i in range(off, len(c) - H, H):
                    if reg[i] == "unknown":
                        rows.append(dict(off=off, coin=coin, w=w, yr=yr[i], day=day[i], f=f[i],
                                         pos=f[i] > 0, ex=c[i+H]/c[i]-1-mu))
    d = pd.DataFrame(rows)
    def summ(g):
        m = g["ex"].mean()
        dev = (g["ex"] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev**2).sum())/len(g)
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), mean=m, t=m/se if se > 0 else np.nan,
                              share_pos=(g["ex"] > 0).mean()))
    out["in_profile_pos_vs_zero_grid0"] = d[d.off == 0].groupby("pos").apply(summ)
    out["forecast_pos_by_grid_offset"] = d[d.pos].groupby("off").apply(summ)
    out["forecast_zero_by_grid_offset"] = d[~d.pos].groupby("off").apply(summ)
    dp = d[d.pos].copy()
    dp["fq"] = pd.qcut(dp["f"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["all_offsets_pos_by_tercile"] = dp.groupby("fq").apply(summ)
    out["all_offsets_pos_by_coin"] = dp.groupby("coin").apply(summ)
    out["all_offsets_pos_by_year"] = dp.groupby("yr").apply(summ)
    out["all_offsets_pos_excl_DOGE"] = summ(dp[dp.coin != "DOGEUSD"])
    return out
