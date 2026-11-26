import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            v = df["volume"].values.astype(float)
            n = len(df)
            r30 = pd.Series(c).pct_change(30).values
            vs = pd.Series(v)
            vratio = (vs.rolling(30).mean() / vs.shift(30).rolling(90, min_periods=45).mean()).values
            ts = pd.to_datetime(df["timestamp"])
            for h in (5, 10, 20):
                for t in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, t=t, day=ts.iloc[t].normalize(),
                                     year=ts.iloc[t].year,
                                     ret=c[t+h]/c[t]-1, fc=df["forecast"].iloc[t],
                                     reg=df["regime"].iloc[t], r30=r30[t], vr=vratio[t]))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby(["coin","h"])["ret"].transform("mean")
    g["ex"] = g["ret"] - g["drift"]
    out = {}
    def tday(s, d):
        x = pd.DataFrame({"s": s, "d": d}).groupby("d")["s"].sum()
        n = len(s)
        m = s.mean()
        dev = (s - m)
        sd = pd.DataFrame({"s": dev, "d": d}).groupby("d")["s"].sum()
        se = np.sqrt((sd**2).sum())/n
        return m/se if se > 0 else np.nan
    res = []
    for h in (5, 10, 20):
        a = g[(g.h==h)]
        ins = a[a.reg=="unknown"]
        sh = ins[ins.fc<0]
        out_ = a[a.reg!="unknown"]
        for name, s in [("in_short", sh), ("in_all", ins), ("in_r30neg", ins[ins.r30<0]), ("out_r30neg", out_[out_.r30<0])]:
            res.append(dict(h=h, grp=name, n=len(s), days=s.day.nunique(), mean_ex=s.ex.mean(),
                            t=tday(s.ex, s.day), corr_r30_ex=s[["r30","ex"]].corr().iloc[0,1]))
    out["by_horizon"] = pd.DataFrame(res)
    s5 = g[(g.h==5)&(g.reg=="unknown")&(g.fc<0)].copy()
    s5["q"] = pd.qcut(-s5.fc, 4, labels=False, duplicates="drop")
    out["short5_by_size_quartile"] = s5.groupby("q").agg(n=("ex","size"), mean_ex=("ex","mean"), r30=("r30","mean"))
    s5["rq"] = pd.qcut(s5.r30, 4, labels=False)
    out["short5_by_r30_quartile"] = s5.groupby("rq").agg(n=("ex","size"), mean_ex=("ex","mean"), r30=("r30","mean"))
    out["short5_by_coin"] = s5.groupby("coin").agg(n=("ex","size"), mean_ex=("ex","mean"))
    out["short5_by_year"] = s5.groupby("year").agg(n=("ex","size"), mean_ex=("ex","mean"), mean_ret=("ret","mean"))
    s5v = s5.dropna(subset=["vr"]).copy()
    s5v["vq"] = pd.qcut(s5v.vr, 3, labels=["low","mid","high"])
    out["short5_by_volume_tercile"] = s5v.groupby("vq").agg(n=("ex","size"), mean_ex=("ex","mean"), r30=("r30","mean"))
    for vq in ["low","mid","high"]:
        x = s5v[s5v.vq==vq]
        out[f"corr_r30_ex_vol_{vq}"] = float(x[["r30","ex"]].corr().iloc[0,1])
    return out
