from PIL import Image, ImageDraw
import piexif, random

def to_dms(val):
    val = abs(val)
    deg = int(val)
    min_float = (val - deg) * 60
    minute = int(min_float)
    sec = (min_float - minute) * 60
    return deg, minute, sec

def dms_to_rational(dms):
    return [(dms[0],1),(dms[1],1),(int(dms[2]*100),100)]

def make_image_with_exif(path, lat, lon, alt):
    W, H = 1200, 800
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # Sky
    for y in range(H//2):
        draw.line((0,y,W,y), fill=(30, 60 + y//4, 120 + y//6))

    # Mountains
    for i in range(6):
        base = random.randint(350, 550)
        peak = random.randint(120, 280)
        x = i * 220
        draw.polygon([(x, base), (x+240, base), (x+120, peak)], fill=(60, 60, 70))

    # Land
    draw.rectangle((0, 520, W, H), fill=(50, 110, 60))

    # Road
    draw.polygon([(540, H), (660, H), (620, 520), (580, 520)], fill=(70,70,70))

    # Sun
    draw.ellipse((900, 80, 980, 160), fill=(255, 200, 120))

    draw.text((40, 40), "Expedition Capture", fill=(255,255,255))

    lat_dms = to_dms(lat)
    lon_dms = to_dms(lon)

    exif = {"0th":{}, "Exif":{}, "GPS":{}, "1st":{}, "thumbnail":None}
    exif["GPS"][piexif.GPSIFD.GPSLatitudeRef] = "N" if lat >= 0 else "S"
    exif["GPS"][piexif.GPSIFD.GPSLongitudeRef] = "E" if lon >= 0 else "W"
    exif["GPS"][piexif.GPSIFD.GPSLatitude] = dms_to_rational(lat_dms)
    exif["GPS"][piexif.GPSIFD.GPSLongitude] = dms_to_rational(lon_dms)
    exif["GPS"][piexif.GPSIFD.GPSAltitude] = (int(alt),1)

    img.save(path, exif=piexif.dump(exif))
    img.close()