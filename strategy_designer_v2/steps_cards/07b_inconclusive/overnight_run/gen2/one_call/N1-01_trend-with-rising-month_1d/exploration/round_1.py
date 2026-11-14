import numpy as np, pandas as pd
from scipy import stats

def _comp(df, cid, key):
    col = f"debug_info.components.{cid}.{key}"
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    if "debug_info.components" in df.columns:
        def g(x):
            try:
                if isinstance(x, str):
                    import json
                    x = json.loads(x)
                return x.get(cid, {}).get(key, np.nan)
            except Exception:
                return np.nan
        return pd.to_numeric(df["debug_info.components"].map(g), errors="coerce")
    return pd.Series(np.nan, index=df.index)

def explore(data):
    rows = []
    allfwd = {}
    for coin, wins in data["bars"].items():
        fw = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            f = np.full(n, np.nan)
            if n > 20:
                f[:n-20] = c[20:] / c[:n-20] - 1
            fw.append(f[~np.isnan(f)])
            dist = _comp(df, "dist", "last_history_value").values
            mom = _comp(df, "mom", "last_history_value").values
            mz = _comp(df, "mom", "post_pipeline_value").values
            dz = _comp(df, "dist", "post_pipeline_value").values
            fc = df["forecast"].astype(float).values
            # past 20-bar coin return as market context
            for i in range(0, n - 20, 20):
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 fwd=f[i], fc=fc[i], dist=dist[i], mom=mom[i], mz=mz[i], dz=dz[i]))
        allfwd[coin] = np.mean(np.concatenate(fw))
    R = pd.DataFrame(rows)
    R["ex"] = R["fwd"] - R["coin"].map(allfwd)
    A = R[R["fc"] > 0].copy()
    I = R[R["fc"] <= 0].copy()

    def summ(g):
        x = g["ex"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(),
                              hit=(x > 0).mean(), sd=x.std(),
                              t=stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan))
    out = {}
    out["active_vs_inactive"] = pd.DataFrame({"active": summ(A), "inactive": summ(I)}).T
    out["by_coin_active"] = A.groupby("coin").apply(summ)
    out["by_year_active"] = A.groupby("year").apply(summ)
    A["fcq"] = pd.qcut(A["fc"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["by_forecast_tercile"] = A.groupby("fcq").apply(summ)
    A["distq"] = pd.qcut(A["dist"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["by_dist_tercile"] = A.groupby("distq").apply(summ)
    A["momq"] = pd.qcut(A["mom"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["by_mom_tercile"] = A.groupby("momq").apply(summ)
    out["dist_mom_ranges"] = A[["dist", "mom", "fc"]].describe().T
    # trimmed mean / outlier influence
    x = A["ex"].dropna().sort_values()
    out["trim"] = pd.Series(dict(trim5_mean=stats.trim_mean(x, 0.05),
                                 top5_sum=x.tail(5).sum(), total_sum=x.sum(),
                                 skew=stats.skew(x)))
    return out
