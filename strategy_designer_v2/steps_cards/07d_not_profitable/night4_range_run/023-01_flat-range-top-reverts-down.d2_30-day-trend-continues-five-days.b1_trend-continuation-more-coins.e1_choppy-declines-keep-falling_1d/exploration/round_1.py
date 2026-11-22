import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars, trades, days = data["bars"], data["trades"], data["days"]
    out = {}
    # coin mean daily return over all windows
    coin_mu = {}
    for c in days:
        r = pd.concat([d["coin_return"] for d in days[c].values()]).dropna()
        coin_mu[c] = r.mean()
    # book daily: mean of coins per day position; build per coin-window daily book returns + avg alloc
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["alloc"] = b["postRebalance_current_allocation"]
            b["g"] = b["alloc"] * (b["close"].shift(-1) / b["close"] - 1)
            b["fee"] = b["postRebalance_total_value"] / b["total_portfolio_value"] - 1
            d = days[c][w]
            br = d["book_return"].values
            tmp = pd.DataFrame({"coin": c, "win": w, "book": br,
                                "coinret": d["coin_return"].values,
                                "alloc_prev": b["alloc"].shift(1).values[:len(br)] if len(b)==len(d) else np.nan,
                                "gross": b["g"].shift(1).values[:len(br)] if len(b)==len(d) else np.nan,
                                "fee": b["fee"].values[:len(br)] if len(b)==len(d) else np.nan,
                                "year": pd.to_datetime(d["day"]).dt.year.values})
            tmp["mkt"] = tmp["alloc_prev"] * coin_mu[c]
            rows.append(tmp)
    D = pd.concat(rows).dropna(subset=["book"])
    out["decomp_per_coinday"] = pd.Series({
        "book_mean": D.book.mean(), "gross_mean": D.gross.mean(), "fee_mean": D.fee.mean(),
        "market_part": D.mkt.mean(), "timing": D.book.mean() - D.mkt.mean(),
        "share_days_short": (D.alloc_prev < 0).mean(), "mean_alloc_when_short": D.alloc_prev[D.alloc_prev<0].mean()})
    g = D.groupby("win").agg(book=("book","mean"), mkt=("mkt","mean"), coin=("coinret","mean"), short=("alloc_prev", lambda x:(x<0).mean()))
    out["by_window"] = g
    out["by_year"] = D.groupby("year").agg(book=("book","mean"), mkt=("mkt","mean"), coin=("coinret","mean"))
    # trades
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values() if len(t)])
    T["days"] = T.duration_minutes/1440
    out["trades"] = pd.Series({"n": len(T), "gross_mean": T.profit_loss_percent.mean(),
        "net_mean": T.net_profit_loss_percent.mean(), "median_days": T.days.median(),
        "win_rate_net": (T.net_profit_loss_percent>0).mean(), "share_short": (T.side=="SHORT").mean()})
    T["fq"] = pd.qcut(T.entry_forecast, 4, duplicates="drop")
    out["trades_by_entry_forecast"] = T.groupby("fq", observed=True).agg(n=("days","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), days=("days","median"))
    # cases on grid: 5-day return after short bars by coin's prior 30d return quantile and 60-day trend
    cs = []
    for c in bars:
        allr = []
        for w, b in bars[c].items():
            cl = b["close"].values
            f = b["forecast"].values
            for i in range(0, len(b)-5, 5):
                allr.append(cl[i+5]/cl[i]-1)
        drift = np.mean(allr) if allr else np.nan
        for w, b in bars[c].items():
            cl = b["close"].reset_index(drop=True)
            f = b["forecast"].values
            r30 = cl/cl.shift(30)-1
            r90 = cl/cl.shift(90)-1
            for i in range(0, len(b)-5, 5):
                if f[i] < 0:
                    cs.append((c, w, f[i], -(cl[i+5]/cl[i]-1), -(cl[i+5]/cl[i]-1-drift), r30[i], r90[i], drift))
    C = pd.DataFrame(cs, columns=["coin","win","f","tot","unus","r30","r90","drift"])
    out["grid_short_n"] = len(C)
    for col in ["f","r30","r90"]:
        q = pd.qcut(C[col], 4, duplicates="drop")
        out["grid_by_"+col] = C.groupby(q, observed=True).agg(n=("tot","size"), total=("tot","mean"), unusual=("unus","mean"), t_tot=("tot", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    C["coin_drift_pos"] = C.drift > 0
    out["grid_by_drift_sign"] = C.groupby("coin_drift_pos").agg(n=("tot","size"), total=("tot","mean"), unusual=("unus","mean"))
    return out
