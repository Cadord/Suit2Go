from django.shortcuts import render
from .models import Roupas
from .forms import RoupasForms
from django.db.models import Q


# Create your views here.
def index(request):
    query = request.GET.get('q', '')
    ultimas_roupas_query = Roupas.objects
    if (query):
        ultimas_roupas_query = ultimas_roupas_query.filter(Q(nome__icontains=query))
    ultimas_roupas = ultimas_roupas_query.order_by('nome').all
    context = {
        "roupas": ultimas_roupas
    }
    return render(request, "index.html", context)


def cadastro_roupa(request):
    if request.method == 'POST':
        form = RoupasForms(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            form = RoupasForms()
            # return render(request, template_name='index.html')
        else:
            print(form.errors)

    else:
        form = RoupasForms()
    context = {'form': form}
    return render(request, template_name='cadastro_roupa.html', context=context)

def roupa_dinamico(request,idroupa):
    context = {'roupa':Roupas.objects.get(id_roupas=idroupa)}
    return render(request,'roupa.html',context)
