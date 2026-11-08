# 실사 재질 사진 16장을 4×4 한 장(textures.jpg)으로 묶는다 (Blender 5.x)
#
#   blender -b -P tools/atlas.py -- <사진 폴더> textures.jpg
#
# 사진: ambientCG (ambientcg.com) CC0 텍스처의 1K-JPG 묶음에서 *_Color.jpg 를 <ID>.jpg 로 둔 것. 순서 = 게임의 재질 번호(SURF, index.html).
# 마지막 줄에 칸별 평균색(sRGB 0..1)을 출력한다 → index.html 의 SURF_AVG 에 붙여 넣는다.

import bpy, sys, os

NAMES = ['PaintedPlaster017', 'Concrete034', 'CorrugatedSteel005', 'Metal021',
         'MetalPlates006', 'Planks037A', 'Bricks085', 'RoofingTiles006',
         'Asphalt031', 'Grass004', 'Rock053', 'Bark012',
         'ScatteredLeaves009', 'PavingStones128', 'Ground085', 'Bricks113A']
TILE, N = 512, 4

src, out = sys.argv[sys.argv.index('--') + 1:][:2]
S = TILE * N
atlas = [0.0] * (S * S * 4)
avgs = []
for i, name in enumerate(NAMES):
    img = bpy.data.images.load(os.path.join(src, name + '.jpg'))
    img.scale(TILE, TILE)
    px = list(img.pixels)
    avgs.append([round(sum(px[c::4]) / (TILE * TILE), 3) for c in range(3)])
    col, row = i % N, i // N
    y0 = (N - 1 - row) * TILE            # 블렌더 픽셀은 아래 줄부터: 0번 칸이 그림의 왼쪽 위에 오게
    for y in range(TILE):
        o = ((y0 + y) * S + col * TILE) * 4
        atlas[o:o + TILE * 4] = px[y * TILE * 4:(y + 1) * TILE * 4]
    print('TILE', i, name, avgs[-1])
im = bpy.data.images.new('atlas', S, S)
im.pixels = atlas
im.filepath_raw = out
im.file_format = 'JPEG'
bpy.context.scene.render.image_settings.quality = 82
im.save()
print('ATLAS', out, os.path.getsize(out), 'bytes')
print('AVG', avgs)
