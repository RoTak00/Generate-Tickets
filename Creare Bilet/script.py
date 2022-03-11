from PIL import Image, ImageDraw, ImageFont
import sys

scope = str(input("g / l:\n"))
if scope == "g":
    f_list = open("listG.txt", "r", encoding = "utf-8")
else:
    f_list = open("listL.txt", "r", encoding = "utf-8")
v_list = []
while True:
    temp_el = f_list.readline().rstrip("\n").rstrip(" ").lstrip(" ")
    #print(temp_el)
    if temp_el == "":
        break
    v_list.append([x.rstrip(" ").lstrip(" ") for x in temp_el.split(",")])
    
q_quit = input("Se vor genera " + str(len(v_list)) + " imagini OK? n/other\n")
if q_quit == "n":
    print("La revedere")
    sys.exit()
    
fnt2 = ImageFont.truetype('arial.ttf', 30) 
for i in range(len(v_list)):
    img = Image.open('biletbase.jpeg')
    d = ImageDraw.Draw(img)

    fnt1size = 40
    fnt1pos = 360
    if len(v_list[i][0]) > 15:
        fnt1size -= 3
        fnt1pos += 3
    if len(v_list[i][0]) > 18:
        fnt1size -= 3
        fnt1pos += 3
    if len(v_list[i][0]) > 21:
        fnt1size -= 3
        fnt1pos += 3
    if len(v_list[i][0]) > 24:
        fnt1size -= 3
        fnt1pos += 3
    fnt1 = ImageFont.truetype('arial.ttf', fnt1size)
    d.text((615, fnt1pos), v_list[i][0].upper(), font=fnt1, fill = (255, 255, 255))
    d.text((1040, 525), "#" + v_list[i][1], font=fnt2, fill = (255, 255, 255))

    print("Se salveaza bilet " + str(v_list[i][0]) + " cod " + str(v_list[i][1]), end = "")
    print(" OK")
    if scope == "g":
        img.save("imagesG/bilet" + str(v_list[i][1]) + ".png")
    else:
        img.save("imagesL/bilet" + str(v_list[i][1]) + ".png")
