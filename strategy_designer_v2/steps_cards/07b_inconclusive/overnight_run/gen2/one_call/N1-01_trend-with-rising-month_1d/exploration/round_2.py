import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    allfwd = {}
    # first pass: per-coin forward returns indexed by timestamp
    fwd_ts = {}
    for coin, wins in data["bars"].items():
        fw = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            f = np.full(n, np.nan)
            if n > 20:
                f[:n-20] = c[20:] / c[:n-20] - 1
            fw.append(f[~np.isnan(f)])
            for i in range(n):
                fwd_ts[(coin, pd.Timestamp(df["timestamp"].iloc[i]))] = f[i]
        allfwd[coin] = np.mean(np.concatenate(fw))
    fts = pd.Series(fwd_ts)
    fts.index = pd.MultiIndex.from_tuples(fts.index, names=["coin", "ts"])
    mkt = fts.groupby(level="ts").mean()
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            fc = df["forecast"].astype(float).values
            bir = pd.to_numeric(df.get("debug_info.bars_in_regime", pd.Series(np.nan, index=df.index)), errors="coerce").values
            for i in range(0, n - 20, 20):
                ts = pd.Timestamp(df["timestamp"].iloc[i])
                f = c[i+20]/c[i]-1
                f5 = c[i+5]/c[i]-1
                rows.append(dict(coin=coin, w=w, fwd=f, f5=f5, fc=fc[i], bir=bir[i],
                                 mkt=mkt.get(ts, np.nan),
                                 btc=fts.get(("BTCUSD", ts), np.nan)))
    R = pd.DataFrame(rows)
    R["ex"] = R["fwd"] - R["coin"].map(allfwd)
    R["rel"] = R["fwd"] - R["mkt"]
    R["lr"] = np.log1p(R["fwd"])
    A = R[R["fc"] > 0].copy()
    I = R[R["fc"] <= 0].copy()

    def summ(x):
        x = pd.Series(x).dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), median=x.median(), hit=(x > 0).mean(),
                              t=stats.ttest_1samp(x, 0).statistic if len(x) > 2 else np.nan))
    out = {}
    out["active_measures"] = pd.DataFrame({
        "ex": summ(A["ex"]), "rel_to_market": summ(A["rel"]),
        "logret": summ(A["lr"]), "raw_fwd5": summ(A["f5"])}).T
    out["inactive_measures"] = pd.DataFrame({
        "ex": summ(I["ex"]), "rel_to_market": summ(I["rel"]), "logret": summ(I["lr"])}).T
    # Welch active vs inactive log return
    out["welch_logret_A_vs_I"] = float(stats.ttest_ind(A["lr"].dropna(), I["lr"].dropna(), equal_var=False).statistic)
    A["fresh"] = pd.cut(A["bir"], [-1, 10, 40, 1e9], labels=["<=10", "11-40", ">40"])
    out["by_bars_in_regime"] = A.groupby("fresh").apply(lambda g: summ(g["lr"]))
    out["bir_desc"] = A["bir"].describe()
    # market (BTC-proxy) state: is BTC itself trending up? use other coins' active share at same ts
    act_share = R.assign(a=(R["fc"] > 0).astype(float)).groupby("mkt")["a"]
    # by coin, rel to market
    out["by_coin_rel"] = A.groupby("coin").apply(lambda g: summ(g["rel"]))
    out["by_coin_logret"] = A.groupby("coin").apply(lambda g: summ(g["lr"]))
    # share of variance explained by market
    AA = A.dropna(subset=["fwd", "mkt"])
    out["corr_fwd_mkt_active"] = float(np.corrcoef(AA["fwd"], AA["mkt"])[0, 1])
    return out
