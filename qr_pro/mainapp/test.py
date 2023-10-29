def orders_save(request):
    if request.user.is_authenticated:
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

            number_mark_packing = request.POST['number_mark_packing']
            number_mark_packing_count = request.POST['number_mark_packing_count']
            number_packing_master = request.POST['number_packing_master']
            number_packing_master_count = request.POST['number_packing_master_count']
            number_packing = request.POST['number_packing']
            number_packing_count = request.POST['number_packing_count']

            uploaded_file = request.FILES['file_input']
            date = datetime.now().date()
            is_new = True

            if uploaded_file.name.endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(uploaded_file)

                num_pages = len(pdf_reader.pages)

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

                for number_m_p in range(number_mark_packing):
                    barcode_generator_packaging_wizard(name_file=f"Marking__{gtin_code_inp}__{number_m_p}", barcode1=f"{gtin_code_inp}__{number_m_p}",
                                                       barcode3=gtin_code_inp, count=number_mark_packing_count, date=date, size=size_inp,
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

                    barcode_generator_packaging_wizard(
                        name_file=f"MasterPackaging__{gtin_code_inp}__{pack_master_obj.id}",
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
                                                    barcode=gtin_code_inp,
                                                    barcode2=f'{gtin_code_inp}__{package_obj.id}',
                                                    count=items_in_current_pack, size=size_inp,
                                                    art=articul_inp, name_pack=name_mark_inp, weight=weight_inp)
                        pack_num += 1
                        for item in range(items_in_current_pack):
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
                                    gtin=str(result).replace("(", "").replace(")", "").replace(" ", "").lower(),
                                    file_name=f'{gtin_code_inp}.pdf',
                                    page=page_num
                                )
                                product_obj.save()
                                page_num += 1