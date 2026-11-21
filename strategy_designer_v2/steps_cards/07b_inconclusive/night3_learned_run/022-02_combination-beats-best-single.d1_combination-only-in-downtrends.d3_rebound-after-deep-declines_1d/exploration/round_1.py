import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            hi = pd.Series(c).rolling(90, min_periods=30).max().values
            raw_depth = c / hi - 1
            r90 = pd.Series(c).pct_change(min(90, max(n-1,1))).values if n > 91 else np.full(n, np.nan)
            ts = pd.to_datetime(df["timestamp"])
            for h in (5, 10, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, year=ts.iloc[i].year,
                        fwd=c[i+h]/c[i]-1, regime=df["regime"].iloc[i],
                        fc=df["forecast"].iloc[i],
                        pp=df.get("debug_info.components.depth.post_pipeline_value", pd.Series([np.nan]*n)).iloc[i],
                        lh=df.get("debug_info.components.depth.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                        rawd=raw_depth[i]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin","h"])["fwd"].transform("mean")
    R["sd"] = R.groupby(["coin","h"])["fwd"].transform("std")
    R["ex"] = R["fwd"] - R["drift"]
    R["str"] = R["ex"]/R["sd"]
    M = R[(R.regime=="mean_reversion") & (R.pp > 0)].copy()
    out = {}
    def slope(d, x="pp", y="ex"):
        d = d.dropna(subset=[x,y])
        if len(d) < 10: return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan, mean_ex=np.nan))
        r = stats.linregress(d[x], d[y])
        return pd.Series(dict(n=len(d), slope=r.slope, t=r.slope/r.stderr, mean_ex=d[y].mean(), mean_str=d["str"].mean()))
    out["by_h"] = M.groupby("h").apply(slope)
    out["by_h_rawdepth_lh"] = M.groupby("h").apply(lambda d: slope(d, x="lh"))
    m5 = M[M.h==5]
    out["h5_by_coin"] = m5.groupby("coin").apply(slope)
    out["h5_by_year"] = m5.groupby("year").apply(slope)
    out["h20_by_year"] = M[M.h==20].groupby("year").apply(slope)
    M["q"] = M.groupby("h")["pp"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["quintiles"] = M.groupby(["h","q"]).agg(n=("ex","size"), fc=("pp","mean"), ex=("ex","mean"), fwd=("fwd","mean"), strn=("str","mean")).reset_index()
    A = R[R.rawd.notna()].copy()
    A["neg"] = -A["rawd"]
    A["inreg"] = A.regime=="mean_reversion"
    out["all_bars_rawdepth"] = A.groupby(["h","inreg"]).apply(lambda d: slope(d, x="neg"))
    out["regime_share"] = R[R.h==5].groupby("regime").agg(n=("ex","size"), ex=("ex","mean"))
    return out
