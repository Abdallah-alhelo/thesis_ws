import cv2
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
MAP_PATH = os.path.join(script_dir, "..", "maps", "hospital_map.pgm")
OUTPUT_DIR = os.path.join(script_dir, "..", "maps", "nav2_submaps")
os.makedirs(OUTPUT_DIR, exist_ok=True)

RESOLUTION = 0.05  
GLOBAL_ORIGIN_X = -12.5  
GLOBAL_ORIGIN_Y = -35.0  

map_img = cv2.imread(MAP_PATH, cv2.IMREAD_GRAYSCALE)
if map_img is None:
    raise FileNotFoundError("Map not found!")

global_height, global_width = map_img.shape

print("[INFO] GUI Opened. Drag a box around a room. Press ENTER to confirm the box.")
print("[INFO] Press ENTER again after the last box to finish and extract.")

# Opens an interactive GUI for you to draw rectangles
rois = cv2.selectROIs("Select Submaps (Press ENTER to confirm, ESC to quit)", map_img, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()

print(f"\n[INFO] You selected {len(rois)} rooms. Extracting now...")

for idx, rect in enumerate(rois):
    x, y, w, h = rect
    room_id = idx + 1
    
    # Create blank unknown map (205)
    submap_img = np.full_like(map_img, 205)
    
    # Copy only the selected rectangle from the original map
    submap_img[y:y+h, x:x+w] = map_img[y:y+h, x:x+w]
    
    # Crop it tightly to the selected area
    cropped_submap = submap_img[y:y+h, x:x+w]
    
    # Calculate new YAML origins based on the bounding box location
    delta_x_meters = x * RESOLUTION
    delta_y_meters = (global_height - (y + h)) * RESOLUTION
    new_origin_x = GLOBAL_ORIGIN_X + delta_x_meters
    new_origin_y = GLOBAL_ORIGIN_Y + delta_y_meters
    
    pgm_filename = f"submap_{room_id}.pgm"
    yaml_filename = f"submap_{room_id}.yaml"
    full_yaml_path = os.path.abspath(os.path.join(OUTPUT_DIR, yaml_filename))
    
    cv2.imwrite(os.path.join(OUTPUT_DIR, pgm_filename), cropped_submap)
    
    world_x_min = GLOBAL_ORIGIN_X + (x * RESOLUTION)
    world_x_max = GLOBAL_ORIGIN_X + ((x + w) * RESOLUTION)
    world_y_min = GLOBAL_ORIGIN_Y + ((global_height - (y + h)) * RESOLUTION)
    world_y_max = GLOBAL_ORIGIN_Y + ((global_height - y) * RESOLUTION)

    print(f"            'submap_{room_id}': {{")
    print(f"                'x_min': {world_x_min:.2f}, 'x_max': {world_x_max:.2f},")
    print(f"                'y_min': {world_y_min:.2f}, 'y_max': {world_y_max:.2f},")
    print(f"                'yaml': '{full_yaml_path}'")
    print(f"            }},")
    
    yaml_content = f"""image: {pgm_filename}
mode: trinary
resolution: {RESOLUTION}
origin: [{new_origin_x:.4f}, {new_origin_y:.4f}, 0.0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.196
"""
    with open(full_yaml_path, "w") as f:
        f.write(yaml_content)

print("\n[SUCCESS] All submaps exported perfectly!")
