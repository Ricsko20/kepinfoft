import flet as ft
from PIL import Image, ImageOps, ImageEnhance
import io

def main(page: ft.Page):
    page.title = "Képkezelés Program"
    
    def kep_kivalasztasa(e):
        if file_picker.result is not None:
            kep_file = file_picker.result.files[0]
            image_path = page.get_file(kep_file.path)
            eredeti_kep.value = image_path
            metaadatok_szoveg.value = get_image_metadata(image_path)
            update_images(image_path)
            page.update()
    
    def get_image_metadata(image_path):
        img = Image.open(image_path)
        info = img.info
        metaadatok = f"Formátum: {img.format}\nMéret: {img.size}\nSzínmód: {img.mode}\n"
        for k, v in info.items():
            metaadatok += f"{k}: {v}\n"
        return metaadatok
    
    def update_images(image_path):
        img = Image.open(image_path)
        original_image.src = img
        original_image.update()
        
        red_image = ImageOps.colorize(img.convert("L"), (0,0,0), (255,0,0))
        red_image_io = io.BytesIO()
        red_image.save(red_image_io, format="PNG")
        red_image_control.src = ft.Image(src=red_image_io.getvalue())
        red_image_control.update()
        
        green_image = ImageOps.colorize(img.convert("L"), (0,0,0), (0,255,0))
        green_image_io = io.BytesIO()
        green_image.save(green_image_io, format="PNG")
        green_image_control.src = ft.Image(src=green_image_io.getvalue())
        green_image_control.update()
        
        blue_image = ImageOps.colorize(img.convert("L"), (0,0,0), (0,0,255))
        blue_image_io = io.BytesIO()
        blue_image.save(blue_image_io, format="PNG")
        blue_image_control.src = ft.Image(src=blue_image_io.getvalue())
        blue_image_control.update()
    
    def kep_atmeretezese(e):
        if eredeti_kep.value:
            img = Image.open(eredeti_kep.value)
            szelesseg = int(atmeretezes_szelesseg.value)
            magassag = int(atmeretezes_magassag.value)
            img_resized = img.resize((szelesseg, magassag))
            img_resized_io = io.BytesIO()
            img_resized.save(img_resized_io, format="PNG")
            resized_image_control.src = img_resized_io.getvalue()
            resized_image_control.update()

    file_picker = ft.FilePicker(on_result=kep_kivalasztasa)
    eredeti_kep = ft.Text(value="")
    metaadatok_szoveg = ft.Text(value="")
    
    atmeretezes_szelesseg = ft.TextField(label="Szélesség", value="100")
    atmeretezes_magassag = ft.TextField(label="Magasság", value="100")
    atmeretezes_gomb = ft.ElevatedButton(text="Átméretezés", on_click=kep_atmeretezese)
    resized_image_control = ft.Image()
    
    original_image = ft.Image()
    red_image_control = ft.Image()
    green_image_control = ft.Image()
    blue_image_control = ft.Image()
    
    page.add(
        ft.Row(controls=[file_picker, ft.ElevatedButton(text="Kép kiválasztása", on_click=lambda e: file_picker.pick_files(allow_multiple=False))]),
        metaadatok_szoveg,
        original_image,
        ft.Row(controls=[red_image_control, green_image_control, blue_image_control]),
        ft.Row(controls=[atmeretezes_szelesseg, atmeretezes_magassag, atmeretezes_gomb]),
        resized_image_control
    )

ft.app(target=main)
