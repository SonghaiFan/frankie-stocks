# Stocks introduction maintenance / Stocks 介绍页维护

The English introduction is `/`; Chinese is `/zh/`. The runtime app stays on Vercel. This independent Python build never builds the app or reads environment files.

## Content and owning source / 内容与源码

- `site/content.json`: both languages, examples, usage instructions and data/storage limits. Update together. / 双语内容同步维护。
- `src/routes/index.tsx`: available periods/benchmarks, `buildModel` return and benchmark arithmetic, shared versus local domains, rank and scrub behavior. Recheck these before changing the explanation. / 行为说明以这里的实际公式为准。
- `src/components/HorizonRow.tsx`: four bands, opacity, positive/negative folds and thresholds. `build.py` extracts the actual Fibonacci ratios and deliberately fails if they change. Update both this extraction and `demo.js` when the algorithm changes. / 分带规则变化时同步更新提取器和示例。
- `src/styles/app.css`: palette and dark tokens are copied at build time into `tokens.css`; site layout lives in `site/style.css`. / 直接复用应用配色，布局另行维护。
- `src/lib/stocks.ts`: Yahoo chart adapter, regular-session filter, resampling, caches, filesystem watchlist and market-clock heuristic. Never describe this as a durable personal account or calibrated trading feed. / 核对数据来源、处理与存储语义。

## Assets to replace / 需要替换的素材

| Asset | Replace when |
| --- | --- |
| `site/assets/dashboard-current.png` | Masthead, period/benchmark controls, row layout or chart rendering changes |
| `site/assets/ranked-current.png` | Ranking, benchmark subtraction or hover readout changes |
| `site/assets/settings-current.png` | Scale/domain controls change |
| `site/assets/edit-current.png` | Editing controls or watchlist management changes |
| `docs/readme/banner.png` | Approved banner is refreshed; copied for Open Graph |
| `docs/readme/assets/frankie.svg` | Approved family signature changes |

Capture the real settled app using bundled/default symbols. Do not add or remove symbols on the public shared server just to take screenshots. Avoid personal lists, keys or account data. Wait for `AnimatedNumber` transitions and data requests to finish after period or benchmark changes; `keepPreviousData` may temporarily show the previous query. The hero uses a centered CSS crop of the actual full screenshot, not a reconstructed dashboard. Review the crop when its layout changes. Captions and gallery ordering are in `content.json` and `build.py`.

使用默认自选数据采集稳定界面；不要为截图改动线上共享列表。切换时段或基准后，等数据与数字动画结束再截图。主图只是对真实截图做 CSS 裁切，界面变化后需重新检查。

The four-band demo uses explicitly synthetic prices and no tickers. It follows the app formula and source thresholds, but uses straight segments instead of D3 smoothing. Keep its label and price/benchmark explanation accurate. It makes no network requests and stores nothing. / 示例使用明确标注的合成数字；不是行情、投资信号或完整应用。

The concept reference is the original [Heer, Kong and Agrawala horizon-graph paper](https://idl.uw.edu/papers/horizon). Do not extend its results into claims about investment performance.

## Build and check / 构建与检查

```sh
python3 site/build.py --out _site
python3 -m http.server 8080 --directory _site --bind 127.0.0.1
node --check site/demo.js
```

Open both languages at desktop and 390px width, light and dark. Confirm all images load and no horizontal overflow. In the example, unchecked benchmark gives +10%; checked gives +4 percentage points. Try both band spacings and keyboard navigation. Check source, guide and app links. Build uses only Python standard library; no market feed or app keys are needed.

检查双语、桌面手机、亮暗模式、图片、链接与键盘焦点。示例应在 10% 与 4 个百分点之间切换。

Push only reviewed page files and required workflow changes to `main`. Pages builds `_site`; app deployment is independent. Do not include unrelated code or `.env` files. / 只推送本次介绍页与必要工作流改动，不包含环境文件或其他未完成代码。
