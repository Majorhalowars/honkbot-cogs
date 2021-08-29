from PIL import Image

jar_img = Image.open("jar.png")
jar_target_img = Image.open("target.png")

w_jar, h_jar = jar_img.size

jar_target_img.thumbnail((w_jar * 0.8, h_jar * 0.8), Image.ANTIALIAS)

w_target, h_target = jar_target_img.size

jar_img.paste(jar_target_img, ((w_jar - w_target + 100) // 2, (h_jar - h_target - 100)), jar_target_img)

jar_img.show()