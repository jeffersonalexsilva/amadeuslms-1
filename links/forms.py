""" 
Copyright 2016, 2017 UFPE - Universidade Federal de Pernambuco
 
Este arquivo é parte do programa Amadeus Sistema de Gestão de Aprendizagem, ou simplesmente Amadeus LMS
 
O Amadeus LMS é um software livre; você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU como publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença.
 
Este programa é distribuído na esperança que possa ser útil, mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
 
Você deve ter recebido uma cópia da Licença Pública Geral GNU, sob o título "LICENSE", junto com este programa, se não, escreva para a Fundação do Software Livre (FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.
"""

# coding=utf-8
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import ugettext_lazy as _

from subjects.forms import ParticipantsMultipleChoiceField
from subjects.models import Tag
from .models import Link


class LinkForm(forms.ModelForm):
    subject = None
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024

    students = ParticipantsMultipleChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        super(LinkForm, self).__init__(*args, **kwargs)

        self.subject = kwargs['initial'].get('subject', None)

        if self.instance.id:
            self.subject = self.instance.topic.subject
            self.initial['tags'] = ", ".join(
                self.instance.tags.all().values_list("name", flat=True))

        self.fields['students'].queryset = self.subject.students.all()
        self.fields['groups'].queryset = self.subject.group_subject.all()

    tags = forms.CharField(label=_('Tags'), required=False)
    link_url = forms.CharField(label=_('Website URL'), required=True)

    class Meta:
        model = Link
        fields = ['name', 'link_url', 'brief_description', 'all_students', 'students', 'groups',
                  'visible']
        labels = {
            'name': _('Link name'),
            'end_view': _('End View'),
            'end_view_date': _('End View Date')
        }
        widgets = {
            'brief_description': forms.Textarea,
            'students': forms.SelectMultiple,
            'groups': forms.SelectMultiple,
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '')

        topics = self.subject.topic_subject.all()

        for topic in topics:
            if self.instance.id:
                same_name = topic.resource_topic.filter(name__iexact=name).exclude(
                    id=self.instance.id).count()
            else:
                same_name = topic.resource_topic.filter(name__iexact=name).count()

            if same_name > 0:
                self._errors['name'] = [_('There is already a link with this name on this subject')]

                return ValueError

        return name

    def clean_link_url(self):
        link_url = self.cleaned_data.get('link_url', '')
        validate = URLValidator(schemes=('http', 'https', 'ftp', 'ftps', 'rtsp', 'rtmp'))
        if link_url[0].lower() != "h":
            link_url = "https://" + link_url
        try:
            validate(link_url)
        except ValidationError:
            self._errors['link_url'] = [_('Invalid URL. It should be an valid link.')]
            return ValueError

        return link_url

    def save(self, commit=True):
        super(LinkForm, self).save(commit=True)

        self.instance.save()

        previous_tags = self.instance.tags.all()

        tags = self.cleaned_data['tags'].split(",")

        # Excluding unwanted tags
        for prev in previous_tags:
            if not prev.name in tags:
                self.instance.tags.remove(prev)

        for tag in tags:
            tag = tag.strip()

            exist = Tag.objects.filter(name=tag).exists()

            if exist:
                new_tag = Tag.objects.get(name=tag)
            else:
                new_tag = Tag.objects.create(name=tag)

            if not new_tag in self.instance.tags.all():
                self.instance.tags.add(new_tag)

        return self.instance
