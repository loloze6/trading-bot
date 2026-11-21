def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    fc_entry = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r24 = c / c.shift(24) - 1
            mad = r24.abs().rolling(720, min_periods=360).mean()
            r720 = c / c.shift(720) - 1
            r168 = c / c.shift(168) - 1
            vol = np.log(c).diff().rolling(720, min_periods=360).std()
            vol_s = np.log(c).diff().rolling(72, min_periods=48).std()
            fwd72 = c.shift(-72) / c - 1
            fwd24 = c.shift(-24) / c - 1
            idx = np.arange(0, len(b), 72)
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "z24": (r24 / mad).iloc[idx].values,
                "r720": r720.iloc[idx].values,
                "r168": r168.iloc[idx].values,
                "volratio": (vol_s / vol).iloc[idx].values,
                "fc": b["forecast"].iloc[idx].values,
                "alloc": b["postRebalance_current_allocation"].iloc[idx].values,
                "fwd72": fwd72.iloc[idx].values,
                "fwd24": fwd24.iloc[idx].values,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.iloc[idx].values,
            })
            rows.append(df)
            f = b["forecast"]
            fc_entry.append(f[f > 0])
    d = pd.concat(rows, ignore_index=True)
    d["drift"] = d.groupby("coin")["fwd72"].transform("mean")
    d["un"] = d["fwd72"] - d["drift"]
    d = d.dropna(subset=["un", "z24", "r720"])
    d["z720"] = d["r720"] / d.groupby("coin")["r720"].transform("std")

    def summ(g):
        x = g["un"]
        return pd.Series({"n": len(x), "mean_un": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    d["z24_q"] = pd.qcut(d["z24"], 7, duplicates="drop")
    out["un72_by_z24"] = d.groupby("z24_q").apply(summ)
    d["z720_q"] = pd.qcut(d["z720"], 5)
    out["un72_by_z720"] = d.groupby("z720_q").apply(summ)
    d["z24s"] = pd.cut(d["z24"], [-99, -1.5, -0.5, 0.5, 1.5, 99])
    d["up30"] = d["r720"] > 0
    out["un72_z24_x_up30"] = d.groupby(["z24s", "up30"]).apply(summ)
    d["r168_q"] = pd.qcut(d["r168"] / d.groupby("coin")["r168"].transform("std"), 5)
    out["un72_by_r168"] = d.groupby("r168_q").apply(summ)
    d["vr_q"] = pd.qcut(d["volratio"], 5)
    out["un72_by_volratio"] = d.groupby("vr_q").apply(summ)
    out["un72_by_coin"] = d.groupby("coin").apply(summ)
    out["un72_in_vs_flat"] = d.groupby(d["alloc"].abs() > 1e-6).apply(summ)
    fe = pd.concat(fc_entry)
    out["fc_pos_dist"] = fe.describe(percentiles=[.1, .25, .5, .75, .9, .99])
    out["share_fc_at_cap"] = float((fe >= 19.99).mean())

    # book: days around largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.reset_index(drop=True).copy()
            x["coin"] = coin
            x["next_coin"] = x["coin_return"].shift(-1)
            x["next_book"] = x["book_return"].shift(-1)
            x["prev_coin"] = x["coin_return"].shift(1)
            dd.append(x)
    D = pd.concat(dd).dropna(subset=["book_return"])
    D["bq"] = pd.qcut(D["book_return"].rank(method="first"), 10, labels=False)
    out["book_deciles"] = D.groupby("bq")[["book_return", "coin_return", "prev_coin", "next_coin", "next_book"]].mean()
    return out
