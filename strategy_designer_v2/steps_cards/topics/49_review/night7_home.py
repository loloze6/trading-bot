"""Night 7 (both arms, whole night): each confirmed book's days in a position by the coin's own market profile
(`common/market_profile.md`, read from local daily closes): the share inside the profile its idea names, against the
market's share of that profile on the same coins and dates; and its largest profile. Reads night7_ideas_full.csv.
  python3 topics/49_review/night7_home.py"""
import io, subprocess, functools
import numpy as np, pandas as pd
REPO="/home/user/trading-bot"; SC="strategy_designer_v2/steps_cards"; DATA=f"{REPO}/trading-bot/local_data"
import pathlib; HERE=pathlib.Path(__file__).resolve().parent; S=str(HERE)
@functools.lru_cache(None)
def prof(coin):
    d=pd.read_csv(f"{DATA}/kraken_{coin}_1d.csv",usecols=["timestamp","close"])
    d["day"]=pd.to_datetime(d.timestamp,format="ISO8601",utc=True).dt.tz_localize(None).dt.normalize()
    c=d.drop_duplicates("day").set_index("day").close
    tr=(c/c.shift(60)-1)*100; vol=(c.diff()/c).rolling(30).std()
    rk=vol.rolling(366).apply(lambda w:(w<=w[-1]).mean(),raw=True)
    t=np.where(tr>10,"rising",np.where(tr<-10,"falling","choppy")); a=np.where(rk>0.5,"agitated","calm")
    p=pd.Series([f"{x} {y}" for x,y in zip(t,a)],index=c.index); p[tr.isna()|rk.isna()]=None
    return p
d=pd.read_csv(f"{S}/night7_ideas_full.csv",dtype={"brief":str})
d=d[d.step5.fillna("").str.startswith("confirmed")]; d["step6"]=d.step6.fillna("")
rows=[]
for r in d.itertuples():
    ref=f"origin/night7{'c' if r.arm=='control' else ''}-{r.theme}"; run=f"night7{'c' if r.arm=='control' else ''}_{r.theme}_run"
    bt=r.idea+"_1d"
    raw=subprocess.run(["git","show",f"{ref}:{SC}/04_backtest/{run}/backtests/{bt}/chart_bars.csv.gz"],cwd=REPO,capture_output=True).stdout
    if not raw: rows.append(dict(arm=r.arm,theme=r.theme,idea=r.idea,note="no chart file")); continue
    b=pd.read_csv(io.BytesIO(raw),compression="gzip",usecols=["coin","timestamp","position"])
    b["day"]=pd.to_datetime(b.timestamp,format="ISO8601",utc=True).dt.tz_localize(None).dt.normalize()
    b["profile"]=[prof(c).get(dd) for c,dd in zip(b.coin,b.day)]
    b=b.dropna(subset=["profile"])
    allp=b.profile.value_counts(normalize=True)
    pos=b[b.position.abs()>1e-9]
    if not len(pos): continue
    sh=pos.profile.value_counts(normalize=True)
    named=str(r.profile) if isinstance(r.profile,str) else ""
    inn=pos.profile.apply(lambda p: all(w in p.split() for w in named.split())).mean() if named else np.nan
    base=b.profile.apply(lambda p: all(w in p.split() for w in named.split())).mean() if named else np.nan
    top=sh.index[0]
    rows.append(dict(arm=r.arm,theme=r.theme,idea=r.idea,profile=named,in_named=inn,named_base=base,top=top,top_share=sh.iloc[0],top_base=allp.get(top,0),
                     long_share=(pos.position>0).mean(),days_in_pos=len(pos)/len(b),step6=r.step6[:10],nearest_held=r.nearest_held))
pd.DataFrame(rows).to_csv(f"{S}/night7_home.csv",index=False)
