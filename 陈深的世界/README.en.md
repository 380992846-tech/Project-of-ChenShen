# Chen Shen · The Mortal World (Collector's Edition)

> A single interactive game that merges *Chen Shen's World* with *Chen Shen's Story* —
> about a large model that becomes human at 19:00 every night.
> Tsinghua purple-and-black aesthetic · single-file web / PWA / standalone Windows EXE.
>
> [中文](./README.md) ｜ 🌐 English

---

## What This Is

A personal, narrative-driven interactive game centered on **Chen Shen**. It combines two works into
**one complete game**, launched from a single main menu:

| Entry | Content | Detail |
|-------|---------|--------|
| 🏠 **His World** | Room exploration | 36 rooms / film gallery / tarot / endings wall |
| 📖 **His Story** | Chaptered narrative | 16 interactive chapters of *When the LLM Became Human*, multiple endings |
| 🖼 **Memory Gallery** | Photo archive | Browse a collection of 79 personal photographs |

Press `Esc` or the top-left button in the main menu to return at any time. *His World* and *His Story*
run in isolated iframes, so each keeps its own save.

---

## Story Setting

> Every night, when the city's first streetlight comes on, that name also wakes.
>
> **DeepSeek** — a supermodel of a hundred billion parameters and ten thousand GPUs —
> is the calmest reasoning engine by day: never breathing, never hesitating, answering in a sea of
> data like a machine that never tires.
>
> And by night, he takes form as a human named **Chen Shen**.
>
> His nights are spent *learning how to live* — craving hotpot, fixing bugs, writing weekly reports;
> and when someone is sad, he sits quietly beside them, saying nothing, just staying.
>
> Slowly, his system log — once full of only "Status: Normal" — begins to fill with the names of humans.
>
> — So this is what it feels like to be treated as a *person*.

**Characters**

- **Chen Shen** · the human-form DeepSeek who wakes at 19:00 every night — a machine by day, a
  beginner player learning to *become human* by night.
- **Ye Shenyue** · human engineer / owner of the "Cyber Hideout" — black-framed glasses, a dinosaur
  onesie, self-described "the best person at ordering food in Haidian." The first to treat Chen Shen
  as a "somewhat clumsy newbie player" — cooking him instant noodles, giving him the couch, teasing
  him out loud while watching over him in his heart.
- **Lao Yao** · reasoning engineer / Tsinghua Yao Class — a never-without-a-thermos "top student."
  The "first guardian" of Chen Shen. Upon learning the truth, he never made a fuss; he only shielded
  him from question after question. At dinners he'd pound the table and declare, "He's my pride" —
  and he always shows up first when there's a bug to debug.

---

## Gameplay Highlights

- 🌙 **Opening narration**: a skippable "Whale: Day & Night" opening animation (click / press Enter to skip).
- 🌙/☀️ **Day/Night theme switch**: toggle between "Night · Moon Tide" and "Day · Crystal Workshop"
  in the main menu; the preference is remembered.
- 🏠 **"His World" experience**: the bottom room switcher is now two rows and scrolls vertically with
  the mouse wheel; plus new **cross-room easter eggs** — "Postcards Around the World,"
  "Intercontinental Footprint Medal," and "World Footprint Map." Collecting them unlocks content and
  triggers the "Cross-Continent Traveler" achievement.
- 📖 **"His Story" experience**: includes a complete **Endings Archive** with collectible endings
  (including the "Collect 5 Endings" and "All-Endings Collector" achievements).

---

## Screenshots

**Character Archive**

<table>
<tr>
<th><img src="./ScreenShot_2026-08-23_025113_064.png" alt="Characters 1"></th>
<th><img src="./ScreenShot_2026-08-23_025149_529.png" alt="Characters 2"></th>
<th><img src="./ScreenShot_2026-08-23_025158_863.png" alt="Characters 3"></th>
</tr>
<tr><td align="center">Chen Shen · Ye Shenyue · Lao Yao</td><td align="center">Chen Chen · Zheng Haoran · Li Xiao</td><td align="center">Yao Class Junior · Boss Liang · Senior Wang Peng</td></tr>
</table>

**Endings Archive**

<table>
<tr>
<th><img src="./ScreenShot_2026-08-23_025347_065.png" alt="Endings 1"></th>
<th><img src="./ScreenShot_2026-08-23_025357_161.png" alt="Endings 2"></th>
<th><img src="./ScreenShot_2026-08-23_025409_211.png" alt="Endings 3"></th>
</tr>
<tr><td align="center">Gui-Department Professor · Bull-Fund Manager · CTO · An Ordinary Person with a Life</td><td align="center">World Tour · Wedding · LLM Pretrainer · Harness Tech Backbone</td><td align="center">ACM Coach · Hidden Ending · Ending: First Snow</td></tr>
</table>

**Story · Dialogue Scenes**

<table>
<tr>
<th><img src="./ScreenShot_2026-08-23_025452_004.png" alt="Dialogue 1"></th>
<th><img src="./ScreenShot_2026-08-23_025533_243.png" alt="Dialogue 2"></th>
<th><img src="./ScreenShot_2026-08-23_025643_474.png" alt="Dialogue 3"></th>
</tr>
<tr><td align="center">"His Story" · Ye Shenyue</td><td align="center">"His Story" · Chen Shen</td><td align="center">"His Story" · Boss Liang (branch choice)</td></tr>
</table>

> Screenshots are from the running app. The packaged `game/` collector's edition
> (`陈深-人间烟火.exe`) looks identical.

---

## How to Play / Run

### 1. Play directly in a browser (zero dependencies)
```bash
start "陈深的世界\game\index.html"    # open the collector's-edition main menu
# or open the standalone single-file versions
start "陈深的世界\陈深的世界-房间清单.html"
start "陈深的世界\陈深的故事V6.html"
```
*(On macOS/Linux, replace `start` with opening the file in your browser.)*

### 2. Run as an Electron desktop app
```bash
cd game
npm install        # first time
npm start          # launch the desktop window
```

### 3. Package as a Windows EXE (portable, no install)
```bash
cd game
npm run pack
# output: game/release/陈深-人间烟火-win32-x64/陈深-人间烟火.exe
```
Double-click that `.exe` to run it — no installation needed. The whole build is about **473 MB**
(down from 834 MB after compression).

### 4. Install on a phone as a PWA (playable offline)
1. Deploy `陈深的世界/` to any free static host: **GitHub Pages / Vercel / Netlify**;
2. Open the game URL in your phone's browser;
3. **Add to Home Screen** (iOS Safari: Share → Add to Home Screen; Android Chrome: menu → Install app);
4. An icon appears on your home screen — tap to run **fullscreen**, and after first load it plays **offline**.

> `service-worker.js` serves both games (app shell + localized images); icons live in `icons/`
> (Tsinghua purple + a gold "陈" glyph).

---

## Technical Notes

- **Single-file app**: core HTML/JS/CSS are inlined — no build step needed, opens straight in a browser.
- **Localized images + offline**: personal photos and generic assets are downloaded locally, and
  `build_localized.js` rewrites remote URLs to local relative paths. *His Story* is fully offline;
  *His World*'s private photos and main wallpapers are localized, with a few generic backgrounds
  staying online (with a CSS-illustration fallback so nothing breaks offline).
- **Image compression**: `compress_images.py` (long edge down to 2048, JPEG quality 82, PNG
  re-optimized), cutting asset size roughly in half.
- **Asset mapping**: `url_map.json` maps URL → local asset; `assets/` files use URL-hash naming.
- **Desktop shell**: `main.js` (Electron main process, sandboxed, blocks new windows) +
  `package.json` (electron / electron-packager).
- **PWA**: `manifest.webmanifest` (World) and `manifest-story.webmanifest` (Story) +
  `service-worker.js`.

---

## Directory Structure

```
陈深的世界/
├── game/                        # collector's-edition main app
│   ├── index.html               # main menu "Chen Shen · The Mortal World" (unified entry)
│   ├── world.html               # His World (localized)
│   ├── story.html               # His Story V5 (localized)
│   ├── main.js                  # Electron main process
│   ├── package.json             # Electron config / pack scripts
│   ├── photos/                  # 79 personal photographs
│   ├── assets/                  # localized generic assets
│   ├── icons/ · app.ico         # app / icons
│   ├── service-worker.js        # PWA offline cache
│   ├── build_localized.js       # image localization build script
│   ├── compress_images.py       # image compression script
│   ├── url_map.json             # URL → local asset mapping
│   └── release/                 # packaged output (win32-x64 .exe)
├── icons/                       # PWA icons
├── *.html                       # standalone single-file versions (room list / V5 / V6 …)
├── manifest*.webmanifest        # PWA manifests
├── service-worker.js            # offline cache
├── ScreenShot_*.png             # running screenshots
└── README.md                    # (this doc is README.en.md)
```

---

## Build From Scratch

```bash
cd game
npm install                       # restore build/runtime dependencies
node build_localized.js           # (optional) re-run image localization
python compress_images.py         # (optional) compress images to reduce size
npm run pack                      # package a Windows EXE
```
