from django.db import models

class marking_Info(models.Model):
    STATUS_CHOICES = (
        ('0', 'Неактивек'),
        ('1', "Активен"),
        ('2', 'Не известно'),
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="ДАТА", null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, verbose_name='СТАТУС', default='1')
    contract = models.CharField(max_length=200, verbose_name='КОНТРАКТ', null=True, blank=True)
    comment = models.CharField(max_length=200, verbose_name='КОММЕНТАРИЙ', null=True, blank=True)

    class Meta:
        verbose_name = 'маркировку'
        verbose_name_plural = 'Информация о маркировки'

    def __str__(self):
        return self.contract


class pack_maste_Info(models.Model):
    STATUS_CHOICES = (
        ('0', 'Пустой'),
        ('1', "Заполненый"),
        ('2', 'Неполный'),
    )
    marking = models.ForeignKey(marking_Info, on_delete=models.CASCADE, verbose_name='Маркировка')
    identifier = models.CharField(max_length=200, verbose_name='ИДЕНТИФИКАТОР', null=True, blank=True)
    contract = models.CharField(max_length=200, verbose_name='КОНТРАКТ', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="ДАТА", null=True, blank=True)
    level = models.CharField(max_length=200, verbose_name='УРОВЕНЬ', null=True, blank=True)
    parent = models.CharField(max_length=200, verbose_name='РОДИТЕЛЬСКАЯ УПАКОВКА (ССЫЛКА)', null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, verbose_name='СТАТУС', default='0')
    owner = models.CharField(max_length=200, verbose_name='ВЛАДЕЛЕЦ', null=True, blank=True)
    ORDER_FOR_MARKING = models.CharField(max_length=200, verbose_name='ЗАКАЗ НА МАРКИРОВКУ', null=True, blank=True)
    specification = models.CharField(max_length=200, verbose_name='СПЕЦИФИКАЦИЯ', null=True, blank=True)
    comment = models.CharField(max_length=200, verbose_name='КОММЕНТАРИЙ', null=True, blank=True)

    class Meta:
        verbose_name = 'мастер-упаковку'
        verbose_name_plural = 'Информация о М-У'

    def __str__(self):
        return self.contract

class package_Info(models.Model):
    STATUS_CHOICES = (
        ('0', 'Пустой'),
        ('1', "Заполненый"),
        ('2', 'Неполный'),
    )
    marking = models.ForeignKey(marking_Info, on_delete=models.CASCADE, verbose_name='Маркировка')
    pack_mast = models.ForeignKey(pack_maste_Info, on_delete=models.CASCADE, verbose_name='Мастер упаковки')
    identifier = models.CharField(max_length=200, verbose_name='ИДЕНТИФИКАТОР', null=True, blank=True)
    contract = models.CharField(max_length=200, verbose_name='КОНТРАКТ', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="ДАТА", null=True, blank=True)
    level = models.CharField(max_length=200, verbose_name='УРОВЕНЬ', null=True, blank=True)
    parent = models.CharField(max_length=200, verbose_name='РОДИТЕЛЬСКАЯ УПАКОВКА (ССЫЛКА)', null=True, blank=True)

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, verbose_name='СТАТУС', default='0')
    owner = models.CharField(max_length=200, verbose_name='ВЛАДЕЛЕЦ', null=True, blank=True)
    ORDER_FOR_MARKING = models.CharField(max_length=200, verbose_name='ЗАКАЗ НА МАРКИРОВКУ', null=True, blank=True)
    specification = models.CharField(max_length=200, verbose_name='СПЕЦИФИКАЦИЯ', null=True, blank=True)
    comment = models.CharField(max_length=200, verbose_name='КОММЕНТАРИЙ', null=True, blank=True)

    class Meta:
        verbose_name = 'мастер-упаковку'
        verbose_name_plural = 'Информация о М-У'

    def __str__(self):
        return self.contract

class product_Info(models.Model):
    marking = models.ForeignKey(marking_Info, on_delete=models.CASCADE, verbose_name='Маркировка')
    pack_mast = models.ForeignKey(pack_maste_Info, on_delete=models.CASCADE, verbose_name='Мастер упаковки')
    package = models.ForeignKey(package_Info, on_delete=models.CASCADE, verbose_name='Мастер упаковки')

    date = models.DateTimeField(auto_now_add=True, verbose_name="ДАТА", null=True, blank=True)
    gtin = models.CharField(max_length=200, verbose_name='GTIN', null=True, blank=True)
    status = models.BooleanField(verbose_name='СТАТУС')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Информация о продукте'

    def __str__(self):
        return self.contract