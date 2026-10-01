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


def esc(value: object) -> str:
    return escape(str(value), quote=True)


def common_css(theme: dict[str, str]) -> str:
    token_css = ":root{" + ";".join(f"--{key}:{value}" for key, value in theme.items()) + "}"
    return (
        token_css
        + f".sans{{font-family:{SANS}}}.mono{{font-family:{MONO}}}"
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


def banner(theme: dict[str, str]) -> str:
    phrases = [
        "retrieval that holds up in prod",
        "multi-agent workflows",
        "the pipelines underneath them",
    ]
    char_width = 19 * 0.6
    prefix_x = 56 + 11 * char_width
    total_seconds = 10.5
    slots = [(0.0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1.0)]
    typing_css = [
        "@keyframes cursorBlink{0%,49%{opacity:1}50%,100%{opacity:0}}",
        ".cursor{fill:var(--accent);visibility:hidden}",
    ]
    typing_body = [
        f'<text class="mono accent" x="56" y="239" font-size="19">&gt; building </text>'
    ]
    for idx, phrase in enumerate(phrases):
        chars = len(phrase)
        width = chars * char_width
        slot_start, slot_end = slots[idx]
        slot_span = slot_end - slot_start
        type_end = slot_start + slot_span * 0.45
        hold_end = slot_start + slot_span * 0.94
        # The final 6% of each slot clears the phrase and returns the cursor.
        pct = lambda val: f"{val * 100:.3f}%"
        typing_css.append(
            f"@keyframes type{idx}{{"
            f"{pct(slot_start)}{{width:0}}{pct(type_end)}{{width:{width:.2f}px}}"
            f"{pct(hold_end)}{{width:{width:.2f}px}}{pct(slot_end)}{{width:0}}"
            f"100%{{width:0}}}}"
        )
        typing_css.append(
            f"@keyframes cursorMove{idx}{{"
            f"{pct(slot_start)}{{transform:translateX(0)}}"
            f"{pct(type_end)}{{transform:translateX({width:.2f}px)}}"
            f"{pct(hold_end)}{{transform:translateX({width:.2f}px)}}"
            f"{pct(slot_end)}{{transform:translateX(0)}}100%{{transform:translateX(0)}}}}"
        )
        typing_css.append(
            f"@keyframes cursorPhase{idx}{{0%{{visibility:hidden}}"
            f"{pct(slot_start)}{{visibility:visible}}{pct(slot_end)}{{visibility:hidden}}"
            "100%{visibility:hidden}}"
        )
        typing_body.append(
            f'<clipPath id="phraseClip{idx}"><rect class="phraseMask phraseMask{idx}" '
            f'x="{prefix_x:.2f}" y="214" width="0" height="31"/></clipPath>'
        )
        typing_body.append(
            f'<text class="mono text phrase phrase{idx}" x="{prefix_x:.2f}" y="239" '
            f'font-size="19" clip-path="url(#phraseClip{idx})">{esc(phrase)}</text>'
        )
        cursor_x = prefix_x
        cursor_y = 220
        typing_body.append(
            f'<rect class="cursor cursor{idx}" x="{cursor_x:.2f}" y="{cursor_y}" '
            f'width="10" height="21"/>'
        )
        typing_css.append(
            f".phraseMask{idx}{{animation:type{idx} {total_seconds:g}s steps({chars},end) infinite}}"
            f".cursor{idx}{{animation:cursorBlink 1s steps(2,end) infinite,"
            f"cursorMove{idx} {total_seconds:g}s steps({chars},end) infinite,"
            f"cursorPhase{idx} {total_seconds:g}s steps(1,end) infinite}}"
        )
    typing_css.append(
        "@keyframes fanFlow{"
        "0%{stroke-dashoffset:220;opacity:0}5%{opacity:0}9%{stroke-dashoffset:170;opacity:1}"
        "28%{stroke-dashoffset:0;opacity:1}35%{stroke-dashoffset:0;opacity:0}"
        "42%{stroke-dashoffset:220;opacity:0}47%{stroke-dashoffset:170;opacity:1}"
        "66%{stroke-dashoffset:0;opacity:1}73%{stroke-dashoffset:0;opacity:0}"
        "100%{stroke-dashoffset:220;opacity:0}}"
        ".edge{fill:none;stroke:var(--faint);stroke-width:1.5;stroke-linecap:round}"
        ".streak{fill:none;stroke-width:2.5;stroke-dasharray:14 600;stroke-dashoffset:220;opacity:0;"
        "stroke-linecap:round;animation:fanFlow 3.2s linear infinite}"
        ".inbound{stroke:var(--teal)}.outbound{stroke:var(--accent)}"
        ".model{fill:var(--violet);transform-box:fill-box;transform-origin:center;"
        "animation:modelPulse 3.2s ease-in-out infinite}"
        "@keyframes modelPulse{0%,24%,65%,100%{transform:scale(1);opacity:1}"
        "28%,33%,69%,74%{transform:scale(1.42);opacity:.72}}"
        ".consensus-ring{fill:none;stroke:var(--accent);stroke-width:2;opacity:0;"
        "transform-box:fill-box;transform-origin:center;animation:ring 3.2s ease-out infinite}"
        "@keyframes ring{0%,56%,100%{opacity:0;transform:scale(.65)}"
        "60%{opacity:.72;transform:scale(.8)}78%{opacity:0;transform:scale(1.8)}}"
    )
    for idx in range(5):
        delay = idx * 0.25
        typing_css.append(
            f".lane{idx}{{animation-delay:-{delay:.2f}s}}"
            f".model{idx}{{animation-delay:-{delay:.2f}s}}"
        )
    typing_css.append(
        "@media(prefers-reduced-motion:reduce){"
        ".streak{display:none}.model,.consensus-ring{animation:none}.consensus-ring{display:none}"
        ".phraseMask{animation:none!important;width:0!important}"
        f".phraseMask0{{width:{len(phrases[0]) * char_width:.2f}px!important}}"
        ".phrase1,.phrase2,.cursor1,.cursor2{display:none}"
        f".cursor0{{animation:none;opacity:1;visibility:visible;transform:translateX({len(phrases[0]) * char_width:.2f}px)}}"
        "}"
    )

    diagram = []
    # Edges sit behind their animated streaks and model dots.
    ys = [72, 116, 160, 204, 248]
    inbound_paths = []
    outbound_paths = []
    for idx, y in enumerate(ys):
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
        ]
    )
    body = (
        '<rect class="panel" x="0.6" y="0.6" width="1198.8" height="318.8" rx="16"/>'
        '<rect x="1" y="1" width="1198" height="318" rx="16" fill="url(#dots)" mask="url(#fadeMask)"/>'
        '<text class="mono muted" x="56" y="58" font-size="15">~/zerodoxxx</text>'
        '<text class="sans text" x="56" y="126" font-size="56" font-weight="700">Nehul Bhatnagar</text>'
        '<text class="sans muted" x="56" y="169" font-size="22">'
        'ML Engineer II at Revionics · ex-Coinbase, Goldman Sachs</text>'
        + "".join(typing_body)
        + "".join(diagram)
    )
    defs = (
        '<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
        '<circle cx="2" cy="2" r="1.2" fill="var(--faint)"/></pattern>'
        '<linearGradient id="fade" x1="0" x2="1">'
        '<stop offset="0%" stop-color="white" stop-opacity="0"/>'
        '<stop offset="46%" stop-color="white" stop-opacity="0"/>'
        '<stop offset="70%" stop-color="white" stop-opacity="1"/>'
        '<stop offset="100%" stop-color="white" stop-opacity="1"/></linearGradient>'
        '<mask id="fadeMask"><rect x="0" y="0" width="1200" height="320" fill="url(#fade)"/></mask>'
    )
    css = "".join(typing_css)
    return svg_doc("Nehul Bhatnagar — ML Engineer", 1200, 320, theme, defs, css, body)


def dashboard_card(theme: dict[str, str]) -> str:
    digits = "12847391"
    digit_x = [32, 54, 83.7, 105.7, 127.7, 157.4, 179.4, 201.4]
    odo_defs = []
    odo_body = []
    odo_css = [
        "@keyframes cardIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}",
        ".entrance{animation:cardIn .65s cubic-bezier(.2,.8,.2,1) both}",
        ".odo-strip{font-size:30px;font-weight:500;text-anchor:middle}",
        ".comma{transform-box:fill-box;transform-origin:center;transform:scaleX(.42)}",
        ".chart-bar{fill:var(--accent);transform-box:fill-box;transform-origin:50% 100%;"
        "transform:scaleY(0);animation:grow .52s cubic-bezier(.2,.8,.2,1) both}",
        "@keyframes grow{to{transform:scaleY(1)}}",
        "@media(prefers-reduced-motion:reduce){.entrance,.odo-strip,.chart-bar{animation:none!important;opacity:1;transform:none!important}}",
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
            f"cubic-bezier(.2,.8,.2,1) {delay:.3f}s both}}"
            f"@keyframes roll{idx}{{to{{transform:translateY(-{final_row * 40}px)}}}}"
            f"@media(prefers-reduced-motion:reduce){{.roll{idx}{{transform:translateY(-{final_row * 40}px)!important}}}}"
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
    body = (
        '<g class="entrance">'
        '<rect class="panel" x="0.6" y="0.6" width="598.8" height="298.8" rx="16"/>'
        '<text class="sans text" x="32" y="52" font-size="28" font-weight="700">ai-usage-dashboard</text>'
        '<rect x="480" y="28" width="88" height="25" rx="12.5" fill="none" stroke="var(--teal)" stroke-width="1.2"/>'
        '<text class="mono teal" x="524" y="45" text-anchor="middle" font-size="12">public</text>'
        '<text class="sans muted" x="32" y="88" font-size="17">Where my AI coding tokens and dollars go.</text>'
        '<text class="sans muted" x="32" y="112" font-size="17">Reads Claude Code, Codex &amp; Antigravity logs locally.</text>'
        '<text class="mono muted" x="32" y="155" font-size="12">TOKENS</text>'
        + "".join(odo_body)
        + '<path d="M 348 226 H 559" stroke="var(--faint)" stroke-width="1"/>'
        + "".join(bar_body)
        + '<text class="mono muted" x="350" y="250" font-size="12">cache hit 91%</text>'
        + '<text class="mono muted" x="32" y="280" font-size="13">Python · Chart.js · local-only</text>'
        + "</g>"
    )
    defs = "".join(odo_defs)
    return svg_doc("ai-usage-dashboard project card", 600, 300, theme, defs, "".join(odo_css), body)


def quorum_card(theme: dict[str, str]) -> str:
    rows_y = [157, 179, 201, 223, 245]
    starts = [22, 188, 54, 206, 78]
    ends = [160, 166, 154, 164, 158]
    row_parts = []
    css = [
        "@keyframes cardIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}",
        ".entrance{animation:cardIn .65s cubic-bezier(.2,.8,.2,1) both}",
        ".bar-fill{fill:var(--violet);animation:converge 1.6s cubic-bezier(.2,.8,.2,1) both}",
        "@keyframes converge{from{width:var(--from)}to{width:var(--to)}}",
        ".contradiction{opacity:0;animation:showContradiction .3s ease-out 1.72s both}",
        "@keyframes showContradiction{from{opacity:0}to{opacity:1}}",
        ".gauge-fill{fill:none;stroke:var(--accent);stroke-width:8;stroke-linecap:round;"
        "stroke-dasharray:263.89;stroke-dashoffset:263.89;animation:gauge .9s cubic-bezier(.2,.8,.2,1) .45s both}",
        "@keyframes gauge{to{stroke-dashoffset:34.31}}",
        "@media(prefers-reduced-motion:reduce){.entrance,.bar-fill,.contradiction,.gauge-fill{animation:none!important;opacity:1}"
        ".bar-fill{width:var(--to)!important}.gauge-fill{stroke-dashoffset:34.31!important}}",
    ]
    for idx, (y, start, end) in enumerate(zip(rows_y, starts, ends)):
        row_parts.append(
            f'<text class="mono muted" x="32" y="{y + 4}" font-size="12">m{idx + 1}</text>'
            f'<rect x="64" y="{y - 5}" width="204" height="8" rx="4" fill="var(--faint)"/>'
            f'<rect class="bar-fill bar{idx}" x="64" y="{y - 5}" width="{start}" height="8" rx="4" '
            f'style="--from:{start}px;--to:{end}px;animation-delay:{idx * 0.07:.2f}s"/>'
        )
    body = (
        '<g class="entrance">'
        '<rect class="panel" x="0.6" y="0.6" width="598.8" height="298.8" rx="16"/>'
        '<text class="sans text" x="32" y="52" font-size="28" font-weight="700">Quorum</text>'
        '<rect x="474" y="28" width="94" height="25" rx="12.5" fill="none" stroke="var(--accent)" stroke-width="1.2"/>'
        '<path d="M 488 39 V 37 A 4 4 0 0 1 496 37 V 39 M 487 39 H 497 V 47 H 487 Z" '
        'fill="none" stroke="var(--accent)" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/>'
        '<text class="mono accent" x="531" y="45" text-anchor="middle" font-size="12">private</text>'
        '<text class="sans muted" x="32" y="88" font-size="17">One prompt, five models, one answer.</text>'
        '<text class="sans muted" x="32" y="112" font-size="17">A private tool, built just for me and my friends.</text>'
        + "".join(row_parts)
        + '<g class="contradiction"><circle cx="279" cy="222" r="3" fill="var(--red)"/>'
        '<text class="mono red" x="287" y="226" font-size="11">contradiction</text></g>'
        + '<circle cx="493" cy="205" r="42" fill="none" stroke="var(--faint)" stroke-width="8"/>'
        + '<circle class="gauge-fill" cx="493" cy="205" r="42" transform="rotate(-90 493 205)"/>'
        + '<text class="mono text" x="493" y="213" text-anchor="middle" font-size="26">0.87</text>'
        + '<text class="mono muted" x="493" y="264" text-anchor="middle" font-size="12">unity score</text>'
        + '<text class="mono muted" x="32" y="280" font-size="13">Python · FastAPI · LangGraph</text>'
        + "</g>"
    )
    return svg_doc("Quorum project card", 600, 300, theme, "", "".join(css), body)


def impact_strip(theme: dict[str, str]) -> str:
    tiles = [
        ("70%+", "faster ticket resolution", "enterprise RAG", 94),
        ("$100k+", "compute saved per year", "inference API on k8s", 132),
        ("$2M+", "new European revenue", "forecasting libraries", 94),
        ("14h → &lt;2h", "Kafka pipeline runtime", "Goldman Sachs", 190),
    ]
    css = [
        "@keyframes tileIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}",
        ".tile{opacity:0;animation:tileIn .62s cubic-bezier(.2,.8,.2,1) both}",
        ".underline{stroke:var(--accent);stroke-width:2;stroke-dasharray:240;stroke-dashoffset:240;"
        "animation:draw .48s ease-out both}",
        "@keyframes draw{to{stroke-dashoffset:0}}",
        "@media(prefers-reduced-motion:reduce){.tile,.underline{animation:none!important;opacity:1;transform:none;stroke-dashoffset:0}}",
    ]
    pieces = [
        '<rect class="panel" x="0.6" y="0.6" width="1198.8" height="148.8" rx="16"/>'
    ]
    for idx in range(1, 4):
        pieces.append(f'<path d="M {idx * 300} 20 V 130" stroke="var(--faint)" stroke-width="1"/>')
    for idx, (number, label, context, underline_len) in enumerate(tiles):
        center = idx * 300 + 150
        delay = idx * 0.15
        pieces.append(
            f'<g class="tile tile{idx}" style="animation-delay:{delay:.2f}s">'
            f'<text class="sans accent" x="{center}" y="53" text-anchor="middle" font-size="38" font-weight="700">{number}</text>'
            f'<path class="underline" d="M {center - underline_len / 2:.1f} 66 H {center + underline_len / 2:.1f}" '
            f'style="animation-delay:{delay + 0.25:.2f}s"/>'
            f'<text class="sans text" x="{center}" y="98" text-anchor="middle" font-size="16">{esc(label)}</text>'
            f'<text class="mono muted" x="{center}" y="124" text-anchor="middle" font-size="12">{esc(context)}</text>'
            '</g>'
        )
    return svg_doc("Career impact stats", 1200, 150, theme, "", "".join(css), "".join(pieces))


def write(name: str, value: str) -> None:
    (OUT / name).write_text(value, encoding="utf-8", newline="\n")


def main() -> None:
    builders = {
        "banner": banner,
        "card-dashboard": dashboard_card,
        "card-quorum": quorum_card,
        "impact": impact_strip,
    }
    for theme_name, theme in THEMES.items():
        for asset, builder in builders.items():
            write(f"{asset}-{theme_name}.svg", builder(theme))


if __name__ == "__main__":
    main()
