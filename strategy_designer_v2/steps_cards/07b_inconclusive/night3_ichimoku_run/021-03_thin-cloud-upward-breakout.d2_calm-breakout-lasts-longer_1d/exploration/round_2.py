import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 40
    drift = {}; usual = {}; volmean = {}
    for coin, ws in bars.items():
        r = []; vv = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                r.append(c[i+H]/c[i]-1)
            lr = np.log(df["close"]).diff()
            vv.append((lr.rolling(20).std()*np.sqrt(365)).dropna())
        drift[coin] = np.mean(r); usual[coin] = np.std(r, ddof=1)
        volmean[coin] = pd.concat(vv).median()
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            lr = np.log(df["close"]).diff()
            vol20 = lr.rolling(20).std()*np.sqrt(365)
            ma200 = df["close"].rolling(200, min_periods=100).mean()
            idx = np.where((df["regime"] == "trending").values)[0]
            for i in idx:
                if i + H >= len(c): continue
                adj = (c[i+H]/c[i]-1) - drift[coin]
                rows.append({"coin": coin, "window": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                             "forecast": df["forecast"].iloc[i], "vol20": vol20.iloc[i],
                             "vol_rel": vol20.iloc[i]/volmean[coin],
                             "above_ma200": float(c[i] > ma200.iloc[i]) if not np.isnan(ma200.iloc[i]) else np.nan,
                             "adj": adj, "z": adj/usual[coin]})
    d = pd.DataFrame(rows).dropna(subset=["vol20"])
    def summ(g, col="z"):
        x = g[col]
        return pd.Series({"n": len(x), "mean_z": x.mean(), "median_z": x.median(),
                          "t": x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "mean_adj": g["adj"].mean(), "share_up": (x > 0).mean()})
    out = {}
    out["corr_forecast_vs_vol"] = pd.Series({
        "spearman_fc_vol20": stats.spearmanr(d["forecast"], d["vol20"]).correlation,
        "spearman_fc_volrel": stats.spearmanr(d["forecast"], d["vol_rel"]).correlation,
        "spearman_volrel_z": stats.spearmanr(d["vol_rel"], d["z"]).correlation,
        "spearman_volrel_z_p": stats.spearmanr(d["vol_rel"], d["z"]).pvalue,
        "spearman_vol20_z": stats.spearmanr(d["vol20"], d["z"]).correlation,
        "spearman_fc_z": stats.spearmanr(d["forecast"], d["z"]).correlation})
    d["coin_rank"] = d.groupby("coin")["vol_rel"].rank(pct=True)
    d["vq"] = pd.cut(d["coin_rank"], [0, 1/3, 2/3, 1.0], labels=["calm", "mid", "violent"], include_lowest=True)
    out["by_within_coin_vol_tercile"] = d.groupby("vq").apply(summ)
    med = d["coin_rank"].median()
    a = d[d["coin_rank"] < med]["z"]; b = d[d["coin_rank"] > med]["z"]
    ar = d[d["coin_rank"] < med]["adj"]; br = d[d["coin_rank"] > med]["adj"]
    out["calm_minus_violent_within_coin"] = pd.Series({
        "diff_z": a.mean()-b.mean(), "welch_t_z": stats.ttest_ind(a, b, equal_var=False).statistic,
        "diff_raw": ar.mean()-br.mean(), "welch_t_raw": stats.ttest_ind(ar, br, equal_var=False).statistic,
        "n_calm": len(a), "n_violent": len(b)})
    out["by_ma200"] = d.dropna(subset=["above_ma200"]).groupby("above_ma200").apply(summ)
    out["by_vq_and_ma200"] = d.dropna(subset=["above_ma200"]).groupby(["above_ma200", "vq"]).apply(summ)
    out["by_vq_coin_t"] = d.groupby(["coin", "vq"]).apply(lambda g: g["z"].mean()).unstack()
    zs = d["z"]
    out["outliers"] = pd.Series({"max_z": zs.max(), "top5_share_of_sum": zs.nlargest(5).sum()/zs.sum(),
                                 "mean_z_drop_top5": zs.drop(zs.nlargest(5).index).mean(),
                                 "violent_top5_count": (d.loc[zs.nlargest(10).index, "vq"] == "violent").sum()})
    return out
