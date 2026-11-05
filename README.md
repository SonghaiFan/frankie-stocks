![Frank Stocks](docs/readme/banner.png)

# Frank Stocks

[English](README.md) · [简体中文](README.zh-CN.md)

Keep a thematic watchlist and compare how its stocks move across time.

[Guide](docs/guide.md) · [Run locally](#run-locally)

## What it does

- Group stock symbols by the themes you follow.
- Compare price history and return horizons with SVG charts.
- Change periods, scales and benchmark comparisons.

## Run locally

```sh
npm ci
npm run dev
```

Open the local URL printed by Vite.

## Before you start

The local watchlist lives in `watchlist.json`. Market data comes through server routes, and `price_cache.json` is a generated cache. Available charts depend on the data returned by the feed.

## For developers

```sh
npm run build
npm run preview
npm start
```

[Project guide](docs/guide.md) · [Artwork](docs/readme/README.md)

---

Made by [Songhai Fan](https://github.com/SonghaiFan) · A Frankie project
