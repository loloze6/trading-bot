import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    sig = []; daily = []
    for coin, wins in data["bars"].items():
        cr = pd.concat([data["days"][coin][w]["coin_return"] for w in wins]).dropna()
        mu = cr.mean()
        for w, b in wins.items():
            c = b["close"].values; a = b["postRebalance_current_allocation"].fillna(0).values
            f = b["forecast"].fillna(0).values; v = b["volume"].values
            r = np.r_[np.nan, c[1:]/c[:-1]-1]
            s = pd.Series(r)
            vol20 = s.rolling(20, min_periods=10).std().values
            ret30 = pd.Series(c).pct_change(30).values
            ret10 = pd.Series(c).pct_change(10).values
            vr = (pd.Series(v)/pd.Series(v).rolling(30, min_periods=10).mean()).values
            n = len(c)
            for t in range(0, n-5, 5):
                if f[t] >= 2:
                    sig.append(dict(coin=coin, win=w, f=f[t], a=a[t],
                        ex5=c[t+5]/c[t]-1-((1+mu)**5-1), d1=c[t+1]/c[t]-1-mu,
                        ret30=ret30[t], ret10=ret10[t], vol20=vol20[t], vr=vr[t], z=r[t]/vol20[t] if vol20[t]>0 else np.nan,
                        held5=np.mean(a[t:t+5])))
            # days since last forecast>=2, position gain per bar
            last = -999
            for t in range(n-1):
                if f[t] > 0.5: last = t
                g = a[t]*(c[t+1]/c[t]-1)
                daily.append(dict(coin=coin, k=t-last if last>=0 else 99, g=g, a=a[t], mexc=a[t]*mu, ex=c[t+1]/c[t]-1-mu))
    S = pd.DataFrame(sig)
    out["n_grid_signals"] = len(S)
    out["held_on_signal_grid"] = S[["a","held5"]].describe().loc[["mean","50%"]]
    def tt(x): x=x.dropna(); return pd.Series(dict(mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))), n=len(x)))
    for col in ["ret30","ret10","vol20","vr","z"]:
        S["q"] = pd.qcut(S[col].rank(method="first"), 3, labels=False)
        out[f"ex5_by_{col}_tercile"] = S.groupby("q").apply(lambda g: pd.concat([tt(g.ex5), pd.Series(dict(xmed=g[col].median()))]))
    S["up30"] = S.ret30 > 0
    out["ex5_by_ret30_sign"] = S.groupby("up30").apply(lambda g: tt(g.ex5))
    D = pd.DataFrame(daily)
    D["kb"] = D.k.clip(upper=8)
    out["pos_gain_by_days_since_signal"] = D.groupby("kb").agg(gain=("g","mean"), alloc=("a","mean"), ex=("ex","mean"), n=("g","size"))
    # book drawdown and per-window book Sharpe pooled
    rows=[]
    for coin in data["days"]:
        for w, d in data["days"][coin].items():
            rows.append(dict(win=w, br=d["book_return"].dropna().values))
    allb = pd.concat([pd.DataFrame({"win":r["win"],"br":r["br"]}) for r in rows])
    pw = allb.groupby("win").br.agg(["mean","std","size"])
    pw["sh"] = pw["mean"]/pw["std"]*np.sqrt(365)
    out["window_sharpe_top_bottom"] = pw.sort_values("sh").iloc[[0,1,2,-3,-2,-1]]
    return out
