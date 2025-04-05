from email.mime import image
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict

def get_prime_factors(n):
    """Return prime factors of a number as a dictionary with counts"""
    factors = defaultdict(int)
    num = n
    i = 2
    while i * i <= num:
        while num % i == 0:
            factors[i] += 1
            num //= i
        i += 1
    if num > 1:
        factors[num] += 1
    return factors

def blend_colors(factors, prime_colors):
    """Blend colors based on prime factors"""
    if not factors:
        return (255, 255, 255)  # White for 1
    
    r, g, b = 0, 0, 0
    total = sum(factors.values())
    
    for prime, count in factors.items():
        if prime in prime_colors:
            pr, pg, pb = prime_colors[prime]
            r += pr * count
            g += pg * count
            b += pb * count
    
    return (
        int(r / total),
        int(g / total),
        int(b / total)
    )

def create_multiplication_table(size=10, cell_size=40):
    # Define prime colors (R,G,B)
    prime_colors = {
        2: (255, 0, 0),    # Red
        3: (0, 0, 255),    # Blue
        5: (255, 0, 255),   # Magenta
        7: (255, 255, 0),  # Yellow
    }
    
    # Create image
    padding = 50  # Space for numbers on left and top
    title = 50
    img_width = cell_size * size + padding +50
    img_height = cell_size * size + padding + title
    img = Image.new('RGB', (img_width, img_height), 'white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to load Arial font, fall back to default if not available
        font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()

    # Draw multiplication table
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            product = i * j
            factors = get_prime_factors(product)
            color = blend_colors(factors, prime_colors)
            
            # Calculate cell position
            x1 = (j - 1) * cell_size + padding
            y1 = (i - 1) * cell_size + padding
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            
            # Draw cell
            draw.rectangle([x1, y1, x2, y2], fill=color, outline='gray')
            
            # Add number
            text_color = 'black' if sum(color) > 382 else 'white'  # Choose text color based on background brightness
            text = str(product)
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = x1 + (cell_size - text_width) // 2
            text_y = y1 + (cell_size - text_height) // 2
            draw.text((text_x, text_y), text, fill=text_color, font=font)
            
            # Draw row/column numbers
            if j == 1:  # Row numbers
                draw.text((padding//2, y1 + cell_size//2), str(i), fill='black', font=font)
            if i == 1:  # Column numbers
                draw.text((x1 + cell_size//2, padding//2), str(j), fill='black', font=font)
    
    # Draw legend
    legend_y = img_height - 30
    legend_x = padding
    for prime, color in prime_colors.items():
        # Draw color square
        draw.rectangle([legend_x, legend_y, legend_x+15, legend_y+15], fill=color, outline='gray')
        # Add prime number
        draw.text((legend_x+20, legend_y), f"Prime {prime}", fill='black', font=font)
        legend_x += 80  # Space between legend items
    
    return img

# Create and save the image
table = create_multiplication_table(10, 30)  # 20x20 table with 30px cells
table.save('multiplication_table.png')
print("Image saved as 'multiplication_table.png'")