import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [1, 3, 6, 12, 24]
    rows = []
    trows = []
    book = []
    for coin, ws in data["bars"].items():
        # drift per horizon: non-overlapping returns over all windows
        drift = {}
        sd = {}
        for h in H:
            allr = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr.append(c[idx + h] / c[idx] - 1)
            allr = np.concatenate(allr)
            drift[h] = allr.mean(); sd[h] = allr.std()
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            f = b["forecast"].fillna(0).values
            r1 = pd.Series(c).pct_change()
            mabs = r1.abs().rolling(720, min_periods=240).mean()
            z = (r1 / mabs).values
            vr = (b["volume"] / b["volume"].rolling(720, min_periods=240).mean()).values
            r24 = pd.Series(c).pct_change(24).values
            vol30 = mabs.values
            hour = pd.to_datetime(b["timestamp"]).dt.hour.values
            grid = np.arange(n) // 6
            seen = set()
            for i in np.where(f <= -2)[0]:
                if grid[i] in seen:
                    continue
                seen.add(grid[i])
                rec = {"coin": coin, "w": w, "f": -f[i], "z": z[i], "vr": vr[i],
                       "r24": r24[i], "vol30": vol30[i], "hour": hour[i]}
                for h in H:
                    if i + h < n:
                        rec[f"u{h}"] = -(c[i + h] / c[i] - 1 - drift[h])
                        rec[f"t{h}"] = -(c[i + h] / c[i] - 1)
                    else:
                        rec[f"u{h}"] = np.nan; rec[f"t{h}"] = np.nan
                rows.append(rec)
        for w, t in data["trades"][coin].items():
            if len(t):
                trows.append(pd.DataFrame({"coin": coin, "gross": t["profit_loss_percent"],
                                           "net": t["net_profit_loss_percent"],
                                           "dur_h": t["duration_minutes"] / 60}))
        for w, d in data["days"][coin].items():
            book.append(pd.DataFrame({"coin": coin, "w": w, "br": d["book_return"], "cr": d["coin_return"]}))
    df = pd.DataFrame(rows)
    T = pd.concat(trows)
    B = pd.concat(book).dropna()

    def summ(g):
        out = {"n": len(g)}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"u{h}%"] = 100 * x.mean()
            out[f"t_u{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["tot6%"] = 100 * g["t6"].mean()
        return pd.Series(out)

    res = {}
    res["all"] = summ(df).to_frame().T
    res["by_coin"] = df.groupby("coin").apply(summ)
    df["fbin"] = pd.cut(df["f"], [2, 4, 8, 14, 20.01], right=False)
    res["by_forecast"] = df.groupby("fbin").apply(summ)
    df["zbin"] = pd.qcut(df["z"], 5, duplicates="drop")
    res["by_z_quintile"] = df.groupby("zbin").apply(summ)
    df["vrbin"] = pd.qcut(df["vr"], 4, duplicates="drop")
    res["by_volratio"] = df.groupby("vrbin").apply(summ)
    df["r24bin"] = pd.qcut(df["r24"], 5, duplicates="drop")
    res["by_prior24h_ret"] = df.groupby("r24bin").apply(summ)
    df["volbin"] = df.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    res["by_vol30_tercile"] = df.groupby("volbin").apply(summ)
    df["hb"] = df["hour"] // 4
    res["by_hour4"] = df.groupby("hb").apply(summ)
    res["trades_by_coin"] = T.groupby("coin").agg(n=("gross", "size"), gross=("gross", "mean"),
                                                  net=("net", "mean"), dur_h=("dur_h", "median"))
    res["book_by_coin"] = B.groupby("coin").agg(book_mean=("br", "mean"), coin_mean=("cr", "mean"), days=("br", "size"))
    return res
