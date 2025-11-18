"""Create a placeholder camera image for demos."""
from PIL import Image, ImageDraw, ImageFont
import os

# Create image
width, height = 400, 300
img = Image.new('RGB', (width, height), color='#1f77b4')

# Add text
draw = ImageDraw.Draw(img)
text = "Mock Camera Feed"

# Try to use default font
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
except:
    font = ImageFont.load_default()

# Calculate text position (center)
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (width - text_width) // 2
y = (height - text_height) // 2

# Draw text
draw.text((x, y), text, fill='white', font=font)

# Save to each demo folder
demo_folders = [
    'streamlit-demo',
    'gradio-demo',
    'dash-demo',
    'reflex-demo',
    'fastapi-htmx-demo'
]

script_dir = os.path.dirname(os.path.abspath(__file__))

for folder in demo_folders:
    folder_path = os.path.join(script_dir, folder)
    if os.path.exists(folder_path):
        img_path = os.path.join(folder_path, 'camera_placeholder.png')
        img.save(img_path)
        print(f"Created: {img_path}")

print("\nPlaceholder images created successfully!")
