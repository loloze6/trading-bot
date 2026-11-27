import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    out = {}
    allc = []
    for h in [7, 10, 14, 21]:
        for coin, ws in bars.items():
            cells = []
            for w, df in ws.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                r30 = pd.Series(c).pct_change(30).values * 100
                r60 = pd.Series(c).pct_change(60).values * 100
                reg = df["regime"].values
                ts = pd.to_datetime(df["timestamp"]).dt.floor("D").values
                for i in range(0, len(df) - h, h):
                    cells.append(dict(coin=coin, w=w, h=h, fwd=c[i + h] / c[i] - 1, r30=r30[i], r60=r60[i],
                                      chop=(reg[i] == "unknown"), day=ts[i]))
            cd = pd.DataFrame(cells)
            if len(cd) == 0:
                continue
            cd["ex"] = cd["fwd"] - cd["fwd"].mean()
            allc.append(cd)
    A = pd.concat(allc)
    A = A[A.chop].dropna(subset=["r30"])

    def dayt(sub, col):
        g = sub.groupby("day")[col].sum()
        n = len(sub)
        m = sub[col].mean()
        se = np.sqrt((g - g.index.map(lambda d: 0) * 0).sub(0).pow(2).sum()) / n if n else np.nan
        dev = sub[col] - m
        gs = dev.groupby(sub["day"]).sum()
        se = np.sqrt((gs ** 2).sum()) / n
        return m / se, len(gs)

    res = []
    for h in [7, 10, 14, 21]:
        d = A[A.h == h]
        for name, sub in [("all", d), ("up", d[d.r30 > 0]), ("down", d[d.r30 <= 0])]:
            r = stats.linregress(sub["r30"], sub["ex"])
            # directional excess: ex * sign(r30)
            dirx = sub["ex"] * np.sign(sub["r30"])
            sub2 = sub.assign(dirx=dirx)
            tdir, nd = dayt(sub2, "dirx")
            res.append(dict(h=h, part=name, n=len(sub), slope=r.slope, t_slope=r.slope / r.stderr,
                            mean_dir_ex=dirx.mean(), t_dir_day=tdir, days=nd))
    out["by_h_side"] = pd.DataFrame(res)

    d7 = A[A.h == 7].copy()
    dn = d7[d7.r30 <= 0].copy()
    out["down7_by_window"] = dn.groupby("w").agg(n=("ex", "size"), mean_ex=("ex", "mean"), r30=("r30", "mean"))
    out["down7_by_coin"] = dn.groupby("coin").agg(n=("ex", "size"), mean_ex=("ex", "mean"))
    up = d7[d7.r30 > 0].copy()
    out["up7_by_window"] = up.groupby("w").agg(n=("ex", "size"), mean_ex=("ex", "mean"))
    d7["q"] = pd.qcut(d7["r30"], 10, labels=False)
    out["deciles7"] = d7.groupby("q").agg(r30=("r30", "mean"), ex=("ex", "mean"), n=("ex", "size"))
    d14 = A[A.h == 14].copy()
    d14["q"] = pd.qcut(d14["r30"], 6, labels=False)
    out["sextiles14"] = d14.groupby("q").agg(r30=("r30", "mean"), ex=("ex", "mean"), n=("ex", "size"))
    # month move against the 60-day return: residual turn
    d7["turn"] = d7["r30"] - d7["r60"] / 2
    r = stats.linregress(d7.dropna(subset=["turn"])["turn"], d7.dropna(subset=["turn"])["ex"])
    out["turn_slope_t7"] = float(r.slope / r.stderr)
    return out
