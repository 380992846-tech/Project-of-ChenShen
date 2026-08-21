# 陈深的世界 · 互动游戏

> 《陈深的世界》互动游戏系列 —— 清华紫黑风格、单文件应用，双击即开。
> 📖 想了解世界观与玩法，请看 [`游戏介绍.md`](游戏介绍.md)。

## 游戏列表

| 文件 | 说明 | 大小 |
|------|------|------|
| `陈深的世界-房间清单.html` | ★ **《陈深的世界》**：36 房间 / 电影画廊 / 塔罗 / 结局墙（图片经 jsDelivr CDN 加载） | 335 KB |
| `陈深的故事V5.html` | ★ **《陈深的故事 V5 》**：DeepSeek成为人类的 16 章互动剧情 | 1.2 MB |

## PWA Mobile适配

两个游戏都已配好 **PWA**（可安装、可离线玩）：

| 游戏 | manifest | 入口 |
|------|----------|------|
| 《陈深的世界》 | `manifest.webmanifest` | `陈深的世界-房间清单.html` |
| 《陈深的故事 V5》 | `manifest-story.webmanifest` | `陈深的故事V5.html` |

共享 `service-worker.js`（离线缓存两个游戏 + CDN 图片）+ `icons/` 图标。

**手机上用**（需要先托管）：
1. 把 `陈深的世界/` 部署到 **GitHub Pages / Vercel / Netlify**（任选一个，免费）；
2. 手机浏览器打开游戏地址；
3. **添加到主屏幕**（iOS Safari：分享 → 添加到主屏幕；Android Chrome：菜单 → 安装应用）；
4. 图标出现在桌面，点开**全屏运行**，首次加载后**离线也能玩**。

> 说明：`service-worker.js` 会缓存应用外壳 + 运行时缓存 CDN 图片（`/photos/`），
> 实现离线。图标在 `icons/`（清华紫 + 金色"陈"字）。

## 部署（三选一）

**① GitHub Pages**（免费、跟着仓库走）
1. 代码已推送到 GitHub 仓库；
2. 仓库 Settings → **Pages** → Source 选 **Deploy from a branch** → 分支 `main`、目录 `/(root)`；
3. 等 1–2 分钟，访问 `https://<你的用户名>.github.io/Project1/陈深的世界/陈深的世界-房间清单.html`

**② Vercel / Netlify**（免费、无需 git，拖拽即可）
1. 打开 vercel.com 或 netlify.com；
2. 新建项目 → **Upload / Drop** → 把整个 `陈深的世界/` 文件夹拖进去；
3. 部署后得到一个 URL，手机打开即可（PWA 也生效）。

**③ 本地预览**：直接双击 HTML 就能玩；PWA 的"安装/离线"功能需在 https 托管下才完整。

>  手机想"像 app"：部署后用手机浏览器打开，选"添加到主屏幕"，桌面会出现图标、全屏运行、可离线。

## 技术说明

- **单文件应用**：所有 HTML/JS/CSS 内嵌，无需构建，直接浏览器打开。
- **图片素材**：存于仓库 `photos/`，游戏通过 **jsDelivr CDN** 加载（CDN 链接钉在某 commit，缓存稳定；改 `photos/` 目录会断图）。
- **体积**：《陈深的故事 V5》约 1.2MB，首次加载较慢；如需优化可做图片懒加载 / 资源外置（见 `docs/架构说明.md`）。

## 打开方式

```bash
# 本地直接开
start 陈深的世界/陈深的世界-房间清单.html
# 或部署到任意静态托管（GitHub Pages / Vercel / Netlify）
```
