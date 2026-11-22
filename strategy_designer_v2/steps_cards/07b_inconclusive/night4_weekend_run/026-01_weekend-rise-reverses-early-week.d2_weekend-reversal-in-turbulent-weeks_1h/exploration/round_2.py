import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    drift = {}
    rows = []
    for coin, ws in bars.items():
        g = {h: [] for h in (48, 96)}
        for w, df in ws.items():
            c = df["close"].values
            for h in g:
                idx = np.arange(0, len(c) - h, h)
                g[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: np.mean(v) for h, v in g.items()}
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            n = len(c)
            lr = np.log(c[1:] / c[:-1])
            vol = pd.Series(np.r_[np.nan, lr]).rolling(720, min_periods=200).std().values
            volrank = pd.Series(vol).rolling(4320, min_periods=720).rank(pct=True).values
            cand = np.where(ts.dt.hour.values == 23)[0]
            for t in cand:
                if t < 48:
                    continue
                cd = (ts.iloc[t] + pd.Timedelta(hours=1)).dayofweek
                p48 = c[t] / c[t - 48] - 1
                r = {"coin": coin, "w": w, "closeday": cd, "past48": p48,
                     "fc": df["forecast"].iloc[t], "regime": df["regime"].iloc[t],
                     "year": ts.iloc[t].year, "vol": vol[t], "vrank": volrank[t]}
                for h in (48, 96):
                    r[f"u{h}"] = (c[t + h] / c[t] - 1 - drift[coin][h]) if t + h < n else np.nan
                rows.append(r)
    D = pd.DataFrame(rows)
    D["z"] = D.past48 / (D.vol * np.sqrt(48))
    out = {}
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    rises = D[D.past48 > 0].copy()
    rises["fall48"] = -rises.u48
    rises["fall96"] = -rises.u96
    rises["hv"] = rises.vrank >= 0.5
    out["rise_fall48_hv_by_closeday"] = rises[rises.hv].groupby("closeday").apply(lambda g: summ(g, "fall48"))
    out["rise_fall48_lv_by_closeday"] = rises[~rises.hv].groupby("closeday").apply(lambda g: summ(g, "fall48"))
    cases = D[(D.fc != 0) & D.fc.notna()].copy()
    cases["fall48"] = -cases.u48
    cases["fall96"] = -cases.u96
    cases["zq"] = pd.qcut(cases.z.rank(method="first"), 4, labels=False)
    a = cases.groupby("zq").apply(lambda g: summ(g, "fall48"))
    a["z_mean"] = cases.groupby("zq").z.mean()
    out["cases_by_volnorm_gain_quartile_48"] = a
    out["cases_by_volnorm_gain_quartile_96"] = cases.groupby("zq").apply(lambda g: summ(g, "fall96"))
    cases["vq"] = pd.qcut(cases.vrank.rank(method="first"), 4, labels=False)
    b = cases.groupby("vq").apply(lambda g: summ(g, "fall48"))
    b["vrank_mean"] = cases.groupby("vq").vrank.mean()
    out["cases_by_volrank_quartile"] = b
    ex = cases[~cases.year.isin([2018, 2025])]
    out["cases_ex_2018_2025"] = summ(ex, "fall48")
    out["spearman_z_fall48"] = str(stats.spearmanr(cases.z, cases.fall48, nan_policy="omit"))
    out["spearman_vrank_fall48"] = str(stats.spearmanr(cases.vrank, cases.fall48, nan_policy="omit"))
    # high-vol Monday rises, top half vs bottom half of raw gain, by year
    cases["big"] = cases.past48 > cases.past48.median()
    out["big_minus_small_by_year"] = cases.groupby("year").apply(
        lambda g: g[g.big].fall48.mean() - g[~g.big].fall48.mean())
    out["fall48_by_window_t"] = cases.groupby("w").fall48.mean().describe()
    return out
