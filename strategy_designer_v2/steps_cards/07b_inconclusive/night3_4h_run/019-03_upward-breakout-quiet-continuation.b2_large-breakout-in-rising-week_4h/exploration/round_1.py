import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rs.extend(list(c[idx + H] / c[idx] - 1))
        drift[coin] = np.mean(rs); usual[coin] = np.std(rs)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            f = df["forecast"].fillna(0).values
            prior_hi = pd.Series(hi).shift(1).rolling(12).max().values
            mr = pd.Series(hi - lo).rolling(180, min_periods=45).mean().values
            raw = np.maximum(0, c - prior_hi) / mr
            r7 = pd.Series(c).pct_change(42).values
            vol = pd.Series(c).pct_change().rolling(180).std().values
            n = len(c)
            runmin = 0.0
            taken = set()
            for t in range(n):
                cell = t // H
                if f[t] - runmin >= 2 and f[t] > 0 and cell not in taken:
                    taken.add(cell)
                    runmin = f[t]
                    if t + H < n:
                        fwd = {}
                        for h in (1, 6, 12, 18, 36):
                            fwd[h] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                        rows.append(dict(coin=coin, w=int(w[1:]), year=df["timestamp"].iloc[t].year if hasattr(df["timestamp"].iloc[t], "year") else pd.to_datetime(df["timestamp"].iloc[t]).year,
                                         f=f[t], raw=raw[t], r7=r7[t], vol=vol[t],
                                         sig_bar=c[t] / c[t - 1] - 1 if t > 0 else np.nan,
                                         u18=fwd[18] - drift[coin], tot18=fwd[18],
                                         r1=fwd[1], r6=fwd[6], r12=fwd[12], r36=fwd[36],
                                         s=(fwd[18] - drift[coin]) / usual[coin]))
                else:
                    runmin = min(runmin, f[t])
    d = pd.DataFrame(rows)
    def summ(g):
        return pd.Series({"n": len(g), "mean_u18": g.u18.mean(), "t": g.u18.mean() / (g.u18.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan, "strength": g.s.mean()})
    out = {}
    out["all"] = summ(d)
    out["forecast_desc"] = d.f.describe()
    out["share_f_at_cap"] = float((d.f >= 19.99).mean())
    d["fq"] = pd.qcut(d.f.rank(method="first"), 5, labels=False)
    out["by_f_quintile"] = d.groupby("fq").apply(summ).join(d.groupby("fq").f.mean())
    d["rq"] = pd.qcut(d.raw.rank(method="first"), 5, labels=False)
    out["by_raw_quintile"] = d.groupby("rq").apply(summ).join(d.groupby("rq").raw.mean())
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["r7q"] = pd.qcut(d.r7.rank(method="first"), 4, labels=False)
    out["by_r7_quartile"] = d.groupby("r7q").apply(summ).join(d.groupby("r7q").r7.mean())
    hz = {}
    for h in ("r1", "r6", "r12", "tot18", "r36"):
        x = d[h].dropna(); hz[h] = pd.Series({"mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))), "n": len(x)})
    out["horizons_total"] = pd.DataFrame(hz).T
    out["sig_bar_mean"] = float(d.sig_bar.mean())
    return out
