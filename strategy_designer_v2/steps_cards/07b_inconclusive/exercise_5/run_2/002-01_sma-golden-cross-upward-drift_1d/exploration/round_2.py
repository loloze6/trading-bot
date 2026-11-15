import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df["debug_info.components.sma_cross.last_history_value"].values if "debug_info.components.sma_cross.last_history_value" in df else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"])
            # days since raw spread turned positive (inside window)
            since = np.full(len(df), np.nan); cnt = np.nan
            for i in range(len(df)):
                if not np.isnan(raw[i]) and raw[i] > 0:
                    if i > 0 and not np.isnan(raw[i-1]) and raw[i-1] > 0 and not np.isnan(cnt):
                        cnt += 1
                    elif i > 0 and not np.isnan(raw[i-1]) and raw[i-1] <= 0:
                        cnt = 0
                    else:
                        cnt = cnt + 1 if not np.isnan(cnt) else np.nan
                else:
                    cnt = np.nan
                since[i] = cnt
            for h in [10, 20]:
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, h=h, f=f[i], raw=raw[i], since=since[i],
                                     past20=(c[i]/c[i-20]-1) if i >= 20 else np.nan,
                                     past60=(c[i]/c[i-60]-1) if i >= 60 else np.nan,
                                     r=c[i+h]/c[i]-1))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby(["coin", "h"])["r"].transform("mean")
    out = {}
    def reg(x, col):
        x = x.dropna(subset=[col, "ex"])
        if len(x) < 20: return pd.Series(dict(n=len(x), slope=np.nan, t=np.nan))
        s = stats.linregress(x[col], x["ex"]); return pd.Series(dict(n=len(x), slope=s.slope, t=s.slope/s.stderr))
    res = []
    for h in [10, 20]:
        g = d[d.h == h]
        for cond, gg in [("all", g), ("on", g[g.f > 0]), ("off", g[g.f <= 0])]:
            for col in ["past20", "past60"]:
                s = reg(gg, col); res.append(dict(h=h, cond=cond, col=col, **s.to_dict()))
    out["slope_on_past_return"] = pd.DataFrame(res)
    g = d[d.h == 10].dropna(subset=["past20"]).copy()
    g["on"] = g.f > 0
    g["p20q"] = pd.qcut(g["past20"], 5, labels=False)
    out["h10_ex_by_on_and_past20q"] = g.groupby(["on", "p20q"])["ex"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    on = g[g.on].copy()
    on["p20pos"] = on.past20 > 0
    out["h10_on_past20sign_by_coin"] = on.groupby(["coin", "p20pos"])["ex"].mean().unstack()
    out["h10_on_past20sign_by_year"] = on.groupby(["year", "p20pos"])["ex"].mean().unstack()
    gs = d[(d.h == 10) & d.since.notna()].copy()
    gs["sb"] = pd.cut(gs["since"], [-1, 30, 90, 180, 10000])
    out["h10_by_days_since_cross"] = gs.groupby("sb")["ex"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    return out
