import os, shutil, subprocess, sys, threading, time
from tqdm import tqdm, trange
from tqdm.contrib.concurrent import thread_map

def mkdirs(path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    return path

temp_name = "/tmp/carto_ysws_tile_temp.png"
temp_name_crop = "/tmp/carto_ysws_tile_temp_%d_%d.png"
orig_file = "inkscape_tiles/export/Page_%d.png"
os.makedirs("tile/", exist_ok=True)

if sys.argv[1] in ("-r", "--refresh"):
    shutil.rmtree("tile/", ignore_errors=True)



def process_tile(zoom, index):
    resolution = 2**(zoom+2)
    split_size = 4096 // resolution
    subprocess.run(["magick", orig_file % index, "-crop", f"{resolution}x{resolution}", "+repage", temp_name_crop.replace("%d", str(index), 1)])
    for j in range(split_size**2):
        x = index // 4 * split_size + j // split_size
        y = index % 4 * split_size + j % split_size
        filename = temp_name_crop % (index, j)
        if zoom == 6:
            shutil.move(filename, mkdirs(f"tile/{zoom}/{x}/{y}.png"))
        else:
            subprocess.run(["magick", filename, "-resize", "256x256", mkdirs(f"tile/{zoom}/{x}/{y}.png")])

def process_zoom(zoom):
    if not os.path.exists(f"tile/{zoom}/{2**zoom-1}/{2**zoom-1}.png"):
        _ = thread_map(lambda i: process_tile(zoom, i), range(16), desc=f"Zoom {zoom}", max_workers=4)

        """ threadpool = []
        for i in range(16):
            threadpool.append(threading.Thread(target=process_tile, args=(zoom, i)))
            threadpool[-1].start()
        with tqdm(total=16, desc=f"Zoom {zoom}") as pbar:
            while threadpool:
                time.sleep(0.1)
                threadpool = [t for t in threadpool if t.is_alive()]
                pbar.n = 16 - len(threadpool)
                pbar.refresh() """



process_zoom(6)
process_zoom(5)
process_zoom(4)
process_zoom(3)



# Zoom 2
if not os.path.exists("tile/2/3/3.png"):
    for i in trange(16, desc="Zoom 2"):
        subprocess.run(["magick", orig_file % i, "-resize", "256x256", mkdirs(f"tile/2/{i//4}/{i%4}.png")])



# Zoom 1
if not os.path.exists("tile/1/1/1.png"):
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
if not os.path.exists("tile/0/0/0.png"):
    for i in trange(1, desc="Zoom 0"):
        subprocess.run(["magick", "montage", "-tile", "4x4", "-geometry", "+0+0"] + [f"tile/2/{i//4}/{i%4}.png" for i in range(16)] + [temp_name])
        subprocess.run(["magick", temp_name, "-resize", "256x256", mkdirs("tile/0/0/0.png")])