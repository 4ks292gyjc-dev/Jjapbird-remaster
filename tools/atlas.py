# 실사 재질 32가지를 8×4 아틀라스 3장으로 묶는다 (Pillow 만 있으면 됨)
#
#   python3 tools/atlas.py <재질 폴더> <출력 폴더>
#
# 재질: ambientCG (ambientcg.com) CC0 텍스처의 1K-JPG 묶음. 재질 폴더/<ID>/ 안에
#   Color.jpg, NormalGL.jpg, Roughness.jpg, (있으면) AmbientOcclusion.jpg
# 순서 = 게임의 재질 번호(SURF, index.html).
# 출력: textures.jpg(색, sRGB) · textures_n.jpg(노멀, OpenGL 방향) · textures_orm.jpg(R=AO, G=거칠기, B=금속)
# 마지막 줄에 칸별 평균색(sRGB 0..1)을 출력한다 → index.html 의 SURF_AVG 에 붙여 넣는다.
import sys, os
from PIL import Image

NAMES = ['PaintedPlaster017', 'Concrete034', 'CorrugatedSteel005', 'Metal021', 'MetalPlates006', 'Planks037A', 'Bricks085', 'RoofingTiles006',
         'Asphalt031', 'Grass004', 'Rock053', 'Bark012', 'ScatteredLeaves009', 'PavingStones128', 'Ground085', 'Bricks113A',
         'CorrugatedSteel007A', 'PaintedMetal004', 'MetalWalkway014', 'Road007', 'Rock035', 'Ground037', 'WoodFloor043', 'Fabric030',
         'Concrete046', 'Concrete047A', 'Concrete048', 'Concrete049', 'Tiles141', 'Metal055B', 'ThatchedRoof001A', 'Asphalt033']
METAL = {'CorrugatedSteel005': 0.6, 'Metal021': 0.7, 'MetalPlates006': 0.7, 'CorrugatedSteel007A': 0.5, 'PaintedMetal004': 0.3, 'MetalWalkway014': 0.7, 'Metal055B': 0.7}
TILE, COLS, ROWS = 512, 8, 4

src, out = sys.argv[1], sys.argv[2]
W, H = TILE * COLS, TILE * ROWS
col_a, nor_a, orm_a = Image.new('RGB', (W, H)), Image.new('RGB', (W, H)), Image.new('RGB', (W, H))
avgs = []
for i, name in enumerate(NAMES):
    d = os.path.join(src, name)
    load = lambda f, mode='RGB': Image.open(os.path.join(d, f)).convert(mode).resize((TILE, TILE), Image.LANCZOS)
    xy = ((i % COLS) * TILE, (i // COLS) * TILE)   # 0번 칸 = 왼쪽 위
    c = load('Color.jpg')
    col_a.paste(c, xy)
    small = c.resize((1, 1), Image.BOX).getpixel((0, 0))
    avgs.append([round(v / 255, 3) for v in small])
    nor_a.paste(load('Normal' + 'GL.jpg'), xy)
    ao = load('AmbientOcclusion.jpg', 'L') if os.path.exists(os.path.join(d, 'AmbientOcclusion.jpg')) else Image.new('L', (TILE, TILE), 255)
    metal = Image.new('L', (TILE, TILE), int(METAL.get(name, 0) * 255))
    orm_a.paste(Image.merge('RGB', (ao, load('Roughness.jpg', 'L'), metal)), xy)
    print('TILE', i, name)
col_a.save(os.path.join(out, 'textures.jpg'), quality=85)
nor_a.save(os.path.join(out, 'textures_n.jpg'), quality=90)
orm_a.save(os.path.join(out, 'textures_orm.jpg'), quality=85)
for f in ('textures.jpg', 'textures_n.jpg', 'textures_orm.jpg'): print(f, os.path.getsize(os.path.join(out, f)), 'bytes')
print('AVG', avgs)
