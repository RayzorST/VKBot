from PIL import Image, ImageDraw, ImageFont

from models.sector import SectorModel

def new_map():
    sectors = SectorModel().select()
    map=Image.new("RGB", (400, 400), (124, 37, 157))
    draw=ImageDraw.Draw(map)
    coords_x=[]
    coords_y=[]
    for coord in sectors:
        coords_x.append(coord.x)
        coords_y.append(coord.y)
    min_x=min(coords_x)
    max_x=max(coords_x)
    min_y=min(coords_y)
    max_y=max(coords_y)
    count_x=len(list(range(max_x-min_x)))
    count_y=len(list(range(max_y-min_y)))
    count=max(count_x, count_y)
    size=map.height/(count*2.5)
    center_x=map.height/2-count_x*size
    center_y=map.width/2+count_y*size
    font=ImageFont.truetype("assets/fonts/ozda.ttf", size=count)
    for sector in sectors:
        x1=sector.x*size*2-size
        y1=(sector.y*size*2-size)*-1
        x2=sector.x*size*2+size
        y2=(sector.y*size*2+size)*-1
        draw.rectangle([(center_x+x1, center_y+y1), (center_x+x2, center_y+y2)], outline="white", fill=(sector.owner.red, sector.owner.green, sector.owner.blue, 40) if sector.owner is not None else None)
        draw.text([center_x+x1+5, center_y+y2+5], sector.name, font=font)
    map.save("assets/other/map.png")