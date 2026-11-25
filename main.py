"""Entry program for make.fun's news-image-20261125 bounty.

The artwork that sums up 25 November 2026's world news lives in this
repository as news.png. Running the program publishes it as the
contest output: it checks the file, then copies it unchanged to
entry.png in the output directory.

The harness runs the program twice, with no network, and both runs
must produce the same bytes, so the copy below is a plain byte
transfer in fixed-size chunks: no timestamps, no randomness, nothing
that can vary between runs.

Try it outside the grader with:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

CHUNK_SIZE = 65536
SIZE_LIMIT = 1048576  # the gate takes at most 1 MiB
PNG_HEADER = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

# The artwork's four panels, one story each:
#   tankers attacked in the Strait of Hormuz,
#   Ukraine's strikes on Russian energy sites,
#   Pakistan's first astronaut reaching orbit,
#   and Nvidia's fading comeback rally.


def artwork_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "news.png")


def destination_path():
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return folder, os.path.join(folder, "entry.png")


def check_artwork(path):
    size = os.path.getsize(path)
    if size > SIZE_LIMIT:
        raise SystemExit("news.png is over the 1 MiB limit: %d bytes" % size)
    with open(path, "rb") as f:
        if f.read(len(PNG_HEADER)) != PNG_HEADER:
            raise SystemExit("news.png is not a PNG file")
    return size


def main():
    src = artwork_path()
    size = check_artwork(src)
    folder, dest = destination_path()
    os.makedirs(folder, exist_ok=True)
    with open(src, "rb") as fin, open(dest, "wb") as fout:
        shutil.copyfileobj(fin, fout, CHUNK_SIZE)
    os.chmod(dest, 0o644)
    print("wrote %s (%d bytes)" % (dest, size))


if __name__ == "__main__":
    main()
