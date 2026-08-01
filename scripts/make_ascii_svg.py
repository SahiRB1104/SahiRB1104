import os
from PIL import Image, ImageEnhance, ImageOps

# Density ramp from bright (blank space) to dark (dense glyphs)
RAMP = " .`:-=+*cs#%@"

def photo_to_ascii(image_path, width=85):
    img = Image.open(image_path)
    
    # Calculate aspect ratio adjustment for monospace fonts (width:height ~ 1:2)
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.48)
    
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    img = img.convert("L")  # Convert to grayscale
    
    # Enhance contrast and auto contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.8)
    img = ImageOps.autocontrast(img, cutoff=2)
    
    ascii_rows = []
    pixels = [img.getpixel((x, y)) for y in range(height) for x in range(width)]
    num_chars = len(RAMP)
    
    for y in range(height):
        row_chars = []
        for x in range(width):
            pixel_val = pixels[y * width + x]
            # Map 0..255 to RAMP indices
            # 255 (brightest) -> index 0 (space)
            # 0 (darkest) -> index num_chars - 1 (@)
            index = int((255 - pixel_val) / 255 * (num_chars - 1))
            char = RAMP[index]
            # Escape HTML special chars
            if char == "&": char = "&amp;"
            elif char == "<": char = "&lt;"
            elif char == ">": char = "&gt;"
            elif char == " ": char = "&#160;"
            row_chars.append(char)
        ascii_rows.append("".join(row_chars))
        
    return ascii_rows

def generate_ascii_svg(ascii_rows, output_path):
    num_rows = len(ascii_rows)
    max_cols = max(len(r) for r in ascii_rows)
    
    font_size = 8.5
    line_height = 10
    char_width = 5.2
    
    padding_x = 20
    padding_y = 45
    
    svg_width = int(max_cols * char_width + padding_x * 2)
    svg_height = int(num_rows * line_height + padding_y + 20)
    
    # SVG Header and Styles
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg.append('<style>')
    svg.append('''
        .bg { fill: #0d1117; rx: 10px; ry: 10px; stroke: #30363d; stroke-width: 1px; }
        .header-dot { rx: 50%; ry: 50%; }
        .title { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 11px; fill: #8b949e; font-weight: 600; }
        .ascii-text { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 8.5px; fill: #58a6ff; white-space: pre; }
        .row { opacity: 0; animation: rowFadeIn 0.05s ease-out forwards; }
        @keyframes rowFadeIn {
            from { opacity: 0; transform: translateY(2px); }
            to { opacity: 1; transform: translateY(0); }
        }
    ''')
    
    # Generate CSS animation delays for each row
    for i in range(num_rows):
        delay = round(i * 0.035, 3)
        svg.append(f'  .row-{i} {{ animation-delay: {delay}s; }}')
        
    svg.append('</style>')
    
    # Terminal Container Window
    svg.append(f'<rect class="bg" width="{svg_width}" height="{svg_height}" />')
    
    # Terminal Header Bar
    svg.append('<circle class="header-dot" cx="20" cy="18" r="5" fill="#ff5f56" />')
    svg.append('<circle class="header-dot" cx="35" cy="18" r="5" fill="#ffbd2e" />')
    svg.append('<circle class="header-dot" cx="50" cy="18" r="5" fill="#27c93f" />')
    svg.append(f'<text class="title" x="{svg_width // 2}" y="22" text-anchor="middle">sahil_portrait.ascii</text>')
    svg.append(f'<line x1="0" y1="34" x2="{svg_width}" y2="34" stroke="#30363d" stroke-width="1" />')
    
    # ASCII Text Lines
    svg.append(f'<g class="ascii-text" transform="translate({padding_x}, {padding_y})">')
    for idx, row in enumerate(ascii_rows):
        y_pos = idx * line_height
        svg.append(f'  <text class="row row-{idx}" x="0" y="{y_pos}">{row}</text>')
    svg.append('</g>')
    
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Successfully generated {output_path} ({svg_width}x{svg_height})")

if __name__ == "__main__":
    input_photo = "photo.png"
    output_svg = "ascii-portrait.svg"
    if os.path.exists(input_photo):
        rows = photo_to_ascii(input_photo, width=78)
        generate_ascii_svg(rows, output_svg)
    else:
        print(f"Error: {input_photo} not found!")
