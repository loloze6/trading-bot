import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []      # one row per coin/window/day-end at 00:00 UTC
    hr_rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].values; v = b["volume"].values
            n = len(b)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            hr_rows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday, "r1": r1}))
            # bars that close at 00:00 (start 23:00)
            idx = np.where(ts.dt.hour.values == 23)[0]
            for i in idx:
                if i < 720 + 1 or i + 48 >= n:
                    continue
                r48 = c[i] / c[i - 48] - 1
                r720 = c[i] / c[i - 720] - 1
                vr = v[i - 47:i + 1].mean() / max(v[i - 167:i - 47].mean(), 1e-12)
                past = c[i - 720:i + 1]
                pr = past[48::48] / past[:-48:48] - 1
                sd48 = np.std(pr, ddof=1)
                rows.append(dict(coin=coin, window=w, endwd=ts.iloc[i].weekday(), year=ts.iloc[i].year,
                                 r48=r48, z48=r48 / sd48 if sd48 > 0 else np.nan, r720=r720, vr=vr,
                                 f12=c[i + 12] / c[i] - 1, f24=c[i + 24] / c[i] - 1, f48=c[i + 48] / c[i] - 1,
                                 fc=b["forecast"].iloc[i]))
    D = pd.DataFrame(rows)
    # drift per coin for f12/f24/f48 approximated by mean of these samples (per endwd all days)
    for h in ["f12", "f24", "f48"]:
        D[h + "u"] = D[h] - D.groupby("coin")[h].transform("mean")
    D["s"] = np.sign(D["r48"])
    def summ(g):
        res = {}
        for h in ["f12u", "f24u", "f48u"]:
            x = (g[h] * g["s"]).dropna()
            res[h + "_mean"] = x.mean(); res[h + "_t"] = x.mean() / (x.std() / np.sqrt(len(x)))
        res["n"] = len(g)
        # graded: corr of z48 with fwd
        res["corr_z_f24"] = stats.spearmanr(g["z48"], g["f24u"], nan_policy="omit")[0]
        return pd.Series(res)
    # endwd 6 -> bar starts Sunday 23:00 -> weekend move (Sat+Sun)
    out["signed fwd after 48h move, by weekday of end bar (6=weekend move)"] = D.groupby("endwd").apply(summ)
    W = D[D.endwd == 6].copy()
    W["trend_same"] = np.sign(W.r48) == np.sign(W.r720)
    W["heavy"] = W.vr > 1
    out["weekend: by trend_same x heavy"] = W.groupby(["trend_same", "heavy"]).apply(summ)
    W["zq"] = pd.qcut(W.z48.abs(), 5, labels=False)
    out["weekend: by |z48| quintile"] = W.groupby("zq").apply(summ)
    W["vq"] = pd.qcut(W.vr, 5, labels=False)
    out["weekend: by vol-ratio quintile"] = W.groupby("vq").apply(summ)
    out["weekend all: by coin"] = W.groupby("coin").apply(summ)
    out["weekend all: by year"] = W.groupby("year").apply(summ)
    # hour of day / weekday mean returns
    H = pd.concat(hr_rows).dropna()
    def tt(x):
        return pd.Series({"mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(len(x))), "n": len(x)})
    out["hourly return by hour"] = H.groupby("hour")["r1"].apply(tt).unstack()
    out["hourly return by weekday"] = H.groupby("wd")["r1"].apply(tt).unstack()
    # vol scaled: abs r1 by hour (liquidity proxy)
    out["abs hourly return by weekday (bp)"] = H.groupby("wd")["r1"].apply(lambda x: x.abs().mean() * 1e4)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median", "std"])
    return out
