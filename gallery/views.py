import json
import math
import os
import platform
from PIL import ImageFile, Image
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from G import G


tree=""
thumb_path=""
def html(request):
    global thumb_path, tree
    info=G.saveHistory(request,'gallery')
    request.session["currentPage"]="/gallery"
    if 'userAccount' not in request.session:
        return redirect("/login")
    if platform.system()=="Linux":
        thumb_path="/data/upload/thumb/"
    else:
        thumb_path = "C:/upload/thumb/"
    root=os.listdir(thumb_path)
    root.sort(reverse=True)
    tree="<ul>"
    for path in root:
        full=os.path.join(thumb_path, path)
        if os.path.isdir(full):
            txt=full.replace(thumb_path, "").replace("\\","/")
            tree +=f"""
                <li>
                    <a href='javascript:void(0)' onclick='loadThumb("{txt}");'>
                        {txt}
                    </a>
                </li>
            """
            listDir(full)
    tree +="</ul>"

    return render(
        request,
        "gallery/gallery.html",
        {"list_dir":mark_safe(tree),"info":info[1],"userAccount":G.userAccount(request)})

def listDir(path):
    global tree
    tree +="<ul>"
    files=os.listdir(path)
    files.sort(reverse=True)
    for file in files:
        full=os.path.join(path, file).replace("\\","/")
        if os.path.isdir(full):
            txt=full.replace(path,"").replace("/","")
            url=full.replace(thumb_path,"")
            tree += f"""
                <li>
                    <a href='javascript:void(0)' onclick='loadThumb("{url}");'>
                        {txt}
                    </a>
                </li>
            """
            listDir(full)
    tree +="</ul>"
def thumb(request):
    info=G.saveHistory(request,'準備製作縮圖')
    request.session["currentPage"]="/gallery/thumb"
    if 'userAccount' not in request.session:
        return redirect("/login")
    return render(request, "gallery/thumb.html",
                  {"info":info[1],"userAccount":G.userAccount(request)}
                  )
def thumb_doing(request):
    if platform.system()=="Linux":
        primitive_path="/data/upload/primitive"
        thumb_path="/data/upload/thumb"
    else:
        primitive_path="C:/upload/primitive"
        thumb_path="C:/upload/thumb"
    if not os.path.exists(thumb_path):
        os.makedirs(thumb_path)
    primitive=dirTree(primitive_path)
    thumb=dirTree(thumb_path)

    #pip install Pillow
    #底下設定是解決圖片太大出現 "exceeds limit of 178956970 pixels, could be decompression" 的例外
    ImageFile.LOAD_TRUNCATED_IMAGES=True
    Image.MAX_IMAGE_PIXELS=None

    #primitive : "d:/upload/primitive/2003/20231109/1.jpg"
    #thumb     :"d:/upload/thumb/2003/20231109/1.jpg"
    #底下那一張圖會被先製作，不知道，因為 set 是無序的
    for p in primitive:
        if not p.replace('primitive','thumb') in thumb:
            target=ext2lower(p)#將副檔名改成小寫，不然在 Linux 下載時，jpg 會變成 jiff
            make_thumb(target)
    info=G.saveHistory(request,'縮圖製作完成')
    return render(request, "gallery/gallery.html",
                  {"info":info[1],"userAccount":G.userAccount(request)}
                  )
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

def listThumbDir(request):
    if platform.system() == "Linux":
        path="/data/upload/thumb"
    else:
        path="C:/upload/thumb"
    if 'dir' in request.GET:
        dir=request.GET["dir"]
    else:
        dir=''
    full=os.path.join(path,dir)
    files=os.listdir(full)
    files.sort()#因為 Linux 不會自動排序
    files=[f'{dir}/{file}'
        for file in files if os.path.isfile(os.path.join(path, dir, file))
    ]
    print(files)
    total=len(files)
    txt=""
    for i in range(math.ceil(total/5)):
        txt +="<div style='display:flex;'>"
        for j in range(5):
            if i * 5 + j < total:
                file=files[i * 5 + j]
                txt +=f"""
                <div class='with_img'>
                    <a href='javascript:void(0)' onclick='showPrimitive({i*5+j});'>
                        <img class ='img_thumb' src='/pictures/thumb/{file}'/>
                    </a>
                </div>
                """
            else:
                txt += "<div class='without_img'></div>"
        txt += '</div>'
    return HttpResponse(
        json.dumps(
            {'url':mark_safe(txt),'files':','.join(files)}
        ),
        content_type='application/json'
    )

