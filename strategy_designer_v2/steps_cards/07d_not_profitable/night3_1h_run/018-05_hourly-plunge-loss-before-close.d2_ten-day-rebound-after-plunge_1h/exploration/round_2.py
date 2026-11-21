import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    coins = list(bars.keys())
    P = []; T = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            s = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = s.pct_change().shift(-1)
            a = b["postRebalance_current_allocation"].astype(float)
            r1440 = s.pct_change(1440)
            ma1440 = s.rolling(1440, min_periods=720).mean()
            r336 = s.pct_change(336)
            hi1440 = s.rolling(1440, min_periods=720).max()
            vol720 = s.pct_change().rolling(720, min_periods=240).std()
            vol168 = s.pct_change().rolling(168, min_periods=120).std()
            df = pd.DataFrame(dict(coin=c, window=w, gain=a * r1, alloc=a, r1440=r1440,
                                   above=(s / ma1440 - 1), r336=r336, offhi=s / hi1440 - 1,
                                   vr=vol168 / vol720, r1=r1))
            P.append(df)
            if w in trades[c] and len(trades[c][w]):
                tr = trades[c][w]
                for _, t in tr.iterrows():
                    i = ts.searchsorted(pd.to_datetime(t["entry_time"]), side="right") - 1
                    if i < 0: continue
                    T.append(dict(coin=c, window=w, net=t["net_profit_loss_percent"],
                                  r1440=r1440[i], above=df["above"][i], r336=r336[i],
                                  offhi=df["offhi"][i], vr=df["vr"][i]))
    P = pd.concat(P, ignore_index=True)
    T = pd.DataFrame(T)
    out["time_in_market"] = pd.Series({"share_long_bars": (P["alloc"] > 0).mean(),
                                       "mean_alloc_when_long": P.loc[P["alloc"] > 0, "alloc"].mean()})
    for col in ["r1440", "above", "r336", "offhi", "vr"]:
        x = P.dropna(subset=[col, "gain"]).copy()
        x["q"] = pd.qcut(x[col], 5, labels=False, duplicates="drop")
        g = x.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), bars=("gain", "size"),
                               share_long=("alloc", lambda v: (v > 0).mean()),
                               gain_bps_per_bar=("gain", lambda v: v.mean() * 1e4),
                               coin_bps_per_bar=("r1", lambda v: v.mean() * 1e4),
                               gain_sd_bps=("gain", lambda v: v.std() * 1e4))
        out["bars_by_" + col] = g
        y = T.dropna(subset=[col]).copy()
        if len(y) > 50:
            y["q"] = pd.qcut(y[col], 5, labels=False, duplicates="drop")
            out["trades_by_" + col] = y.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("net", "size"),
                                                         mean_net=("net", "mean"), median=("net", "median"),
                                                         p10=("net", lambda v: v.quantile(.1)),
                                                         share_win=("net", lambda v: (v > 0).mean()))
    # sign split above 60d mean
    x = P.dropna(subset=["above", "gain"])
    out["above_vs_below_ma60"] = x.groupby(x["above"] > 0).agg(bars=("gain", "size"),
        share_long=("alloc", lambda v: (v > 0).mean()), gain_bps=("gain", lambda v: v.mean() * 1e4),
        gain_t=("gain", lambda v: v.mean() / v.std() * np.sqrt(len(v))))
    # bars without 60d history
    out["share_bars_no_r1440"] = P["r1440"].isna().mean()
    # gain in the worst stretch windows vs rest
    P["bad"] = P["window"].isin(["w7", "w9", "w13", "w14"])
    out["bad_windows"] = P.groupby("bad").agg(share_long=("alloc", lambda v: (v > 0).mean()),
        gain_bps=("gain", lambda v: v.mean() * 1e4), coin_bps=("r1", lambda v: v.mean() * 1e4),
        mean_above=("above", "mean"))
    return out
