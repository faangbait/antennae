from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required

from .forms import UploadPGNForm
from .utils import PGNImport

@require_http_methods(["GET", "POST"])
@staff_member_required
def upload_pgn(request):
    context = {
        'form': UploadPGNForm()
    }
    if request.method == "POST":
        if request.FILES.get('pgn', None):
            pgn = request.FILES['pgn']
            
            context['form'] = UploadPGNForm(request.POST, request.FILES)
            if context['form'].is_valid():
                context['uploaded_file_url'] = PGNImport(pgn).url
    
    return render(request, 'metadata/upload.html', context)
