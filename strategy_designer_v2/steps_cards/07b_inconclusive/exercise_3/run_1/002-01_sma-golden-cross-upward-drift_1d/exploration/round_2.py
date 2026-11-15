import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].values
            raw = df["debug_info.components.sma_cross.last_history_value"].values
            vol = df["sizing_realised_vol"].values
            n = len(df)
            sgn = np.sign(raw)
            # bars since last cross inside window, nan if none seen
            since = np.full(n, np.nan); last = None
            for i in range(1, n):
                if not np.isnan(sgn[i]) and not np.isnan(sgn[i-1]) and sgn[i] != sgn[i-1]:
                    last = i
                if last is not None: since[i] = i - last
            # 10-bar momentum of raw (spread change), known at close
            draw = np.full(n, np.nan); draw[10:] = raw[10:] - raw[:-10]
            past = np.full(n, np.nan); past[20:] = c[20:]/c[:-20]-1
            for h in [10, 20, 40]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, f=f[i], raw=raw[i], since=since[i], draw=draw[i],
                                     vol=vol[i], past=past[i], ret=c[i+h]/c[i]-1,
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin","h"])["ret"].transform("mean")
    out = {}
    def tm(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    d["state"] = np.where(d.raw>0, "up", "down")
    d["fresh"] = pd.cut(d["since"], [-1, 30, 200]).astype(str)
    out["state_fresh"] = d.groupby(["h","state","fresh"])["ex"].apply(tm).unstack()
    # within up-state: spread widening vs narrowing
    up = d[d.raw>0].copy()
    up["dsign"] = np.where(up.draw>0, "widening", "narrowing")
    out["up_by_spreadchange"] = up.groupby(["h","dsign"])["ex"].apply(tm).unstack()
    dn = d[d.raw<0].copy(); dn["dsign"] = np.where(dn.draw>0, "narrowing", "widening")
    out["down_by_spreadchange"] = dn.groupby(["h","dsign"])["ex"].apply(tm).unstack()
    # up-state by vol tercile
    up["vt"] = up.groupby("h")["vol"].transform(lambda x: pd.qcut(x, 3, labels=["lo","mid","hi"]))
    out["up_by_vol"] = up.groupby(["h","vt"])["ex"].apply(tm).unstack()
    # past 20-bar return slope on ex at 10, 20 (own momentum)
    m = []
    for h, g in d.dropna(subset=["past"]).groupby("h"):
        s = stats.linregress(g.past, g.ex); m.append(dict(h=h, n=len(g), slope=s.slope, t=s.slope/s.stderr))
        gu = g[g.raw>0]; s = stats.linregress(gu.past, gu.ex); m[-1].update(up_slope=s.slope, up_t=s.slope/s.stderr)
    out["past20_slope"] = pd.DataFrame(m)
    # book decomposition
    rr = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            dd = days[coin][w].copy()
            b = df.copy(); b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last().shift(1)
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D") if not np.issubdtype(dd["day"].dtype, np.datetime64) else dd["day"].dt.floor("D")
            dd = dd.merge(pos.rename("pos").reset_index(), on="day", how="left")
            dd["coin"] = coin; rr.append(dd)
    D = pd.concat(rr)
    D["cmean"] = D.groupby("coin")["coin_return"].transform("mean")
    D["mkt"] = D["pos"] * D["cmean"]
    out["book"] = pd.Series(dict(book_mean=D.book_return.mean(), mkt_part=D.mkt.mean(),
                                 timing=D.book_return.mean()-D.mkt.mean(), mean_pos=D.pos.mean(),
                                 hold_mean=D.coin_return.mean()))
    return out
