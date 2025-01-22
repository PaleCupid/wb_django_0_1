from django.db import models

class NameImgIdModel(models.Model):
    nmID = models.CharField(max_length=20, primary_key=True, unique=True, default='0')
    name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=200)

class IdSizeModel(models.Model):
    nmID = models.ForeignKey(NameImgIdModel, to_field='nmID', on_delete=models.CASCADE)
    sizes = models.CharField(max_length=20)