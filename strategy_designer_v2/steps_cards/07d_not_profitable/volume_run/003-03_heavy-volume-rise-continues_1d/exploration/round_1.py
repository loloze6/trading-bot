import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    sig = []
    for coin, wins in data["bars"].items():
        # coin mean daily return over all windows
        cr = pd.concat([data["days"][coin][w]["coin_return"] for w in wins]).dropna()
        mu = cr.mean()
        for w, b in wins.items():
            d = data["days"][coin][w]
            c = b["close"].values
            a = b["postRebalance_current_allocation"].fillna(0).values
            f = b["forecast"].fillna(0).values
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            fees = (b["total_portfolio_value"]-b["postRebalance_total_value"]).clip(lower=0).sum()/b["total_portfolio_value"].iloc[0]
            rows.append(dict(coin=coin, win=w, book=d["book_return"].mean(), hold=d["coin_return"].mean(),
                             mkt=a.mean()*mu, expo=(a!=0).mean(), absalloc=np.abs(a).mean(), fees=fees))
            # forward returns after signal bars, day k
            for t in range(len(c)):
                if f[t] > 0:
                    rec = dict(coin=coin, win=w, f=f[t], a=a[t])
                    for k in range(1, 11):
                        rec[f"d{k}"] = c[t+k]/c[t+k-1]-1-mu if t+k < len(c) else np.nan
                    sig.append(rec)
    R = pd.DataFrame(rows)
    out["by_coin"] = R.groupby("coin")[["book","hold","mkt","expo","absalloc","fees"]].mean()
    R["wn"] = R.win.str[1:].astype(int)
    out["by_window"] = R.groupby("wn")[["book","hold","fees"]].mean()
    S = pd.DataFrame(sig)
    out["n_signal_bars"] = len(S)
    dk = [f"d{k}" for k in range(1,11)]
    m = S[dk].mean(); t = S[dk].mean()/(S[dk].std()/np.sqrt(S[dk].count()))
    out["excess_by_day_after_signal"] = pd.DataFrame({"mean":m,"t":t,"n":S[dk].count()})
    S["fb"] = pd.qcut(S.f.rank(method="first"), 4, labels=False)
    S["cum5"] = S[[f"d{k}" for k in range(1,6)]].sum(axis=1)
    out["by_forecast_q"] = S.groupby("fb").agg(fmean=("f","mean"), alloc=("a","mean"), d1=("d1","mean"), cum5=("cum5","mean"), n=("f","size"))
    out["alloc_quantiles_on_signal"] = S.a.describe()
    # trades
    T = pd.concat([data["trades"][c][w] for c in data["trades"] for w in data["trades"][c]])
    out["trades"] = pd.Series(dict(n=len(T), dur_days=T.duration_minutes.mean()/1440, pl=T.profit_loss_percent.mean(), net=T.net_profit_loss_percent.mean(), win=(T.net_profit_loss_percent>0).mean()))
    return out
