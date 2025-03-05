import os.path
import platform

from PIL import ImageFile, Image
from django.shortcuts import render, redirect
from G import G

def html(request):
    info = G.saveHistory(request, 'gallery')
    request.session["currentPage"] = "gallery/gallery"
    if 'userAccount' not in request.session:
        return redirect("/login")
    return render(request,'gallery/gallery.html',{"info":info[1],"userAccount":G.userAccount(request)})

def thumb(request):
    info = G.saveHistory(request, '準備製作縮圖')
    request.session["currentPage"] = "/gallery/thumb"
    if 'userAccount' not in request.session:
        return redirect("/login")
    return render(request, "gallery/thumb.html",{"info":info[1],"userAccount":G.userAccount(request)})

def thumb_doing(request):
    #info=G.saveHistory(request,'開始製作縮圖')
    if platform.system()=="Linux":
        primitive_path="data/upload/primitive"
        thumb_path="/data/upload/thumb"
    else:
        primitive_path="C:/upload/primitive"
        thumb_path = "C:/upload/thumb"
    if not os.path.exists(thumb_path):
        os.makedirs(thumb_path)
    primitive=dirTree(primitive_path)
    thumb=dirTree(thumb_path)
    ImageFile.LOAD_TRUNCATED_IMAGES=True
    Image.MAX_IMAGE_PIXELS=None

    for p in primitive:
        if not p.replace('primitive','thumb') in thumb:
            target = ext2lower(p)  # 將副檔名改成小寫，不然在 Linux 下載時，jpg 會變成 jiff
            make_thumb(target)
    info = G.saveHistory(request, '縮圖製作完成')
    return render(request, "gallery/gallery.html", {"info": info[1],"userAccount":G.userAccount(request)})

def make_thumb(file):
    thumb_dir=os.path.dirname(file).replace("primitive","thumb")
    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    #使用 Pillow 會比 cv2 快很多
    pil=Image.open(file)
    pil.thumbnail((800,600))#橫圖:寬為 800, 高會等比例計算。直圖 : 高為 600, 寬會等比例計算
    file=os.path.basename(file)
    pil.save(os.path.join(thumb_dir, file))

def ext2lower(file):
    master, slave=os.path.splitext(file)
    slave=slave.lower()
    target=f"{master}{slave}"
    os.rename(file, target)
    return target

def dirTree(path):
    #一定要用 set, 速度才會快
    s=set([])
    for root, subdirs, files in os.walk(path):
        for file in files:
            lower=file.lower()
            if lower.endswith('.jpg') or lower.endswith('.png') or lower.endswith('.bmp'):
                full_path=os.path.join(root, file).replace("\\","/")
                s.add(full_path)
    return s

