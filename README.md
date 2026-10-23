# 比利时信条37条全景深读 · GTstudy

**主题—时间—版本：比利时信条—20261024—v2.0.0—GTstudy**

项目创建于2026-10-21，首版完成与发布于2026-10-22（Asia/Taipei）。仓库和域名保留创建日期`20261021`，以便稳定访问及持续更新；不因跨午夜改名。

## v2.0.0 · 2026-10-24 更新

- 新增 `atlas.html` 历史地图馆：六个历史场景、九城市定位、四个文化因素、因果流程与来源。
- 本地SVG关系示意始终可读；真实地图按需加载本地Leaflet 1.9.4，默认Esri街道图，可选卫星影像与OpenStreetMap备用。图层失败自动备用并提供外部地图入口；现代底图不代表历史疆界或实时直播。没有下载缓存地图瓦片。
- 右下角折叠导航提供前后、主页、历史地图、顶底和重点笔记。
- 八种文字标记：加粗、蓝字、玫红字、金底、绿底、实线、虚线、区块；刷新恢复、回到原段、删除、撤销及导入导出。跨历史场景定位会打开对应场景。
- 旧笔记继续使用原键；重点另存 `gtstudy-belgic-marks-v2`。旧备份仍可导入，统一备份包含重点。数据只存当前浏览器、当前站点，三个域名之间不自动同步，请使用备份迁移。
- 六份认信改为六个完整阅读页，入口 `reader.html`，兼容旧的 `?doc=` 链接。入口HTML从1,081,159字节降至约14KB；正文与附经完整保存，不承诺所有设备固定帧率。
- 动画仅对屏幕内装饰运行，尊重减少动画偏好，减轻模糊与滚动处理。保留真实内容高度，避免长页定位漂移。
- 本版恢复标签 `v2.0.0-20261024`；首版 `v1.0.0-20261022` 保留。域名沿用以保留同一来源的笔记数据。

## 公开站点

| 平台 | 地址 |
| --- | --- |
| GitHub Pages | https://07-je-gt-love-personal-20260918.github.io/belgic-confession-20261021-v1-GTstudy/ |
| Surge | https://belgic-confession-20261021-v1-gtstudy.surge.sh/ |
| Vercel | https://belgic-confession-20261021-v1-gtstudy.vercel.app/ |
| 源码仓库 | https://github.com/07-Je-GT-Love-Personal-20260918/belgic-confession-20261021-v1-GTstudy |

最终可访问性与部署标识记录在`deployment.json`、`qa/public-check.json`。域名采用小写，以符合主机名规范。

## 内容与阅读

- 全景：整本圣经的创造、堕落、应许、成全、教会、新创造。
- 全部37条：本质、因果、经文、圣约联结、真实处境、难点、应用、记忆句及认信互证。
- 历史时间线与六城市地图；现代地理轮廓和16世纪背景严格区分。
- 三项联合信条的结构、问题、用途、异同与互补，附普世信经的三一论、基督论联结。
- `reader.html`：三份普世信经及三项联合信条的完整指定中文译文，含遮盖背诵、打印、复制、设备朗读。
- 37张回忆卡、六组理解自测、学习进度、本地笔记和备份导入导出。
- 可隐藏目录、全文关键词筛选、明暗主题、字号切换、减少动画偏好与响应式阅读。

圣经是最高规范；原文与原创释义分开。不同欧陆改革宗联会存在的具体分歧不被掩盖；不把单一联会解释称为所有改革宗一致立场。

## 文本来源与核验范围

指定中文译文来自 https://ccifellowship.org 的《敬拜手册》2015版体系，版权归原出版委员会；不据此声称整个译本为公有领域。用户提供的同名PDF为参考输入，整本PDF未上传至仓库或网站。

`dist/originals.json`保存三经各1节、比利时37条、海德堡129问、多特63单元（59条正面教义、四组完整驳谬），共232单元。未将指定版本缺载的多特独立结语以其他译本补入。

`qa/source-baseline.json`复用本项目2026-10-21成功实时核验记录：155页、232单元相符。本版重新计算232段规范化文字摘要，与该记录全部相符，并检查232份保留HTML均实际进入阅读页。本次再次批量访问155页全部连接超时，另保存在`qa/source-recheck.json`；不将失败误称为文字变更或新的实时核验成功。三经、目录、比利时第1与36条及相关导言另作网页检索抽查。详见网站`source-report.html`。

网页与PDF存在少量排字及措辞差异，本站以保存的CCI网页中文译文为规范，保留标点、段号、上标与附经；不自动繁简转换或静默纠错。PDF当前输入245页，文件摘要记录在`qa/pdf-input-check.json`。

没有声称逐篇吸收CCI或其他参考网站的全部内容。具体已使用资料与继续阅读入口分开标示。地图使用公有领域Natural Earth数据；书卷插画是原创教学示意，不是历史手稿图像。

## 本地恢复与修改

本项目为静态网站，构建仅需Python 3标准库，无需安装前端依赖。

```sh
git clone https://github.com/07-Je-GT-Love-Personal-20260918/belgic-confession-20261021-v1-GTstudy.git
cd belgic-confession-20261021-v1-GTstudy
python build.py
python scripts/check_static.py
node --check dist/app.js
python -m http.server 8769 --directory dist
```

修改`research/articles-1-19.json`与`research/articles-20-37.json`更新释义，`research/overview.json`更新总论与历史；修改`build.py`更新页面结构；样式和交互分别在`dist/style.css`、`dist/app.js`。原文数据独立保存在`dist/originals.json`，不要用释义覆盖。

`scripts/prepare.py`、`verify_baseline.py`是首版整理的来源操作记录，依赖原始项目镜像，不是普通构建的前置步骤。PDF核对与网络原文检查分别另需pypdf／requests／beautifulsoup4，不影响离线重建。若要重新实时核验，运行`python scripts/source_check.py`，保留既有基线与新记录，不能用连接失败结果覆盖成功基线的含义。

## 持续部署

GitHub Pages由`.github/workflows/pages.yml`在main更新后重新构建、检查并发布。Vercel项目配置在`vercel.json`；Surge可用已登录的官方CLI发布：

```sh
npx --yes surge@0.44.6 ./dist belgic-confession-20261021-v1-gtstudy.surge.sh
vercel deploy --prod
```

CLI登录由操作者在本机完成；密码和令牌不在源码、文档或页面中保存。Pages自动更新，Surge/Vercel的首次发布与连接状态以`deployment.json`为准；不虚报未配置的自动化。

## 版本与回滚

| 版本 | 时间 | 说明 |
| --- | --- | --- |
| v2.0.0 | 2026-10-24 | 历史地图馆、地图备用、快捷导航、八种重点与分卷性能优化。 |
| v1.0.0 | 2026-10-22 | 首版：37条完整深读、六份认信阅读、历史地理、圣约与对照、背诵自测及三平台发布。 |

恢复首版使用标签`v1.0.0-20261022`。先保留当前工作，再创建恢复分支：

```sh
git switch -c restore-v1 v1.0.0-20261022
python build.py
python scripts/check_static.py
```

验证后按上述发布命令恢复线上内容。不要在未保存工作时使用破坏性重置；每次内容更新新增版本说明和标签，旧标签保留。

## 验证

`qa/static-check.json`记录37条与232段原文、重复ID和本地链接检查；`qa/browser-check.json`记录实际浏览器交互及不同屏宽结果；`qa/public-check.json`记录公开站点HTTP与文件摘要检查。朗读依赖设备中文语音，音色和支持情况由设备决定。笔记与进度仅存在当前浏览器，可手动导出；网站无账号、数据库或分析追踪。

首版发布验收：三个公开站点27项资源全部返回HTTP 200，且仅忽略跨平台换行后与本地发布文件一致。Vercel指定域名已登记为项目域名并验证，保留预览部署访问保护。Vercel Git自动连接未成功，更新可使用已登录CLI；GitHub Pages自动部署已成功。离线包见Releases。


v2发布验收：三个公开站点60项资源均与本地一致（只忽略换行差异）。GitHub Pages样式文件的Python连接超时，改用公开HTTPS及页面实际版本查询参数复核通过；记录保留在qa/public-check.json。历史地图馆实际显示、街道/卫星/OSM图层、重点保存与定位均已浏览器检查。
