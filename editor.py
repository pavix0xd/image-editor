from PIL import Image, ImageFilter, ImageEnhance
import os
import numpy as np
import shutil
import sys
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Global folders
adjusted_folder = "./adjustedImgs"
edited_folder = "./editedImgs"
cache_filename = "cached_image.jpg"

def advanced_sharpen(image, strength=1.0, radius=1.0, threshold=0):
    if radius < 1:
        radius = 1
    img_array = np.array(image)
    blurred = np.array(image.filter(ImageFilter.GaussianBlur(radius)))
    difference = img_array - blurred
    if threshold > 0:
        low_contrast = np.abs(difference) < threshold
        difference[low_contrast] = 0
    sharpened = img_array + difference * strength
    sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
    return Image.fromarray(sharpened)

def prompt_float(label, default=1.0):
    while True:
        value = input(f"{Fore.CYAN}{label} [{default}]: {Style.RESET_ALL}").strip().lower()
        if value == 'q':
            print(Fore.YELLOW + "Exiting by user request.")
            sys.exit()
        if not value:
            return default
        try:
            return float(value)
        except ValueError:
            print(Fore.RED + "Please enter a number or 'q' to quit.")

def prompt_int(label, default=0):
    while True:
        value = input(f"{Fore.CYAN}{label} [{default}]: {Style.RESET_ALL}").strip().lower()
        if value == 'q':
            print(Fore.YELLOW + "Exiting by user request.")
            sys.exit()
        if not value:
            return default
        try:
            return int(value)
        except ValueError:
            print(Fore.RED + "Please enter an integer or 'q' to quit.")

def get_user_params():
    print(Fore.MAGENTA + "\n📸 Let's fine-tune your image!")
    print(Fore.LIGHTBLACK_EX + "You can skip a setting by just pressing Enter. Enter 'q' anytime to quit.\n")

    print(Fore.GREEN + "🛠️  Parameters explained:")
    print(Fore.LIGHTWHITE_EX + """
    • Contrast: Makes shadows darker and highlights brighter.
    • Brightness: Lightens or darkens the entire image.
    • Saturation (Color): Makes colors more vivid or muted.
    • Sharpness Strength: Emphasizes edges and details.
    • Sharpness Radius: Area around each pixel affected by sharpening.
    • Sharpness Threshold: Limits sharpening to high-contrast edges.
    • Exposure (simulated): Adds brightness to simulate camera exposure.
    • Shadows (simulated): Brings out details in dark areas.
    • Highlights (simulated): Recovers detail in bright areas.
    • Black Point (simulated): Adjusts how deep the blacks appear.
    """)

    contrast    = prompt_float("Contrast (e.g., 1.0 = original)", 1.0)
    brightness  = prompt_float("Brightness (1.0 = original)", 1.0)
    color       = prompt_float("Saturation (1.0 = original)", 1.0)
    strength    = prompt_float("Sharpness Strength (1.0 = normal)", 1.0)
    radius      = prompt_float("Sharpness Radius (≥1.0 recommended)", 1.0)
    threshold   = prompt_int("Sharpness Threshold (0-255)", 0)

    exposure    = prompt_float("Exposure Adjustment (add light)", 0.0)
    shadows     = prompt_float("Shadows (brighten darks)", 1.0)
    highlights  = prompt_float("Highlights (dim brights)", 1.0)
    black_point = prompt_float("Black Point (boost dark contrast)", 1.0)

    return {
        'enhance': {
            'contrast': contrast,
            'brightness': brightness + exposure,
            'color': color,
            'shadows': shadows,
            'highlights': highlights,
            'black_point': black_point
        },
        'sharpen': {
            'strength': strength,
            'radius': radius,
            'threshold': threshold
        }
    }

def apply_simulated_effects(img, enhance_params):
    img_np = np.array(img).astype(np.float32)

    img_np = np.where(img_np < 128, img_np * enhance_params['shadows'], img_np)
    img_np = np.where(img_np > 128, img_np * enhance_params['highlights'], img_np)
    img_np = img_np - (255 - img_np) * (1 - enhance_params['black_point'])

    img_np = np.clip(img_np, 0, 255).astype(np.uint8)
    return Image.fromarray(img_np)

def get_valid_choice(prompt, choices=('y', 'n', 'q')):
    while True:
        choice = input(f"{Fore.YELLOW}{prompt} {Style.RESET_ALL}").strip().lower()
        if choice in choices:
            return choice
        print(Fore.RED + "Please enter one of: " + ", ".join(choices))

def process_image_interactive(image_path):
    os.makedirs(adjusted_folder, exist_ok=True)
    os.makedirs(edited_folder, exist_ok=True)

    while True:
        params = get_user_params()
        enhance = params['enhance']
        sharpen = params['sharpen']

        try:
            img = Image.open(image_path)
            original_mode = img.mode
            if original_mode != 'RGB':
                img = img.convert('RGB')

            img = ImageEnhance.Contrast(img).enhance(enhance['contrast'])
            img = ImageEnhance.Brightness(img).enhance(enhance['brightness'])
            img = ImageEnhance.Color(img).enhance(enhance['color'])

            img = apply_simulated_effects(img, enhance)
            img = advanced_sharpen(img, **sharpen)
            img = img.filter(ImageFilter.EDGE_ENHANCE)

            if original_mode != 'RGB':
                img = img.convert(original_mode)

            adjusted_path = os.path.join(adjusted_folder, cache_filename)
            img.save(adjusted_path)
            img.show()

            decision = get_valid_choice("\n💬 Are you satisfied with the result? (y = save, n = retry, q = quit): ")
            if decision == 'y':
                final_path = os.path.join(edited_folder, os.path.basename(image_path))
                shutil.move(adjusted_path, final_path)
                print(Fore.GREEN + f"Final adjusted image saved: {final_path}")
                break
            elif decision == 'n':
                os.remove(adjusted_path)
                print(Fore.CYAN + "Retrying adjustments...")
            elif decision == 'q':
                if os.path.exists(adjusted_path):
                    os.remove(adjusted_path)
                print(Fore.YELLOW + "Exited without saving.")
                break

        except Exception as e:
            print(Fore.RED + f"Error processing {image_path}: {e}")
            break

def main():
    input_folder = "./imgs"
    if not os.path.exists(input_folder):
        print(Fore.RED + "Input folder './imgs' does not exist.")
        return

    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_formats)]

    if not images:
        print(Fore.YELLOW + "No images found in './imgs'.")
        return

    for img_file in images:
        print(Fore.BLUE + f"\n🎨 === Processing: {img_file} ===")
        image_path = os.path.join(input_folder, img_file)
        process_image_interactive(image_path)

if __name__ == "__main__":
    main()
