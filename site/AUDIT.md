# Stocks introduction code, UI and concept audit

Audited 2026-11-06. Scope: `site/` and the Pages input-watch paths. No app behavior, dependency, key, server watchlist or environment file was changed.

## Design read

Reading this as an explanatory introduction for people comparing a thematic watchlist, preserving the actual app’s Braun-like paper/ink, hairlines and restrained Klein blue controls. Green/red remain data signals. Variance 5, motion 1, density 4. The build copies real light/dark tokens from `src/styles/app.css`; native CSS extends them, with stronger prose contrast. This replaces the old sage template. No new UI framework, font network dependency or generated art.

## Real app inspected

Opened https://frank-stocks-songhaifans-projects.vercel.app in shared Ego9/p4 after the coordinating agent resumed the workspace. The initial empty/loading state resolved to real data for the bundled thematic rows. Chose M, S&P 500, Rank, hover readout, Normal/Fibonacci and Global/Local per stock. Opened Edit, then exited without adding/removing a symbol or altering shared server data. Four actual settled screenshots are under `site/assets/*-current.png`. Captured date is explicit; displayed values are a feed snapshot, not independently verified market quotes or predictions. Waited for data/number transitions before the final hero capture.

## Source read and resulting explanations

- `src/routes/index.tsx`: periods and benchmarks, theme labels, rank, scrubbing, add/remove, query retry/refetch and `keepPreviousData`. `buildModel` starts each row at its first returned close, computes simple percentage price change and subtracts the benchmark change at matching dates. Missing benchmark dates currently subtract zero. The stats are means of loaded rows, not weighted portfolio returns. Symbols can recur across themes.
- `src/components/HorizonRow.tsx`: four sign-separated layers, source opacity and actual Fibonacci thresholds versus equal-width bands. D3 area uses `curveMonotoneX`. Global domain uses common dates and a shared 98th-percentile magnitude; Local normalizes each row’s own dates and magnitude. Outliers can saturate the color range, so readouts matter.
- `src/lib/stocks.ts`: raw Yahoo chart close data, regular-session filtering, isolated-spike heuristic, mean-bucket resampling and period-sensitive cache. No adjusted-close/dividend-reinvestment total-return calculation. Client/server caches mean no tick-by-tick accuracy promise.
- `src/routes/api/watchlist.ts`, `watchlist.$symbol.ts` and filesystem functions: mutable server workspace without auth. Local files live beside the running server; Vercel `/tmp` is warm-instance storage, not durable per-user storage. No browser-local personal watchlist or backup UI is claimed.
- `getMarketStatus`: weekday/hour heuristic in New York, without exchange-holiday handling. The page explains this rather than treating Closed/Open as an authoritative exchange calendar.
- `src/styles/app.css`, `src/routes/__root.tsx`: actual visible product name, source tokens/type and family signature.

The tiny diagram is explicitly synthetic. It adapts the actual return and band arithmetic; build extracts the app’s thresholds. Straight-segment paths simplify the app’s D3 smoothing. There are no ticker recommendations, quote requests, saving or account side effects. At the example’s end, 100→110 is +10%; against 100→106 it is +4 percentage points.

## Primary references

Read the original author/lab page for [Heer, Kong and Agrawala, Sizing the Horizon (CHI 2009)](https://idl.uw.edu/papers/horizon), DOI10.1145/1518701.1518897. The page paraphrases layering bands to reduce chart height and links this primary source. It does not reuse the study’s empirical results to claim this app improves decisions or investment performance.

Read official [D3 area documentation](https://d3js.org/d3-shape/area) to ground the distinction between a filled area generator and this adapted band diagram. App-specific formulas and storage claims come from owning code, not general finance marketing.

## Verification

- Standard-library Python build generated English `/` and Chinese `/zh/`.
- Coordinating HTML/asset/link checker: two pages, zero issues. `node --check site/demo.js` and `git diff --check` passed.
- Actual browser example produced +10% without benchmark, +4 percentage points with benchmark; both band modes render eight sign/layer paths.
- EN and Chinese at actual390×844 per-target emulation: innerWidth390 / scrollWidth390. Desktop no overflow. Desktop and Chinese mobile screenshots visually reviewed. Device override cleared afterward.
- Light/dark and image readiness checks completed below. No Lighthouse score or financial-data accuracy certification is claimed.
- All six images loaded after explicitly checking lazy gallery readiness. Actual light prose color is approximately #62615f on #f4f3f1; dark prose approximately #a7a6a3 on #151514, providing readable contrast while preserving the source palette. Dark desktop and final Chinese phone screenshots were visually reviewed; media override cleared.
