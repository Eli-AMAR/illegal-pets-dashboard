#!/bin/bash
set -e
cd "$(dirname "$0")"
FF=$(python3 -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())")
mkdir -p logs out audio cfg frames

python3 make_configs.py

echo "=== rendering frames (2 concurrent) ==="
printf '%s\n' video1 video2 video3 video4 video5 | \
  xargs -P 2 -I{} bash -c 'node render.js cfg/{}.json frames/{} > logs/{}.render.log 2>&1 && echo "render OK: {}"'

echo "=== audio + encode ==="
python3 -c "import json
for m in json.load(open('manifest.json')): print(m['id'], m['slug'], m['total_s'], m['seed'], m['transpose'], m['bpm'])" | \
while read -r id slug total seed trans bpm; do
  python3 audio.py "$total" "$seed" "$trans" "$bpm" "audio/$id.wav" > "logs/$id.audio.log" 2>&1
  "$FF" -y -framerate 30 -i "frames/$id/%05d.jpg" -i "audio/$id.wav" \
    -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p \
    -c:a aac -b:a 160k -shortest -movflags +faststart \
    "out/$slug.mp4" > "logs/$id.encode.log" 2>&1
  echo "encode OK: $slug.mp4"
done

echo "=== done ==="
ls -la out/
