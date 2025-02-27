from django.db import models

class NameImgIdModel(models.Model):
    nmID = models.CharField(max_length=20, primary_key=True, unique=True, default='0')
    vendorCode = models.CharField(max_length=50)
    photos = models.CharField(max_length=200)

class IdSizeModel(models.Model):
    nmID = models.ForeignKey(NameImgIdModel, to_field='nmID', on_delete=models.CASCADE)
    sizes = models.CharField(max_length=20)

class SalesTable(models.Model):
    date = models.DateTimeField()
    supplierArticle = models.CharField(max_length=100)
    nmId = models.CharField(max_length=30)
    techSize = models.CharField(max_length=50)
    priceWithDisc = models.CharField(max_length=30)
    saleID = models.CharField(max_length=30, primary_key=True, default='0')

class OrdersTable(models.Model):
    srid = models.CharField(max_length=100, primary_key=True, default='0')
    date = models.DateTimeField()
    warehouseName = models.CharField(max_length=30)
    oblastOkrugName = models.CharField(max_length=50)
    regionName = models.CharField(max_length=50)
    supplierArticle = models.CharField(max_length=100)
    nmId = models.CharField(max_length=30)
    barcode = models.CharField(max_length=30)
    incomeID = models.CharField(max_length=30)
    finishedPrice = models.CharField(max_length=30)
    priceWithDisc = models.CharField(max_length=30)
    isCancel = models.CharField(max_length=10, default='0')