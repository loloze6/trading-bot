import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [6, 18]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values
            f = df["forecast"].fillna(0).values
            raw = df["debug_info.components.down_streak.last_history_value"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            down = np.r_[False, c[1:] < c[:-1]]
            streak = np.zeros(n, int)
            for i in range(1, n):
                streak[i] = streak[i-1] + 1 if down[i] else 0
            for cell in range(0, n, 18):
                for i in range(cell, min(cell + 18, n)):
                    if f[i] >= 2:
                        if i + 18 >= n: break
                        L = streak[i]; s0 = i - L
                        pre = v[max(0, s0 - 30):s0]
                        vf = np.mean(v[s0+1:i+1]) / np.mean(pre) if len(pre) > 5 and np.mean(pre) > 0 else np.nan
                        tr = c[i] / c[max(0, i-180)] - 1
                        r = {"coin": coin, "win": w, "year": ts[i].year, "f": f[i], "raw": raw[i], "L": L,
                             "vfade": vf, "trend": tr}
                        for h in H:
                            r[f"u{h}"] = c[i+h]/c[i]-1 - drift[(coin, h)]
                        rows.append(r)
                        break
    d = pd.DataFrame(rows)
    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    d["rawq"] = pd.qcut(d["raw"], 5, labels=False)
    d["vq"] = pd.qcut(d["vfade"], 4, labels=False)
    d["trq"] = pd.qcut(d["trend"], 4, labels=False)
    top = d[d["rawq"] == 4]
    out["top_raw_by_coin"] = top.groupby("coin").apply(summ)
    out["top_raw_by_year"] = top.groupby("year").apply(summ)
    out["raw_x_vol"] = d.groupby(["rawq", "vq"]).apply(summ)
    out["vol_by_year_topq"] = d[d["vq"] == 3].groupby("year").apply(summ)
    out["vol_by_coin_topq"] = d[d["vq"] == 3].groupby("coin").apply(summ)
    out["corr_raw_vfade"] = float(d[["raw", "vfade"]].corr().iloc[0, 1])
    out["raw_x_trend"] = d.groupby(["rawq", "trq"]).apply(summ)
    out["f_eq20_vs_less"] = d.groupby(d["f"] >= 19.99).apply(summ)
    return out
