#!/usr/bin/env python3
"""Generate the self-hosted dark and light SVGs for the profile README."""

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent

# Shared design tokens and system font stacks. Every SVG is generated from these.
THEMES = {
    "dark": {
        "bg": "#0B0F14",
        "border": "#1F2630",
        "text": "#E6EDF3",
        "muted": "#7D8590",
        "faint": "#1A212B",
        "accent": "#FFB547",
        "teal": "#5EEAD4",
        "violet": "#A78BFA",
        "red": "#F87171",
    },
    "light": {
        "bg": "#FAFAF7",
        "border": "#E4E2DA",
        "text": "#1F2328",
        "muted": "#656D76",
        "faint": "#ECEAE3",
        "accent": "#B45309",
        "teal": "#0F766E",
        "violet": "#6D28D9",
        "red": "#B91C1C",
    },
}
SANS = '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif'
MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace'
SERIF = '"Iowan Old Style", "Charter", "Palatino Linotype", Palatino, Georgia, serif'
EASE = "cubic-bezier(.2,.8,.2,1)"
MONO_CHAR = 0.6  # Monospace advance width in em, used to size pills around their labels.


def esc(value: object) -> str:
    return escape(str(value), quote=True)


def common_css(theme: dict[str, str]) -> str:
    token_css = ":root{" + ";".join(f"--{key}:{value}" for key, value in theme.items()) + "}"
    return (
        token_css
        + f".sans{{font-family:{SANS}}}.mono{{font-family:{MONO}}}.serif{{font-family:{SERIF}}}"
        + ".tracked{letter-spacing:.08em}"
        + ".text{fill:var(--text)}.muted{fill:var(--muted)}.accent{fill:var(--accent)}"
        + ".teal{fill:var(--teal)}.violet{fill:var(--violet)}.red{fill:var(--red)}"
        + ".panel{fill:var(--bg);stroke:var(--border);stroke-width:1.2}"
    )


def svg_doc(title: str, width: int, height: int, theme: dict[str, str], defs: str, css: str, body: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">\n'
        f"  <title>{esc(title)}</title>\n"
        f"  <defs>{defs}</defs>\n"
        f"  <style>{common_css(theme)}{css}</style>\n"
        f"  {body}\n"
        "</svg>\n"
    )


def corner_ticks(width: int, height: int, inset: int = 14, arm: int = 10) -> str:
    """Four L-shaped registration marks, like the corners of an engineering drawing."""
    a, b = inset, inset + arm
    r, btm = width - inset, height - inset
    d = (
        f"M {a} {b} V {a} H {b} "
        f"M {r - arm} {a} H {r} V {b} "
        f"M {r} {btm - arm} V {btm} H {r - arm} "
        f"M {b} {btm} H {a} V {btm - arm}"
    )
    return f'<path d="{d}" fill="none" stroke="var(--muted)" stroke-width="1" opacity=".5"/>'


def banner(theme: dict[str, str]) -> str:
    css = [
        "@keyframes rise{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}",
        f".rise{{animation:rise .6s {EASE} both}}",
        "@keyframes fanFlow{"
        "0%{stroke-dashoffset:220;opacity:0}5%{opacity:0}9%{stroke-dashoffset:170;opacity:1}"
        "28%{stroke-dashoffset:0;opacity:1}35%{stroke-dashoffset:0;opacity:0}"
        "42%{stroke-dashoffset:220;opacity:0}47%{stroke-dashoffset:170;opacity:1}"
        "66%{stroke-dashoffset:0;opacity:1}73%{stroke-dashoffset:0;opacity:0}"
        "100%{stroke-dashoffset:220;opacity:0}}",
        ".edge{fill:none;stroke:var(--faint);stroke-width:1.5;stroke-linecap:round}",
        ".streak{fill:none;stroke-width:2.5;stroke-dasharray:14 600;stroke-dashoffset:220;opacity:0;"
        "stroke-linecap:round;animation:fanFlow 3.2s linear infinite}",
        ".inbound{stroke:var(--teal)}.outbound{stroke:var(--accent)}",
        ".model{fill:var(--violet);transform-box:fill-box;transform-origin:center;"
        "animation:modelPulse 3.2s ease-in-out infinite}",
        "@keyframes modelPulse{0%,24%,65%,100%{transform:scale(1);opacity:1}"
        "28%,33%,69%,74%{transform:scale(1.42);opacity:.72}}",
        ".consensus-ring{fill:none;stroke:var(--accent);stroke-width:2;opacity:0;"
        "transform-box:fill-box;transform-origin:center;animation:ring 3.2s ease-out infinite}",
        "@keyframes ring{0%,56%,100%{opacity:0;transform:scale(.65)}"
        "60%{opacity:.72;transform:scale(.8)}78%{opacity:0;transform:scale(1.8)}}",
    ]
    for idx in range(5):
        delay = idx * 0.25
        css.append(
            f".lane{idx}{{animation-delay:-{delay:.2f}s}}"
            f".model{idx}{{animation-delay:-{delay:.2f}s}}"
        )
    css.append(
        "@media(prefers-reduced-motion:reduce){"
        ".rise{animation:none!important;opacity:1;transform:none}"
        ".streak{display:none}.model,.consensus-ring{animation:none}.consensus-ring{display:none}"
        "}"
    )

    diagram = []
    # Edges sit behind their animated streaks and model dots.
    ys = [72, 116, 160, 204, 248]
    inbound_paths = []
    outbound_paths = []
    for y in ys:
        p_in = f"M 810 160 C 850 160 870 {y} 917 {y}"
        p_out = f"M 931 {y} C 987 {y} 1020 160 1072 160"
        inbound_paths.append(p_in)
        outbound_paths.append(p_out)
        diagram.append(f'<path class="edge" d="{p_in}"/>')
        diagram.append(f'<path class="edge" d="{p_out}"/>')
    for idx, path in enumerate(inbound_paths):
        diagram.append(f'<path class="streak inbound lane{idx}" d="{path}"/>')
    for idx, path in enumerate(outbound_paths):
        diagram.append(f'<path class="streak outbound lane{idx}" d="{path}"/>')
    diagram.append(
        '<rect x="726" y="142" width="84" height="36" rx="9" '
        'fill="var(--bg)" stroke="var(--border)" stroke-width="1.3"/>'
        '<text class="mono muted" x="768" y="164" text-anchor="middle" font-size="13">prompt</text>'
    )
    for idx, y in enumerate(ys):
        diagram.append(f'<circle class="model model{idx}" cx="924" cy="{y}" r="7"/>')
    diagram.extend(
        [
            '<circle class="consensus-ring" cx="1094" cy="160" r="22"/>',
            '<circle cx="1094" cy="160" r="22" fill="var(--bg)" stroke="var(--accent)" stroke-width="2"/>',
            '<circle cx="1094" cy="160" r="5" fill="var(--accent)" opacity=".82"/>',
            '<text class="mono muted" x="1094" y="204" text-anchor="middle" font-size="12">consensus</text>',
            # Caption centred on the diagram's extent (726 to 1116).
            '<text class="mono muted" x="921" y="292" text-anchor="middle" font-size="11">'
            "fig. 0 — one prompt, five models, one answer</text>",
        ]
    )
    gap = "&#160;" * 3
    left = [
        '<text class="mono muted tracked rise" x="56" y="60" font-size="12">'
        "BENGALURU · ML ENGINEER II, REVIONICS</text>",
        '<text class="serif text rise" x="54" y="138" font-size="62" font-weight="600" '
        'style="animation-delay:.08s">Nehul Bhatnagar</text>',
        '<text class="sans muted rise" font-size="21" style="animation-delay:.16s">'
        '<tspan x="56" y="184">Retrieval, multi-agent workflows,</tspan>'
        '<tspan x="56" y="212">and the pipelines underneath them.</tspan></text>',
        f'<text class="mono muted rise" x="56" y="262" font-size="13" style="animation-delay:.24s">'
        f"prev. Coinbase · Goldman Sachs{gap}·{gap}ICWSM 2026</text>",
    ]
    body = (
        '<rect class="panel" x="0.6" y="0.6" width="1198.8" height="318.8" rx="16"/>'
        + corner_ticks(1200, 320)
        + "".join(left)
        + "".join(diagram)
    )
    return svg_doc(
        "Nehul Bhatnagar — ML Engineer II at Revionics, Bengaluru", 1200, 320, theme, "", "".join(css), body
    )


TAG_COLOURS = {"early access": "accent", "open source": "teal", "private": "muted"}


def status_tag(label: str) -> str:
    colour = TAG_COLOURS[label]
    lock = label == "private"
    text_w = len(label) * 11 * MONO_CHAR
    width = text_w + 24 + (18 if lock else 0)
    x = 568 - width
    parts = [
        f'<rect x="{x:.1f}" y="20" width="{width:.1f}" height="24" rx="12" fill="none" '
        f'stroke="var(--{colour})" stroke-width="1"/>'
    ]
    text_x = 568 - 12 - text_w / 2
    if lock:
        lx, ly = x + 12, 30
        parts.append(
            f'<path d="M {lx + 1} {ly} V {ly - 2} A 4 4 0 0 1 {lx + 9} {ly - 2} V {ly} '
            f'M {lx} {ly} H {lx + 10} V {ly + 8} H {lx} Z" fill="none" stroke="var(--{colour})" '
            'stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    parts.append(
        f'<text class="mono {colour}" x="{text_x:.1f}" y="36" text-anchor="middle" font-size="11">{esc(label)}</text>'
    )
    return "".join(parts)


CARD_CSS = (
    "@keyframes cardIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}"
    f".entrance{{animation:cardIn .65s {EASE} both}}"
    "@media(prefers-reduced-motion:reduce){.entrance{animation:none!important;opacity:1;transform:none}}"
)


def card(
    theme: dict[str, str],
    *,
    index: str,
    title: str,
    tag: str,
    lines: tuple[str, str],
    illustration: str,
    stack: str,
    destination: str,
    destination_class: str,
    css: str = "",
    defs: str = "",
) -> str:
    """Shared figure-sheet frame: index, serif title, tag, two lines, figure zone, hairline, footer."""
    body = (
        '<g class="entrance">'
        '<rect class="panel" x="0.6" y="0.6" width="598.8" height="298.8" rx="16"/>'
        f'<text class="mono muted" x="32" y="36" font-size="12">{esc(index)}</text>'
        f'<text class="serif text" x="32" y="68" font-size="30" font-weight="600">{esc(title)}</text>'
        + status_tag(tag)
        + f'<text class="sans muted" x="32" y="100" font-size="16">{lines[0]}</text>'
        f'<text class="sans muted" x="32" y="124" font-size="16">{lines[1]}</text>'
        + illustration
        + '<path d="M 32 258 H 568" stroke="var(--faint)" stroke-width="1"/>'
        f'<text class="mono muted" x="32" y="283" font-size="12">{esc(stack)}</text>'
        f'<text class="mono {destination_class}" x="568" y="283" text-anchor="end" font-size="12">{esc(destination)}</text>'
        "</g>"
    )
    return svg_doc(f"{title} project card", 600, 300, theme, defs, CARD_CSS + css, body)


def dashboard_card(theme: dict[str, str]) -> str:
    digits = "12847391"
    digit_x = [32, 54, 83.7, 105.7, 127.7, 157.4, 179.4, 201.4]
    odo_defs = []
    odo_body = []
    odo_css = [
        ".odo-strip{font-size:30px;font-weight:500;text-anchor:middle}",
        ".comma{transform-box:fill-box;transform-origin:center;transform:scaleX(.42)}",
        ".chart-bar{fill:var(--accent);transform-box:fill-box;transform-origin:50% 100%;"
        f"transform:scaleY(0);animation:grow .52s {EASE} both}}",
        "@keyframes grow{to{transform:scaleY(1)}}",
        "@media(prefers-reduced-motion:reduce){.chart-bar{animation:none!important;transform:none!important}}",
    ]
    for idx, digit_char in enumerate(digits):
        digit = int(digit_char)
        final_row = 10 + idx * 2 + digit
        sequence = [str(row % 10) for row in range(final_row)] + [digit_char]
        x = digit_x[idx]
        odo_defs.append(
            f'<clipPath id="digitWindow{idx}"><rect x="{x}" y="174" width="22" height="32" rx="2"/></clipPath>'
        )
        anim_seconds = 0.50 + idx * 0.04
        delay = idx * 0.03
        odo_css.append(
            f".roll{idx}{{transform:translateY(0);animation:roll{idx} {anim_seconds:.3f}s "
            f"{EASE} {delay:.3f}s both}}"
            f"@keyframes roll{idx}{{to{{transform:translateY(-{final_row * 40}px)}}}}"
            f"@media(prefers-reduced-motion:reduce){{.roll{idx}{{animation:none!important;"
            f"transform:translateY(-{final_row * 40}px)!important}}}}"
        )
        texts = "".join(
            f'<text class="mono text odo-strip" x="{x + 11}" y="{200 + row * 40}">{value}</text>'
            for row, value in enumerate(sequence)
        )
        # Keep the clipping window fixed while only the digit strip moves inside it.
        odo_body.append(
            f'<g clip-path="url(#digitWindow{idx})"><g class="roll{idx}">{texts}</g></g>'
        )
    odo_body.extend(
        [
            '<text class="mono text comma" x="79.85" y="200" font-size="25" text-anchor="middle">,</text>',
            '<text class="mono text comma" x="153.55" y="200" font-size="25" text-anchor="middle">,</text>',
        ]
    )
    bars = [18, 27, 22, 34, 29, 41, 35, 47, 40, 49, 44, 55, 48, 59]
    bar_body = []
    for idx, height in enumerate(bars):
        x = 352 + idx * 15
        y = 226 - height
        delay = idx * 0.06
        bar_body.append(
            f'<rect class="chart-bar" x="{x}" y="{y}" width="9" height="{height}" rx="2" '
            f'style="animation-delay:{delay:.2f}s"/>'
        )
    illustration = (
        '<text class="mono muted tracked" x="32" y="158" font-size="11">TOKENS</text>'
        + "".join(odo_body)
        + '<text class="mono muted" x="32" y="236" font-size="11">this month</text>'
        + '<path d="M 348 226 H 559" stroke="var(--faint)" stroke-width="1"/>'
        + "".join(bar_body)
        + '<text class="mono muted" x="350" y="246" font-size="11">cache hit 91%</text>'
    )
    return card(
        theme,
        index="04",
        title="ai-usage-dashboard",
        tag="open source",
        lines=("Where my AI coding tokens and dollars go.", "Reads Claude Code, Codex &amp; Antigravity logs locally."),
        illustration=illustration,
        stack="Python · Chart.js · local-only",
        destination="repo ↗",
        destination_class="accent",
        css="".join(odo_css),
        defs="".join(odo_defs),
    )


def quorum_card(theme: dict[str, str]) -> str:
    rows_y = [154, 176, 198, 220, 242]
    starts = [22, 188, 54, 206, 78]
    ends = [160, 166, 154, 164, 158]
    # Gauge geometry: circumference and the dash offset that leaves 0.87 of it drawn.
    gauge_r = 38
    circumference = 2 * 3.14159265 * gauge_r
    gauge_end = circumference * 0.13
    row_parts = []
    css = [
        f".bar-fill{{fill:var(--violet);animation:converge 1.6s {EASE} both}}",
        "@keyframes converge{from{width:var(--from)}to{width:var(--to)}}",
        ".contradiction{opacity:0;animation:showContradiction .3s ease-out 1.72s both}",
        "@keyframes showContradiction{from{opacity:0}to{opacity:1}}",
        ".gauge-fill{fill:none;stroke:var(--accent);stroke-width:8;stroke-linecap:round;"
        f"stroke-dasharray:{circumference:.2f};stroke-dashoffset:{circumference:.2f};"
        f"animation:gauge .7s {EASE} .45s both}}",
        f"@keyframes gauge{{to{{stroke-dashoffset:{gauge_end:.2f}}}}}",
        "@media(prefers-reduced-motion:reduce){.bar-fill,.contradiction,.gauge-fill{animation:none!important;opacity:1}"
        f".bar-fill{{width:var(--to)!important}}.gauge-fill{{stroke-dashoffset:{gauge_end:.2f}!important}}}}",
    ]
    for idx, (y, start, end) in enumerate(zip(rows_y, starts, ends)):
        row_parts.append(
            f'<text class="mono muted" x="32" y="{y + 4}" font-size="12">m{idx + 1}</text>'
            f'<rect x="64" y="{y - 5}" width="204" height="8" rx="4" fill="var(--faint)"/>'
            f'<rect class="bar-fill bar{idx}" x="64" y="{y - 5}" width="{start}" height="8" rx="4" '
            f'style="--from:{start}px;--to:{end}px;animation-delay:{idx * 0.07:.2f}s"/>'
        )
    illustration = (
        "".join(row_parts)
        + '<g class="contradiction"><circle cx="279" cy="219" r="3" fill="var(--red)"/>'
        '<text class="mono red" x="287" y="223" font-size="11">contradiction</text></g>'
        + f'<circle cx="493" cy="188" r="{gauge_r}" fill="none" stroke="var(--faint)" stroke-width="8"/>'
        + f'<circle class="gauge-fill" cx="493" cy="188" r="{gauge_r}" transform="rotate(-90 493 188)"/>'
        + '<text class="mono text" x="493" y="196" text-anchor="middle" font-size="24">0.87</text>'
        + '<text class="mono muted" x="493" y="246" text-anchor="middle" font-size="11">unity score</text>'
    )
    return card(
        theme,
        index="03",
        title="Quorum",
        tag="private",
        lines=("One prompt, five models, one answer.", "A private tool, built just for me and my friends."),
        illustration=illustration,
        stack="Python · FastAPI · LangGraph",
        destination="friends only",
        destination_class="muted",
        css="".join(css),
    )


def focusnotes_card(theme: dict[str, str]) -> str:
    select_x, select_y, select_w, select_h = 25, 163, 200, 44
    # The dash length must cover the full perimeter so the outline draws on without a gap.
    select_length = 2 * (select_w + select_h)
    screen_bars = [(150, 168), (170, 186), (190, 140), (210, 176), (230, 112)]
    bar_parts = "".join(
        f'<rect x="32" y="{y}" width="{width}" height="10" rx="5" fill="var(--faint)"/>'
        for y, width in screen_bars
    )
    css = [
        f".select-box{{fill:none;stroke:var(--accent);stroke-width:1.4;stroke-dasharray:{select_length};"
        f"animation:drawSelect .7s {EASE} .4s both}}",
        f"@keyframes drawSelect{{from{{stroke-dashoffset:{select_length}}}to{{stroke-dashoffset:0}}}}",
        ".note-line{animation:noteIn .4s ease-out both}",
        "@keyframes noteIn{from{opacity:0}to{opacity:1}}",
        "@media(prefers-reduced-motion:reduce){.select-box,.note-line{animation:none!important;opacity:1;stroke-dashoffset:0}}",
    ]
    illustration = (
        bar_parts
        + f'<rect class="select-box" x="{select_x}" y="{select_y}" width="{select_w}" height="{select_h}" rx="6"/>'
        '<path d="M 258 189 L 266 195 L 258 201" fill="none" stroke="var(--muted)" stroke-width="1.5" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect class="panel" x="300.5" y="142.5" width="267" height="104" rx="10"/>'
        '<text class="mono muted note-line" x="316" y="164" font-size="12" style="animation-delay:.5s">inbox.md</text>'
        '<text class="mono text note-line" x="316" y="189" font-size="12" style="animation-delay:.9s">- selected quote</text>'
        '<text class="mono text note-line" x="316" y="210" font-size="12" style="animation-delay:1.3s">- OCR → text</text>'
        '<text class="mono teal note-line" x="316" y="231" font-size="12" style="animation-delay:1.7s">#reading</text>'
    )
    return card(
        theme,
        index="02",
        title="focusnotes",
        tag="open source",
        lines=("Take notes without breaking focus.", "Selected text, screen areas &amp; quick notes → Markdown."),
        illustration=illustration,
        stack="Swift · C#/WPF · on-device OCR",
        destination="focusnotes.pages.dev ↗",
        destination_class="accent",
        css="".join(css),
    )


def groupbasket_card(theme: dict[str, str]) -> str:
    # Three flatmates' WhatsApp replies merge into one cart, like lines into a transit interchange.
    messages = [
        ("R", "atta and coke zero", "teal", 160),
        ("A", "ek doodh bhi mangwa lena", "violet", 195),
        ("N", "eggs too, shared", "accent", 230),
    ]
    cart_x, cart_y, cart_w, cart_h = 296, 181, 134, 28
    cart_cy = cart_y + cart_h / 2
    css = [
        "@keyframes pop{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}",
        f".pop{{animation:pop .45s {EASE} both}}",
        ".route{fill:none;stroke-width:2;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;"
        f"animation:drawRoute .6s {EASE} both}}",
        "@keyframes drawRoute{to{stroke-dashoffset:0}}",
        ".r-teal{stroke:var(--teal)}.r-violet{stroke:var(--violet)}.r-accent{stroke:var(--accent)}",
        ".bubble{fill:none;stroke:var(--border);stroke-width:1}",
        "@media(prefers-reduced-motion:reduce){.pop,.route{animation:none!important;opacity:1;transform:none;stroke-dashoffset:0}}",
    ]
    parts = []
    routes = []
    for idx, (initial, text, colour, cy) in enumerate(messages):
        delay = 0.35 + idx * 0.3
        bubble_w = round(len(text) * 6.4 + 22)
        bx = 62
        end_x = bx + bubble_w
        parts.append(
            f'<g class="pop" style="animation-delay:{delay:.2f}s">'
            f'<circle cx="44" cy="{cy}" r="10" fill="none" stroke="var(--{colour})" stroke-width="1.2"/>'
            f'<text class="mono {colour}" x="44" y="{cy + 4}" text-anchor="middle" font-size="11" font-weight="600">{initial}</text>'
            f'<rect class="bubble" x="{bx}.5" y="{cy - 12}.5" width="{bubble_w}" height="24" rx="9"/>'
            f'<text class="sans text" x="{bx + 11}" y="{cy + 4}" font-size="12">{esc(text)}</text>'
            "</g>"
        )
        route_delay = 1.3 + idx * 0.12
        routes.append(
            f'<path class="route r-{colour}" pathLength="1" style="animation-delay:{route_delay:.2f}s" '
            f'd="M {end_x + 6} {cy} C {end_x + 40} {cy} {cart_x - 40} {cart_cy} {cart_x} {cart_cy}"/>'
            f'<circle class="pop" cx="{end_x + 6}" cy="{cy}" r="2.5" fill="var(--{colour})" '
            f'style="animation-delay:{route_delay:.2f}s"/>'
        )
    right_x = 450
    right = (
        # Branches out of the cart: the losing quote in a hairline, the winner in teal.
        f'<path class="route" pathLength="1" style="stroke:var(--border);stroke-width:1.5;animation-delay:2s" '
        f'd="M {cart_x + cart_w} {cart_cy} C {cart_x + cart_w + 12} {cart_cy} {right_x - 16} 167 {right_x - 6} 167"/>'
        f'<path class="route r-teal" pathLength="1" style="animation-delay:2s" '
        f'd="M {cart_x + cart_w} {cart_cy} H {right_x - 6}"/>'
        f'<text class="mono muted pop" x="{right_x}" y="171" font-size="12" style="animation-delay:2.2s">Instamart ₹471</text>'
        f'<text class="mono text pop" x="{right_x}" y="199" font-size="12" style="animation-delay:2.35s">'
        'Zepto ₹438 <tspan class="teal">✓</tspan></text>'
        f'<text class="mono muted pop" x="{right_x}" y="231" font-size="11" style="animation-delay:2.5s">split → Splitwise</text>'
    )
    cart = (
        f'<g class="pop" style="animation-delay:1.2s">'
        f'<rect x="{cart_x}.5" y="{cart_y}.5" width="{cart_w}" height="{cart_h}" rx="14" fill="var(--bg)" '
        'stroke="var(--muted)" stroke-width="1.2"/>'
        f'<text class="mono text" x="{cart_x + cart_w / 2:.1f}" y="{cart_cy + 4:.1f}" text-anchor="middle" font-size="12">'
        "1 cart · 4 items</text></g>"
    )
    illustration = "".join(routes) + "".join(parts) + cart + right
    return card(
        theme,
        index="01",
        title="GroupBasket",
        tag="early access",
        lines=(
            "One grocery order for the whole flat.",
            "Asks everyone on WhatsApp, compares carts, splits on Splitwise.",
        ),
        illustration=illustration,
        stack="TypeScript · Cloudflare Workers",
        destination="groupbasket.in ↗",
        destination_class="accent",
        css="".join(css),
    )


def impact_strip(theme: dict[str, str]) -> str:
    tiles = [
        ("ENTERPRISE RAG", "70%+", "faster ticket resolution"),
        ("INFERENCE API ON K8S", "$100k+", "compute saved per year"),
        ("FORECASTING", "$2M+", "new European revenue"),
        ("GOLDMAN SACHS", "14h → &lt;2h", "Kafka pipeline runtime"),
    ]
    css = [
        "@keyframes tileIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}",
        f".tile{{animation:tileIn .62s {EASE} both}}",
        "@media(prefers-reduced-motion:reduce){.tile{animation:none!important;opacity:1;transform:none}}",
    ]
    pieces = [
        '<rect class="panel" x="0.6" y="0.6" width="1198.8" height="148.8" rx="16"/>',
        corner_ticks(1200, 150),
    ]
    for idx in range(1, 4):
        pieces.append(f'<path d="M {idx * 300} 24 V 126" stroke="var(--faint)" stroke-width="1"/>')
    for idx, (context, number, label) in enumerate(tiles):
        center = idx * 300 + 150
        delay = idx * 0.15
        pieces.append(
            f'<g class="tile" style="animation-delay:{delay:.2f}s">'
            f'<text class="mono muted tracked" x="{center}" y="42" text-anchor="middle" font-size="11">{esc(context)}</text>'
            f'<text class="serif accent" x="{center}" y="88" text-anchor="middle" font-size="40" font-weight="600">{number}</text>'
            f'<text class="sans text" x="{center}" y="118" text-anchor="middle" font-size="15">{esc(label)}</text>'
            "</g>"
        )
    return svg_doc("Career impact results", 1200, 150, theme, "", "".join(css), "".join(pieces))


def write(name: str, value: str) -> None:
    (OUT / name).write_text(value, encoding="utf-8", newline="\n")


def main() -> None:
    builders = {
        "banner": banner,
        "card-groupbasket": groupbasket_card,
        "card-focusnotes": focusnotes_card,
        "card-quorum": quorum_card,
        "card-dashboard": dashboard_card,
        "impact": impact_strip,
    }
    for theme_name, theme in THEMES.items():
        for asset, builder in builders.items():
            write(f"{asset}-{theme_name}.svg", builder(theme))


if __name__ == "__main__":
    main()
