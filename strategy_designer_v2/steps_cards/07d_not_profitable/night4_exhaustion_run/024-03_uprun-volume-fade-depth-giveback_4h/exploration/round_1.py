import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    rows = []
    book = []
    trades_all = []
    for coin, wins in data["bars"].items():
        # drift and usual move on 18-bar grid
        grid_rets = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            grid_rets += list(c[idx + H] / c[idx] - 1)
        drift = np.mean(grid_rets); usual = np.std(grid_rets)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            v = b["volume"].values
            f = b["forecast"].fillna(0).values
            rg = b["debug_info.components.run_gain.last_history_value"].values
            vf = b["debug_info.components.vol_fade.last_history_value"].values
            up = np.r_[False, c[1:] > c[:-1]]
            streak = np.zeros(n)
            for i in range(1, n):
                streak[i] = streak[i-1] + 1 if up[i] else 0
            ret30 = pd.Series(c).pct_change(180).values
            ret5 = pd.Series(c).pct_change(30).values
            fwd = {}
            for h in (6, 12, 18, 36):
                fr = np.full(n, np.nan); fr[:n-h] = c[h:] / c[:n-h] - 1
                fwd[h] = fr
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            cell = np.arange(n) // H
            seen = set()
            for i in range(n):
                if f[i] <= -2 and cell[i] not in seen and not np.isnan(fwd[18][i]):
                    seen.add(cell[i])
                    rows.append(dict(coin=coin, w=w, year=yr[i], rg=rg[i], vf=vf[i], streak=streak[i],
                                     ret30=ret30[i], ret5=ret5[i], f=f[i],
                                     un6=-(fwd[6][i]-drift/3), un12=-(fwd[12][i]-drift*2/3),
                                     un18=-(fwd[18][i]-drift), un36=-(fwd[36][i]-2*drift) if not np.isnan(fwd[36][i]) else np.nan,
                                     tot18=-fwd[18][i], st=-(fwd[18][i]-drift)/usual))
        for w, d in data["days"][coin].items():
            bb = wins[w].copy()
            bb["day"] = pd.to_datetime(bb["timestamp"]).dt.floor("D")
            al = bb.groupby("day")["postRebalance_current_allocation"].mean()
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"])
            dd = dd.merge(al.rename("alloc").reset_index(), on="day", how="left")
            dd["coin"] = coin; dd["w"] = w
            book.append(dd)
        for w, t in data["trades"][coin].items():
            t = t.copy(); t["coin"] = coin; t["w"] = w; trades_all.append(t)
    R = pd.DataFrame(rows)
    B = pd.concat(book); T = pd.concat(trades_all)
    out = {}
    def summ(g):
        return pd.Series(dict(n=len(g), un18=g.un18.mean(), t=g.un18.mean()/(g.un18.std()/np.sqrt(len(g))),
                              tot18=g.tot18.mean(), un6=g.un6.mean(), un12=g.un12.mean(), un36=g.un36.mean()))
    out["all"] = summ(R)
    R["rg_q"] = pd.qcut(R.rg, 5, labels=False, duplicates="drop")
    out["by_run_gain_quintile"] = R.groupby("rg_q").apply(summ)
    R["vf_q"] = pd.qcut(R.vf.rank(method="first"), 5, labels=False)
    out["by_vol_fade_quintile"] = R.groupby("vf_q").apply(summ)
    R["sk"] = R.streak.clip(upper=6)
    out["by_streak_len"] = R.groupby("sk").apply(summ)
    R["r30_q"] = pd.qcut(R.ret30, 5, labels=False)
    out["by_30d_return_quintile"] = R.groupby("r30_q").apply(summ)
    R["r5_q"] = pd.qcut(R.ret5, 5, labels=False)
    out["by_5d_return_quintile"] = R.groupby("r5_q").apply(summ)
    out["by_year"] = R.groupby("year").apply(summ)
    out["by_coin"] = R.groupby("coin").apply(summ)
    B = B.dropna(subset=["book_return"])
    cm = B.groupby("coin")["coin_return"].mean()
    B["mkt"] = B.alloc * B.coin.map(cm)
    daily = B.groupby(["w", "day"]).agg(book=("book_return", "mean"), mkt=("mkt", "mean"), coinr=("coin_return", "mean"), alloc=("alloc", "mean"))
    out["book_decomp"] = pd.Series(dict(book_mean=daily.book.mean(), market_part=daily.mkt.mean(),
                                        timing=daily.book.mean()-daily.mkt.mean(), mean_alloc=daily.alloc.mean(),
                                        share_days_short=(daily.alloc < -0.01).mean()))
    out["trades"] = pd.Series(dict(n=len(T), gross_mean=T.profit_loss_percent.mean(), net_mean=T.net_profit_loss_percent.mean(),
                                   win=(T.profit_loss_percent > 0).mean(), dur_h=T.duration_minutes.mean()/60))
    return out
