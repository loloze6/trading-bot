import numpy as np
import pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0:
        return np.nan
    return x.mean() / (x.std() / np.sqrt(len(x)))

def _summ(g, col):
    return pd.Series({"n": g[col].notna().sum(), "mean_bps": g[col].mean()*1e4, "t": _t(g[col])})

def explore(data):
    out = {}
    rows = {4: [], 24: [], 1: []}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            vr = b["volume"].astype(float) / b["volume"].astype(float).rolling(720, min_periods=240).mean()
            z = r1 / sd
            r24p = c / c.shift(24) - 1
            sd24 = sd * np.sqrt(24)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            for h in (1, 4, 24):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                df = pd.DataFrame({
                    "coin": coin, "win": w, "z": z.values[idx], "vr": vr.values[idx],
                    "z24": (r24p / sd24).values[idx], "sdlvl": sd.values[idx],
                    "hour": ts.dt.hour.values[idx], "wd": ts.dt.weekday.values[idx],
                    "fwd": fwd.values[idx],
                    "fwd_unit": (fwd / (sd*np.sqrt(h))).values[idx],
                })
                rows[h].append(df)
    G = {h: pd.concat(v, ignore_index=True) for h, v in rows.items()}
    for h, g in G.items():
        drift = g.groupby("coin")["fwd"].transform("mean")
        g["unus"] = g["fwd"] - drift
    # 1. move size x volume, signed by the move's direction (continuation positive)
    for h in (4, 24):
        g = G[h].dropna(subset=["z", "vr", "unus"]).copy()
        g["az"] = pd.cut(g["z"].abs(), [0, 1, 2, 3, 5, 100])
        g["vrb"] = pd.cut(g["vr"], [0, 1, 2, 4, 1e9])
        g["cont"] = np.sign(g["z"]) * g["unus"]
        out[f"cont_{h}h_by_absz_vol"] = g.groupby(["az", "vrb"], observed=True).apply(lambda x: _summ(x, "cont"))
        g["dir"] = np.where(g["z"] > 0, "up", "down")
        g2 = g[g["z"].abs() > 2]
        out[f"unus_{h}h_after_|z|>2_by_dir_vol"] = g2.groupby(["dir", "vrb"], observed=True).apply(lambda x: _summ(x, "unus"))
    # 2. 24h past return (scaled) -> next 24h
    g = G[24].dropna(subset=["z24", "unus"]).copy()
    g["q"] = pd.qcut(g["z24"], 5, labels=False)
    out["unus_24h_by_past24_quintile"] = g.groupby("q").apply(lambda x: _summ(x, "unus"))
    # 3. vol level -> 24h move
    g["vq"] = g.groupby("coin")["sdlvl"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["unus_24h_by_vol_tercile"] = g.groupby("vq").apply(lambda x: _summ(x, "unus"))
    # 4. hour of day, 1h returns
    g1 = G[1].dropna(subset=["unus"])
    out["unus_1h_by_hour"] = g1.groupby("hour").apply(lambda x: _summ(x, "unus"))
    # 5. weekday, daily
    d = pd.concat([df.assign(coin=c, win=w) for c, ws in data["days"].items() for w, df in ws.items()])
    d["wd"] = pd.to_datetime(d["day"]).dt.weekday
    d["cu"] = d["coin_return"] - d.groupby("coin")["coin_return"].transform("mean")
    out["coin_day_by_weekday"] = d.groupby("wd").apply(lambda x: _summ(x, "cu"))
    # 6. book
    bk = d.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
    out["book_summary"] = pd.Series({"days": len(bk), "book_mean_bps": bk.br.mean()*1e4, "book_t": _t(bk.br),
                                     "coin_mean_bps": bk.cr.mean()*1e4, "corr_book_coin": bk.br.corr(bk.cr)})
    out["book_by_weekday"] = d.assign(wd=d["wd"]).groupby("wd").apply(lambda x: _summ(x, "book_return"))
    # 7. trades
    tr = pd.concat([df.assign(coin=c) for c, ws in data["trades"].items() for w, df in ws.items()])
    tr["fq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 5, labels=False)
    out["trades_by_entry_forecast_q"] = tr.groupby("fq").agg(n=("net_profit_loss_percent", "size"),
        fc=("entry_forecast", "mean"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur_h=("duration_minutes", lambda s: s.mean()/60))
    return out
