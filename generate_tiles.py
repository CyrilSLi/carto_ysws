import os, shutil, subprocess, sys
from tqdm import trange

def mkdirs(path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    return path

temp_name = mkdirs("/tmp/carto_ysws_tile_temp/temp.png")
temp_name_crop = os.path.join(os.path.dirname(temp_name), "temp_%d.png")
orig_file = "inkscape_tiles/export/Page_%d.png"
os.makedirs("tile/", exist_ok=True)

if sys.argv[1] in ("-r", "--refresh"):
    shutil.rmtree("tile/", ignore_errors=True)



# Zoom 6
if not os.path.exists("tile/6/63/63.png"):
    for i in trange(16, desc="Zoom 6"):
        subprocess.run(["magick", orig_file % i, "-crop", "256x256", "+repage", temp_name_crop])
        for j in range(256):
            x = i // 4 * 16 + j // 16
            y = i % 4 * 16 + j % 16
            shutil.move(temp_name_crop % j, mkdirs(f"tile/6/{x}/{y}.png"))



# Zoom 5
if not os.path.exists("tile/5/31/31.png"):
    for i in trange(16, desc="Zoom 5"):
        subprocess.run(["magick", orig_file % i, "-crop", "512x512", "+repage", temp_name_crop])
        for j in range(64):
            x = i // 4 * 8 + j // 8
            y = i % 4 * 8 + j % 8
            subprocess.run(["magick", temp_name_crop % j, "-resize", "256x256", mkdirs(f"tile/5/{x}/{y}.png")])



# Zoom 4
if not os.path.exists("tile/4/15/15.png"):
    for i in trange(16, desc="Zoom 4"):
        subprocess.run(["magick", orig_file % i, "-crop", "1024x1024", "+repage", temp_name_crop])
        for j in range(16):
            x = i // 4 * 4 + j // 4
            y = i % 4 * 4 + j % 4
            subprocess.run(["magick", temp_name_crop % j, "-resize", "256x256", mkdirs(f"tile/4/{x}/{y}.png")])



# Zoom 3
if not os.path.exists("tile/3/7/7.png"):
    for i in trange(16, desc="Zoom 3"):
        subprocess.run(["magick", orig_file % i, "-crop", "2048x2048", "+repage", temp_name_crop])
        for j in range(4):
            x = i // 4 * 2 + j // 2
            y = i % 4 * 2 + j % 2
            subprocess.run(["magick", temp_name_crop % j, "-resize", "256x256", mkdirs(f"tile/3/{x}/{y}.png")])



# Zoom 2
if not os.path.exists("tile/2/3/3.png"):
    for i in trange(16, desc="Zoom 2"):
        subprocess.run(["magick", orig_file % i, "-resize", "256x256", mkdirs(f"tile/2/{i//4}/{i%4}.png")])



# Zoom 1
zoom1_tiles = (
    ((0, 0), (0, 1), (1, 0), (1, 1)),
    ((0, 2), (0, 3), (1, 2), (1, 3)),
    ((2, 0), (2, 1), (3, 0), (3, 1)),
    ((2, 2), (2, 3), (3, 2), (3, 3))
)
for i in trange(4, desc="Zoom 1"):
    subprocess.run(["magick", "montage", "-tile", "2x2", "-geometry", "+0+0"] + [f"tile/2/{x}/{y}.png" for x, y in zoom1_tiles[i]] + [temp_name])
    subprocess.run(["magick", temp_name, "-resize", "256x256", mkdirs(f"tile/1/{i//2}/{i%2}.png")])



# Zoom 0
for i in trange(1, desc="Zoom 0"):
    subprocess.run(["magick", "montage", "-tile", "4x4", "-geometry", "+0+0"] + [f"tile/2/{i//4}/{i%4}.png" for i in range(16)] + [temp_name])
    subprocess.run(["magick", temp_name, "-resize", "256x256", mkdirs("tile/0/0/0.png")])



# Cleanup
shutil.rmtree(os.path.dirname(temp_name), ignore_errors=True)