import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    tfun = lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    H = []
    ev = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(720, min_periods=300).std()
            ret24 = c / c.shift(24) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "year": ts.dt.year.values,
                               "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values,
                               "r": r1.values, "vol": vol.values,
                               "past24z": (ret24 / (vol * np.sqrt(24))).values})
            # evening return: close of hour-20 bar -> close of hour-22 bar (bars 21,22)
            H.append(df)
            cv = c.values; n = len(cv)
            hv = ts.dt.hour.values
            for i in np.where(hv == 20)[0]:
                if i + 2 >= n or i - 24 < 0 or np.isnan(vol.iloc[i]):
                    continue
                if ts.iloc[i + 2] - ts.iloc[i] != pd.Timedelta(hours=2):
                    continue
                ev.append(dict(coin=coin, win=w, year=ts.iloc[i].year, wd=ts.iloc[i].weekday(),
                               ev2=cv[i + 2] / cv[i] - 1, s=vol.iloc[i] * np.sqrt(2),
                               p24z=df["past24z"].iloc[i], vol=vol.iloc[i]))
    H = pd.concat(H).dropna(subset=["r"])
    E = pd.DataFrame(ev).dropna()
    E["z"] = E["ev2"] / E["s"]
    out["evening2h_by_coin"] = E.groupby("coin").agg(n=("ev2", "size"), bp=("ev2", lambda x: x.mean()*1e4),
                                                    t=("ev2", tfun), z=("z", "mean"))
    out["evening2h_by_year"] = E.groupby("year").agg(n=("ev2", "size"), bp=("ev2", lambda x: x.mean()*1e4),
                                                    t=("ev2", tfun))
    out["evening2h_by_wd"] = E.groupby("wd").agg(n=("ev2", "size"), bp=("ev2", lambda x: x.mean()*1e4),
                                                t=("ev2", tfun))
    E["vq"] = E.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 4, labels=False))
    out["evening2h_by_vol_quartile"] = E.groupby("vq").agg(n=("ev2", "size"), bp=("ev2", lambda x: x.mean()*1e4),
                                                          t=("ev2", tfun), z=("z", "mean"))
    E["pq"] = pd.qcut(E["p24z"], 5, labels=False)
    out["evening2h_by_past24z_quintile"] = E.groupby("pq").agg(n=("ev2", "size"), p24z=("p24z", "mean"),
                                                              bp=("ev2", lambda x: x.mean()*1e4), t=("ev2", tfun))
    sl = stats.linregress(E["p24z"], E["z"])
    out["evening_z_on_past24z"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(E)})
    # hour 21 and 3 and 14 per coin
    out["hour21_by_coin_bp_t"] = H[H.hour == 21].groupby("coin")["r"].agg(bp=lambda x: x.mean()*1e4, t=tfun)
    out["hour3_by_coin_bp_t"] = H[H.hour == 3].groupby("coin")["r"].agg(bp=lambda x: x.mean()*1e4, t=tfun)
    out["hour14_by_coin_bp_t"] = H[H.hour == 14].groupby("coin")["r"].agg(bp=lambda x: x.mean()*1e4, t=tfun)
    # Saturday mean by coin
    out["saturday_by_coin_bp_t"] = H[H.wd == 5].groupby("coin")["r"].agg(bp=lambda x: x.mean()*1e4, t=tfun)
    # book by window: share of windows positive, and hold
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D).dropna(subset=["book_return"])
    bw = D.groupby("win").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    out["book_windows_pos_share"] = pd.Series({"book_pos": (bw.book > 0).mean(), "coin_pos": (bw.coin > 0).mean(),
                                               "corr": bw.book.corr(bw.coin)})
    return out
