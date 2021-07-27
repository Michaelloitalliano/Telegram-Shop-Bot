from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django_project.telegrambot.usersmanage.models import *
from django.template import Template, Context
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import FileResponse# TEST

from django_project.telegrambot.usersmanage.models import User, Payment#, Task

import io# TEST
import os, shutil, zipfile, re

from hashlib import sha256
import base64, datetime


m_key = 'KEY'

def mk_sign(arHash):
    return sha256(":".join(arHash).encode()).hexdigest().upper()

@csrf_exempt
def pay(request):
    for param in ('amount', 'oid'):
        if not param in request.GET:
            return redirect("https://t.me/bot")
    amount = request.GET["amount"]
    m_shop = 'shop_id'
    m_orderid = request.GET["oid"]
    m_amount = f"{amount}.00"
    m_curr = "RUB"
    m_desc = base64.b64encode(b'Balance replenishment').decode("utf-8")
    arHash = m_shop,m_orderid,m_amount,m_curr,m_desc,m_key
    sign = mk_sign(arHash)
    return render(request, "pay.html", {'sign':sign, 'desc': m_desc, 'curr': m_curr, 'amount': m_amount, 'oid': m_orderid, 'shop': m_shop})


def home(request):
    return render(request, 'index.html')

@csrf_protect
def upload(request):
    answer = ""
    if request.method == 'POST' and request.FILES['archive']:
        if request.POST["pass"]!="123":
            return render(request, 'upload.html', {'answer':"\n\nОшибка: неверный пароль"})
        if not Product.objects.filter(id=request.POST["id"]).exists():
            return render(request, 'upload.html', {'answer':"\n\nОшибка: ID Товара не найден"})
        tmp_up = 'temp_upld'
        shutil.rmtree(tmp_up, ignore_errors=True)
        zipname = os.path.join(tmp_up,"up.zip")
        fs = FileSystemStorage()
        filename = fs.save(zipname, request.FILES['archive'])
        if not os.path.isdir(tmp_up):
            os.mkdir(tmp_up)
        if not os.path.isdir('logs'):
            os.mkdir('logs')
        if not zipfile.is_zipfile(zipname):
            return render(request, 'upload.html', {'answer':"\n\nОшибка: Файл не является zip-архивом"})
        # shutil.unpack_zipfile(zipname, tmp_up)
        zip = zipfile.ZipFile(zipname)
        zip.extractall(tmp_up)
        zip.close
        product = Product.objects.get(id=request.POST["id"])
        i=0
        for dirc in os.listdir(tmp_up):
            fullpath = os.path.join(tmp_up, dirc)
            if not os.path.isdir(fullpath):
                continue
            for block in ["BLOCKED_DIRS"]:
                fuck_path = os.path.join(fullpath, block)
                if os.path.isdir(fuck_path):
                    shutil.rmtree(fuck_path)
            parse_type = product.subcategory.parse_type
            dirc = dirc.replace(" ", "")
            if parse_type==1:
                clear = re.findall(r"[A-Z]{2}\[.{32}\]", dirc)
                if len(clear)==0:
                    reg = "WN"
                else:
                    reg = clear[0][:2]
            elif parse_type==2:
                found = re.findall(r"_[A-Z]{2}_123", dirc)
                if len(found)==0:
                    reg="WN"
                else:
                    reg = found[0].replace("_", "").replace("123", "")
            if product.pair_eu:
                if reg in ['LALA']:
                    subproduct = product.pair_eu
                else:
                    subproduct = product
            else:
                subproduct = product
            newpath = os.path.join('logs', str(subproduct.id), dirc)
            if not os.path.isdir(os.path.join('logs', str(subproduct.id))):
                os.mkdir(os.path.join('logs', str(subproduct.id)))
            if os.path.isdir(newpath):
                answer+=f"\nПапка \"{dirc}\" уже добавлен, пропуск."
                continue
            shutil.copytree(fullpath, newpath)
            LogLink.objects.create(link=newpath, product=subproduct, reg=reg)
            i+=1
        answer+=f"\nДобавлено {i} папок для товара {subproduct.name} (ID:{subproduct.id})"
        # return HttpResponse(page+answer)
        return render(request, 'upload.html', {'answer':answer})
    return render(request, 'upload.html', {'answer':answer})