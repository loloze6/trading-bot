import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [3, 6, 12, 18, 36]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs)
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
                        vlast = v[i] / np.mean(v[s0+1:i+1]) if L > 0 else np.nan
                        tr = c[i] / c[max(0, i-180)] - 1
                        r = {"coin": coin, "win": w, "year": ts[i].year, "f": f[i], "raw": raw[i], "L": L,
                             "vfade": vf, "vlast": vlast, "trend": tr}
                        for h in H:
                            if i + h < n:
                                r[f"u{h}"] = c[i+h]/c[i]-1 - drift[(coin, h)]
                        # return after streak ends: from next up close
                        j = i
                        while j + 1 < n and c[j+1] < c[j]: j += 1
                        j += 1
                        if j + 18 < n:
                            r["u18_after_end"] = c[j+18]/c[j]-1 - drift[(coin, 18)]
                        rows.append(r)
                        break
    d = pd.DataFrame(rows)
    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["horizons"] = pd.DataFrame({h: summ(d, f"u{h}") for h in H} | {"after_end18": summ(d, "u18_after_end")}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["rawq"] = pd.qcut(d["raw"], 5, duplicates="drop")
    out["by_raw_quintile"] = d.groupby("rawq").apply(summ)
    d["Lq"] = pd.cut(d["L"], [0, 1, 2, 3, 4, 6, 100])
    out["by_streak_len"] = d.groupby("Lq").apply(summ)
    d["vfq"] = pd.qcut(d["vfade"], 4)
    out["by_vol_fade"] = d.groupby("vfq").apply(summ)
    d["vlq"] = pd.qcut(d["vlast"], 4, duplicates="drop")
    out["by_vol_last"] = d.groupby("vlq").apply(summ)
    d["trq"] = pd.qcut(d["trend"], 4)
    out["by_trend"] = d.groupby("trq").apply(summ)
    out["by_trend_h36"] = d.groupby("trq").apply(lambda g: summ(g, "u36"))
    out["forecast_desc"] = d["f"].describe()
    out["usual18"] = pd.Series({k[0]: v for k, v in usual.items() if k[1] == 18})
    return out
