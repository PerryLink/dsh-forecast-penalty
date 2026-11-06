#!/usr/bin/env python3
"""README visuals for dsh-forecast-penalty, derived from the shipped pipeline.

Everything drawn here is read off the repository, not off a generic checker
template:

  * `src/index.ts` registers `forecast_penalty` and calls
    `readMaterial` -> `parseMaterial` -> `runCheck` -> `buildView`;
  * `src/model.ts` declares the 12 canonical row columns and the 4 header
    fields, and `parseMaterial` canonicalises the material's own column names
    onto them;
  * `rules/forecast-penalty.yaml` declares the seven rules: FP-001
    `headerPresence`, FP-002 `number`, FP-003 `formula` (percent,
    forecastValue / actualValue x 100, tolerance 1.5), FP-004 `formula`
    (product, penaltyBase x penaltyRate, tolerance 0.01), FP-005 `pattern`,
    FP-006 `unique`, FP-007 `containsAny`; every rule carries
    `basis.kind` and the loader caps severity by it;
  * `src/shared/rows.ts` either adds an issue (`locator` row + canonical field,
    `found` / `expected` / `fix`) or hands the reason to `ctx.skip`, and
    `runTableCheck` puts every rule that did not run in `skipped`.

Outputs
-------
hero 1440x576, four WebP files (`-hero-{zh,en}-{light,dark}.webp`)
    Left column: kicker / wordmark / two value lines / two subtitle lines /
    meta / footer. Right side: the plugin's own instrument, not a generic
    diagram --
      (1) one real ledger row from `tests/fixtures/FP-003-unsafe.json`
          (period 2026-03, forecast 966, actual 1000, accuracy 88.00,
          charge 4000, currency CNY) with the rule that mounts on each column
          printed underneath it, and FP-001 annotated on the header fields;
      (2) the finding card for FP-003 with the engine's own arithmetic
          (966 / 1000 x 100 = 96.6, gap 8.6 pp > tolerance 1.5) and a
          tolerance ruler showing the declared 88.00 needle against the
          expected 96.6 band.
    The hero therefore shows one run of one documented fixture; nothing is
    invented.

flow 1100x660, two hand-written SVG files (`-flow-v5-{light,dark}.svg`)
    Grammar: a RULE SCOREBOARD WITH TWO INSTRUMENTS -- not a row of nodes.
    Two input strips (`material / file` and `rules/*.yaml`) feed one scoring
    panel: seven rows (rule, field, check kind, basis -> severity cap,
    disposition). The two arithmetic rules carry their own instrument in the
    disposition column: a tolerance ruler for FP-003 (declared 88.00 against
    expected 96.6, tolerance +/-1.5 pp) and an equation receipt for FP-004
    (80 x 50 = 4000, declared 4000, |diff| = 0 <= 0.01). Below the panel the
    two exits are drawn separately: `issues[]` (one located finding) and
    `skipped[]` (dashed, empty for this run, with the three reasons a rule can
    land there). The labels are English so all five README languages share the
    same pair; the alt text is localised in each README.

Text is measured before it is drawn; a label that would overflow aborts the
run instead of shipping clipped text.

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow, Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf.
"""
from __future__ import annotations

import os
from functools import lru_cache
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")
NAME = "dsh-forecast-penalty"

FONT_FILES = {
    "cjk": r"C:\Windows\Fonts\msyh.ttc",
    "cjk_bold": r"C:\Windows\Fonts\msyhbd.ttc",
    "mono": r"C:\Windows\Fonts\consola.ttf",
    "mono_bold": r"C:\Windows\Fonts\consolab.ttf",
}
for _kind, _path in FONT_FILES.items():
    if not os.path.exists(_path):
        raise SystemExit(f"FATAL: font missing: {_path}")
os.makedirs(OUT, exist_ok=True)

RADIUS = 20
SHADOW = 26

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", edge="#e6e2ef",
        text="#16171d", sub="#4d5261", faint="#8b90a0",
        accent="#4B67B4", pill="#ece7f9", band="#f5f2fb", grid="#e7e4f0",
        mark="#b45309", mark_bg="#fdf3e9",
        ok="#15803d", ok_bg="#eaf6ee",
        shadow="#2b2440", shadow_a=34, glow=30,
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", pill="#242d42", band="#202839", grid="#262f42",
        mark="#d9a441", mark_bg="#2a2216",
        ok="#3fb950", ok_bg="#16281c",
        shadow="#000000", shadow_a=96, glow=44,
    ),
}


# ------------------------------------------------------------------ primitives
@lru_cache(maxsize=None)
def font(size: int, kind: str = "cjk") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], size)


_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def measure(text: str, size: int, kind: str = "cjk") -> float:
    return _MEASURE.textlength(text, font=font(size, kind))


def hx(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def mix(a: str, b: str, t: float) -> tuple[int, int, int]:
    ca, cb = hx(a), hx(b)
    return tuple(int(p + (q - p) * t) for p, q in zip(ca, cb))


def gradient(w: int, h: int, top: str, bottom: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    a, b = hx(top), hx(bottom)
    for y in range(h):
        t = 0.10 * (y / h) + 0.90 * (y / h) ** 1.25
        draw.line([(0, y), (w, y)],
                  fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: str,
         alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rgb = hx(color)
    for i in range(10, 0, -1):
        rr = r * i / 10
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=rgb + (max(1, int(alpha * (1 - i / 11))),))
    return Image.alpha_composite(img.convert("RGBA"),
                                 layer.filter(ImageFilter.GaussianBlur(r / 6))
                                 ).convert("RGB")


def card(img: Image.Image, box: tuple[int, int, int, int], s: dict,
         radius: int = RADIUS, shadow: int = SHADOW,
         fill: str | None = None, edge: str | None = None) -> Image.Image:
    x0, y0, x1, y1 = box
    if shadow > 0:
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        layer_draw = ImageDraw.Draw(layer)
        layer_draw.rounded_rectangle(
            [x0, y0 + shadow // 3, x1, y1 + shadow // 3],
            radius=radius, fill=hx(s["shadow"]) + (s["shadow_a"],))
        img = Image.alpha_composite(
            img.convert("RGBA"),
            layer.filter(ImageFilter.GaussianBlur(shadow / 2))).convert("RGB")
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(box, radius=radius, fill=hx(fill or s["card"]),
                        outline=hx(edge or s["edge"]), width=2)
    return img


def text_at(d: ImageDraw.ImageDraw, x: float, y: float, text: str, size: int,
            color: str, kind: str = "cjk", anchor: str = "ls") -> None:
    d.text((x, y), text, font=font(size, kind), fill=hx(color), anchor=anchor)


def tracked(d: ImageDraw.ImageDraw, x: float, y: float, text: str, size: int,
            color: str, kind: str = "cjk", tracking: float = 2.0) -> float:
    cursor = x
    for ch in text:
        d.text((cursor, y), ch, font=font(size, kind), fill=hx(color),
               anchor="ls")
        cursor += measure(ch, size, kind) + tracking
    return cursor


def require_w(text: str, size: int, kind: str, max_w: float,
              what: str) -> None:
    width = measure(text, size, kind)
    if width > max_w:
        raise SystemExit(
            f"FATAL: {what} overflows ({width:.1f}px > {max_w:.1f}px): {text!r}")


def fit(text: str, kind: str, max_w: float, start: int, minimum: int) -> int:
    for size in range(start, minimum - 1, -1):
        if measure(text, size, kind) <= max_w:
            return size
    return minimum


def fit_lines(lines: list[str], kind: str, max_w: float, start: int,
              minimum: int) -> int:
    size = start
    for line in lines:
        size = min(size, fit(line, kind, max_w, start, minimum))
    return size


def chip(img: Image.Image, s: dict, x: float, y: float, text: str, fg: str,
         bg: str, size: int = 11, kind: str = "mono", padx: int = 9,
         height: int = 23, dot: str | None = None) -> tuple[Image.Image, float]:
    width = measure(text, size, kind) + padx * 2 + (14 if dot else 0)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, y, x + width, y + height], radius=height / 2,
                        fill=hx(bg))
    if dot is not None:
        cy = y + height / 2
        d.ellipse([x + padx - 4, cy - 2.8, x + padx + 1.6, cy + 2.8],
                  fill=hx(dot))
    d.text((x + padx + (12 if dot else 0), y + height / 2 + size * 0.36), text,
           font=font(size, kind), fill=hx(fg))
    return img, x + width


def chip_right(img: Image.Image, s: dict, right: float, y: float, text: str,
               fg: str, bg: str, size: int = 11, kind: str = "mono",
               padx: int = 9, height: int = 23,
               dot: str | None = None) -> Image.Image:
    width = measure(text, size, kind) + padx * 2 + (14 if dot else 0)
    return chip(img, s, right - width, y, text, fg, bg, size, kind, padx,
                height, dot)[0]


def dashed_round_rect(d: ImageDraw.ImageDraw, box: tuple[float, float, float,
                                                         float], color: str,
                      radius: int, width: int = 2, dash: int = 6,
                      gap: int = 4) -> None:
    """Dashed rounded rectangle: four dashed edges plus four solid corners."""
    x0, y0, x1, y1 = box
    rgb = hx(color)

    def dashed(p0: tuple[float, float], p1: tuple[float, float]) -> None:
        length = ((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2) ** 0.5
        if length <= 0:
            return
        step = dash + gap
        pos = 0.0
        while pos < length:
            end = min(pos + dash, length)
            a = (p0[0] + (p1[0] - p0[0]) * pos / length,
                 p0[1] + (p1[1] - p0[1]) * pos / length)
            b = (p0[0] + (p1[0] - p0[0]) * end / length,
                 p0[1] + (p1[1] - p0[1]) * end / length)
            d.line([a, b], fill=rgb, width=width)
            pos += step

    dashed((x0 + radius, y0), (x1 - radius, y0))
    dashed((x0 + radius, y1), (x1 - radius, y1))
    dashed((x0, y0 + radius), (x0, y1 - radius))
    dashed((x1, y0 + radius), (x1, y1 - radius))
    d.arc([x0, y0, x0 + radius * 2, y0 + radius * 2], 180, 270, fill=rgb,
          width=width)
    d.arc([x1 - radius * 2, y0, x1, y0 + radius * 2], 270, 360, fill=rgb,
          width=width)
    d.arc([x0, y1 - radius * 2, x0 + radius * 2, y1], 90, 180, fill=rgb,
          width=width)
    d.arc([x1 - radius * 2, y1 - radius * 2, x1, y1], 0, 90, fill=rgb,
          width=width)


def ruler(img: Image.Image, s: dict, x0: float, x1: float, axis_y: float,
          vmin: float, vmax: float, declared: float, expected: float,
          tol: float, label_y: float) -> Image.Image:
    """Tolerance ruler: shaded +/-tol band around `expected`, needle at `declared`."""
    d = ImageDraw.Draw(img)
    scale = lambda v: x0 + (v - vmin) / (vmax - vmin) * (x1 - x0)
    band0, band1 = scale(expected - tol), scale(expected + tol)
    d.rectangle([band0, axis_y - 20, band1, axis_y],
                fill=mix(s["card"], s["accent"], 0.18),
                outline=mix(s["card"], s["accent"], 0.60), width=1)
    d.line([x0, axis_y, x1, axis_y], fill=hx(s["grid"]), width=2)
    for edge in (x0, x1):
        d.line([edge, axis_y - 5, edge, axis_y + 5], fill=hx(s["faint"]),
               width=2)
    ex = scale(expected)
    d.line([ex, axis_y - 26, ex, axis_y + 5], fill=hx(s["accent"]), width=2)
    nx = scale(declared)
    d.polygon([(nx - 5, axis_y - 28), (nx + 5, axis_y - 28),
               (nx, axis_y - 20)], fill=hx(s["mark"]))
    d.line([nx, axis_y - 20, nx, axis_y + 5], fill=hx(s["mark"]), width=2)
    # labels
    text_at(d, x0, label_y, f"{vmin:.0f}", 11, s["faint"], "mono")
    text_at(d, x1, label_y, f"{vmax:.0f}", 11, s["faint"], "mono", "rs")
    text_at(d, nx, label_y, f"{declared:.2f}", 11, s["mark"], "mono", "ms")
    text_at(d, ex, label_y, f"{expected:.1f}", 11, s["accent"], "mono", "ms")
    return img


# ------------------------------------------------------------------------ hero
HERO = {
    "zh": dict(
        kicker="DEEPSEEK HARNESS 插件 · 预测准确率考核核对",
        value=["核对台账的齐备与考核费用算术",
               "给出「哪一行、哪一栏、差什么」的清单"],
        sub=["七条随包规则（FP-001…FP-007）逐条核对台账；",
             "未能执行的检查写入 skipped，绝不静默通过。"],
        meta="forecast_penalty · v0.2.10 · Apache-2.0 · DSH ≥0.2.1 <0.3.0 · 只读 · 无网络",
        foot="PerryLink / dsh-forecast-penalty · 社区插件，与 DeepSeek 官方无关",
        sheet_title="考核台账 · 1 行",
        rule_chip="rules/*.yaml · 7 条",
        header_fields="subject 某某风电场 · market 省内现货",
        ok_chip="FP-001 · 0 diff",
        headers=["考核期", "预测值", "实际值", "准确率", "考核费用", "币制", "备注"],
        values=["2026-03", "966", "1000", "88.00", "4000", "CNY", "—"],
        tags=["FP-006", "FP-002", "—", "FP-003", "FP-004", "FP-005", "FP-007"],
        gutter="行 1",
        find_chip="FP-003",
        severity_chip="info",
        locator="第 1 行 · accuracy",
        find_line="填报 88.00，按定义式应为 96.6",
        formula_line="966 ÷ 1000 × 100 = 96.6",
        gap_line="差 8.6 个百分点 > 容差 1.5 · 依据封顶 ≤ info",
        report_line="issues[] 1 · skipped[] 0",
        human_chip="结论留给人",
        tol_caption="容差 ±1.5 pp",
    ),
    "en": dict(
        kicker="DEEPSEEK HARNESS PLUGIN · FORECAST ACCURACY CHECK",
        value=["Completeness and charge arithmetic,",
               "row, column, gap — verdict stays yours."],
        sub=["Seven bundled rules (FP-001…FP-007) check the ledger;",
             "unrun checks are named in skipped, never silently passed."],
        meta="forecast_penalty · v0.2.10 · Apache-2.0 · DSH ≥0.2.1 <0.3.0 · read-only · offline",
        foot="PerryLink / dsh-forecast-penalty · community plugin, not affiliated with DeepSeek",
        sheet_title="Assessment ledger · 1 row",
        rule_chip="rules/*.yaml · 7",
        header_fields="subject Some Wind Farm · market Provincial Spot",
        ok_chip="FP-001 · 0 diff",
        headers=["Period", "Forecast", "Actual", "Accuracy", "Charge", "Currency", "Remark"],
        values=["2026-03", "966", "1000", "88.00", "4000", "CNY", "—"],
        tags=["FP-006", "FP-002", "—", "FP-003", "FP-004", "FP-005", "FP-007"],
        gutter="row 1",
        find_chip="FP-003",
        severity_chip="info",
        locator="row 1 · accuracy",
        find_line="declared 88.00, expected 96.6",
        formula_line="966 ÷ 1000 × 100 = 96.6",
        gap_line="gap 8.6 pp > tolerance 1.5 · cap ≤ info",
        report_line="issues[] 1 · skipped[] 0",
        human_chip="verdict stays human",
        tol_caption="tolerance ±1.5 pp",
    ),
}


def hero(lang: str, skin: str) -> None:
    s = SKIN[skin]
    h = HERO[lang]
    W, H = 1440, 576
    img = gradient(W, H, s["bg_from"], s["bg_to"])
    img = glow(img, 1230, 92, 430, s["accent"], s["glow"])
    img = glow(img, 210, 600, 320, s["accent"], max(6, s["glow"] // 3))
    m, col = 64, 612
    d = ImageDraw.Draw(img)

    # ---- left column --------------------------------------------------------
    d.rounded_rectangle([m, 84, m + 26, 88], radius=2, fill=hx(s["accent"]))
    tracked(d, m + 38, 98, h["kicker"], 14, s["accent"], "cjk", 2.0)
    require_w(h["kicker"], 14, "cjk", col - 38, "hero kicker")

    title_size = fit(NAME, "mono_bold", col, 60, 48)
    text_at(d, m - 1, 172, NAME, title_size, s["text"], "mono_bold")
    require_w(NAME, title_size, "mono_bold", col, "hero title")
    d.rounded_rectangle([m, 196, m + 76, 200], radius=2, fill=hx(s["accent"]))

    value_size = fit_lines(h["value"], "cjk_bold", col, 34, 27)
    for i, line in enumerate(h["value"]):
        text_at(d, m, 268 + i * 48, line, value_size, s["text"], "cjk_bold")
        require_w(line, value_size, "cjk_bold", col, "hero value line")

    sub_size = fit_lines(h["sub"], "cjk", col, 20, 16)
    for i, line in enumerate(h["sub"]):
        text_at(d, m, 376 + i * 27, line, sub_size, s["sub"])
        require_w(line, sub_size, "cjk", col, "hero subtitle")

    text_at(d, m, 452, h["meta"], 15, s["faint"], "cjk")
    require_w(h["meta"], 15, "cjk", col, "hero meta")
    d.line([m, 476, m + col, 476], fill=hx(s["grid"]), width=1)
    text_at(d, m, 502, h["foot"], 13, s["faint"], "cjk")
    require_w(h["foot"], 13, "cjk", col, "hero footer")

    # ---- ledger sheet -------------------------------------------------------
    img = card(img, (712, 92, 1376, 296), s)
    d = ImageDraw.Draw(img)
    text_at(d, 736, 128, h["sheet_title"], 15, s["text"], "cjk_bold")
    require_w(h["sheet_title"], 15, "cjk_bold", 300, "sheet title")
    img = chip_right(img, s, 1352, 107, h["rule_chip"], s["accent"], s["pill"],
                     size=11, kind="cjk")
    d = ImageDraw.Draw(img)
    text_at(d, 736, 154, h["header_fields"], 12, s["sub"], "cjk")
    require_w(h["header_fields"], 12, "cjk", 340, "header fields")
    img = chip_right(img, s, 1352, 140, h["ok_chip"], s["ok"], s["ok_bg"],
                     size=11, dot=s["ok"])
    d = ImageDraw.Draw(img)
    d.line([736, 170, 1352, 170], fill=hx(s["grid"]), width=1)
    d.rounded_rectangle([728, 178, 1360, 202], radius=8, fill=hx(s["band"]))

    widths = [84, 84, 84, 92, 92, 64, 66]
    x = 780
    xs = []
    for w in widths:
        xs.append(x)
        x += w
    text_at(d, 736, 195, h["gutter"], 11, s["faint"], "cjk")
    for i, head in enumerate(h["headers"]):
        text_at(d, xs[i] + 5, 195, head, 11, s["sub"], "cjk_bold")
        require_w(head, 11, "cjk_bold", widths[i] - 8, "sheet column head")
    d.line([736, 206, 1352, 206], fill=hx(s["grid"]), width=1)

    # marked cell: accuracy 88.00 against expected 96.6
    d.rounded_rectangle([xs[3] + 1, 211, xs[3] + widths[3] - 3, 239],
                        radius=8, fill=hx(s["mark_bg"]))
    d.rounded_rectangle([xs[3] + 1, 211, xs[3] + widths[3] - 3, 239],
                        radius=8, outline=hx(s["mark"]), width=1)
    for i, value in enumerate(h["values"]):
        size = 14
        kind = "mono"
        color = s["mark"] if i == 3 else (s["faint"] if value == "—" else s["text"])
        text_at(d, xs[i] + 5, 232, value, size, color, kind)
        require_w(value, size, kind, widths[i] - 8, "sheet cell")

    d.line([736, 248, 1352, 248], fill=hx(s["grid"]), width=1)
    for i, tag in enumerate(h["tags"]):
        if tag == "—":
            text_at(d, xs[i] + widths[i] / 2, 268, tag, 11, s["faint"], "mono",
                    "mm")
            continue
        fg, bg = (s["mark"], s["mark_bg"]) if tag == "FP-003" else (
            s["sub"], s["band"])
        dot = s["mark"] if tag == "FP-003" else s["ok"]
        size = 10
        width = measure(tag, size, "mono") + 22
        px = xs[i] + (widths[i] - width) / 2
        d.rounded_rectangle([px, 254, px + width, 274], radius=10, fill=hx(bg))
        cy = 264
        d.ellipse([px + 6, cy - 2.4, px + 11.2, cy + 2.4], fill=hx(dot))
        d.text((px + 15, cy + size * 0.36), tag, font=font(size, "mono"),
               fill=hx(fg))
        require_w(tag, size, "mono", widths[i] - 22, "rule tag")

    # ---- finding card -------------------------------------------------------
    img = card(img, (712, 316, 1376, 508), s)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([736, 336, 740, 488], radius=2, fill=hx(s["mark"]))
    img, x_after = chip(img, s, 756, 336, h["find_chip"], s["mark"],
                        s["mark_bg"], size=11)
    img, x_after = chip(img, s, x_after + 6, 336, h["severity_chip"],
                        s["accent"], s["pill"], size=11)
    d = ImageDraw.Draw(img)
    text_at(d, x_after + 16, 352, h["locator"], 11, s["faint"], "cjk")
    require_w(h["locator"], 11, "cjk", 1088 - x_after - 20, "locator")
    text_at(d, 756, 396, h["find_line"], 14, s["text"], "cjk_bold")
    require_w(h["find_line"], 14, "cjk_bold", 330, "finding line")
    text_at(d, 756, 420, h["formula_line"], 12, s["sub"], "mono")
    require_w(h["formula_line"], 12, "mono", 330, "formula line")
    text_at(d, 756, 446, h["gap_line"], 11, s["sub"], "cjk")
    require_w(h["gap_line"], 11, "cjk", 330, "gap line")
    text_at(d, 756, 482, h["report_line"], 11, s["faint"], "mono")
    img = chip_right(img, s, 1352, 466, h["human_chip"], s["ok"], s["ok_bg"],
                     size=11, kind="cjk")
    d = ImageDraw.Draw(img)
    d.line([1088, 336, 1088, 488], fill=hx(s["grid"]), width=1)
    text_at(d, 1100, 356, h["tol_caption"], 11, s["faint"], "cjk")
    img = ruler(img, s, 1100, 1352, 424, 84, 100, 88.0, 96.6, 1.5, 444)
    d = ImageDraw.Draw(img)

    name = f"{NAME}-hero-{lang}-{skin}.webp"
    img.save(os.path.join(OUT, name), "WEBP", quality=90, method=6)
    print(f"wrote {name} ({W}x{H})")


# ------------------------------------------------------------------------ flow
FLOW = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        panel="#ffffff", card="#ffffff", edge="#e6e2ef",
        band="#f5f2fb", pill="#ece7f9", text="#141419", sub="#4d5261",
        faint="#8b90a0", accent="#4B67B4", grid="#e7e4f0",
        mark="#b45309", mark_bg="#fdf3e9", ok="#15803d", ok_bg="#eaf6ee",
        shadow="#2b2440", shadow_op="0.12", dot="#cfc8e2", dot_op="0.5",
        band_op="0.18",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        panel="#1b2231", card="#1b2231", edge="#2e374b",
        band="#202839", pill="#242d42", text="#f0f3f9", sub="#a8b1c4",
        faint="#737b8d", accent="#8496f5", grid="#262f42",
        mark="#d9a441", mark_bg="#2a2216", ok="#3fb950", ok_bg="#16281c",
        shadow="#000000", shadow_op="0.42", dot="#2b3448", dot_op="0.65",
        band_op="0.26",
    ),
}

SANS = ("'Microsoft YaHei','Segoe UI','PingFang SC','Noto Sans CJK SC',"
        "sans-serif")
MONO = "Consolas,'Microsoft YaHei',ui-monospace,monospace"

RULES = [
    # id, field(s) read, check kind, basis kind, severity cap, disposition
    ("FP-001", "subject · market", "headerPresence", "derived", "warn", "clean"),
    ("FP-002", "forecastValue", "number", "derived", "warn", "clean"),
    ("FP-003", "accuracy", "formula · percent", "institutional", "info", "diff"),
    ("FP-004", "penalty", "formula · product", "institutional", "info", "clean"),
    ("FP-005", "currency", "pattern ^[A-Z]{3}$", "derived", "warn", "clean"),
    ("FP-006", "period", "unique", "derived", "warn", "clean"),
    ("FP-007", "note", "containsAny", "derived", "warn", "clean"),
]


def _est(text: str, size: float, mono: bool = True) -> float:
    if mono:
        return len(text) * size * 0.61
    total = 0.0
    for ch in text:
        total += size * (1.0 if ord(ch) > 0x2E80 else 0.55)
    return total


def _fit_ok(text: str, size: float, avail: float, what: str,
            mono: bool = True) -> None:
    width = _est(text, size, mono)
    if width > avail:
        raise SystemExit(
            f"FATAL flow: {what} overflows ({width:.1f} > {avail:.1f}): "
            f"{text!r}")


def flow_svg(skin: str) -> str:
    s = FLOW[skin]
    out: list[str] = []
    add = out.append
    W, H = 1100, 660
    add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">')
    add('<title id="t">dsh-forecast-penalty rule scoreboard</title>')
    add('<desc id="d">Two inputs (a JSON/YAML material and the seven-rule '
        'pack) feed one scoreboard: seven rows give rule, field, check kind, '
        'basis-to-severity cap and disposition. The two arithmetic rules carry '
        'an instrument: FP-003 a tolerance ruler (declared 88.00 against '
        'expected 96.6, tolerance plus or minus 1.5 percentage points) and '
        'FP-004 an equation receipt (80 x 50 = 4000, declared 4000, difference '
        '0 within 0.01). Below the panel sit the two exits: issues[] with one '
        'located finding, and skipped[] with the three reasons a rule can land '
        'there. The verdict stays with the reviewer.</desc>')
    add('<defs>')
    add(f'<linearGradient id="bg" x1="0" y1="0" x2="0.25" y2="1">'
        f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
        f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>')
    add(f'<pattern id="dots" width="26" height="26" '
        f'patternUnits="userSpaceOnUse"><circle cx="1.1" cy="1.1" r="1.1" '
        f'fill="{s["dot"]}"/></pattern>')
    add(f'<filter id="soft" x="-20%" y="-20%" width="140%" height="160%">'
        f'<feDropShadow dx="0" dy="6" stdDeviation="8" '
        f'flood-color="{s["shadow"]}" flood-opacity="{s["shadow_op"]}"/>'
        f'</filter>')
    add('</defs>')
    add(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    add(f'<rect width="{W}" height="{H}" fill="url(#dots)" '
        f'opacity="{s["dot_op"]}"/>')

    def txt(x: float, y: float, body: str, size: float, color: str,
            kind: str = "sans", weight: int = 400, anchor: str | None = None,
            tracking: float | None = None) -> None:
        family = MONO if kind == "mono" else SANS
        extra = ""
        if weight != 400:
            extra += f' font-weight="{weight}"'
        if anchor:
            extra += f' text-anchor="{anchor}"'
        if tracking is not None:
            extra += f' letter-spacing="{tracking}"'
        add(f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" '
            f'font-family="{family}" font-size="{size}"{extra}>'
            f'{escape(body)}</text>')

    def rect(x: float, y: float, w: float, h: float, rx: float, fill: str,
             stroke: str | None = None, width: float = 1,
             extra: str = "") -> None:
        stroke_attr = (f' stroke="{stroke}" stroke-width="{width}"'
                       if stroke else "")
        add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx}" fill="{fill}"{stroke_attr}{extra}/>')

    def line(x1: float, y1: float, x2: float, y2: float, color: str,
             width: float = 1, extra: str = "") -> None:
        add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{width}"{extra}/>')

    # ---- header -------------------------------------------------------------
    txt(44, 58, "dsh-forecast-penalty", 28, s["text"], "mono", 700)
    txt(44, 84, "Seven rules on one ledger row: field → check kind → severity "
        "cap → disposition.", 13.5, s["sub"])
    _fit_ok("Seven rules on one ledger row: field → check kind → severity "
            "cap → disposition.", 13.5, 730, "flow subtitle", mono=False)
    chip_w, chip_h = 222, 26
    rect(834, 32, chip_w, chip_h, 13, s["pill"])
    txt(846, 50, "forecast_penalty · native | ptc", 11.5, s["accent"],
        "mono")
    txt(44, 108, "IN · material / file · JSON | YAML · 1 row · 12 canonical columns",
        11, s["faint"], "mono")
    txt(1056, 108, "OUT · issues[] + skipped[] · read-only", 11, s["faint"],
        "mono", anchor="end")
    line(44, 118, 1056, 118, s["grid"])

    # ---- input strips -------------------------------------------------------
    for x0, x1, title, subline in (
        (44, 544, "parseMaterial · 1 row · 12 canonical columns",
         "column aliases canonicalised · header {subject, market}"),
        (556, 1056, "rules/forecast-penalty.yaml · v2026.1",
         "7 rules · only / disabled first · kind → severity cap"),
    ):
        rect(x0, 128, x1 - x0, 60, 14, s["card"], s["edge"], 1.4,
             ' filter="url(#soft)"')
        rect(x0 + 14, 146, 3, 24, 1.5, s["accent"])
        txt(x0 + 26, 152, title, 13, s["text"], "mono", 700)
        txt(x0 + 26, 172, subline, 11.5, s["faint"], "mono")
        _fit_ok(title, 13, x1 - x0 - 40, "strip title")
        _fit_ok(subline, 11.5, x1 - x0 - 40, "strip subline")

    # ---- scoreboard panel ---------------------------------------------------
    rect(44, 200, 1012, 354, 18, s["panel"], s["edge"], 1.5,
         ' filter="url(#soft)"')
    add(f'<path d="M62 236 h976 a18 18 0 0 0 -18 -18 h-940 a18 18 0 0 0 -18 18 z" '
        f'fill="{s["band"]}"/>')
    for label, x in (("RULE", 64), ("FIELD", 150), ("CHECK KIND", 340),
                     ("BASIS → CAP", 545), ("DISPOSITION · GAUGE", 706)):
        txt(x, 223, label, 11, s["faint"], "sans", 700, tracking=0.6)
    txt(1036, 223, "1 diff · 6 clean · 0 skipped", 11, s["faint"], "mono",
        anchor="end")

    heights = [36, 36, 68, 60, 36, 36, 36]
    tops: list[int] = []
    cursor = 236
    for height in heights:
        tops.append(cursor)
        cursor += height
    bottom = cursor  # 544

    # grouped band behind the two arithmetic rows
    rect(52, tops[2] - 1, 996, heights[2] + heights[3] + 2, 12, s["band"])
    rect(52, tops[2] - 1, 3, heights[2] + heights[3] + 2, 1.5, s["accent"])

    for i, (rid, field, kind, basis, cap, state) in enumerate(RULES):
        top = tops[i]
        center = top + heights[i] / 2
        if i not in (2, 3):
            line(60, top, 1040, top, s["grid"], 1)
        lamp = s["mark"] if state == "diff" else s["ok"]
        add(f'<circle cx="68" cy="{center:.1f}" r="3.6" fill="{lamp}"/>')
        txt(80, center + 4.6, rid, 13.5, s["text"], "mono", 700)
        txt(150, center + 4.6, field, 13, s["text"], "mono")
        txt(340, center + 4.6, kind, 13, s["text"], "mono")
        txt(545, center + 4.2, f"{basis} → ≤ {cap}", 11,
            s["accent"] if basis == "institutional" else s["sub"], "mono")
        _fit_ok(f"{basis} → ≤ {cap}", 11, 150, "cap label")
        _fit_ok(kind, 13, 200, "check kind")
        _fit_ok(field, 13, 185, "field")
        if i == 2:
            txt(706, top + 22, "1 diff · info", 13, s["mark"], "sans", 700)
            # tolerance ruler: 80..100 across 810..1030
            x0, x1, axis = 810, 1030, top + 48

            def sx(v: float) -> float:
                return x0 + (v - 80) / 20 * (x1 - x0)

            b0, b1 = sx(95.1), sx(98.1)
            ex = sx(96.6)
            nx = sx(88.0)
            add(f'<rect x="{b0:.1f}" y="{axis - 20:.1f}" '
                f'width="{b1 - b0:.1f}" height="20" rx="3" '
                f'fill="{s["accent"]}" fill-opacity="{s["band_op"]}" '
                f'stroke="{s["accent"]}" stroke-opacity="0.65"/>')
            line(x0, axis, x1, axis, s["sub"], 1.2,
                 ' stroke-opacity="0.6"')
            line(x0, axis - 4, x0, axis + 4, s["faint"], 1.2)
            line(x1, axis - 4, x1, axis + 4, s["faint"], 1.2)
            line(ex, axis - 20, ex, axis + 4, s["accent"], 1.6)
            add(f'<polygon points="{nx - 4.5:.1f},{axis - 24:.1f} '
                f'{nx + 4.5:.1f},{axis - 24:.1f} {nx:.1f},{axis - 18:.1f}" '
                f'fill="{s["mark"]}"/>')
            line(nx, axis - 18, nx, axis + 4, s["mark"], 2)
            txt(ex, axis - 25, "±1.5 pp", 11, s["accent"], "mono",
                anchor="middle")
            txt(x0, axis + 14, "80", 11, s["faint"], "mono")
            txt(x1, axis + 14, "100", 11, s["faint"], "mono", anchor="end")
            txt(nx, axis + 14, "88.00", 11, s["mark"], "mono",
                anchor="middle")
            txt(ex, axis + 14, "96.6", 11, s["accent"], "mono",
                anchor="middle")
        elif i == 3:
            txt(706, top + 24, "80 × 50 = 4000", 13.5, s["text"], "mono",
                700)
            txt(1036, top + 24, "declared 4000", 11, s["faint"], "mono",
                anchor="end")
            txt(706, top + 45, "|4000 − 4000| = 0 ≤ tolerance 0.01 → clean",
                11.5, s["sub"], "mono")
            _fit_ok("|4000 − 4000| = 0 ≤ tolerance 0.01 → clean", 11.5, 330,
                    "equation line")
        else:
            txt(706, center + 4.6, "executed · 0 diff", 13, s["ok"], "sans")
    line(60, bottom, 1040, bottom, s["grid"], 1)

    # ---- exits --------------------------------------------------------------
    # issues[]: the one located finding of the run
    rect(44, 564, 604, 60, 14, s["card"], s["edge"], 1.4,
         ' filter="url(#soft)"')
    rect(58, 578, 3, 32, 1.5, s["accent"])
    txt(70, 587, "issues[] · 1", 12.5, s["accent"], "sans", 700)
    rect(588, 572, 44, 21, 10.5, s["mark_bg"])
    txt(610, 587, "info", 11, s["mark"], "mono", anchor="middle")
    txt(70, 609, "FP-003 · row 1 · field accuracy · declared 88 → expected "
        "96.6", 11.5, s["sub"], "mono")
    _fit_ok("FP-003 · row 1 · field accuracy · declared 88 → expected 96.6",
            11.5, 560, "issues line")
    # skipped[]: dashed, empty for this run, with the three ways a rule lands here
    rect(660, 564, 396, 60, 14, s["card"], s["mark"], 1.4,
         ' stroke-dasharray="7 5" filter="url(#soft)"')
    txt(676, 587, "skipped[] · 0", 12.5, s["faint"], "sans", 700)
    txt(676, 603, "all 7 executed; a missing column, a disabled", 11,
        s["faint"], "mono")
    txt(676, 616, "or an only-unselected rule is named with its reason", 11,
        s["faint"], "mono")
    _fit_ok("or an only-unselected rule is named with its reason", 11, 366,
            "skipped line")

    # ---- footer -------------------------------------------------------------
    txt(44, 644, "example: tests/fixtures/FP-003-unsafe.json · 1 issue (info)"
        " · 0 skipped", 11, s["faint"], "mono")
    txt(1056, 644, "differences only — the verdict stays with the reviewer",
        11.5, s["sub"], "sans", anchor="end")
    _fit_ok("differences only — the verdict stays with the reviewer", 11.5,
            470, "footer", mono=False)
    add("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    for skin in ("light", "dark"):
        for lang in ("zh", "en"):
            hero(lang, skin)
    for skin in ("light", "dark"):
        path = os.path.join(OUT, f"{NAME}-flow-v5-{skin}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow_svg(skin))
        print(f"wrote {NAME}-flow-v5-{skin}.svg (1100x660)")


if __name__ == "__main__":
    main()
