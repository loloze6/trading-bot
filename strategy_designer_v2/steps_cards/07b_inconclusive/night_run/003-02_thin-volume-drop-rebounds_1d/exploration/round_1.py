import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    # coin mean h-return over grid, per horizon
    H = [1, 2, 3, 5, 10]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float); v = df["volume"].values.astype(float)
            n = len(df)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            vm = pd.Series(v).shift(1).rolling(30, min_periods=30).mean().values
            vr = v / vm
            r20 = pd.Series(c).pct_change(20).values
            yr = pd.to_datetime(df["timestamp"].iloc[0]).year
            fc = df["forecast"].fillna(0).values
            for h in H:
                for t in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, yr=yr, h=h, t=t, fwd=c[t + h] / c[t] - 1,
                                     fc=fc[t], r1=r1[t], vr=vr[t], r20=r20[t],
                                     fall=df["debug_info.components.fall.post_pipeline_value"].iloc[t] if "debug_info.components.fall.post_pipeline_value" in df else np.nan,
                                     thin=df["debug_info.components.thin.post_pipeline_value"].iloc[t] if "debug_info.components.thin.post_pipeline_value" in df else np.nan))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["mu"]
    d["m"] = d["fc"] / 10 * d["ex"]

    def tt(x):
        x = x.dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan))

    pos = d[d.fc > 0]
    out = {}
    out["by_h_measure"] = pos.groupby("h")["m"].apply(tt).unstack()
    out["by_h_excess_pos"] = pos.groupby("h")["ex"].apply(tt).unstack()
    p5 = pos[pos.h == 5]
    out["h5_by_coin"] = p5.groupby("coin")["m"].apply(tt).unstack()
    out["h5_by_year"] = p5.groupby("yr")["m"].apply(tt).unstack()
    p5 = p5.copy()
    p5["trend"] = np.where(p5.r20 > 0, "up20", "down20")
    out["h5_by_trend"] = p5.groupby("trend")["ex"].apply(tt).unstack()
    p5["fq"] = pd.qcut(p5.fc.rank(method="first"), 4, labels=False)
    out["h5_by_fc_quart"] = p5.groupby("fq")["ex"].apply(tt).unstack()
    # brief comparison: down days thin vs heavy volume, all down days, by horizon
    dn = d[(d.r1 < 0) & d.vr.notna()].copy()
    dn["vol"] = np.where(dn.vr < 1, "thin", "heavy")
    g = dn.groupby(["h", "vol"])["ex"].apply(tt).unstack()
    out["down_thin_vs_heavy"] = g
    # big down days (r1 below coin's 20th pct) thin vs heavy
    q = d.groupby("coin")["r1"].transform(lambda x: x.quantile(0.2))
    bd = d[(d.r1 < q) & d.vr.notna()].copy()
    bd["vol"] = np.where(bd.vr < 1, "thin", "heavy")
    out["bigdown_thin_vs_heavy"] = bd.groupby(["h", "vol"])["ex"].apply(tt).unstack()
    # big up days thin vs heavy
    qu = d.groupby("coin")["r1"].transform(lambda x: x.quantile(0.8))
    bu = d[(d.r1 > qu) & d.vr.notna()].copy()
    bu["vol"] = np.where(bu.vr < 1, "thin", "heavy")
    out["bigup_thin_vs_heavy"] = bu.groupby(["h", "vol"])["ex"].apply(tt).unstack()
    return out
