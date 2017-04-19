from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import News
from resubmit.widgets import ResubmitFileWidget
from os.path import join
from PIL import Image
import os
from amadeus import settings

class NewsForm(forms.ModelForm):
    MAX_UPLOAD_SIZE = 5*1024*1024

	#Cropping image
    x = forms.FloatField(widget=forms.HiddenInput(),required=False)
    y = forms.FloatField(widget=forms.HiddenInput(),required=False)
    width = forms.FloatField(widget=forms.HiddenInput(),required=False)
    height = forms.FloatField(widget=forms.HiddenInput(),required=False)

    def save(self, commit=True):
        super(NewsForm, self).save(commit=False)
        self.deletepath = ""

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        if self.instance.image :
	        image = Image.open(self.instance.image)
	        if not x is None:
		        cropped_image = image.crop((x, y, w+x, h+y))
		        resized_image = cropped_image.resize((1200, 250), Image.ANTIALIAS)

		        folder_path = join(settings.MEDIA_ROOT, 'news')
		        #check if the folder already exists
		        if not os.path.isdir(folder_path):
		            os.makedirs(folder_path)

		        if ("news" not in self.instance.image.path):
		            self.deletepath = self.instance.image.path

		        resized_image.save(self.instance.image.path)

        self.instance.save()
        if (self.deletepath):
	        os.remove(self.deletepath)
        return self.instance

    class Meta:
        model = News
        fields = ['title','image','content']
        widgets = {
            'content': forms.Textarea,
            'image': ResubmitFileWidget(attrs={'accept':'image/*'}),

        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if title == '':
            self._errors['name'] = [_('This field is required')]

            return ValueError

        return title
    def clean_image(self):
        image = self.cleaned_data.get('image', False)

        if image:
            if hasattr(image, '_size'):
                if image._size > self.MAX_UPLOAD_SIZE:
                    self._errors['image'] = [_("The image is too large. It should have less than 5MB.")]
                    return ValueError
        else:
            self._errors['image'] = [_("This field is required.")]

            return ValueError

        return image
