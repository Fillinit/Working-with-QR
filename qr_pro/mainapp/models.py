from django.db import models


class marking_Info(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="ДАТА", null=True, blank=True)
    contract = models.CharField(max_length=200, verbose_name='КОНТРАКТ', null=True, blank=True)
    comment = models.CharField(max_length=200, verbose_name='КОММЕНТАРИЙ', null=True, blank=True)
    status = models.BooleanField(verbose_name='СТАТУС[Отправлено]', null=True, blank=True, default=0)
    class Meta:
        verbose_name = 'маркировку'
        verbose_name_plural = 'Информация о маркировки'

    def __str__(self):
        return self.name


class pack_master_Info(models.Model):
    STATUS_CHOICES = (
        ('0', 'Пустой'),
        ('1', "Заполненный"),
        ('2', 'Неполный'),
    )
    marking = models.ForeignKey(marking_Info, on_delete=models.CASCADE, verbose_name='Маркировка', null=True, blank=True)
    articul = models.CharField(max_length=200, verbose_name='Артикул', null=True, blank=True)
    gtin = models.CharField(max_length=200, verbose_name='GTIN', null=True, blank=True)
    size = models.CharField(max_length=200, verbose_name='size', null=True, blank=True)
    weight = models.CharField(max_length=200, verbose_name='weight', null=True, blank=True)
    color = models.CharField(max_length=200, verbose_name='color', null=True, blank=True)
    inn = models.CharField(max_length=200, verbose_name='inn', null=True, blank=True)
    Importer_info = models.CharField(max_length=200, verbose_name='Importer_info', null=True, blank=True)
    contract = models.CharField(max_length=200, verbose_name='КОНТРАКТ', null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, verbose_name='СТАТУС', default='0')
    date = models.DateTimeField(auto_now_add=True, verbose_name="ДАТА", null=True, blank=True)
    container_pm = models.CharField(max_length=200, verbose_name='Ёмкость мастер-упаковки 2', null=True, blank=True, default='0')
    container_p = models.CharField(max_length=200, verbose_name='Ёмкость упаковки 1', null=True, blank=True, default='0')
    status_send = models.BooleanField(verbose_name='СТАТУС[Отправлено]', null=True, blank=True, default=0)
    file_name = models.CharField(max_length=200, verbose_name='Наименование файла', null=True, blank=True)
    class Meta:
        verbose_name = 'мастер-упаковку'
        verbose_name_plural = 'Информация о М-У'

    def __str__(self):
        return self.gtin


class package_Info(models.Model):
    STATUS_CHOICES = (
        ('0', 'Пустой'),
        ('1', "Заполненный"),
        ('2', 'Неполный'),
    )
    marking = models.ForeignKey(marking_Info, on_delete=models.CASCADE, verbose_name='Маркировка', null=True, blank=True)
    pack_mast = models.ForeignKey(pack_master_Info, on_delete=models.CASCADE, verbose_name='Мастер упаковки', null=True, blank=True)
    gtin = models.CharField(max_length=200, verbose_name='GTIN', null=True, blank=True)

    contract = models.CharField(max_length=200, verbose_name='КОНТРАКТ', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="ДАТА", null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, verbose_name='СТАТУС', default='0')

    file_name = models.CharField(max_length=200, verbose_name='Наименование файла', null=True, blank=True)
    class Meta:
        verbose_name = 'упаковку'
        verbose_name_plural = 'Информация о Упаковки'

    def __str__(self):
        return self.gtin


class product_Info(models.Model):
    marking = models.ForeignKey(marking_Info, on_delete=models.CASCADE, verbose_name='Маркировка', null=True, blank=True)
    pack_mast = models.ForeignKey(pack_master_Info, on_delete=models.CASCADE, verbose_name='Мастер упаковки', null=True, blank=True)
    package = models.ForeignKey(package_Info, on_delete=models.CASCADE, verbose_name='Упаковки',
                                related_name='products', null=True, blank=True)

    file_name = models.CharField(max_length=200, verbose_name='Наименование файла', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="ДАТА", null=True, blank=True)
    gtin = models.CharField(max_length=200, verbose_name='GTIN', null=True, blank=True)
    status = models.BooleanField(verbose_name='СТАТУС', null=True, blank=True, default=0)
    is_print = models.BooleanField(verbose_name='Печать',null=True, blank=True, default=0)
    page = models.CharField(max_length=200, verbose_name='Страница', null=True, blank=True)


    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Информация о продукте'

    def __str__(self):
        return self.gtin

