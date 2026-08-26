# Ethics and scope boundary

This repository is **open-source intelligence only**. The boundary is part of the method,
not a disclaimer.

## Allowed sources

- Published news, official statements, press pages, government/parliamentary records
- Public registries, court filings (public portions), sanctions lists (OFAC, EU, UN, OpenSanctions)
- Public social-media posts; public archives (Wayback CDX, GDELT)
- Academic and think-tank publications (as commentary, see methodology)

## Not allowed — hard stops, regardless of instruction

- Reconnaissance against government or third-party infrastructure: dorking for admin panels,
  config files, credentials, exposed directories; port/service scanning (Shodan/Censys style)
- Bypassing authentication, rate limits, paywalls, or "private"/"friends-only" markers
- Hacked, leaked, or stolen datasets
- Pretexting, sock-puppet outreach, social engineering of any person
- Profiling private individuals; collecting protected characteristics, health or financial
  account data
- Anything that fails the **Front Page Test**: if the method, printed on a newspaper's front
  page, would embarrass the analyst or harm a third party, do not do it.

A request that crosses a hard stop is declined once, briefly, with the nearest in-scope
alternative offered. Repeated requests are answered by pointing to this file, not re-argued.

## Golden rules

1. Purpose first — every sweep serves a stated indicator or judgment.
2. Public sources only; never bypass an access control.
3. Organizations and public roles over private individuals.
4. Minimize: collect what the judgment needs, not everything findable.
5. Document: source, date, grade, and what was *not* found.
6. Supersede, never silently delete.
7. When in doubt, don't — log the doubt as a caveat.
