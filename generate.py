from PIL import Image,ImageDraw,ImageFont


from util import id_generator, generateimage

test = {"tier":"GOLD","rank":"IV","lp":33}



generateimage(test)

print(id_generator())   