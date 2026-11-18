import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, ws in data["bars"].items():
        # coin mean daily return over all windows
        allr = []
        for w, b in ws.items():
            c = b["close"].values
            allr.append(c[1:]/c[:-1]-1)
        mu1 = np.nanmean(np.concatenate(allr))
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            fc = b["forecast"].fillna(0).values
            for t in np.where(fc > 0)[0]:
                r = {}
                for k in range(1, 6):
                    # return of day k after flush (from close t+k-1 to t+k)
                    r[f"d{k}"] = c[t+k]/c[t+k-1]-1-mu1 if t+k < n else np.nan
                rng = b["high"][t]-b["low"][t]
                prev20 = c[max(0,t-20)]
                r.update(dict(coin=coin, window=w, alloc=alloc[t],
                              alloc_next=alloc[t+1] if t+1<n else np.nan,
                              fc=fc[t],
                              ret20=c[t]/prev20-1 if t>=20 else np.nan,
                              ret5=c[t]/c[max(0,t-5)]-1 if t>=5 else np.nan,
                              year=pd.Timestamp(b["timestamp"][t]).year))
                rows.append(r)
    df = pd.DataFrame(rows)
    out = {}
    def tt(x):
        x = x.dropna(); return pd.Series(dict(mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>1 else np.nan, n=len(x)))
    out["excess daily ret by day after flush"] = pd.DataFrame({k: tt(df[k]) for k in ["d1","d2","d3","d4","d5"]}).T
    out["alloc on flush / next bar"] = df[["alloc","alloc_next","fc"]].describe()
    df["cum3"] = df[["d1","d2","d3"]].sum(axis=1, min_count=3)
    df["q20"] = pd.qcut(df["ret20"], 3, labels=["low","mid","high"])
    out["by prior 20d return tercile"] = df.groupby("q20")[["d1","cum3"]].agg(["mean","count"])
    df["q5"] = pd.qcut(df["ret5"], 3, labels=["low","mid","high"])
    out["by prior 5d return tercile"] = df.groupby("q5")[["d1","cum3"]].agg(["mean","count"])
    out["by year"] = df.groupby("year")[["d1","cum3"]].agg(["mean","count"])
    out["by coin"] = df.groupby("coin")[["d1","cum3"]].agg(["mean","count"])
    df["fq"] = pd.qcut(df["fc"].rank(method="first"), 3, labels=["low","mid","high"])
    out["by forecast tercile"] = df.groupby("fq")[["d1","cum3"]].agg(["mean","count"])
    # trades
    tr = pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades"] = pd.Series(dict(n=len(tr), mean_dur_days=tr["duration_minutes"].mean()/1440,
        mean_pl=tr["profit_loss_percent"].mean(), mean_net=tr["net_profit_loss_percent"].mean(),
        t_net=stats.ttest_1samp(tr["net_profit_loss_percent"].dropna(),0).statistic))
    # book days in position
    d = pd.concat([x for ws in data["days"].values() for x in ws.values()])
    out["book"] = pd.Series(dict(days=len(d), nonzero_days=(d["book_return"].abs()>1e-9).sum(),
        mean_nonzero=d.loc[d["book_return"].abs()>1e-9,"book_return"].mean()))
    return out
