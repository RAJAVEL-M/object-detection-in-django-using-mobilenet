from django.db import models

# Create your models here.

class Image_model(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    detected_img = models.ImageField(upload_to='images/',blank=True)
    

    def delete(self,*args,**kwargs):
        self.image.delete()
        self.detected_img.delete()
        super().delete(*args,**kwargs)
