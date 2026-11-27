def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 5
    rows = []
    drift = {}
    for coin, ws in bars.items():
        rets = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rets) if rets else np.nan
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            sma = c.rolling(20).mean()
            sd = c.pct_change().rolling(20).std()
            raw = (c - sma) / sma / sd
            rec = df.get("debug_info.components.stretch.last_history_value")
            n = len(df)
            for hh in [1, 3, 5, 10]:
                for i in range(0, n - hh, hh):
                    rows.append(dict(coin=coin, w=w, h=hh, i=i,
                        ts=df["timestamp"].iloc[i],
                        fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                        raw=raw.iloc[i], rec=(rec.iloc[i] if rec is not None else np.nan),
                        r=c.iloc[i + hh] / c.iloc[i] - 1))
    d = pd.DataFrame(rows)
    d["year"] = pd.to_datetime(d["ts"]).dt.year
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["drift_h"] = d.apply(lambda x: drift[x.coin] * x.h / 5, axis=1)
    d["ex"] = d["r"] - d["drift_h"]
    ch = d[d.reg == "unknown"]
    def tpool(sub, col):
        g = sub.groupby("day")[col].sum()
        m = sub[col].mean()
        dd = sub.groupby("day").apply(lambda s: (s[col] - m).sum())
        D = len(dd)
        se = np.sqrt((dd ** 2).sum() * D / (D - 1)) / len(sub) if D > 1 else np.nan
        return pd.Series(dict(n=len(sub), days=D, mean=m, t=m / se if se else np.nan))
    out = {}
    # short side excess (positive = fall) by horizon, below avg
    res = {}
    for hh in [1, 3, 5, 10]:
        s = ch[(ch.h == hh) & (ch.raw < 0)].copy(); s["sx"] = -s["ex"]
        res[f"below_h{hh}"] = tpool(s, "sx")
        s2 = ch[(ch.h == hh) & (ch.raw > 0)].copy(); s2["lx"] = s2["ex"]
        res[f"above_long_h{hh}"] = tpool(s2, "lx")
        s3 = ch[(ch.h == hh) & (ch.fc < 0)].copy(); s3["sx"] = -s3["ex"]
        res[f"fcneg_h{hh}"] = tpool(s3, "sx")
    out["by_horizon"] = pd.DataFrame(res).T
    s5 = ch[(ch.h == 5) & (ch.raw < 0)].copy(); s5["sx"] = -s5["ex"]
    s5["rq"] = pd.qcut(s5["raw"], 5, labels=False)
    out["below_h5_by_raw_quintile"] = s5.groupby("rq").apply(lambda s: pd.concat([tpool(s, "sx"), pd.Series(dict(raw_mean=s.raw.mean()))]))
    f5 = ch[(ch.h == 5) & (ch.fc < 0)].copy(); f5["sx"] = -f5["ex"]
    f5["fq"] = pd.qcut(f5["fc"], 5, labels=False, duplicates="drop")
    out["fcneg_h5_by_fc_quintile"] = f5.groupby("fq").apply(lambda s: pd.concat([tpool(s, "sx"), pd.Series(dict(fc_mean=s.fc.mean()))]))
    out["below_h5_by_year"] = s5.groupby("year").apply(lambda s: tpool(s, "sx"))
    out["below_h5_by_coin"] = s5.groupby("coin").apply(lambda s: tpool(s, "sx"))
    out["below_h5_by_window"] = s5.groupby("w").apply(lambda s: tpool(s, "sx"))
    # raw vs |fc| correlation and raw ret
    out["corr_raw_fc"] = float(f5[["raw", "fc"]].corr().iloc[0, 1])
    out["below_h5_total_short_mean"] = float((-s5["r"]).mean())
    # 60d trend within choppy split (sign of trend recomputable only partially) -> use 20d return
    return out
