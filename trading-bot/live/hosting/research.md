# Where the live bot can run when the PC is off: research (2026-11-19)

Research only: nothing bought, no account created, no secret stored, no code of the bot changed.
Criteria, in the operator's order: 1 cost, 2 simplicity, 3 performance, 4 flexibility.

## Executive summary

**Decision.** Try these in order:
1. **1blu VPS Eco** (Germany), if its order page confirms the deal;
2. otherwise **OVH VPS-1** in an EU data centre (not London, not Singapore);
3. otherwise **netcup VPS nano** (Germany), if it is under about €4.50 a month.

All three are in the EU, have a fixed IPv4 for locking the Kraken key, and run the bot's 3 runs today.

**Price difference** (with VAT; 1blu's price includes German VAT, French VAT adds about 1%):

| | 1blu VPS Eco | OVH VPS-1 | netcup VPS nano |
|---|---|---|---|
| Per month, first 12 months | **€1** (deal) | €5.39 | €3.72, or about €4.43 after the Sept. 2026 rise |
| Per month, after 12 months | **€3.99** | €5.39 | same |
| Year 1 | **€12** | €64.68 | €44.64 – €53.16 |
| Year 2 | **€47.88** | €64.68 | €44.64 – €53.16 |
| Two years | **€59.88** | €129.36 | €89.28 – €106.32 |
| Saving against OVH over two years | **€69.48** | — | €23.04 – €40.08 |
| Billing | every 3 months, renews by itself | monthly, no commitment | 6-month minimum term |

**Feature difference:**

| | 1blu VPS Eco | OVH VPS-1 | netcup VPS nano |
|---|---|---|---|
| Memory | 4 GB (about 13 runs) | 4 GB (about 13 runs) | 2 GB (about 6 runs) |
| Processor, disk | 2 vCores, 64 GB SSD | 2 vCores, 40 GB NVMe | 2 vCores, 60 GB |
| Fixed IPv4 | yes | yes | yes |
| Backup | 2 GB of backup space | **daily automatic backup** | snapshots |
| Where | Germany | France (Gravelines, Strasbourg) or other EU | Germany |
| User reviews | **too few** (3 reviews, 1/10) | many, mixed: stable for long-term users; support split | many, mixed: good uptime; slow ticket support; maintenance up to an hour |
| Main risk | the deal may be gone; a French resident may not be able to order; Docker only in its "KVM" mode; panel probably in German | stock comes and goes (only Singapore shown on 2026-11-19) | the price after the September rise is not confirmed |

**Others, for reference** (details in section 3, "Every option found"):
- **Big clouds, paid** (AWS Lightsail 2 GB about €12.40; Vultr, DigitalOcean, Linode about €10–12): 2–3 times the price.
- **Big clouds, free:**
  - AWS: credits for 6 months;
  - Azure: 12 months, 1 GB;
  - Google: US only, 1 GB;
  - Oracle: reclaims idle machines, and accounts have been closed without warning.
- **Hetzner:** €7.19 and not orderable.
- **Home laptop:** often switched off.

**Before real orders, whichever host:**
- Set `KillSignal=SIGINT` in the service. Without it the bot dies on a server stop without saving its local book (section 5, step 10).
- Ask Kraken support whether a server in another EU country is fine (section 4).

**Words used below.**
- **Server**: a computer that stays on in a data centre. You reach it from your PC over the internet.
- **VPS** (virtual private server): a slice of a big server, rented by the month. It behaves like a small
  computer of your own.
- **Fixed IP**: the server's internet address never changes. Kraken can then be told to accept your key from that
  address only.
- **Service**: a program the server's system starts by itself at boot and restarts after a crash. On Linux the
  part of the system that does this is called systemd.
- **HT / TTC**: price before VAT / with VAT. French VAT is 20%, and a French private customer of an EU host pays
  French VAT.

**How sure each price is.** This session's network blocked most providers' own pages. Every price comes from one
of four places, marked in the tables:
- **[O]**: the provider's own page or blog, read through a search extract;
- **[3]**: a third-party comparison, with its date;
- **[M]**: my own memory, not checked today;
- **[calc]**: my arithmetic.

Dollar prices are converted at about 1 USD = 0.86 EUR, a rate I did not check today. **Before paying, open the
provider's order page once by hand: prices rose several times in 2026.**

---

## 1. What the bot needs (measured)

| Need | Value | Where it comes from |
|---|---|---|
| Memory per live run | **250 MB after loading, 273 MB at peak** | measured today on Linux, Python 3.13: a 912-day warm-up of `first_paper`'s strategy, then 30 simulated days. Offline, on synthetic candles through the parity test's fake Kraken, because this container's network refuses futures.kraken.com |
| Memory, 3 runs at once | about 820 MB, plus about 250–400 MB for the server's own system | 3 × 273 MB [calc] |
| So: server size | **1 GB is too tight for 3 runs; 2 GB is enough; 4 GB leaves room** for more coins and the research viewer | |
| CPU | negligible: warm-up plus 30 days of polls took 6 s | measured |
| Disk | Python libraries 490 MB, the repository clone about 1 GB, a run folder 2.3 MB after 30 days | measured |
| ARM processors (cheaper machines) | fine: every pinned package has a ready-made Python 3.13 ARM file | checked on PyPI today |
| Network | outbound HTTPS to futures.kraken.com only; nothing comes in | `live/kraken.py` |
| Key | read from two environment variables, `KRAKEN_FUTURES_API_KEY` and `KRAKEN_FUTURES_API_SECRET` | `live/kraken.py` |
| Restart of an existing run | `python main.py run_live --run NAME`. It reads the folder's own `strategy_config.json`. **It needs the key**: `start_value` is null, so the local book starts at the real account's value | `live/runner.py` |

**Two facts from the code that matter for any host.**
1. **The bot stops cleanly only on Ctrl+C.** A server stops a program with a different signal (SIGTERM) by default.
   On that signal the bot dies on the spot: `local_book.csv` is not written and no "stop requested" line is
   logged. Tested today: SIGTERM ends the process with code 143 and its `finally` block never runs; SIGINT (what
   Ctrl+C sends) gives "clean stop" and code 0. This is what the three runs show from 2026-11-18. On a server the
   fix is one line in the service file (`KillSignal=SIGINT`, see the setup plan): no code change.
2. **Every restart is a new session**: a new warm-up, and the local book starts again at the real account's value
   (card, "Open"). Automatic restarts after a crash or a reboot will therefore add sessions to a run. That is
   expected, but each one is visible in the record.

---

## 2. Comparison of all options

Cost is per month with VAT unless said otherwise. Simplicity runs from 1 (hard) to 5 (easy) for someone who has
never used a server. "Fit" says whether 3 runs (about 820 MB) fit.

### 2a. Rented small servers (VPS)

| Option | Exact plan | Cost / month | Simp. | Fit (3 runs) | Flexibility | Main risk |
|---|---|---|---|---|---|---|
| **OVHcloud VPS-1** (France) | 2 vCores, 4 GB, 40 GB NVMe, unlimited traffic at 500 Mbit/s, **daily backup and IPv4 included**, 99.9% uptime promise. Datacentres in France: Gravelines, Strasbourg [3] | **€4.57** with a 12-month commitment, **paid upfront: about €54.86 at once** (€3.81 HT) [calc]; **€5.39** with none (€4.49 HT) [O] OVH blog "VPS 2027" + [3] dev.to, 2026-11-13 | 4 | yes, with room | good: bigger plans in one click | the renewal price after the commitment is not known; OVH raised its previous range by 45% in April 2026 [3] next.ink; a 2021 fire in Strasbourg cost data to VPS customers without backups (section 7) |
| netcup VPS nano G11.5s (Germany) | 2 vCores, 2 GB, 60 GB, IPv4 included | **€3.69** with German VAT, about €3.72 with French VAT [calc]; **6-month contract** [O] netcup.com/en/server/vps-lite (extract; the nano price was cut off in round 2, so it is not re-confirmed) | 4 | yes, with room for 2–3 more runs | medium | **snapshots included** [O] same page, one free snapshot download, more are paid [3] |
| netcup VPS pico G11.5s | 1 vCore, 1 GB, 30 GB | €2.21 with VAT, 12-month contract [O] same page | 3 | **no** (1–2 runs) | low | too small for 3 runs |
| IONOS VPS XS (France/Germany) | 1 vCore, 1 GB, 10 GB | €1.20 [calc from €1 HT] **+ €12 setup fee**, probably a long commitment [3] experte.com/whtop 2026 | 3 | **no** | low | promotional price; renewal unclear |
| Contabo Cloud VPS 10 (Germany) | 3 vCPU, 8 GB, 75 GB [M] | €4.40 first term, then €5.50 (VAT unclear) **+ a setup fee of unknown amount** [3] pricingsaas Jun 2026 + [O] Contabo support | 3 | yes | high (8 GB) | many reports of slow, overloaded CPUs and of new servers getting IP addresses blacklisted for earlier abuse (r/VPS 2024–25, many users) |
| Hetzner CX23 (Germany/Finland) | 2 vCPU, 4 GB, 40 GB, 20 TB [M] | **€7.19** [calc: €5.49 + €0.50 IPv4 HT, since 15 June 2026] [3] northflank/bitdoze 2026 | 4 | yes | good | **reported impossible to order on every check from September to 2026-10-20**, no restock date; Hetzner says capacity is limited and restocks depend on cancellations [3] bitdoze + [O] Hetzner order-processing doc; sign-up asks for an ID document plus a selfie, and some sign-ups are refused without reason [O] Hetzner FAQ + many users |
| Vultr Regular (Paris) | 1 vCPU, 1 GB, 25 GB, 1 TB | about €5.2 [calc from $5 + VAT] [3] costbench 2026 | 4 | **no** (2 GB plan needed, price not checked) | good | billed in USD |
| Linode/Akamai Nanode (Paris) | 1 vCPU, 1 GB, 25 GB, 1 TB | about €5.2 [calc from $5] [3] activepieces Nov 2026 | 4 | **no** | good | billed in USD |
| DigitalOcean Basic (Frankfurt/Amsterdam) | 1 vCPU, 1 GB, 25 GB, 1 TB | about €6.2 [calc from $6] [3] costbench Oct 2026; backups +20% [M] | 4 | **no** | good | no Paris datacentre [M] |
| Scaleway DEV1-S (Paris) | 2 vCPU, 2 GB, 20 GB | about €11.5 [calc: €6.55 + about €3 for IPv4, HT] [O] Scaleway pricing blog, June 2026 | 3 | yes | good | **IPv4 billed on top**; the cheap Stardust1-S (1 GB, about €4 with IPv4) is often out of stock [M] |
| Hostinger KVM 1 (Paris) | 1 vCPU, 4 GB, 50 GB | €5.49 only if 24 months are paid upfront, **€11.99 at renewal** [3] ouiheberg 2026 | 4 | yes | medium | renewal price twice the entry price |

### 2b. The big clouds' free or small machines

| Option | What is free, for how long | Cost / month | Simp. | Fit | Main risk |
|---|---|---|---|---|---|
| Oracle Cloud Always Free | ARM machine up to **2 OCPU / 12 GB** (halved from 4/24 on 2026-06-15), no end date; only in the region chosen at sign-up (France has Paris `eu-paris-1` and Marseille `eu-marseille-1` [O] Oracle region list; whether free ARM capacity is available there: I do not know) | **€0** | **1–2** (complex console; often "out of capacity") | yes | Oracle **reclaims idle free machines**: under 20% CPU, network and memory over 7 days [O] Oracle docs. This bot is far below all three, so it would be reclaimed unless the account is upgraded to pay-as-you-go (card, billing risk). Many reports of whole accounts closed without warning [many users, 2024–26]. The free allowance was cut without notice in 2026 [3] InfoQ July 2026 |
| AWS Lightsail (Paris region exists [M]) | free plan = $100–200 of credits for 6 months, then the account closes unless upgraded [O] AWS, 2025-07-15 | after credits: about €7.2 for 1 GB (**$7**), about €12.4 for 2 GB ($12), IPv4 included [O] Lightsail docs (extract) | 3 | 2 GB plan | not free for long |
| Google Cloud e2-micro | free with no end date, **in US regions only** (us-west1, us-central1, us-east1) [O] | €0 (a user reports a network charge) | 2 | **no** (1 GB) | **US server: Kraken's EU perpetuals are not offered in the US** (see section 4) |
| Azure free account | B1s 750 h/month for **12 months**, then about $8.7 in France Central [3] | €0, then about €9 | 2 | **no** (1 GB) | ends after 12 months |

### 2c. Managed app platforms (they run the program for you; no server to look after)

| Option | Cost / month for this bot | Simp. | Fit | Main risk |
|---|---|---|---|---|
| Railway Hobby | $5 plan including $5 of usage; RAM $10/GB → **about €11.5–12.5 for 1 GB** [O] docs.railway.com | 4 | yes (1 GB) | fixed outbound IP only on the $20 Pro plan; usage-based bill |
| Fly.io | 1 GB about $6.70 + volume $0.15/GB + IPv4 $3.60 → **about €9–11** [O] fly.io pricing, 2026 | 3 (command line and Docker) | yes | no free allowance for new accounts [3] |
| Render | worker 512 MB **$7 per run**, disk $0.25/GB → 3 runs about €22–23 [O] render.com/pricing | 4 | one run per 512 MB worker | dedicated IP $100/month |
| Northflank | 512 MB about $5.4 → 3 runs need more [O] northflank.com/pricing | 3 | partly | could not verify fixed IP |
| PythonAnywhere | Developer plan €10, **1 always-on task** [O] blog.pythonanywhere.com/222 | 4 | **1 run only** | memory limit of a task: I do not know |
| Heroku, Koyeb | Heroku: files wiped at every restart, maintenance-only since 2026-02 [O]; Koyeb: free tier closed to new users since Feb 2026 [O] | — | — | not suitable |

### 2d. Scheduled jobs instead of an always-on program

| Option | Cost | Verdict |
|---|---|---|
| GitHub Actions on a timer | free within 2,000 min/month on a private repository [O] GitHub docs. One daily run of about 2 min (installing 490 MB of libraries plus the warm-up) is about 60 min a month; hourly is about 1,440 | **Not suitable today.** |
| Google Cloud Run jobs + Scheduler, AWS Lambda + EventBridge | free quotas cover a daily run; Lambda's free quota is about 9 days of continuous 512 MB running [O] | Same rewrite needed. Cloud Run or Lambda add a cloud account and its console to learn. |

Why GitHub Actions is not suitable today:
- **The bot's design does not allow it.** A run keeps its strategy and local book in memory between bars, and
  every stop closes the local position. A timer job would need the strategy's state and the local book saved
  between runs: a code change to the shared bot, which needs the operator's go.
- **Timing.** Scheduled runs are delayed at busy hours, and the top of the hour is the busiest. That goes against
  step 3b, which aims to decide 3 s after the close.
- **No fixed IP.** Runs come from shared US addresses, so the key cannot be locked to one address, and US addresses
  are a risk with Kraken (section 4).
- **Terms of use.** GitHub's terms appear to rule out using Actions for work unrelated to the repository's
  software. I could not read the live text.

### 2e. A device at home

| Option | Cost | Simp. | Fit | Main risk |
|---|---|---|---|---|
| An old laptop you already own | €0 to buy; 15–20 W → **€26–35 a year, €2.2–2.9 a month** at €0.2001/kWh [3] Selectra/hellowatt, EDF Tarif Bleu Base from 2026-08-01 [calc] | 3 | yes | **home power or internet cut = bot stopped**. A laptop can go to sleep: the recorder's notes record a real 4-hour hole caused exactly by that (`deploy/kraken_recorder/install_systemd_unit.sh`). A battery left charging for years may swell |
| Raspberry Pi 5, 4 GB, with power supply, case and small SSD | about **€170–230 once** (board about $110 after the 2026 price rises [3] RPi forum; total is my estimate) + 3.5–5 W → about €6–9 a year | 2 | yes | same home risks. SD cards get corrupted by power cuts, so boot from an SSD [many users]. Raspberry Pi OS Trixie ships Python 3.13 [O]. Over 3 years about €5–7 a month: not cheaper than OVH |
| A NAS you already own (e.g. Synology) | about €26 a year at 14.7 W [O] Synology spec | 3 | depends on its memory | same home risks |

At home the fixed IP depends on the internet provider: I do not know yours. Without a fixed IP, the key cannot be
locked to the bot's address.

### 2f. Not suitable, confirmed

- **A Claude Code cloud session.** Its container is reclaimed after a period of inactivity (this environment's own
  documentation), so the bot would stop and its local files would be lost. Its network is also set per environment:
  **in this session futures.kraken.com was refused** (proxy answer 403), while the operator saw Kraken reachable in
  another environment.
- **Heroku**: files wiped at every restart. **Koyeb**: free tier closed to new users. **Google's free machine**: US
  only, 1 GB.

---

## 3. Recommendation

### Decision (final, 2026-11-19)

Try these in order:
1. **1blu VPS Eco** (Germany), deal confirmed on the order page: €1 a month for 12 months, then €3.99.
2. **OVH VPS-1** in an EU data centre: €5.39 a month.
3. **netcup VPS nano**, if under about €4.50 a month.

The steps that led here are below: the operator's rulings, the deals, every option compared.

### Why OVH VPS-1 is the reference (first written as the recommendation, before the deals were found)

| Criterion | Why |
|---|---|
| 1 Cost | The cheapest monthly option in France with room to grow (see the operator's rulings below). Cheaper ones give up room (netcup nano, 2 GB, 6-month contract), stability (an old laptop at home, about €2.5 of electricity), or are not monthly |
| | **Everything is included**: fixed IPv4, daily automatic backup, unlimited traffic. Hetzner and Scaleway bill the IPv4 apart; DigitalOcean and Vultr bill backups apart |
| 2 Simplicity | Billed in euros with French VAT; month-to-month possible (€5.39) to try it before committing |
| | A web console in the browser for when the connection from the PC fails |
| | A standard Debian image that already has Python 3.13 (Debian 13 ships it [O] Debian release notes) |
| 3 Performance | 4 GB for about 820 MB of need; 2 vCores for one decision a day |
| 4 Flexibility | Several runs or coins (one service per run) |
| | The research viewer, reached privately through an SSH tunnel; no port opened |
| | A bigger plan later in one click. Heavy backtests stay on the PC: 2 vCores are not a backtest machine |
| Kraken rules | Server in France, inside the European Economic Area like you, which is what Kraken's EU terms expect |
| | Fixed IPv4, so the key can be locked to it |

What I recommend against, and why:
- **Oracle's free machine.** It is the only €0 option big enough, but this bot is so light that Oracle's idle rule
  would reclaim it. The way around (pay-as-you-go) brings back billing. The console is the hardest of all, and
  accounts have been closed without warning.
- **Hetzner.** It used to be the usual cheap pick. In 2026 it is pricier (€7.19), sign-up is strict, and its cheap
  plans were often not orderable.

### The operator's rulings (2026-11-19) and what they decide

| Ruling | Effect |
|---|---|
| **Pay monthly**, unless a whole year costs **less than €20** | OVH's 12-month price is paid upfront (about €55), so: **OVH monthly, €5.39** (€4.49 HT). netcup nano's 6-month contract does not fit |
| **France is not a requirement** (operator: an unjustified concern) | Any EU data centre will do; not the UK or the US (section 4) |
| **Extra memory is nice to have, worth about $1 a month** (read as $1 for France and memory together) | OVH's 4 GB counts as about €0.86 a month against a 2 GB plan; the table below shows what it buys |

How long the memory lasts, one run per program as today (273 MB each, about 400 MB for the system) [calc]:

| Server | Runs that fit | Today 3; +1 a month: full in about |
|---|---|---|
| 2 GB (netcup nano) | about 6 | **3 months** |
| 4 GB (OVH VPS-1) | about 13 | **10 months** |

After that, two ways on:
- a bigger plan: OVH VPS-2, whose price I did not check;
- several coins in one program, the card's plan ("later several coins in one bot"): the libraries' 250 MB would be loaded once instead of once per run, so an added coin would cost far less memory. Not measured.

Plans paid monthly with at least 2 GB in the EU [from section 2a]:
- **OVH VPS-1**, 4 GB: €5.39.
- **netcup nano**, 2 GB: €3.72 at the price found, about €4.43 if September 2026's rise of up to 20% applies; 6-month
  minimum term.
- **More expensive:** Contabo (€5.50 + setup fee), IONOS VPS S (€6 after 3 months + €12 setup), Hetzner CX23
  (€7.19, not orderable), Vultr, DigitalOcean and Linode 2 GB (about $10–12), Scaleway DEV1-S (about €11.5).

**Result, by the operator's own values:**
- take **netcup nano** if its order page shows it **under about €4.50 a month with VAT** (OVH's €5.39 minus the
  $1), and the 6-month minimum term is acceptable;
- otherwise take **OVH VPS-1, paid monthly, €5.39 with VAT**;
- in a near-tie (netcup about €4.43), OVH, for its included daily backups and no minimum term;
- if the $1 was meant for each of the two, the threshold is about €3.70 and OVH almost surely wins.

### Deals (monthly or yearly), checked 2026-11-19

The operator's rule, clarified: a cheap monthly price counts as much as a cheap year. Black Friday is 2026-11-27;
most deals run to about 2026-11-30.

A deal qualifies if **all** of these hold:
- **cost:** cheaper than OVH's €5.39 a month, over the first and the following years;
- **memory:** 4 GB or more (worth about $1; 2 GB would fill in about 3 months);
- **place:** a data centre in the EU, not the UK (on Kraken's derivatives restricted list) or the US;
- **host:** one that has existed for several years.

| Offer | Price | Verdict |
|---|---|---|
| **1blu VPS Eco** (German host; 2 vCores, 4 GB, 64 GB SSD, own IPv4, 2 GB backup space, traffic included) | **€1 a month for 12 months (€12 the first year), then €3.99 a month**; billed every 3 months; renews automatically [3] mydealz / monsterdealz, 2026 | **Qualifies, and beats OVH**: €12 against about €65 in year 1, then €3.99 against €5.39. To check on the order page: is it still offered (re-released after a promotion ended in October); can a French resident order it; is it a full virtual machine (a deal note says Docker works reliably only after switching it to "KVM"); the language of its panel. Reviews: 1 of 10 from only 3 reviews, too few to judge |
| HostDZire (LowEndTalk thread 222164, "since 2013" according to one aggregator) | from €18 a year; a 4 GB, 2-core plan at €21 a year; locations India, France, Netherlands, USA | **Maybe**: about €1.75 a month. Plan, location and terms not seen; reputation not checked independently |
| Contabo Cloud VPS 4 | $5.28 a month for 24 months (20% off) | no: 24-month term; reliability complaints |
| Hostinger KVM 2 | $8.79 a month in the sale, long prepay | no: costs more than OVH |
| IONOS VPS S+ | $2 a month for 3 months, then €5 HT + setup | no: about €6.1 a month over the first year |
| Hetzner, netcup, OVH | no Black Friday VPS sale found (a tracker on 2026-11-03) | — |
| A new provider in Marseille, 1 GB at €10 a year | €10 a year | no: 1 GB, new provider |
| LiteServer (NL), Eurohoster (NL) | 50% and 80% offers seen in earlier years; no 2026 offer found | check their pages by hand |
| UK EPYC 4 GB £27 a year; DediRock 8 GB $24.99 a year; PetroSky France €4.89 a month | — | no: UK; location not seen; memory not seen |

Sources:
- mydealz.de/deals/1blu-vps-eco-4gb-ram-64gb-ssd-2-cores-amd-epyc-top-de-cix-anbindung-top-fur-n8n-vpn-kleine-ki-agenten-hermesopenclaw-2867639
- monsterdealz.de/shopping/1blu-vps-eco-vserver-12-euro-jahr/1585033
- whtop.com/plans/1blu.de/160066
- lowendtalk.com/discussion/222164/early-black-friday-sale-vps-dedicated-server-deals-starting-at-just-18-year
- cybernews.com/best-web-hosting/vps-black-friday-deals/
- vpsledger.com/black-friday-vps-deals-2026/
- vpsbenchmarks.com/black_friday_vps
- lowendbox.com/blog/new-provider-new-location-dirt-cheap-pricing-e10-yr-for-a-1gb-vps-in-marseille-france/

### Question only the operator can answer (answered 2026-11-19)

| Question | If yes | If no |
|---|---|---|
| Do you already own a laptop or NAS you can leave on at home, with a fixed internet address? | About €2.5/month of electricity instead of €5.39. The risks are power cuts, internet cuts and sleep; a Healthchecks alert (below) still warns you | OVH |

**Answer:** the operator has a laptop, but it will often be switched off, so it cannot host the bot. Option #2 is out.


### Every option found, compared by the operator's rules (2026-11-19)

Rules:
- cost first, while viable and stable;
- monthly payment, unless a whole year costs under €20;
- an EU location (France not required; not the UK or the US);
- extra memory worth about $1 a month;
- today 3 runs, so at least 2 GB.

Cost is per month with VAT. "Feedback" is what users report: forums, review sites, and press when it relays user
reports (weight in section 6).

**Viable**, cheapest first:

| # | Option | Cost / month | Main risk users report | Verdict |
|---|---|---|---|---|
| 1 | Oracle Always Free ARM (2 OCPU / 12 GB) **upgraded to pay-as-you-go**, Paris or Marseille | €0 if kept within the free limits | accounts closed without warning (fewer reports on paid accounts, still some); Oracle does not confirm that pay-as-you-go protects an idle machine from reclaiming; some unexpected charges (a $0.01 budget alert is the usual guard); free limits halved without notice in 2026; the free ARM machine often hard to get | **no** for real orders: a sudden closure leaves a position unwatched. Possible for paper runs only, if €0 matters more than stability |
| 2 | A laptop or NAS you already own, at home | about €2.5 (electricity) | power and internet cuts, sleep, a swelling battery | **no**: the operator's laptop will often be switched off |
| 3 | **1blu VPS Eco, 4 GB, Germany** (deal) | **€1 for 12 months, then €3.99** | too few reviews to judge (3); deal availability and order conditions unconfirmed | **yes: first choice if the order page confirms it** |
| 4 | netcup VPS nano, 2 GB, Germany | €3.72, or about €4.43 after the September 2026 rise | support by ticket, slow; maintenance of up to an hour called normal; 6-month minimum term | **yes if under about €4.50** on its order page |
| 5 | Used mini PC at home | about €4–6 over 3 years | home risks as #2 | no: not cheaper than #6, less stable |
| 6 | **OVH VPS-1, 4 GB** | **€5.39** | support split; renewal price rises on its older range; 2021 fire (backups now included) | **yes: the default choice** |
| 7 | Contabo Cloud VPS 10, 8 GB | €5.50 + a setup fee | CPU taken by other customers ("steal") 20–80%; recycled IP addresses already blacklisted | no: costs more than #6, more reliability complaints |
| 8 | IONOS VPS S, 2 GB | €2.40 for 3 months, then €6, + €12 setup | promotional entry price | no: about €6.1 a month over the first year |
| 9 | Hetzner CX23, 4 GB | €7.19 | not orderable at every check up to 2026-10-20; strict sign-up | no |
| 10 | Fly.io, Railway (1 GB) | about €9–12 | bills by usage; fixed address costs extra | no: about twice #6 |
| 11 | Vultr, DigitalOcean, Linode (2 GB); Scaleway DEV1-S; AWS Lightsail (2 GB) | about €10–12.4 | none notable | no: about twice #6 |
| 12 | PythonAnywhere | €10, 1 always-on task | — | no: 1 run only |
| 13 | Render (one 512 MB worker per run) | about €22–23 for 3 runs | — | no |

**Not suitable for this bot:**

| Option | Why |
|---|---|
| Google free machine | US only, 1 GB |
| Azure free | 12 months, then about €9; 1 GB |
| AWS free plan | 6 months of credits |
| GitHub Actions and other timer jobs | the bot needs a rewrite; no fixed address; US addresses; late starts |
| Heroku | files wiped at every restart |
| Koyeb | free tier closed to new users |
| Hostinger | 24 months prepaid, then €11.99 |
| netcup pico, IONOS XS (1 GB) | only 1–2 runs; later, once several coins run in one program |
| Old Android phone | background programs killed; the pinned libraries cannot be installed directly |
| Freqtrade bot hosting | built for another bot |
| Keeping Oracle's free machine artificially busy | against the purpose of the idle rule; account risk |
| A Claude Code cloud session | reclaimed after inactivity |

**Result: 1blu VPS Eco (#3)** if its order page confirms the deal and the checks above; otherwise **OVH VPS-1 (#6)** in an EU data centre (not London, not Singapore; OVH stock "goes in and out pretty often" [LowEndTalk], so retry), , unless:
- a qualifying deal (section 3, "Deals") appears by about 2026-11-30;
- **#4** netcup nano under about €4.50 on its order page;

Sources added for Oracle pay-as-you-go:
- docs.oracle.com/en-us/iaas/Content/FreeTier/resourceref.htm
- bestusavps.com/reviews/oracle-cloud/ (2026)
- news.ycombinator.com/item?id=36010572 (2023)
- redlib mirror of r/oraclecloud "account terminated without warning" (2024-09)
- trustpilot.com/review/cloud.oracle.com
- infoq.com/news/2026/07/oracle-cloud-free-tier-limits/

---

## 4. Kraken Futures from France: what the server's location changes

Kraken's own pages (support.kraken.com, docs.kraken.com) were blocked in this session, so these come from search
extracts and press articles. **Read them once by hand, or ask Kraken support, before real orders (step 5).**

| Question | Finding | How sure |
|---|---|---|
| **Your own account** | **You already hold a Kraken Futures account read by the bot with a key** (value 105.94 USD on 2026-11-17, `live/validation/reading.md`). So access as a French resident is already granted. Whether real orders need one more step (the appropriateness test for derivatives) depends on your account: I do not know | the repository's own record |
| Who offers the perpetuals to a French resident? | Payward Europe Digital Solutions (CY) Ltd, a Cyprus investment firm (CySEC licence 342/17, EU MiFID II rules). EEA launch 2025-05-20 | press: CoinDesk and Cointelegraph, 2025-05-20 |
| Conditions | identity verification, tax number, retail or professional classification, an appropriateness test; leverage at most 10x for EEA clients (less for some contracts) | Kraken pages "derivatives eligibility requirements (EEA)" and "margin schedule (EEA)" (extracts, undated) |
| Is France excluded? | not in any extract of the restricted list (which names e.g. the UK, Canada, Australia). I did not see the full list, so the answer is "probably not", not "no" | extracts; a third-party site says the list was updated in July 2026 |
| Spot (separate) | Payward Europe Solutions Ltd (Ireland), on the AMF's white list since 2025-07-03 | [O] amf-france.org |
| Does the server's country matter? | Kraken's EU terms expect the client "located in an EEA jurisdiction"; the perpetuals are **not offered to the US**, which has its own Kraken product; its promotion rules treat a VPN as abuse. **A server in France or the EU is the safe case; a US server (Google's free machine, GitHub Actions) is the risky one.** Whether Kraken blocks US addresses on the API: I do not know | extracts and inference; no official statement on servers found |
| A server in Singapore (OVH showed VPS-1 stock only there, 2026-11-19) | **avoid**. Since 2025-06-19 Singapore's regulator reportedly forbids offering crypto derivatives to retail customers [3] comparison site, not checked against MAS; Kraken says it is not licensed in Singapore [3]. Every request would come from outside the EEA, where Kraken's EU terms expect the client to be. Whether Kraken checks: I do not know | secondary sources: bitget.com/academy/singapore-crypto-exc, moneysense.gov.sg, asiaforexmentor.com/kraken-review |
| What users report on the same question (searched 2026-11-19) | no first-hand report of a Kraken Futures bot on a foreign server, nor of an EU resident's account limited for it; no freqtrade issue on Kraken blocking. Kraken's help centre: restrictions follow the **verified residency** (extract). Kraken's API guide offers bot traders a connection through its AWS access point, so servers are expected. Unofficial blogs: an ID/IP country mismatch can freeze an account, but their examples are residents of restricted countries hiding their location. **Reading: an EU server is consistent with every source; outside the EU, probably allowed by residency but unconfirmed, so avoided** | support.kraken.com "where is Kraken licensed" (extract); docs-legacy.kraken.com/api/docs/guides/global-intro/; coinperps.com/learn/kraken-restricted-countries; sipsak.org and stakeliquid.com blogs (low weight) |
| Kraken blocking data-centre addresses (like Binance's 451) | no report found for Kraken | none found |
| Can a key be locked to fixed addresses? | **Yes**: the futures API key form takes a list of allowed IPv4/IPv6 addresses; Kraken's docs recommend it and have a call that returns a key's allowed ranges | [O] docs.kraken.com "check v3 API key" + two independent setup guides (Tealstreet, HaasOnline) that describe the field: "comma delimited list of IPv4 or IPv6 IP addresses or ranges" |
| Key access levels | general API: read-only or full; withdrawals: can be "No access" | third-party guide + Kraken help (extract) |
| Request limits | one candle request a minute is far below any limit found (private calls: 500 cost units per 10 s) | [O] docs.kraken.com "futures rate limits" |

---

## 5. Setup plan, step by step, for a first server

Written for OVH VPS-1. From step 3 on, it is the same on any Debian server (1blu, netcup). For **1blu**, in its
customer centre:
- switch the server to its **KVM** mode (a full virtual machine; a deal note says Docker works reliably only there);
- choose **Debian 13** if offered (else the Python fallback in step 5);
- use the user name its email gives.

I do not know 1blu's panel beyond that.

**Nothing below has been run on a real server.** The service file is a draft: prove it on the server (step 10)
before trusting it.
- "Type in PowerShell" means on your Windows PC (Start menu → PowerShell).
- "On the server" means in the window that step 3 opens.
- Never paste the Kraken key anywhere except the one file in step 8.

1. **Make a login key on the PC (5 min).** An SSH key is a pair of files that replaces a password. The private
   one stays on your PC; the public one goes to the server.
   - Type in PowerShell: `ssh-keygen -t ed25519`, then press Enter three times.
   - Then type `type $HOME\.ssh\id_ed25519.pub` and copy the single line it shows. That line is the public half;
     it is safe to share.
2. **Order (10 min).** On ovhcloud.com/fr/vps, choose **VPS-1**, then:
   - a datacentre in **France** (Gravelines or Strasbourg; not Beauharnois, which is in Canada);
   - the image **Debian 13**;
   - paste the public line from step 1 where it asks for an SSH key;
   - no paid options (the daily backup is included).

   Note the **IPv4 address** shown in the OVH panel, and the user name in the delivery email (for Debian images it
   is `debian` for a Debian image: OVH's guide says the user name matches the system chosen [3] mirror of OVH's
   "starting with a VPS" guide; check it in the email).
3. **Connect.** Type in PowerShell `ssh debian@YOUR_IP` and answer `yes` the first time. You are now "on the
   server". To leave, type `exit`.
4. **Mask any sleep.** A server should not sleep, but check once on the server:
   `sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target`.
5. **Update and protect (5 min), on the server:**
   - `sudo apt update && sudo apt full-upgrade -y`
   - `sudo apt install -y git python3-venv unattended-upgrades ufw curl`. Unattended-upgrades installs security
     fixes by itself.
   - `sudo ufw allow OpenSSH && sudo ufw enable`. The firewall now accepts only your logins; the bot needs nothing
     else, since it only calls out.
   - `python3 --version` must say 3.13. Whether OVH offers a Debian 13 image I could not confirm. If only Debian 12
     or Ubuntu 24.04 is offered (Python 3.11 or 3.12), install Python 3.13 with uv, a Python installer:
     `curl -LsSf https://astral.sh/uv/install.sh | sh`, then in step 7 use
     `~/.local/bin/uv venv --python 3.13 ~/venv` and
     `~/.local/bin/uv pip install --python ~/venv/bin/python -r ~/trading-bot/trading-bot/requirements.txt`.
6. **Get the code (10 min).** The server needs read-only access to the repository: a **deploy key**, an SSH key that
   can read this one repository and nothing else.
   - On the server: `ssh-keygen -t ed25519 -f ~/.ssh/github_deploy -N ""` then `cat ~/.ssh/github_deploy.pub`.
   - On GitHub: repository Settings → Deploy keys → Add. Paste the line and leave "Allow write access" unticked.
   - On the server: `GIT_SSH_COMMAND="ssh -i ~/.ssh/github_deploy" git clone --branch live-kraken-futures
     git@github.com:loloze6/trading-bot.git ~/trading-bot`
7. **Install the libraries (5–10 min).**
   - `python3 -m venv ~/venv`
   - `~/venv/bin/pip install -r ~/trading-bot/trading-bot/requirements.txt` (about 490 MB).
   - Check, from `~/trading-bot/trading-bot`: `~/venv/bin/python main.py live_check --symbol BTCUSD`. It must print
     the instrument and recent candles, and "key found: no".
8. **A new Kraken key for the server only (10 min).**
   - In Kraken Pro → Settings → Connections & API → **Futures** API, create a key:
     - general access **read-only**, for now;
     - withdrawals **No access**;
     - allowed IP: **the server's IPv4** from step 2.
   - Keep the PC's key separate, so either one can be deleted alone.
   - On the server, type `sudo mkdir -p /etc/trading-bot && sudo nano /etc/trading-bot/kraken.env` and write two
     lines:

     ```
     KRAKEN_FUTURES_API_KEY=...
     KRAKEN_FUTURES_API_SECRET=...
     ```

     Save with Ctrl+O, Enter, Ctrl+X.
   - Then `sudo chmod 600 /etc/trading-bot/kraken.env`. Only the system can read it now. It is not in git, not on
     your screen again, and the service hands it to the bot at start.
   - OVH's daily backup does contain this file. If the server is ever lost or handed back, delete the key in Kraken.
9. **Phone alerts (10 min).** Both are free:
   - **ntfy**: install the ntfy app on the phone and subscribe to a long, random topic name, e.g. 30 random
     letters. Anyone who knows the name can read the alerts, so treat it like a password. The service file below
     sends a message at every start and every stop: a crash, a reboot, or a stop by hand.
   - **Healthchecks.io**, the free "Hobbyist" plan with 20 checks [O], with Telegram and ntfy among its alert
     channels on the free plan [3] comparison article + a user report: it alerts you when the server goes *silent*.
     A message sent by the bot cannot cover a dead server; this can.
     - Create one check per run, with a period of 1 hour and a grace time of 1 hour.
     - Add your phone through its Telegram or email integration.
     - On the server, `crontab -e` and add one line per run:

       ```
       0 * * * * find ~/trading-bot/trading-bot/live_runs/first_paper/summary.md -mmin -1560 | grep -q . && curl -fsS -m 10 https://hc-ping.com/YOUR-CHECK-ID >/dev/null
       ```

       The line pings every hour while `summary.md` is less than 26 h old (it is rewritten after every bar).
       A stale summary or a dead server stops the pings, and Healthchecks warns you within about 2 hours.
10. **The service (15 min).** Type `sudo nano /etc/systemd/system/trading-bot-live@.service` and write:

    ```ini
    [Unit]
    Description=Trading bot live run %i
    After=network-online.target
    Wants=network-online.target
    StartLimitIntervalSec=3600
    StartLimitBurst=5

    [Service]
    User=debian
    WorkingDirectory=/home/debian/trading-bot/trading-bot
    EnvironmentFile=/etc/trading-bot/kraken.env
    ExecStart=/home/debian/venv/bin/python main.py run_live --run %i
    # The bot stops cleanly only on Ctrl+C (SIGINT); the default SIGTERM would skip writing local_book.csv.
    KillSignal=SIGINT
    TimeoutStopSec=60
    Restart=on-failure
    RestartSec=60
    ExecStartPost=-/usr/bin/curl -s -m 10 -d "live run %i started" https://ntfy.sh/YOUR_TOPIC
    ExecStopPost=-/usr/bin/curl -s -m 10 -d "live run %i stopped: ${SERVICE_RESULT} ${EXIT_STATUS}" https://ntfy.sh/YOUR_TOPIC

    [Install]
    WantedBy=multi-user.target
    ```

    How it behaves:
    - `%i` is the run's name.
    - The `-` before `/usr/bin/curl` means a failed alert never fails the run.
    - A crash restarts the run after 60 s, at most 5 times an hour; then it stays stopped and the phone has the
      messages.
    - A reboot starts every enabled run again.

    Then:
    - `sudo systemctl daemon-reload`
    - `sudo systemctl enable --now trading-bot-live@first_paper`, and the same for the other runs.

    **Proof before trusting it:**
    - Read `summary.md` and `run.log` once the next bar is decided.
    - `sudo systemctl stop trading-bot-live@first_paper` must write "stop requested" in `run.log` and an updated
      `local_book.csv`.
    - `sudo reboot` must bring the run back, with a new session folder and two ntfy messages.

    **Never run the same run on the PC and on the server at the same time.**
11. **Everyday use.**
    - Is it running? `systemctl status trading-bot-live@first_paper`
    - The run's own log: `tail -f ~/trading-bot/trading-bot/live_runs/first_paper/run.log` (Ctrl+C leaves the
      display; the bot keeps running)
    - What the system saw: `journalctl -u trading-bot-live@first_paper -n 100`
    - Today's state: `cat .../live_runs/first_paper/summary.md`
12. **Updating the bot.**
    - `cd ~/trading-bot && GIT_SSH_COMMAND="ssh -i ~/.ssh/github_deploy" git pull`
    - If `requirements.txt` changed, rerun the pip line from step 7.
    - Then `sudo systemctl restart trading-bot-live@NAME`. A restart is a new session (warm-up again, local book
      from the account's value), so do it well away from 00:00 UTC.
13. **Keep a copy at home.** The session files (`candles.csv`, books) are not committed, so the server is their only
    home besides OVH's daily backup. Weekly, type in PowerShell:
    `scp -r debian@YOUR_IP:trading-bot/trading-bot/live_runs C:\path\to\copy`.

---

## 6. What other people running small bots report

Weight runs high to low: official doc > maintained community doc > many consistent users > single anecdote >
seller's blog.

| Source, date | What it says | Weight |
|---|---|---|
| freqtrade docs, installation and advanced setup (stable, undated) | Docker is the recommended install; on Raspberry Pi use Docker. The bot can report to systemd so systemd restarts it after a failure. No VPS provider is named | official |
| hummingbot docs, installation (undated) | 4 GB RAM and 1 vCPU per instance; reach it through Tailscale rather than opening a port | official |
| Oracle docs, Always Free resources | idle machines are reclaimed (under 20% CPU, network and memory over 7 days) | official |
| InfoQ, 2026-07; linuxiac | Oracle halved the free ARM allowance without announcement (15 June 2026); machines above the new limit terminated from 18 August 2026 | press, consistent |
| community.oracle.com, r/oraclecloud, 2024–26 | accounts closed without warning and without recovery | many users |
| r/hetzner, LowEndTalk, 2024–26 | new accounts refused or cancelled after ID checks; staff advise not to use a VPN at sign-up | many users |
| r/VPS, Jun 2024 to Jan 2025 | Contabo: CPU "steal" of 20–80% (the host lends your processor to others); a new server suspended because its recycled IP had abuse reports; some long-term users satisfied | many users, mixed |
| Hetzner terms | crypto **mining** is forbidden; nothing about **trading** | official |
| theblock.co, 2022 | Hetzner told a customer that broader crypto activity breached its terms | single, old |
| ccxt blog "How far is your exchange", 2025–26 | Bybit refused data-centre addresses in 4 of 5 samples; Binance refuses most US addresses | community measurement |
| quotaguard blog | Kraken is "less aggressive" on IPs than other exchanges | seller's blog |
| Home Assistant community; Raspberry Pi white paper RP-003610-WP | SD cards corrupt on power cuts; use an SSD and a small backup battery | many users + official |
| GitHub Actions docs | scheduled runs delayed at peak hours; public-repo schedules disabled after 60 days without activity | official |

Hidden costs found:
- IPv4 billed apart: Hetzner €0.50, Scaleway about €3, Fly $3.60.
- Backups billed apart: DigitalOcean and Vultr, about +20%.
- Setup fees: IONOS €10 HT; Contabo, amount unknown.
- Renewal prices: Hostinger €5.49 → €11.99.
- Expiring credits: AWS (6 months), Azure (12 months).
- Price rises in 2026: Hetzner (twice), OVH's previous range (+45%), Scaleway, Contabo, Raspberry Pi (+55%).

Not found:
- I found no host whose written terms ban trading bots, and no verified case of an account suspended for running one.
- r/freqtrade, r/algotrading and Hacker News gave no usable result through search.

---

## 7. How the choice evolved: second pass (2026-11-19)

A second round of searches on the gaps the first one left. The providers' and Kraken's own pages were still
blocked, so these are search extracts too.

| Gap | Found | Changes the choice? |
|---|---|---|
| Can a French resident use Kraken Futures? | No official list of eligible EEA countries found. **You already have a Kraken Futures account read by the bot**, so access is granted | no |
| Locking the key to the server's address | confirmed by two independent setup guides; IPv4 or IPv6 | no: it confirms the fixed-address need |
| OVH commitment | the €3.81 HT price is **12 months paid upfront** (about €54.86 with VAT, at once); about 18% more without commitment; no source gives the price after 12 months | no; it is a question for you (section 3) |
| OVH data centres | France: Gravelines, Strasbourg; Beauharnois is in Canada | no |
| OVH reliability | March 2021: a fire destroyed one Strasbourg data centre (SBG2); VPS customers without a backup lost data, and some backups were in the same building. OVH then promised backups for all; a March 2026 review says the new range's daily backups are stored in separate buildings (not confirmed on OVH's page) | no, but it makes step 13 (a copy at home) a rule: never rely on the provider's backup alone |
| Hetzner cheap plans | still unavailable at every check up to 2026-10-20; no restock date | no |
| netcup nano | snapshots included; the price was cut off in the extract | no |
| Oracle's free machine in France | Paris and Marseille regions exist; free ARM capacity there unknown | no: the idle-reclaim rule remains |
| Healthchecks free plan | Telegram and ntfy reported available | no |
| Latency to Kraken | matters for fast trading, not for one decision per day: any EU server is enough | no |

Sources of round 2:
- dev.to/neurau_tech/vps-pas-cher-en-novembre-2026-8-hebergeurs-compares-au-prix-officiel-25k6 (2026-11-13)
- ovhcloud.com/en/vps/vps-france/
- datacenterdynamics.com/en/opinions/lessons-ovh-fire-disaster-recovery-plans-are-not-work-fiction
- techradar.com/news/ovh-says-it-doesnt-hold-backups-for-some-systems-affected-by-data-center-fire
- docs.ovhcloud.com/en/guides/bare-metal-cloud/virtual-private-servers/starting-with-a-vps
- docs.tealstreet.io/docs/connect/kraken-futures
- help.haasonline.com/usage/exchanges/kraken-futures/
- docs.kraken.com/exchange/guides/rest/api-keys
- bitdoze.com/hetzner-cloud-cost-optimized-plans/
- docs.hetzner.com/general/infrastructure-and-availability/order-processing
- netcup.com/en/server/vps-lite
- docs.oracle.com/iaas/Content/General/Concepts/regions.htm
- dev.to/urtuba/drumbeats-vs-healthchecksio-an-honest-comparison-2026-1in9
- cybernews.com/vps/best-vps-for-trading-bots/

### Third pass: new ideas from recent user discussions (2026-11-19)

| Idea | Cost | Verdict |
|---|---|---|
| Black Friday yearly deals (LowEndTalk, LowEndBox) | can be €10–30 a year | second choice, under the conditions in section 3 |
| A 1 GB plan once few programs run (IONOS about €1.20/month + €12 setup; netcup pico €2.21/month, 12 months) | €1–2.5 a month | later, if several coins run in one program; not with one run per program and +1 a month |
| Used mini PC at home (e.g. ThinkCentre Tiny M720q/M920q), a popular homelab choice | $90–150 used + 6–15 W, about €11–26 a year | better than a laptop (no battery), same home risks; about €4–6 a month over 3 years, so no cheaper than OVH |
| Old Android phone with Termux | €0, a few watts | no: Android kills background programs unless set up carefully; PyPI's ready-made library files are for normal Linux, not Android, so the exact pinned versions cannot be installed directly |
| Ready-made bot hosting (VolatiCloud, RackWorks one-click) | from about $7/month | no: built for freqtrade, not for this bot |
| Keeping Oracle's free machine artificially busy | €0 | no: against the purpose of Oracle's idle rule; account risk |

What recent reviews add about the two finalists (Trustpilot, G2, hosttest, LowEndTalk; low to moderate weight):
- **netcup:** good uptime for many; support by ticket only, often slow (faster in German); maintenance of "a few minutes
  to an hour" called normal by netcup itself; VPS Lite prices up to +20% for new orders in September 2026.
- **OVH:** stable for long-term users; support split; CPU rated "fair" (irrelevant for one decision a day); price rises
  at renewal on its previous range from 2026-10-01.
- A maintenance reboot means a restart, so a new session with a new warm-up. The setup plan's alerts report it; near
  00:00 UTC it would delay that day's decision.

Sources of round 3:
- lowendtalk.com/discussion/221336/netcup-price-increase-september-2026
- trustpilot.com/review/netcup.com
- hosttest.co.uk/reviews/netcup-vps
- g2.com/products/ovhcloud
- capitalandcompute.net/blog/ovhcloud-price-increase-2026/
- us.ovhcloud.com/lp/new-services-repricing/
- lowendbox.com/tag/black-friday-vps-deals/
- vpsbenchmarks.com/black_friday_vps
- lowendtalk.com/discussion/223377/petrosky-black-friday-sale-30-off-kvm-vps-in-canada-france-from-4-89-mo
- budgethomelab.pages.dev/articles/used-mini-pc-homelab-under-200/
- idlewatt.vercel.app/models/lenovo-thinkcentre-m920q-tiny
- dev.to/shaktitiwari/how-to-use-termux-for-nse-algorithmic-trading-a-complete-guide-2026-a2d
- volaticloud.com/crypto-trading-bot-hosting

## 8. What I could not verify ("I do not know")

**Prices**
- **No price was read on a provider's own page**: this session's network blocked them, and all come from search
  extracts or third-party pages.
- OVH: the renewal price after the 12-month commitment, and whether a running VPS can move to it later; whether a
  Debian 13 image is offered.
- netcup: the nano price, re-checked in round 2 but cut off; whether daily automatic backups exist besides
  snapshots. Contabo: the setup fee. Hetzner: whether the cheap plans can be ordered today (unavailable at every
  check up to 2026-10-20).
- The USD-to-EUR rate.

**Kraken**
- Whether France is absent from the **full** restricted list. Kraken's support pages could not be opened, and a
  second search found no official list of eligible EEA countries. Your existing Futures account answers the access
  question; whether real orders need more steps on it is for Kraken support or your account page.
- Whether Kraken blocks US or data-centre addresses on the futures API.
- Whether the server's country is checked at all.

**Home and monitoring**
- Whether your internet provider gives a fixed address at home.
- Healthchecks.io's free-plan channels are confirmed only by a comparison article and a user report, not by its own
  page.

**The server itself**
- The OVH Debian image's default user name: `debian`, according to a copy of OVH's guide; not seen on OVH's own page.
- The service file and the alerts **have not been run** on any server.
- The memory figure comes from Linux in this container with synthetic candles. It has not been measured on the VPS.

## Sources (read through search extracts on 2026-11-19 unless stated)

**OVH**
- blog.ovhcloud.com/vps-2027-fr/
- dev.to/neurau_tech/vps-pas-cher-en-novembre-2026-8-hebergeurs-compares-au-prix-officiel-25k6
- next.ink/225720/ovhcloud-augmente-fortement-le-prix-de-ses-vps-2026-et-ipv4/

**netcup**: netcup.com/en/server/vps-lite

**Hetzner**
- northflank.com/blog/hetzner-cloud-server-price-increases
- bitdoze.com/hetzner-cloud-cost-optimized-plans/
- findstack.com/resources/hetzner-price-increase-2026
- docs.hetzner.com/general/security-and-identify/fraud-prevention-faq/
- hetzner.com/legal/terms-and-conditions/

**Scaleway**: scaleway.com/en/blog/a-transparent-update-on-scaleway-pricing/

**Contabo**
- pricingsaas.com/companies/contabo.main/diffs/2026W25
- contabo.freshdesk.com/en/support/solutions/articles/103000398194

**IONOS**
- experte.com/fr/serveur/vps-pas-chers
- whtop.com/plans/ionos.fr/140732

**Vultr, DigitalOcean, Linode**
- costbench.com/software/cloud-infrastructure/vultr/
- activepieces.com/blog/digitalocean-pricing-plans-and-real-costs-in-2026.md
- activepieces.com/blog/linode-pricing-plans-costs-and-extra-fees-2026.md

**Hostinger**: ouiheberg.com/fr/comparatifs/meilleur-vps-france-2026

**Oracle**
- docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- infoq.com/news/2026/07/oracle-cloud-free-tier-limits/
- linuxiac.com/oracle-quietly-cuts-free-tier-ampere-a1-resources-in-half/

**AWS**
- aws.amazon.com/about-aws/whats-new/2025/07/aws-free-tier-credits-month-free-plan
- docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-bundles.md

**Google Cloud**
- cloud.google.com/free/docs/compute-getting-started
- cloud.google.com/run/pricing

**Azure**
- azure.microsoft.com/en-us/free/virtual-machines
- costcalc.cloudoptimo.com/azure-pricing-calculator/vm/Standard-B1s

**Managed platforms**
- fly.io/docs/about/pricing/
- docs.railway.com/pricing/plans
- render.com/pricing
- northflank.com/pricing
- blog.pythonanywhere.com/222/
- techzine.eu/news/infrastructure/138611/salesforce-puts-heroku-development-on-hold/
- koyeb.com/blog/koyeb-is-joining-mistral-ai-to-build-the-future-of-ai-infrastructure

**GitHub Actions**
- docs.github.com/en/billing/concepts/product-billing/github-actions
- docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features

**Kraken**
- coindesk.com/business/2025/05/20/kraken-rolls-out-regulated-crypto-derivatives-in-europe
- support.kraken.com/articles/derivatives-eligibility-requirements-eea
- support.kraken.com/articles/360023786632-kraken-derivatives-eligibility
- amf-france.org/en/warnings/white-lists/daspcasp/payward-europe-solutions-limited-kraken-digital-asset-exchange-kraken
- docs.kraken.com/api-reference/api-keys/check-v3-api-key
- docs.kraken.com/api/docs/guides/futures-rate-limits

**Monitoring**
- healthchecks.io/pricing/
- docs.ntfy.sh/publish/
- pushover.net/pricing

**Home device and electricity**
- raspberrypi.com/news/price-increases-for-2gb-raspberry-pi-4-and-raspberry-pi-5/
- jeffgeerling.com/blog/2024/new-2gb-pi-5-has-33-smaller-die-30-idle-power-savings/
- raspberrypi.com/news/trixie-the-new-version-of-raspberry-pi-os/
- Selectra/hellowatt summaries of the CRE decision of 2026-07-15 (EDF Tarif Bleu)
- synology.com/en-us/products/DS224+?tab=specs

**Community**
- freqtrade.io/en/stable/installation and /advanced-setup/
- hummingbot.org/client/installation/
- docs.ccxt.com/blog/how-far-is-your-exchange
- quotaguard.com/blog/static-ip-crypto-trading-bot-binance-okx-bybit-kraken
