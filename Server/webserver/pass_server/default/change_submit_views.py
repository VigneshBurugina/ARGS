from django.http import HttpResponse
from django.shortcuts import render

wd = '~/PycharmProjects/School\ Project/Server/web.info'
pin = "+++++"

# Create your views here.
def index(request):
    d = request.POST
    print(d)
    print(list(d.keys()))
    if ('password' not in list(d.keys())) or ('username' not in list(d.keys())) or ('pin' not in list(d.keys())) :
        return render(request=request, template_name='error.html') 
    elif d['pin'] != pin:
        return render(request=request, template_name='invalid.html')
    with open(wd,'w') as fl:
        wl.write(f'{d['username']}\n{d['password']}')
    return render(request=request, template_name='page2.html')
