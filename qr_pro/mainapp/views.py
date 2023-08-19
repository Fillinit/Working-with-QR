import PyPDF2, math, os, json, win32print, win32api
from reportlab.lib.pagesizes import portrait, landscape
from reportlab.lib.units import mm
from django.conf import settings

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import marking_Info, pack_master_Info, package_Info, product_Info
from reportlab.pdfgen import canvas
from barcode import get_barcode_class, Code128
from barcode.writer import ImageWriter

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST


def index(request):
    template = "mainapp/index.html"
    return render(request, template)


def orders(request):
    template = "mainapp/orders.html"
    mark_Info = marking_Info.objects.all()
    context = {
        'mark_Info': mark_Info,
        'info': []
    }

    for marking_iter in mark_Info:
        pm_Info = pack_master_Info.objects.all().filter(marking=marking_iter)
        p_Info = package_Info.objects.all().filter(marking=marking_iter)
        pro_Info = product_Info.objects.all().filter(marking=marking_iter)
        Temporary_Dict = {"markingId": marking_iter.id,
                          'vu': len(p_Info),
                          'zu': len(package_Info.objects.all().filter(marking=marking_iter, status=1)),
                          'pu': len(package_Info.objects.all().filter(marking=marking_iter, status=0)),
                          'nu': len(package_Info.objects.all().filter(marking=marking_iter, status=2)),
                          'vmu': len(pm_Info),
                          'zmu': len(pack_master_Info.objects.all().filter(marking=marking_iter, status=1)),
                          'pmu': len(pack_master_Info.objects.all().filter(marking=marking_iter, status=0)),
                          'nmu': len(pack_master_Info.objects.all().filter(marking=marking_iter, status=2)), }
        context['info'].append(Temporary_Dict)

    return render(request, template, context)


def orders_more(request, orders_id):
    template = "mainapp/orders_more.html"
    mark_Info = marking_Info.objects.get(id=orders_id)
    pm_Info = pack_master_Info.objects.all().filter(marking=mark_Info)
    p_Info = package_Info.objects.all().filter(marking=mark_Info)
    context = {
        'mark_Info': mark_Info,
        'pm_Info': pm_Info,
        'p_Info': p_Info,
        'vu': len(p_Info),
        'zu': len(package_Info.objects.all().filter(marking=mark_Info, status=1)),
        'pu': len(package_Info.objects.all().filter(marking=mark_Info, status=0)),
        'nu': len(package_Info.objects.all().filter(marking=mark_Info, status=2)),
        'vmu': len(pm_Info),
        'zmu': len(pack_master_Info.objects.all().filter(marking=mark_Info, status=1)),
        'pmu': len(pack_master_Info.objects.all().filter(marking=mark_Info, status=0)),
        'nmu': len(pack_master_Info.objects.all().filter(marking=mark_Info, status=2)),
        'v_art': '',
        "tasks": [],
        "marking": [],
        "sscc_info": [],
        "master_packaging": [],
    }
    for pm_iter in pm_Info:
        gtin = str(pm_iter.gtin).split("=")[0]
        master_pack_len = len(pack_master_Info.objects.all().filter(marking=mark_Info, gtin__icontains=gtin))
        product_count = len(product_Info.objects.all().filter(marking=mark_Info, pack_mast=pm_iter))
        for n in range(int(pm_iter.container_pm)):
            if context['tasks']:
                if gtin == context['tasks'][-1]["gtin"]:
                    continue
                else:
                    Temporary_Dict = {
                        'name_1': gtin,
                        'gtin': gtin,
                        'name_2': mark_Info.name,
                        'container_1': pm_iter.container_p,
                        'count_1': master_pack_len * int(pm_iter.container_pm),
                        'container_2': pm_iter.container_pm,
                        'count': product_count * master_pack_len,
                        'master_pack': master_pack_len,
                        'count_master_pack': product_count}
                    context['tasks'].append(Temporary_Dict)
            else:
                Temporary_Dict = {
                    'name_1': gtin,
                    'gtin': gtin,
                    'name_2': mark_Info.name,
                    'container_1': pm_iter.container_p,
                    'count_1': master_pack_len * int(pm_iter.container_pm),
                    'container_2': pm_iter.container_pm,
                    'count': product_count * master_pack_len,
                    'master_pack': master_pack_len,
                    'count_master_pack': product_count}
                context['tasks'].append(Temporary_Dict)

            if context['marking']:
                product_count = len(product_Info.objects.all().filter(marking=mark_Info))

                if gtin == context['marking'][-1]["gtin"]:
                    continue
                else:
                    Temporary_Dict = {'file_name': f'{gtin}.pdf',
                                      'art': pm_iter.articul,
                                      'name': mark_Info.name,
                                      'count': int(pm_iter.container_p) * int(pm_iter.container_pm) * master_pack_len,
                                      'gtin': gtin,
                                      'print_1': 0,
                                      }
                    context['marking'].append(Temporary_Dict)
            else:
                Temporary_Dict = {'file_name': f'{gtin}.pdf',
                                  'art': pm_iter.articul,
                                  'name': mark_Info.name,
                                  'count': int(pm_iter.container_p) * int(pm_iter.container_pm) * master_pack_len,
                                  'gtin': gtin,
                                  'print_1': 0}
                context['marking'].append(Temporary_Dict)

        pm_instance = pack_master_Info.objects.get(pk=pm_iter.id)
        related_packages = pm_instance.package_info_set.all()

        for p_iter in related_packages:
            Temporary_Dict = {'file_name': f'{p_iter.file_name}',
                              'id': p_iter.id,
                              'spec': gtin,
                              'sscc': p_iter.gtin,
                              'count': int(pm_iter.container_p),
                              'difference': 0}

            context['sscc_info'].append(Temporary_Dict)

        Temporary_Dict = {'file_name': pm_iter.file_name,
                          'spec': f"Мастер {gtin}",
                          'gtin': gtin,
                          'sscc': pm_iter.gtin,
                          'count': int(pm_iter.container_pm),
                          'difference': 0}
        context['master_packaging'].append(Temporary_Dict)

        context['v_art'] = len(context['master_packaging'])

    return render(request, template, context)


def orders_add(request):
    template = "mainapp/add_order.html"
    all_marks = marking_Info.objects.all()
    context = {'marks': all_marks}
    return render(request, template, context)


def distribute_items(number_pm, number_p, num_pages):
    count_pac = number_pm * number_p
    items_per_pack = math.ceil(num_pages / count_pac)

    packs = [items_per_pack] * count_pac
    remaining_items = count_pac * items_per_pack - num_pages
    for i in range(remaining_items):
        packs[i] -= 1

    return packs


def orders_save(request):
    if request.method == "POST":
        name_mark_drop = request.POST['dropdown']
        name_mark_inp = request.POST['name_marking']
        gtin_code_inp = request.POST['gtin_code']
        articul_inp = request.POST['articul']
        weight_inp = request.POST['weight']
        size_inp = request.POST['size']
        color_inp = request.POST['color']
        inn_inp = request.POST['inn']

        words = str(request.POST['Importer']).split()
        middle = len(words) // 2
        Importer_inp_1 = ' '.join(words[:middle])
        Importer_inp_2 = ' '.join(words[middle:])

        contract_request = request.POST['contract']
        comment_request = request.POST['comment']
        number_pm = int(request.POST['number_packing_master'])
        number_p = int(request.POST['number_packing'])
        uploaded_file = request.FILES['file_input']
        date = datetime.now().date()
        is_new = True

        if uploaded_file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)

            num_pages = len(pdf_reader.pages)
            page_num = 0
            pack_num = 0
            items_in_pack = distribute_items(number_pm, number_p, num_pages)

            if name_mark_drop != "New":
                name_mark_inp = name_mark_drop
                is_new = False
            if is_new:
                marking_obj = marking_Info(
                    name=name_mark_inp,
                    contract=contract_request,
                    comment=comment_request)
                marking_obj.save()
            else:
                marking_obj = marking_Info.objects.get(name=name_mark_inp)

            barcode_generator_packaging_wizard(name_file=f"Marking__{gtin_code_inp}_", barcode1=gtin_code_inp,
                                               barcode3=gtin_code_inp, count=number_pm, date=date, size=size_inp,
                                               art=articul_inp, name_pack=name_mark_inp, weight=weight_inp,
                                               color=color_inp, inn=inn_inp,
                                               Importer_1=Importer_inp_1, Importer_2=Importer_inp_2)

            for pm in range(number_pm):
                pack_master_obj = pack_master_Info(
                    marking=marking_obj,
                    contract=contract_request,
                    articul=articul_inp,
                    gtin=f'{gtin_code_inp}={pm}',
                    size=size_inp,
                    weight=weight_inp,
                    color=color_inp,
                    inn=inn_inp,
                    Importer_info=request.POST['Importer'],
                    container_pm=number_p,
                    container_p=items_in_pack[0],
                    file_name=""
                )
                pack_master_obj.save()

                pack_master_obj.file_name = f"MasterPackaging__{gtin_code_inp}__{pack_master_obj.id}.pdf"
                pack_master_obj.save()

                barcode_generator_packaging_wizard(name_file=f"MasterPackaging__{gtin_code_inp}__{pack_master_obj.id}",
                                                   barcode1=f"{gtin_code_inp}__{pack_master_obj.id}",
                                                   barcode3=gtin_code_inp, count=number_p, date=date,
                                                   size=size_inp, art=articul_inp, name_pack=name_mark_inp,
                                                   weight=weight_inp, color=color_inp, inn=inn_inp,
                                                   Importer_1=Importer_inp_1, Importer_2=Importer_inp_2)

                for p in range(number_p):
                    package_obj = package_Info(
                        marking=marking_obj,
                        pack_mast=pack_master_obj,
                        gtin=f'{gtin_code_inp}={pm * 3 + p + 1}',
                        contract=contract_request,
                        file_name=''
                    )
                    package_obj.save()
                    package_obj.file_name = f"Package__{gtin_code_inp}__{package_obj.id}.pdf"
                    package_obj.save()

                    items_in_current_pack = items_in_pack[pack_num]
                    barcode_generator_packaging(name_file=f"Package__{gtin_code_inp}__{package_obj.id}",
                                                barcode=gtin_code_inp, barcode2=f'{gtin_code_inp}__{package_obj.id}',
                                                count=items_in_current_pack, size=size_inp,
                                                art=articul_inp, name_pack=name_mark_inp, weight=weight_inp)
                    pack_num += 1
                    for item in range(items_in_current_pack):
                        print('page_num', page_num)
                        if page_num < num_pages:
                            page = pdf_reader.pages[page_num]
                            page_text = page.extract_text()

                            found = False
                            result = ""
                            for line in page_text.split('\n'):
                                if gtin_code_inp in line:
                                    found = True
                                    result = line
                                elif found:
                                    result += " " + line

                            product_obj = product_Info(
                                marking=marking_obj,
                                pack_mast=pack_master_obj,
                                package=package_obj,
                                gtin=str(result).replace("(", "").replace(")", "").replace(" ", ""),
                            )
                            product_obj.save()
                            page_num += 1

            base_dir = settings.BASE_DIR
            pdf_path = os.path.join(base_dir, 'static/pdf')

            if not os.path.exists(pdf_path):
                os.makedirs(pdf_path)

            new_file_name = f'{gtin_code_inp}.pdf'  # Замените на нужное имя файла

            # Получаем полный путь для сохранения файла с новым именем
            file_path = os.path.join(pdf_path, new_file_name)

            # Сохраняем файл на диск
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

    return redirect('mainapp:orders')


def packaging(request):
    template = "mainapp/packaging.html"
    pack_Info = package_Info.objects.all()
    context = {
        'pack_Info': pack_Info,
        'info': []
    }
    for package_iter in pack_Info:
        count_scan = product_Info.objects.filter(package=package_iter, status=True)
        Temporary_Dict = {'id': package_iter.id,
                          'sscc': package_iter.gtin,
                          'n_z': package_iter.id,
                          'comment': package_iter.marking.comment,
                          'count': package_iter.products.count(),
                          'count_scan': len(count_scan),
                          'contract': package_iter.contract}
        context['info'].append(Temporary_Dict)

    return render(request, template, context)


def pack_more(request, pack_id):
    template = "mainapp/pack_more.html"
    pack_Info = package_Info.objects.get(id=pack_id)
    packs_Info = package_Info.objects.all().filter(marking=pack_Info.marking)
    productAll = product_Info.objects.all().filter(package=pack_Info)
    context = {
        "pack_Info": pack_Info,
        "parents": pack_Info.marking,
        'count': len(product_Info.objects.all().filter(package=pack_Info)),
        'Scan_count': len(product_Info.objects.all().filter(package=pack_Info, status=True)),
        'codeMark': [],
        'Package': [],
    }
    for product in productAll:
        Temporary_Dict = {
            'SGTIN': product.gtin,
            'name': product.marking.name,
            'status': product.status
        }
        context['codeMark'].append(Temporary_Dict)
    for packs in packs_Info:
        Temporary_Dict = {
            'id': packs.id,
            'SSCC': packs.gtin,
            'count': len(product_Info.objects.all().filter(package=packs)),
            'difference': len(product_Info.objects.all().filter(package=packs, status=False)),
        }
        context['Package'].append(Temporary_Dict)
    return render(request, template, context)


@csrf_protect
@require_POST
def scan_pack(request):
    data = json.loads(request.body)
    barcode_value = data.get('barcodeValue')
    pack_id = int(str(barcode_value).split("__")[1])
    pack_Info = package_Info.objects.get(id=pack_id)

    context = {
        "pack_Info": {"id": pack_Info.id},
        'count': len(product_Info.objects.all().filter(package=pack_Info, status=False)),
        'Scan_count': len(product_Info.objects.all().filter(package=pack_Info, status=True))
    }

    return JsonResponse(context)


@csrf_protect
@require_POST
def scan_pro_pack(request):
    data = json.loads(request.body)
    barcode_value = data.get('barcodeValue')
    barcode_without_brackets = str(barcode_value).replace("(", "").replace(")", "")
    pack_id = data.get('pack_id')

    product_info_pack = product_Info.objects.filter(gtin=barcode_without_brackets, package__gtin=pack_id).first()

    if product_info_pack is not None:
        product_info_pack.status = True
        product_info_pack.save()
    else:
        print("No package_Info object found with the specified gtin.")

    products_in_pack_F = len(product_Info.objects.filter(package__gtin=pack_id, status=False))
    products_in_pack = len(product_Info.objects.filter(package__gtin=pack_id, ))
    pack_info = package_Info.objects.filter(gtin=pack_id).first()
    if products_in_pack_F == 0:
        if pack_info is not None:
            pack_info.status = '1'
            pack_info.save()
        else:
            print("No package_Info object found with the specified gtin.")
    elif products_in_pack_F != 0 and products_in_pack_F != products_in_pack:
        if pack_info is not None:
            pack_info.status = '2'
            pack_info.save()
        else:
            print("No package_Info object found with the specified gtin.")

    pack_obj = package_Info.objects.filter(gtin=pack_id).first()
    pack_in_pm_F = len(package_Info.objects.filter(pack_mast=pack_obj.pack_mast, status=0))
    pack_in_pm = len(package_Info.objects.filter(pack_mast=pack_obj.pack_mast))

    pack_info = package_Info.objects.filter(gtin=pack_id).first()
    pm_obj = pack_info.pack_mast
    if pack_in_pm_F == 0:
        if pm_obj is not None:
            pm_obj.status = '1'
            pm_obj.save()
        else:
            print("No package_Info object found with the specified gtin.")
    elif pack_in_pm_F != 0 and pack_in_pm_F != pack_in_pm:
        if pm_obj is not None:
            pm_obj.status = '2'
            pm_obj.save()
        else:
            print("No package_Info object found with the specified gtin.")

    new_scan_count = len(product_Info.objects.filter(package__gtin=pack_id, status=True))
    new_difference = len(product_Info.objects.filter(package__gtin=pack_id, status=False))
    context = {
        "Scan_count": new_scan_count,
        'New_difference': new_difference
    }

    return JsonResponse(context)


def operations(request):
    template = "mainapp/operations.html"
    mark_Info = marking_Info.objects.all()
    context = {
        'mark_Info': mark_Info,
        'info': []
    }
    for marking_iter in mark_Info:
        pm_Info = pack_master_Info.objects.all().filter(marking=marking_iter)
        p_Info = package_Info.objects.all().filter(marking=marking_iter)
        pro_Info = product_Info.objects.all().filter(marking=marking_iter)
        Temporary_Dict = {"markingId": marking_iter.id,
                          'vu': len(p_Info),
                          'zu': len(package_Info.objects.all().filter(marking=marking_iter, status=1)),
                          'pu': len(package_Info.objects.all().filter(marking=marking_iter, status=0)),
                          'nu': len(package_Info.objects.all().filter(marking=marking_iter, status=2)),
                          'vmu': len(pm_Info),
                          'zmu': len(pack_master_Info.objects.all().filter(marking=marking_iter, status=1)),
                          'pmu': len(pack_master_Info.objects.all().filter(marking=marking_iter, status=0)),
                          'nmu': len(pack_master_Info.objects.all().filter(marking=marking_iter, status=2)), }
        context['info'].append(Temporary_Dict)

    return render(request, template, context)


def operations_more(request, operation_id):
    template = "mainapp/operations_more.html"
    marking = marking_Info.objects.filter(id=operation_id).first()
    context = {
        'marking': marking,
        'codeM_Info': [],
        'pack_Info': [],
        'product_Info': [],
    }
    pack_master_list = pack_master_Info.objects.all().filter(marking__id=operation_id)
    for p_m_info in pack_master_list:
        Temporary_Dict = {'specif': str(p_m_info.gtin).split('=')[0],
                          "gtin": p_m_info.gtin,
                          'artic': p_m_info.articul,
                          'count_specif': len(package_Info.objects.all().filter(pack_mast=p_m_info)),
                          'not_scan_count_specif': len(
                              package_Info.objects.filter(pack_mast=p_m_info).exclude(status=1).all())
                          }
        context['codeM_Info'].append(Temporary_Dict)

    pack_list = package_Info.objects.all().filter(marking__id=operation_id)
    for p_info in pack_list:
        Temporary_Dict = {'specif': str(p_info.pack_mast.gtin).split('=')[0],
                          "sscc": p_info.gtin,
                          'artic': p_info.pack_mast.articul,
                          'count_specif': len(product_Info.objects.all().filter(package=p_info)),
                          'not_scan_count_specif': len(
                              product_Info.objects.filter(package=p_info, status=0).all())
                          }
        context['pack_Info'].append(Temporary_Dict)

    product_list = product_Info.objects.all().filter(marking__id=operation_id)
    for p_info in product_list:
        Temporary_Dict = {'specif': str(p_info.pack_mast.gtin).split('=')[0],
                          "sscc": p_info.package.gtin,
                          'artic': p_info.pack_mast.articul,
                          'sgtin': p_info.gtin,
                          }
        context['product_Info'].append(Temporary_Dict)

    return render(request, template, context)


def marking_codes(request):
    template = "mainapp/marking_codes.html"
    return render(request, template)


@csrf_protect
@require_POST
def scanMarkCodes(request):
    data = json.loads(request.body)
    barcode_value = str(data.get('barcodeValue')).replace("(", "").replace(")", "").replace(" ", "")
    product = product_Info.objects.filter(gtin=barcode_value).first()
    if product:
        context = {
            "pack_Info": {"id": product.package.id},
        }
        return JsonResponse(context)
    else:
        pass  # send status 100


def barcode_generator_img(id_barcode):
    ean = get_barcode_class('ean13')
    ean_code = ean(id_barcode, writer=ImageWriter())

    img_folder = os.path.join(os.getcwd(), "static/img")
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    file_name = f'{id_barcode}'
    image_path = os.path.join(img_folder, file_name)
    ean_code.save(image_path)


def barcode_generator_img_2(id_barcode):
    img_folder = os.path.join(os.getcwd(), "static/img")
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
    code128 = Code128(id_barcode, writer=ImageWriter())
    img_path = os.path.join(img_folder, f"{id_barcode}")
    code128.save(img_path)


def barcode_generator_packaging_wizard(name_file, barcode1, barcode3, count, date, size, art, name_pack,
                                       weight, color, inn, Importer_1, Importer_2):
    base_dir = settings.BASE_DIR
    pdf_folder = os.path.join(base_dir, 'static/pdf')
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    pdf_path = os.path.join(pdf_folder, f"{name_file}.pdf")

    barcode_generator_img_2(barcode1)
    barcode_generator_img(barcode3)

    pdf = canvas.Canvas(pdf_path, pagesize=portrait((150 * mm, 100 * mm)))
    pdfmetrics.registerFont(TTFont("TimesNewRoman", "times.ttf"))

    pdf.setFont("TimesNewRoman", 14)
    pdf.drawString(5 * mm, 143 * mm, f"{name_pack} {art} {size}")
    pdf.drawString(5 * mm, 138 * mm, f"{weight}, {color}")

    pdf.setFont("TimesNewRoman", 8)
    pdf.drawString(5 * mm, 130 * mm, "Изготовитель: ООО «SAM RAFOAT TEKSTIL». 140319, Узбекистан,")
    pdf.drawString(5 * mm, 127 * mm, "Самаркандская область, Самаркандский район, Село Конигил")

    pdf.drawString(5 * mm, 120 * mm, f"Импортер: {Importer_1}")
    pdf.drawString(5 * mm, 117 * mm, f"д.{Importer_2} ИНН {inn}")

    pdf.drawString(5 * mm, 110 * mm, "Сделано в Узбекистане (Республике Узбекистан).")

    image_path = os.path.join(base_dir, 'static/img', f'{barcode3}.png')
    pdf.drawImage(image_path, 30 * mm, 93 * mm, width=40 * mm, height=15 * mm)

    pdf.setFont("TimesNewRoman", 14)
    pdf.drawString(5 * mm, 88 * mm, f"Кол-во: {count} шт.")

    pdf.setFont("TimesNewRoman", 8)
    pdf.drawString(5 * mm, 81 * mm, "Брутто вес, кг: _____________ Нетто вес, кг: ______________")
    pdf.drawString(5 * mm, 74 * mm, "Номер партии соответствует дате изготовления.")
    pdf.drawString(5 * mm, 71 * mm, "Срок годности не ограничен.")
    pdf.drawString(5 * mm, 68 * mm, f"Дата изготовления: {date}")

    pdf.drawString(5 * mm, 63 * mm, "TP TC 017/2011")
    image_path_1 = os.path.join(base_dir, 'static/img', '1.jpg')
    image_path_2 = os.path.join(base_dir, 'static/img', '2.jpg')
    image_path_3 = os.path.join(base_dir, 'static/img', '3.jpg')
    image_path_4 = os.path.join(base_dir, 'static/img', '4.jpg')
    image_path_5 = os.path.join(base_dir, 'static/img', '5.jpg')
    image_path_6 = os.path.join(base_dir, 'static/img', '6.jpg')
    pdf.drawImage(image_path_1, 30 * mm, 62 * mm, width=5 * mm, height=5 * mm, mask="auto")
    pdf.drawImage(image_path_2, 35 * mm, 62 * mm, width=5 * mm, height=5 * mm, mask="auto")
    pdf.drawImage(image_path_3, 40 * mm, 62 * mm, width=5 * mm, height=5 * mm, mask="auto")
    pdf.drawImage(image_path_4, 45 * mm, 62 * mm, width=5 * mm, height=5 * mm, mask="auto")
    pdf.drawImage(image_path_5, 50 * mm, 62 * mm, width=5 * mm, height=5 * mm, mask="auto")
    pdf.drawImage(image_path_6, 55 * mm, 62 * mm, width=5 * mm, height=5 * mm, mask="auto")

    image_path = os.path.join(base_dir, 'static/img', f'{barcode1}.png')
    pdf.drawImage(image_path, 30 * mm, 46 * mm, width=40 * mm, height=15 * mm)

    pdf.setFont("TimesNewRoman", 12)
    pdf.drawString(5 * mm, 41 * mm, f"GTIN: {barcode3} Размер: {size}+-2см")
    pdf.drawString(5 * mm, 36 * mm, f"Цвет: {color}")

    pdf.setFont("TimesNewRoman", 8)
    pdf.drawString(5 * mm, 29 * mm, f"Наименование: {name_pack},")
    pdf.drawString(5 * mm, 25 * mm, f"{art}, {size}, {weight}")

    pdf.setFont("TimesNewRoman", 12)
    pdf.drawString(5 * mm, 18 * mm, f"Артикул:{art}")
    pdf.drawString(45 * mm, 18 * mm, f"Цвет: {color}")

    image_path = os.path.join(base_dir, 'static/img', f'{barcode3}.png')
    pdf.drawImage(image_path, 30 * mm, 2 * mm, width=40 * mm, height=15 * mm)

    pdf.save()

    image_path1 = os.path.join(base_dir, 'static/img', f'{barcode1}.png')
    image_path3 = os.path.join(base_dir, 'static/img', f'{barcode3}.png')
    if os.path.exists(image_path1):
        os.remove(image_path1)
    if os.path.exists(image_path3):
        os.remove(image_path3)


def barcode_generator_packaging(name_file, barcode, barcode2, count, size, art, name_pack, weight):
    barcode_generator_img(barcode)
    barcode_generator_img_2(barcode2)

    base_dir = settings.BASE_DIR
    pdf_folder = os.path.join(base_dir, 'static/pdf')
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    pdf_path = os.path.join(pdf_folder, f"{name_file}.pdf")

    pdf = canvas.Canvas(pdf_path, pagesize=landscape((100 * mm, 50 * mm)))

    pdfmetrics.registerFont(TTFont("TimesNewRoman", "times.ttf"))

    image_path = os.path.join(base_dir, 'static/img', f'{barcode2}.png')
    pdf.drawImage(image_path, 25 * mm, 36 * mm, width=50 * mm, height=12 * mm)
    pdf.setFont("TimesNewRoman", 8)
    pdf.drawString(5 * mm, 33 * mm, f"Наименование: {name_pack}, {art}, {size},")
    pdf.drawString(5 * mm, 29 * mm, f"{weight} Состав: 100% хлопок, Размер: {size}")
    pdf.drawString(5 * mm, 25 * mm, "Вся необходимая информация указана на картонном ярлыке")
    pdf.drawString(5 * mm, 21 * mm, f"Кол-во: {count} шт.")
    pdf.drawString(5 * mm, 17 * mm, f"Размер: {size} GTIN: {barcode} ")
    pdf.drawString(5 * mm, 13 * mm, "TP TC 017/2011")

    image_path_1 = os.path.join(base_dir, 'static/img', '1.jpg')
    image_path_2 = os.path.join(base_dir, 'static/img', '5.jpg')
    pdf.drawImage(image_path_1, 30 * mm, 12 * mm, width=4 * mm, height=4 * mm, mask="auto")
    pdf.drawImage(image_path_2, 35 * mm, 12 * mm, width=4 * mm, height=4 * mm, mask="auto")

    image_path = os.path.join(base_dir, 'static/img', f'{barcode}.png')
    pdf.drawImage(image_path, 30 * mm, 1 * mm, width=40 * mm, height=11 * mm)

    pdf.save()

    image_path_1 = os.path.join(base_dir, 'static/img', f'{barcode}.png')
    image_path_2 = os.path.join(base_dir, 'static/img', f'{barcode2}.png')
    if os.path.exists(image_path_1):
        os.remove(image_path_1)
    if os.path.exists(image_path_2):
        os.remove(image_path_2)


def print_pdf(request):
    base_dir = settings.BASE_DIR
    referer = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        if 'selected_checkboxes' in request.POST:
            print("POST selected_checkboxes:", request.POST['selected_checkboxes'])

        if 'selected_checkboxes_2' in request.POST:
            print("POST selected_checkboxes_2:", request.POST['selected_checkboxes_2'])

        if 'selected_checkboxes_3' in request.POST:
            print("POST selected_checkboxes_3:", request.POST['selected_checkboxes_3'])

        # copy_count = int(request.POST.get('copy_count', 1))
        #
        # start_page = 5
        # end_page = 6
        #
        # pdf_writer = PyPDF2.PdfWriter()
        # pdf_path_1 = os.path.join(base_dir, 'static/pdf', 'sample.pdf')
        # pdf_path_2 = os.path.join(base_dir, 'static/pdf', 'print_output.pdf')
        # with open(pdf_path_1, 'rb') as pdf_file:
        #     pdf_reader = PyPDF2.PdfReader(pdf_file)
        #
        #     for _ in range(copy_count):
        #         for page_num in range(start_page - 1, end_page):
        #             page = pdf_reader.pages[page_num]
        #             pdf_writer.add_page(page)
        #
        # with open(pdf_path_2, 'wb') as output_pdf:
        #     pdf_writer.write(output_pdf)

        # printer_name = win32print.GetDefaultPrinter()
        # pdf_path_to_print = os.path.join(base_dir, 'static/pdf', 'print_output.pdf')
        # win32api.ShellExecute(0, "print", pdf_path_to_print, f'"/d:{printer_name}"', ".", 0)

        if referer:
            return redirect(referer)

    return HttpResponse("This view is meant to be accessed via a POST request.")
