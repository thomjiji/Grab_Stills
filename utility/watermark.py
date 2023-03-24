from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import argparse

def watermark_to_jpg(jpg_file_path:str,output_path:str,scene_text:str):
    # settings
    source = jpg_file_path # source image file
    target = output_path # target image file
    text = "服装组专阅" # text to write
    scene_text=scene_text
    font = ImageFont.truetype("PingFang.ttc", 220) # font and size
    scene_font=ImageFont.truetype("PingFang.ttc", 50)
    color = (255, 255, 255,30) # text color
    scene_color = (255, 255, 255,200) # text color
    angle = 35 # rotation angle in degrees
    # open source image and convert it to RGBA mode
    img = Image.open(source).convert("RGB")

    # create a new transparent image for text watermark
    txt_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
    scene_txt_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
    # get a drawing context for text watermark
    draw_text = ImageDraw.Draw(txt_img)
    draw_scene=ImageDraw.Draw(scene_txt_img)
    # get size of text watermark
    text_width, text_height = draw_text.textsize(text, font)
    # print(f'{text_width}x{text_height}')

    #print(f'{text_width}x{text_height}')
    # calculate center coordinates of image
    center_x = (img.width - text_width) // 2 
    center_y = (img.height - text_height) // 2

    # adjust center coordinates according to rotation angle 
    offset_x = int(text_height * math.sin(math.radians(angle)) / 2)
    offset_y = int(text_height * math.cos(math.radians(angle)) / 2)
    center_x -= offset_x 
    center_y -= offset_y

    # draw text watermark on new transparent image with center coordinates 
    draw_text.text((center_x , center_y), text=text , fill=color , font=font)
    draw_scene.text([10,img.height-70], text=scene_text , fill=scene_color , font=scene_font)

    # rotate text watermark by angle degrees 
    txt_img = txt_img.rotate(angle)

    # paste text watermark on source image with alpha channel 
    img.paste(txt_img , (0 ,0), txt_img)
    img.paste(scene_txt_img,(0 ,0),scene_txt_img)

    # save target image file 
    img.save(target)

if __name__ == "__main__":
    paser=argparse.ArgumentParser("add watermark to jpg file for 802302 toDressing ")
    paser.add_argument('-p',required=True,help='path for jpg file')
    paser.add_argument('-o',required=True,help='output path for jpg file')
    paser.add_argument('-sc',required=True,help='scene name(str) for watermark')
    args=paser.parse_args()
    watermark_to_jpg(jpg_file_path=args.p,output_path=args.o,scene_text=args.sc)