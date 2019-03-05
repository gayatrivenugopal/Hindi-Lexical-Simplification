#PIL did not word, installed pyvips

'''from PIL import Image, ImageDraw, ImageFont
 
img = Image.new('RGB', (100, 30), color = (73, 109, 137))
 
d = ImageDraw.Draw(img)
font = ImageFont.truetype('mangal.ttf')
d.text((10,10), "सांस्कृतिक वैविध्य हमारी संस्कृति का सौंदर्य है और उन वैविध्यों में आंतरिक ऐक्य इसकी अनुपम अतुल्य विशिष्टता है।", fill=(255,255,0))
 
img.save('pil_text.png')'''
#Source: https://stackoverflow.com/questions/39630916/how-can-i-print-hindi-sentencesunicode-on-image-in-python
import pyvips
import os

os.chdir("T:/Research/Ph.D/Ph.D/Work/HWN API/JHWNL_1_2/Final Corpora/Manual Annotation/")


output_file = "instructions.png"
#text = "सांस्कृतिक वैविध्य हमारी संस्कृति का सौंदर्य है और उन वैविध्यों में आंतरिक ऐक्य इसकी अनुपम अतुल्य विशिष्टता है।"
MAX_W, MAX_H = 1500, 1500

'''
for i in range(1,9):
    fp = open("Block " + str(i) + "/Sentences.txt", "r", encoding="utf-8")
    line = fp.readline()
    j = 1
    while line:
        if line == "\n" or line == " ":
            line = fp.readline()
            continue
        image = pyvips.Image.text(line, width=MAX_W, height=MAX_H, font='Mangal', dpi=96)
        image.write_to_file("Block " + str(i) + " Sentence " + str(j) + ".png")
        j = j + 1
        print(f'File Written at : {"Block " + str(i) + " Sentence " + str(j-1)}')
        line = fp.readline()
'''
fp = open("Task Complete.txt", "r")
instructions = fp.read()
image = pyvips.Image.text(instructions, width=MAX_W, height=MAX_H, dpi=96)
image.write_to_file("Task Complete.png")