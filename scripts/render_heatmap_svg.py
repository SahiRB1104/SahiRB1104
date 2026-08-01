import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def render_heatmap(json_path="data/contributions.json", output_svg="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Missing {json_path}. Run fetch_contributions.py first!")
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    days = data.get("days", [])
    total_contributions = data.get("total_contributions", 0)
    max_streak = data.get("max_streak", 0)
    current_streak = data.get("current_streak", 0)
    
    box_size = 11
    gap = 3.5
    step = box_size + gap
    
    padding_x = 35
    padding_y = 50
    
    # Organize days into 53 weeks x 7 days
    num_weeks = 53
    svg_width = 860
    svg_height = 200
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg.append('<style>')
    svg.append('''
        .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }
        .header-dot { rx: 50%; ry: 50%; }
        .title { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }
        .stat-text { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11.5px; fill: #c9d1d9; font-weight: 500; }
        .highlight { fill: #7ee787; font-weight: 700; }
        .legend-text { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 10px; fill: #8b949e; }
        .day-box { rx: 2.5px; ry: 2.5px; opacity: 0; animation: boxPop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
        @keyframes boxPop {
            from { opacity: 0; transform: scale(0.2); }
            to { opacity: 1; transform: scale(1); }
        }
    ''')
    
    # Calculate grid items animation delays
    # We delay based on col + row for a beautiful diagonal ripple effect
    for col in range(num_weeks):
        for row in range(7):
            delay = round(0.05 + (col + row) * 0.015, 3)
            svg.append(f'  .c-{col}-{row} {{ animation-delay: {delay}s; transform-origin: center; }}')
            
    svg.append('</style>')
    
    # Container Window
    svg.append(f'<rect class="bg" width="{svg_width}" height="{svg_height}" />')
    
    # Window Dots & Header
    svg.append('<circle class="header-dot" cx="20" cy="18" r="5" fill="#ff5f56" />')
    svg.append('<circle class="header-dot" cx="35" cy="18" r="5" fill="#ffbd2e" />')
    svg.append('<circle class="header-dot" cx="50" cy="18" r="5" fill="#27c93f" />')
    svg.append(f'<text class="title" x="{svg_width // 2}" y="22" text-anchor="middle">sahil@github ~ ./contributions.sh</text>')
    svg.append(f'<line x1="0" y1="34" x2="{svg_width}" y2="34" stroke="#30363d" stroke-width="1" />')
    
    # Day Boxes Grid
    svg.append(f'<g transform="translate({padding_x}, {padding_y})">')
    
    # We layout day boxes week by week
    idx = 0
    total_days = len(days)
    
    for col in range(num_weeks):
        for row in range(7):
            if idx < total_days:
                d = days[idx]
                level = min(d.get("level", 0), len(PALETTE) - 1)
                color = PALETTE[level]
                x = col * step
                y = row * step
                svg.append(f'  <rect class="day-box c-{col}-{row}" x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" />')
                idx += 1
    svg.append('</g>')
    
    # Footer Stats Summary
    footer_y = svg_height - 18
    svg.append(f'<g transform="translate({padding_x}, {footer_y})">')
    svg.append(f'  <text class="stat-text" x="0" y="0"><tspan class="highlight">{total_contributions:,}</tspan> contributions in the last year &#183; Max Streak: <tspan class="highlight">{max_streak}</tspan> days &#183; Current Streak: <tspan class="highlight">{current_streak}</tspan> days</text>')
    
    # Legend on bottom right
    legend_x = svg_width - padding_x - 130
    svg.append(f'  <g transform="translate({legend_x - 50}, -9)">')
    svg.append('    <text class="legend-text" x="0" y="8">Less</text>')
    for l_idx, color in enumerate(PALETTE):
        lx = 28 + l_idx * 13
        svg.append(f'    <rect x="{lx}" y="0" width="10" height="10" rx="2" fill="{color}" />')
    svg.append('    <text class="legend-text" x="96" y="8">More</text>')
    svg.append('  </g>')
    
    svg.append('</g>')
    svg.append('</svg>')
    
    with open(output_svg, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Successfully rendered {output_svg} ({svg_width}x{svg_height})")

if __name__ == "__main__":
    render_heatmap()
