from django import forms
from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from wsgiref.util import FileWrapper

import urllib.parse
import io

from . import utils

class ServiceForm(forms.Form):
    """form for service
    """
    file_id = forms.CharField(max_length=50, required=True)

class UploadFileForm(forms.Form):
    """form for uploaded file
    """
    file = forms.FileField()
    file_name = forms.CharField(max_length=100, required=False)

class DownloadForm(forms.Form):
    """form for download
    """
    file_id = forms.CharField(max_length=50, required=True)

class Index(View):
    """index page view
    """
    def get(self, request):
        """handle get request
        """
        return render(request, 'index.html')

class Service(View):
    """service page view
    """
    def get(self, request):
        """handle get request
        """
        form = ServiceForm(request.GET)
        results = []

        if form.is_valid():
            file_id = form.cleaned_data['file_id']
            file_name, status, results = utils.get_cached_data(file_id)

            data = {
                'file_id': file_id,
                'file_name': file_name,
                'status': status, 
                'results': results,
            }
        return render(request, 'result.html', data)

    def post(self, request):
        """handle post request
        """
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = form.cleaned_data['file_name']
            print(file_name)
            file_id = utils.handle_uploaded_file(request.FILES['file'], file_name)

            result_page = reverse('service') + '?' + urllib.parse.urlencode({'file_id': file_id})
            return HttpResponseRedirect(result_page)

        return HttpResponseRedirect(reverse('service'))

class Download(View):
    """Download result
    """
    def get(self, request):
        form = DownloadForm(request.GET)
        if not form.is_valid():
            raise Http404()
        file_id = form.cleaned_data['file_id']
        file_name, status, results = utils.get_cached_data(file_id)
        output_file_name = file_name + '.out'

        if status == 'finish_processing':
            out = io.BytesIO()
            for r in results:
                out.write('{}\n'.format(r).encode('ascii'))
            out.seek(0)
            response = HttpResponse(FileWrapper(out))
            response['Content-Disposition'] = f'attachment; filename={output_file_name}'
            return response

        result_page = reverse('service') + '?' + urllib.parse.urlencode({'file_id': file_id})
        return HttpResponseRedirect(result_page)
