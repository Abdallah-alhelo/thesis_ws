import cv2
import numpy as np
import os
# ==========================================
# 1. PARAMETERS
# ==========================================
MAP_PATH = "hospital_map.pgm"
RESOLUTION = 0.05  # meters/pixel

# Door width in meters to pinch shut (typically 0.8m - 1.2m)
DOOR_WIDTH_METERS = 2.9  

# Minimum room size in square meters (filters out tiny leftover pockets)
MIN_ROOM_AREA_SQM = 0.2  

# ==========================================
# 2. LOAD & THICKEN WALLS
# ==========================================
map_img = cv2.imread(MAP_PATH, cv2.IMREAD_GRAYSCALE)
if map_img is None:
    raise FileNotFoundError(f"Could not find: {MAP_PATH}")

# Binary threshold: Free space = 255 (white), Walls/Obstacles = 0 (black)
_, free_space = cv2.threshold(map_img, 250, 255, cv2.THRESH_BINARY)

# Thicken the thin SLAM walls by slightly eroding the free space (2-3 pixels)
wall_thicken_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
solid_free_space = cv2.erode(free_space, wall_thicken_kernel, iterations=1)

# ==========================================
# 3. DOOR PINCHING (EROSION)
# ==========================================
door_px = int((DOOR_WIDTH_METERS / 2.0) / RESOLUTION)
ksize = door_px if door_px % 2 == 1 else door_px + 1

print(f"[INFO] Door erosion kernel size: {ksize}x{ksize} px")

# Circular kernel erodes equally in all directions
erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
eroded_rooms = cv2.erode(solid_free_space, erode_kernel, iterations=1)

# ==========================================
# 4. FILTER ROOM CORES
# ==========================================
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(eroded_rooms, connectivity=8)

min_area_px = int(MIN_ROOM_AREA_SQM / (RESOLUTION ** 2))
valid_labels = []

for i in range(1, num_labels):
    if stats[i, cv2.CC_STAT_AREA] >= min_area_px:
        valid_labels.append(i)

print(f"[INFO] Detected {len(valid_labels)} room cores.")

# ==========================================
# 5. EXPAND CORES BACK TO WALLS (WATERSHED)
# ==========================================
markers = np.zeros_like(free_space, dtype=np.int32)

# Set obstacles and walls as background marker
markers[solid_free_space == 0] = 1

# Place unique marker ID for each surviving room core
for idx, lbl in enumerate(valid_labels):
    markers[labels == lbl] = idx + 2

# Apply watershed to expand back out to walls and doorways
map_bgr = cv2.cvtColor(map_img, cv2.COLOR_GRAY2BGR)
cv2.watershed(map_bgr, markers)

# ==========================================
# 6. VISUALIZATION
# ==========================================
submap_viz = np.zeros_like(map_bgr)
np.random.seed(10)
colors = np.random.randint(40, 240, size=(len(valid_labels) + 2, 3)).tolist()

for idx in range(len(valid_labels)):
    submap_viz[markers == (idx + 2)] = colors[idx + 2]

# Draw doorway cut-lines in red
submap_viz[markers == -1] = [0, 0, 255]

# Save and show
cv2.imwrite("bormann_segmented_rooms.png", submap_viz)
cv2.imshow("Step 1: Eroded Cores (Check doorways closed)", eroded_rooms)
cv2.imshow("Step 2: Segmented Submaps", submap_viz)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ==========================================
# 7. EXPORT SUBMAPS FOR ROS 2 NAV2
# ==========================================
print("\n[INFO] Starting Submap Extraction...")

# ---- UPDATE THESE VALUES FROM YOUR MAIN YAML FILE ----
GLOBAL_ORIGIN_X = -12.5  # Put your map's YAML origin X here
GLOBAL_ORIGIN_Y = -35.0  # Put your map's YAML origin Y here
# ------------------------------------------------------

# Create a folder to save all the submaps
output_dir = "nav2_submaps"
os.makedirs(output_dir, exist_ok=True)

global_height, global_width = map_img.shape

# A kernel to dilate the room mask so we capture the walls and doorway
# 10 pixels is roughly 50cm of wall thickness (10 * 0.05)
wall_grab_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (22, 22))

# Loop through every valid room label we found in Step 5
for idx, lbl in enumerate(valid_labels):
    room_id = idx + 1
    
    # 1. Isolate just this specific room (True/False mask)
    # Remember, markers were shifted by +2 in the previous step
    room_mask = np.uint8(markers == (idx + 2)) * 255
    
    # 2. Dilate the mask to grab the surrounding walls and part of the doorway
    expanded_mask = cv2.dilate(room_mask, wall_grab_kernel, iterations=1)
    
    # 3. Create a blank grey map (205 = Unknown space in ROS)
    submap_img = np.full_like(map_img, 127)
    
    # 4. Copy the original map pixels ONLY where our expanded mask is white
    submap_img[expanded_mask == 255] = map_img[expanded_mask == 255]
    
    # 5. Crop the image to save memory (Find the bounding box of the expanded mask)
    y_coords, x_coords = np.where(expanded_mask == 255)
    y_min, y_max = np.min(y_coords), np.max(y_coords)
    x_min, x_max = np.min(x_coords), np.max(x_coords)
    
    # Add a small 5-pixel padding around the crop
    y_min = max(0, y_min - 5)
    y_max = min(global_height, y_max + 5)
    x_min = max(0, x_min - 5)
    x_max = min(global_width, x_max + 5)
    
    cropped_submap = submap_img[y_min:y_max, x_min:x_max]
    
    # 6. Calculate the New Origin for the YAML file
    # ROS Origin is the bottom-left corner. We find how far the crop's bottom-left
    # is from the global image's bottom-left, in meters.
    delta_x_meters = x_min * RESOLUTION
    delta_y_meters = (global_height - y_max) * RESOLUTION
    
    new_origin_x = GLOBAL_ORIGIN_X + delta_x_meters
    new_origin_y = GLOBAL_ORIGIN_Y + delta_y_meters
    
    # 7. Save the .pgm file
    pgm_filename = f"submap_{room_id}.pgm"
    cv2.imwrite(os.path.join(output_dir, pgm_filename), cropped_submap)
    
    # 8. Save the .yaml file
    yaml_filename = f"submap_{room_id}.yaml"
    yaml_content = f"""image: {pgm_filename}
mode: trinary
resolution: {RESOLUTION}
origin: [{new_origin_x:.4f}, {new_origin_y:.4f}, 0.0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.196
"""
    with open(os.path.join(output_dir, yaml_filename), "w") as f:
        f.write(yaml_content)
        
    print(f"[SUCCESS] Exported {pgm_filename} and {yaml_filename}")

print(f"\n[INFO] All submaps saved in the '{output_dir}/' directory.")



