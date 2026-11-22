import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # portfolio daily
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    P = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    P = P.dropna()
    eq = (1 + P["book_return"]).cumprod().values
    peak = np.maximum.accumulate(eq)
    dd = eq / peak - 1
    P["dd"] = dd
    i = int(np.argmin(dd)); pk = int(np.argmax(eq[:i + 1]))
    seg = P.iloc[pk:i + 1]
    out["deepest_fall"] = pd.Series({"depth": dd[i], "days": i - pk, "windows_from": seg.wn.iloc[0], "windows_to": seg.wn.iloc[-1],
                                     "coin_chain_ret": (1 + seg.coin_return).prod() - 1, "book_chain_ret": (1 + seg.book_return).prod() - 1})
    pw = P.groupby("wn").apply(lambda g: pd.Series({
        "book": (1 + g.book_return).prod() - 1, "coin": (1 + g.coin_return).prod() - 1,
        "maxdd": ((1 + g.book_return).cumprod() / (1 + g.book_return).cumprod().cummax() - 1).min()}))
    out["per_window"] = pw.round(4)
    # book daily return vs coin daily return state
    P["coin_q"] = pd.qcut(P.coin_return, 5, labels=False)
    out["book_by_coin_day_quintile"] = P.groupby("coin_q")[["book_return", "coin_return"]].mean()
    # trades with entry features
    T = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            b = data["bars"][c][w].reset_index(drop=True)
            if len(t) == 0: continue
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values; vol = b["volume"].values
            r = pd.Series(cl).pct_change()
            absmv = r.abs().rolling(180, min_periods=60).mean().values
            for _, x in t.iterrows():
                e = pd.to_datetime(x["entry_time"])
                k = ts.searchsorted(e)
                if k >= len(b): continue
                ret30 = cl[k] / cl[k - 180] - 1 if k >= 180 else np.nan
                ret7 = cl[k] / cl[k - 42] - 1 if k >= 42 else np.nan
                vol30 = r.iloc[max(0, k - 180):k].std()
                volshort = r.iloc[max(0, k - 18):k].std()
                # streak length
                s = 0; j = k
                while j > 0 and cl[j] < cl[j - 1]: s += 1; j -= 1
                loss = (cl[k] / cl[j] - 1) / absmv[k] if absmv[k] > 0 else np.nan
                fwd_low = (b["low"].values[k + 1:k + 19].min() / cl[k] - 1) if k + 1 < len(b) else np.nan
                T.append(dict(coin=c, wn=int(w[1:]), pnl=x["net_profit_loss_percent"], dur=x["duration_minutes"] / 240,
                              ret30=ret30, ret7=ret7, volratio=volshort / vol30 if vol30 > 0 else np.nan,
                              streak=s, loss_um=loss, fwd_low=fwd_low, fc=x["entry_forecast"]))
    T = pd.DataFrame(T)
    out["trades_summary"] = pd.Series({"n": len(T), "mean_pnl": T.pnl.mean(), "median": T.pnl.median(),
                                       "share_win": (T.pnl > 0).mean(), "mean_dur_bars": T.dur.mean(),
                                       "worst5pct_mean": T.pnl[T.pnl <= T.pnl.quantile(.05)].mean()})
    def grp(col):
        g = T.dropna(subset=[col]).copy()
        g["q"] = pd.qcut(g[col], 5, labels=False, duplicates="drop")
        return g.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("pnl", "size"), mean_pnl=("pnl", "mean"),
                                  share_win=("pnl", lambda v: (v > 0).mean()), p10=("pnl", lambda v: v.quantile(.1)),
                                  fwd_low=("fwd_low", "mean"))
    for col in ["ret30", "ret7", "volratio", "loss_um", "streak", "fc"]:
        out["by_" + col] = grp(col).round(4)
    out["pnl_by_coin"] = T.groupby("coin").pnl.agg(["size", "mean", "median"]).round(3)
    return out
