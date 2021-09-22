import numpy as np
from . import object_detection
import cv2

from django.shortcuts import render
import os
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from djangoapp.forms import ImageForm

from django.views.generic import DetailView
from djangoapp.models import Image_model

class Image(TemplateView):

    form = ImageForm
    template_name = 'image.html'

    def post(self, request, *args, **kwargs):

        form = ImageForm(request.POST, request.FILES)


        if form.is_valid():
            obj = form.save()
            print(obj.name)
            print(obj.image.url)
            outputFile,frame=object_detection.detect(obj.image.url)
            #outputFile=os.path.basename(outputFile)
            obj.detected_img = outputFile
            print(obj.detected_img)
            obj.save()
            return HttpResponseRedirect(reverse_lazy('image_display', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class ImageDisplay(DetailView):
    model = Image_model
    template_name = 'image_display.html'
    context_object_name = 'context'

def deleteimg(request,pk):
    if request.method=='POST':
        model = Image_model.objects.get(pk=pk)
        model.delete()
        return HttpResponseRedirect(reverse_lazy('home'))
