import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        # drift per horizon: mean of non-overlapping grid returns over all windows
        dd = {}
        for h in H:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            dd[h] = np.mean(rs) if rs else np.nan
        drift[coin] = dd
        for w, df in ws.items():
            c = df["close"].values
            f = df["forecast"].values
            raw = df.get("debug_info.components.stretch.last_history_value")
            raw = raw.values if raw is not None else np.full(len(c), np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            for h in H:
                for i in range(0, len(c) - h, h):
                    if f[i] == 0 or np.isnan(f[i]):
                        continue
                    r = c[i + h] / c[i] - 1 - dd[h]
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], raw=raw[i], yr=yr[i], day=day[i], r=r))
    d = pd.DataFrame(rows)
    out = {}

    def slope(g):
        if len(g) < 10:
            return pd.Series(dict(n=len(g)))
        s = stats.linregress(g["f"], g["r"])
        dirm = (np.sign(g["f"]) * g["r"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr,
                              dir_mean=dirm.mean(), dir_t=dirm.mean() / (dirm.std() / np.sqrt(len(g)))))
    out["by_horizon"] = d.groupby("h").apply(slope)
    d10 = d[d.h == 10].copy()
    d10["side"] = np.where(d10.f > 0, "long", "short")
    out["h10_by_side"] = d10.groupby("side").apply(slope)
    out["h10_by_coin"] = d10.groupby("coin").apply(slope)
    out["h10_by_year"] = d10.groupby("yr").apply(slope)
    d10["absq"] = pd.qcut(d10.f.abs(), 4, labels=False)
    out["h10_by_absforecast_quartile"] = d10.groupby(["absq", "side"]).apply(slope)
    d5 = d[d.h == 5].copy(); d5["side"] = np.where(d5.f > 0, "long", "short")
    out["h5_by_side"] = d5.groupby("side").apply(slope)
    d20 = d[d.h == 20].copy(); d20["side"] = np.where(d20.f > 0, "long", "short")
    out["h20_by_side"] = d20.groupby("side").apply(slope)
    # raw stretch vs forecast
    d10["rawq"] = pd.qcut(d10.raw, 5, labels=False, duplicates="drop")
    out["h10_by_raw_stretch_quintile"] = d10.groupby("rawq").apply(
        lambda g: pd.Series(dict(n=len(g), raw_mean=g.raw.mean(), f_mean=g.f.mean(), r_mean=g.r.mean(),
                                 t=g.r.mean() / (g.r.std() / np.sqrt(len(g))))))
    out["corr_raw_f"] = float(d10[["raw", "f"]].corr().iloc[0, 1])
    return out
