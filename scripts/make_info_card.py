import os

def generate_info_card_svg(output_path="info-card.svg"):
    lines = [
        ("Host", "Sahil Bhalekar (Software Dev)", "#7ee787"),
        ("Primary Focus", "AI/ML, LLM Dev & Async Systems", "#58a6ff"),
        ("Core Stack", "Python, React.js, FastAPI, Node", "#79c0ff"),
        ("AI / ML Pipeline", "HuggingFace, Transformers, NLP", "#d2a8ff"),
        ("Databases", "PostgreSQL, MongoDB, Redis", "#ffa657"),
        ("Cloud & DevOps", "Docker, GCP Cloud Run, AWS", "#58a6ff"),
        ("DSA & OOP", "Java (Active Practice & DSA)", "#7ee787"),
        ("Certifications", "OCI AI Associate, AWS Cloud", "#f0883e"),
        ("Featured Work", "NewsAura AI, Atomic Audit Engine", "#79c0ff"),
        ("Portfolio", "python-phi-nine.vercel.app", "#a5d6ff"),
    ]
    
    card_width = 410
    card_height = 340
    line_height = 24
    padding_x = 16
    padding_y = 52
    
    svg = ['<?xml version="1.0" encoding="UTF-8"?>']
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {card_width} {card_height}" width="{card_width}" height="{card_height}">')
    svg.append('<style>')
    svg.append('''
        .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }
        .header-dot { rx: 50%; ry: 50%; }
        .title { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }
        .label { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 10.5px; fill: #8b949e; font-weight: 600; }
        .val { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 10.5px; font-weight: 500; }
        .prompt-symbol { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11px; fill: #7ee787; font-weight: 700; }
        .line { opacity: 0; animation: lineFadeIn 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        @keyframes lineFadeIn {
            from { opacity: 0; transform: translateX(-6px); }
            to { opacity: 1; transform: translateX(0); }
        }
    ''')
    
    for i in range(len(lines)):
        delay = round(0.08 + i * 0.07, 3)
        svg.append(f'  .line-{i} {{ animation-delay: {delay}s; }}')
        
    svg.append('</style>')
    
    # Terminal Frame
    svg.append(f'<rect class="bg" width="{card_width}" height="{card_height}" />')
    
    # Header Dots & Title
    svg.append('<circle class="header-dot" cx="20" cy="18" r="5" fill="#ff5f56" />')
    svg.append('<circle class="header-dot" cx="35" cy="18" r="5" fill="#ffbd2e" />')
    svg.append('<circle class="header-dot" cx="50" cy="18" r="5" fill="#27c93f" />')
    svg.append(f'<text class="title" x="{card_width // 2}" y="22" text-anchor="middle">sahil@neofetch ~ info</text>')
    svg.append(f'<line x1="0" y1="34" x2="{card_width}" y2="34" stroke="#30363d" stroke-width="1" />')
    
    # Content Lines
    svg.append(f'<g transform="translate({padding_x}, {padding_y})">')
    for idx, (label, val, val_color) in enumerate(lines):
        y_pos = idx * line_height
        svg.append(f'  <g class="line line-{idx}">')
        svg.append(f'    <text class="prompt-symbol" x="0" y="{y_pos}">&#10095;</text>')
        svg.append(f'    <text class="label" x="14" y="{y_pos}">{label}:</text>')
        # Label offset
        label_width = len(label) * 6.6 + 20
        svg.append(f'    <text class="val" x="{label_width}" y="{y_pos}" fill="{val_color}">{val}</text>')
        svg.append('  </g>')
    svg.append('</g>')
    
    # Color palette bar at bottom
    color_bar_y = card_height - 16
    palette_colors = ["#484f58", "#ff7b72", "#7ee787", "#ffa657", "#79c0ff", "#d2a8ff", "#a5d6ff", "#ffffff"]
    svg.append(f'<g transform="translate({padding_x}, {color_bar_y})">')
    for idx, color in enumerate(palette_colors):
        x_pos = idx * 15
        svg.append(f'  <rect x="{x_pos}" y="0" width="11" height="7" rx="2" fill="{color}" />')
    svg.append('</g>')
    
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Successfully generated {output_path} ({card_width}x{card_height})")

if __name__ == "__main__":
    generate_info_card_svg("info-card.svg")
