import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 18
    rows = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        allr = {6: [], 12: [], 18: [], 36: []}
        for w, df in ws.items():
            c = df["close"].values
            for h in allr:
                idx = np.arange(0, len(c) - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(v) for h, v in allr.items()}
        usual[coin] = np.std(allr[18])
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            raw = df["debug_info.components.vol_surge.last_history_value"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            barret = np.r_[np.nan, c[1:] / c[:-1] - 1]
            prior6 = np.r_[[np.nan] * 6, c[6:] / c[:-6] - 1]
            prior18 = np.r_[[np.nan] * 18, c[18:] / c[:-18] - 1]
            for start in range(0, n - H, H):
                cell = np.arange(start, start + H)
                hit = cell[f[cell] >= 2]
                if len(hit) == 0:
                    continue
                t = hit[0]
                r = {}
                for h in [6, 12, 18, 36]:
                    r[h] = (c[t + h] / c[t] - 1 - drift[coin][h]) if t + h < n else np.nan
                rows.append(dict(coin=coin, window=w, year=ts.iloc[t].year,
                                 f=f[t], raw=raw[t], barret=barret[t],
                                 prior6=prior6[t], prior18=prior18[t],
                                 ex6=r[6], ex12=r[12], ex18=r[18], ex36=r[36],
                                 strength=r[18] / usual[coin] if not np.isnan(r[18]) else np.nan))
    d = pd.DataFrame(rows)

    def summ(g, col="ex18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["overall"] = pd.DataFrame({h: summ(d, f"ex{h}") for h in [6, 12, 18, 36]}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["bar_dir"] = np.where(d["barret"] > 0, "surge_bar_up", "surge_bar_down")
    out["by_surge_bar_dir"] = d.groupby("bar_dir").apply(summ)
    d["p6q"] = pd.qcut(d["prior6"], 5, labels=False)
    out["by_prior1d_quintile"] = d.groupby("p6q").apply(lambda g: pd.concat([summ(g), pd.Series({"prior6_mean": g.prior6.mean()})]))
    d["p18q"] = pd.qcut(d["prior18"], 5, labels=False)
    out["by_prior3d_quintile"] = d.groupby("p18q").apply(lambda g: pd.concat([summ(g), pd.Series({"prior18_mean": g.prior18.mean()})]))
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 4, labels=False)
    out["by_forecast_quartile"] = d.groupby("fq").apply(lambda g: pd.concat([summ(g), pd.Series({"f_mean": g.f.mean()})]))
    d["bq"] = pd.qcut(d["barret"], 5, labels=False)
    out["by_surge_bar_return_quintile"] = d.groupby("bq").apply(lambda g: pd.concat([summ(g), pd.Series({"barret_mean": g.barret.mean()})]))
    dd = d.dropna(subset=["ex18", "prior18", "barret"])
    out["spearman"] = pd.Series({
        "f_vs_ex18": stats.spearmanr(dd.f, dd.ex18)[0],
        "prior18_vs_ex18": stats.spearmanr(dd.prior18, dd.ex18)[0],
        "barret_vs_ex18": stats.spearmanr(dd.barret, dd.ex18)[0],
        "signed_f_by_bar_vs_ex18": stats.spearmanr(dd.f * np.sign(dd.barret), dd.ex18)[0],
        "signed_f_by_prior18_vs_ex18": stats.spearmanr(dd.f * np.sign(dd.prior18), dd.ex18)[0],
        "mean_strength": d.strength.mean()})
    return out
