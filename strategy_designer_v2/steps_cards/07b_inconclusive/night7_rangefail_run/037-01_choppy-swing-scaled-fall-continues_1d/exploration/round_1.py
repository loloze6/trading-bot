import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    drift = {}
    usual = {}
    # drift per coin per horizon from grid returns over all windows
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
            usual[(coin, h)] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            f = df["forecast"].values
            r60 = pd.Series(c).pct_change(min(60, n - 1)).values
            lr = np.log(pd.Series(c)).diff()
            vol30 = lr.rolling(30).std().values
            vol120 = lr.rolling(120, min_periods=60).median().values if False else lr.abs().rolling(120, min_periods=60).mean().values
            raw = df.get("debug_info.components.fall_in_swings.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            # recompute swing-scaled 5d return
            r5 = pd.Series(c).pct_change(5).values
            sd20 = pd.Series(c).pct_change().rolling(20).std().values
            z = r5 / sd20
            for i in range(0, n, 5):
                if not (f[i] < 0):
                    continue
                rec = dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                           day=str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                           f=f[i], z=z[i], vol30=vol30[i])
                for h in H:
                    if i + h < n:
                        rec[f"u{h}"] = -(c[i + h] / c[i] - 1 - drift[(coin, h)])
                        rec[f"s{h}"] = rec[f"u{h}"] / usual[(coin, h)]
                    else:
                        rec[f"u{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}

    def tday(x, col):
        x = x.dropna(subset=[col])
        g = x.groupby("day")[col].sum()
        G = len(g); N = len(x)
        m = x[col].mean()
        dev = x.groupby("day")[col].apply(lambda s: (s - m).sum())
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / N if G > 1 else np.nan
        return pd.Series(dict(n=N, days=G, mean=m, t=m / se if se else np.nan))

    out["by horizon"] = pd.DataFrame({f"h{h}": tday(d, f"u{h}") for h in H}).T
    out["by coin h5"] = d.groupby("coin").apply(lambda x: tday(x, "u5"))
    out["by window h5"] = d.groupby("w").apply(lambda x: tday(x, "u5"))
    out["by year h5"] = d.groupby("year").apply(lambda x: tday(x, "u5"))
    d["fq"] = pd.qcut(d["f"].abs().rank(method="first"), 4, labels=["q1small", "q2", "q3", "q4large"])
    out["by |forecast| quartile"] = pd.DataFrame({h: d.groupby("fq").apply(lambda x: tday(x, f"u{h}"))["mean"] for h in H})
    out["by |forecast| quartile t h5/h10"] = d.groupby("fq").apply(lambda x: pd.Series(dict(t5=tday(x, "u5")["t"], t10=tday(x, "u10")["t"], n=len(x))))
    d["zq"] = pd.qcut(d["z"].rank(method="first"), 4, labels=["z1deep", "z2", "z3", "z4shallow"])
    out["by raw z quartile"] = pd.DataFrame({h: d.groupby("zq").apply(lambda x: tday(x, f"u{h}"))["mean"] for h in H})
    out["z quart mean"] = d.groupby("zq")["z"].mean()
    d["vq"] = pd.qcut(d.groupby("coin")["vol30"].rank(pct=True), 2, labels=["calmer", "agitated"])
    out["by agitation h5"] = d.groupby("vq").apply(lambda x: tday(x, "u5"))
    out["by agitation h10"] = d.groupby("vq").apply(lambda x: tday(x, "u10"))
    return out
