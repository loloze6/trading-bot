import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    days = data["days"]; bars = data["bars"]; trades = data["trades"]
    coins = list(days.keys())
    windows = sorted({w for c in coins for w in days[c].keys()}, key=lambda s: int(s[1:]))
    # book daily, mean of coins per day, in window order
    rows = []
    for w in windows:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        if not frames: continue
        d = pd.concat(frames)
        g = d.groupby("day")[["book_return", "coin_return"]].mean().reset_index()
        g["window"] = w
        rows.append(g)
    B = pd.concat(rows).dropna(subset=["book_return"]).reset_index(drop=True)
    B["eq"] = (1 + B["book_return"]).cumprod()
    B["peak"] = B["eq"].cummax()
    B["dd"] = B["eq"] / B["peak"] - 1
    B["heq"] = (1 + B["coin_return"].fillna(0)).cumprod()
    B["hdd"] = B["heq"] / B["heq"].cummax() - 1
    # per window
    pw = B.groupby("window", sort=False).agg(
        n=("book_return", "size"),
        book_ret=("book_return", lambda x: (1 + x).prod() - 1),
        hold_ret=("coin_return", lambda x: (1 + x.fillna(0)).prod() - 1),
        min_dd_chain=("dd", "min"))
    out["per_window"] = pw
    # drawdown episodes
    eps = []
    in_dd = False
    for i, r in B.iterrows():
        if r["dd"] < 0 and not in_dd:
            in_dd = True; start = i
        if r["dd"] == 0 and in_dd:
            in_dd = False
            seg = B.loc[start:i]
            j = seg["dd"].idxmin()
            eps.append((B.loc[start, "window"], B.loc[j, "window"], B.loc[i, "window"], j - start, i - j, seg["dd"].min(),
                        B.loc[start:j, "coin_return"].add(1).prod() - 1))
    if in_dd:
        seg = B.loc[start:]
        j = seg["dd"].idxmin()
        eps.append((B.loc[start, "window"], B.loc[j, "window"], "open", j - start, len(B) - 1 - j, seg["dd"].min(),
                    B.loc[start:j, "coin_return"].add(1).prod() - 1))
    E = pd.DataFrame(eps, columns=["start_w", "trough_w", "end_w", "days_to_trough", "days_to_recover", "depth", "coins_avg_ret_to_trough"])
    out["worst_dd_episodes"] = E.sort_values("depth").head(8)
    yrs = len(B) / 365
    out["summary"] = pd.Series({"years": yrs, "cagr": B["eq"].iloc[-1] ** (1 / yrs) - 1, "maxdd": B["dd"].min(), "hold_maxdd": B["hdd"].min(),
                                "book_vol_ann": B["book_return"].std() * np.sqrt(365)})
    # per-coin per-window book stats in worst trough window
    # trade features
    T = []
    for c in coins:
        for w, b in bars[c].items():
            if w not in trades[c] or len(trades[c][w]) == 0: continue
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            s = pd.Series(cl)
            r24 = s.pct_change(24)
            mabs = r24.abs().rolling(720, min_periods=240).mean()
            r720 = s.pct_change(720)
            r168 = s.pct_change(168)
            hi720 = s.rolling(720, min_periods=240).max()
            vol = s.pct_change().rolling(720, min_periods=240).std()
            vol_s = s.pct_change().rolling(72, min_periods=48).std()
            tr = trades[c][w]
            for _, t in tr.iterrows():
                et = pd.to_datetime(t["entry_time"]); xt = pd.to_datetime(t["exit_time"])
                i = ts.searchsorted(et, side="right") - 1
                k = ts.searchsorted(xt, side="right") - 1
                if i < 0: continue
                path = cl[i:k + 1] / cl[i] - 1
                T.append(dict(coin=c, window=w, net=t["net_profit_loss_percent"], gross=t["profit_loss_percent"],
                              hours=t["duration_minutes"] / 60, mae=path.min() if len(path) else np.nan,
                              z24=r24[i] / mabs[i] if mabs[i] else np.nan, r720=r720[i], r168=r168[i],
                              off_hi=cl[i] / hi720[i] - 1, volratio=vol_s[i] / vol[i] if vol[i] else np.nan,
                              vol=vol[i], fc=t["entry_forecast"]))
    T = pd.DataFrame(T)
    out["trades_overall"] = pd.Series({"n": len(T), "mean_net": T["net"].mean(), "median_net": T["net"].median(),
                                       "share_win": (T["net"] > 0).mean(), "mean_hours": T["hours"].mean(),
                                       "mean_mae": T["mae"].mean(), "p10_net": T["net"].quantile(.1)})
    def grp(col):
        x = T.dropna(subset=[col]).copy()
        x["q"] = pd.qcut(x[col], 5, labels=False, duplicates="drop")
        return x.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("net", "size"), mean_net=("net", "mean"),
                                  share_win=("net", lambda v: (v > 0).mean()), mean_mae=("mae", "mean"),
                                  worst=("net", "min"))
    for col in ["z24", "r720", "r168", "off_hi", "volratio", "vol", "fc"]:
        out["by_" + col] = grp(col)
    out["by_coin"] = T.groupby("coin").agg(n=("net", "size"), mean_net=("net", "mean"), worst=("net", "min"), mae=("mae", "mean"))
    return out
