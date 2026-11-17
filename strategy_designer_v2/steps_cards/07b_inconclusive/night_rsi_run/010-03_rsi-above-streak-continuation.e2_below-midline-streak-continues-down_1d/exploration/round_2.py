import numpy as np, pandas as pd
from scipy import stats

def wilder_rsi(c, n=14):
    d = c.diff()
    up = d.clip(lower=0); dn = -d.clip(upper=0)
    au = up.ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    ad = dn.ewm(alpha=1/n, adjust=False, min_periods=n).mean()
    return 100 - 100/(1+au/ad)

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lh = b.get("debug_info.components.rsi_below_age.last_history_value")
            rsi = wilder_rsi(c)
            for i in range(0, len(c) - 7, 7):
                rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                 wn=int(w[1:]), fc=b["forecast"].iloc[i], lh=lh.iloc[i],
                                 rsi=rsi.iloc[i], rsi7=rsi.iloc[i]-rsi.iloc[i-7] if i>=7 else np.nan,
                                 ret=c.iloc[i+7]/c.iloc[i]-1))
    df = pd.DataFrame(rows)
    df["ex"] = df["ret"] - df.groupby("coin")["ret"].transform("mean")
    neg = df[df.fc < 0].copy(); neg["len"] = -neg["lh"]
    def st(x, y):
        m = ~(np.isnan(x) | np.isnan(y))
        r = stats.linregress(x[m], y[m]); return pd.Series(dict(slope=r.slope, t=r.slope/r.stderr, n=int(m.sum())))
    out["neg_slope_on_log_len"] = st(np.log(neg["len"].values), neg["ex"].values)
    neg["fresh"] = neg["len"] <= 7
    out["fresh_vs_old_by_coin"] = neg.groupby(["coin", "fresh"])["ex"].agg(["mean", "count"])
    neg["half"] = np.where(neg.wn <= 12, "w1-12", "w13-24")
    out["fresh_vs_old_by_half"] = neg.groupby(["half", "fresh"])["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["fresh_by_year"] = neg[neg.fresh].groupby("year")["ex"].agg(["mean", "count"])
    out["old_by_year"] = neg[~neg.fresh].groupby("year")["ex"].agg(["mean", "count"])
    # among bars below 50: slope on RSI 7-day change
    b50 = df[df.rsi < 50]
    out["below_slope_on_rsi7"] = st(b50["rsi7"].values, b50["ex"].values)
    out["all_slope_on_rsi7"] = st(df["rsi7"].values, df["ex"].values)
    out["all_slope_on_rsi_minus50"] = st((df["rsi"]-50).values, df["ex"].values)
    out["mean_ex_neg_t"] = pd.Series(dict(mean=neg.ex.mean(), t=neg.ex.mean()/neg.ex.std()*np.sqrt(len(neg)), n=len(neg)))
    return out
