import os
from PIL import Image

src_img = r"C:\Users\МобайлМаркет\.gemini\antigravity\brain\c1d6a37c-bf4d-4fef-a9e2-1059369ef0e1\.user_uploaded\media_1789132103426.jpg"
out_dir = r"C:\Users\МобайлМаркет\.gemini\antigravity\scratch\Eshkeri"

img = Image.open(src_img).convert("RGBA")

# Save PNG for UI usage
png_path = os.path.join(out_dir, "app_icon.png")
img.save(png_path, format="PNG")

# Save multi-resolution ICO for Windows exe and window icon
ico_path = os.path.join(out_dir, "app_icon.ico")
icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
img.save(ico_path, format="ICO", sizes=icon_sizes)

print(f"Icons generated successfully: {png_path} and {ico_path}")
