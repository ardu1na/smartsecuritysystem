

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required 
from django.core.files.storage import  default_storage
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404


from rest_framework import generics

from alarms.serializers import AlarmaEventSerializer
from alarms.forms import *
from alarms.models import *

today = date.today()



class AlarmaEventAPIView(generics.RetrieveAPIView):
    queryset = AlarmaEvent.objects.all()
    serializer_class = AlarmaEventSerializer

    def get_object(self):
        return AlarmaEvent.objects.last()



# ajax
def latest(request):
    ultima = AlarmaEvent.objects.last()
    userurl = reverse('usuario', args=[ultima.miembro.id])

    data = {
        'miembro': str(ultima.miembro),
        'userurl': userurl,
        'tipo': str(ultima.tipo),
        'alarma_vecinal': str(ultima.miembro.vivienda.alarma_vecinal),
        'datetime': str(ultima.datetime.strftime('%d/%m/%Y %H:%M')),        
    }
    return JsonResponse(data)




def has_new_data(request):
    latest_datetime = request.GET.get('latest_datetime')  # Get the latest datetime from the client-side
    latest_event = AlarmaEvent.objects.last()
    has_new_data = latest_event.datetime.strftime('%d/%m/%Y %H:%M') > latest_datetime  # Compare the latest datetime to the client-side value

    data = {
        'has_new_data': has_new_data
    }
    return JsonResponse(data)

###
@login_required
def alertas(request, pk=None):
    template_name = 'sistema/alertas/alertas.html'

    if pk:
        alertas = AlarmaEvent.objects.filter(miembro__id=pk).order_by('-datetime')

    else:
        alertas = AlarmaEvent.objects.all().order_by('-datetime')    
    
    ultima = alertas.last()
    
    sos = alertas.filter(tipo="SOS", datetime__month=today.month, datetime__year=today.year)
    fuego = alertas.filter(tipo="Fuego", datetime__month=today.month, datetime__year=today.year)
    emerg = alertas.filter(tipo="Emergencia", datetime__month=today.month, datetime__year=today.year)

    context={
        "alertas" : alertas,
        "ultima": ultima,
        "sos": sos,
        "fuego": fuego,
        "emerg": emerg,
        "last_s": sos.last(),
        "last_f": fuego.last(),
        "last_e": emerg.last(),
        "page_title":"Alertas de Alarma"
    }
    return render(request, template_name,  context)
    
    
    
    
    
    
    
@login_required  
def sos(request): 
    usuario = Miembro.objects.get(user=request.user)
    alerta = AlarmaEvent.objects.create(miembro=usuario, tipo="SOS")
    return redirect('success', pk=alerta.pk)

@login_required
def fuego(request):
    usuario = Miembro.objects.get(user=request.user)
    alerta = AlarmaEvent.objects.create(miembro=usuario, tipo="Fuego")
    return redirect('success', pk=alerta.pk)


@login_required
def emergencia(request):
    usuario = Miembro.objects.get(user=request.user)
    alerta = AlarmaEvent.objects.create(miembro=usuario, tipo="Emergencia")
    return redirect('success', pk=alerta.pk)

@login_required
def success (request, pk):
    alerta = AlarmaEvent.objects.get(id=pk)
    template_name = 'sistema/alertas/recibida.html'
    context={
        "alerta" : alerta,     
    }
    return render(request, template_name, context)




def planb(request):
    return render (request, 'planb.html', {})

############################################################################################################
#### sistema de alarmas barriales ######

@login_required
def index(request):
    template_name = 'index.html'
    barrios = AlarmaVecinal.objects.filter(state=True)
    alarmas_this_m = AlarmaEvent.objects.filter(datetime__month=today.month, datetime__year=today.year)
    alarmas = AlarmaEvent.objects.all()
    ultima = alarmas.last()
    usuarios = Miembro.objects.filter(state=True)
    viviendas = Vivienda.objects.filter(state=True)
    e_this_m = alarmas_this_m.filter(tipo="Emergencia")
    e_last = alarmas.filter(tipo="Emergencia").last()   
    s_this_m = alarmas_this_m.filter(tipo="SOS")
    s_last = alarmas.filter(tipo="SOS").last()     
    f_this_m = alarmas_this_m.filter(tipo="Fuego")
    f_last = alarmas.filter(tipo="Fuego").last() 

    context={
        "barrios" : barrios,
        "alarmas_this_m": alarmas_this_m,
        "ultima": ultima,
        "usuarios": usuarios,
        "viviendas": viviendas,
        "e_this_m": e_this_m,
        "e_last": e_last,
        "s_this_m": s_this_m,
        "s_last": s_last,
        "f_this_m": f_this_m,
        "f_last": f_last,
        "page_title":"Plan B"
    }
    return render(request, template_name,  context)


###########################################################################################








########################################################################
########################### crud de barrios #######################################

@login_required
def barrios_list(request):
    template_name = 'sistema/barrios/barrios.html'
    
    barrios=AlarmaVecinal.objects.filter(state=True)
    alertas = AlarmaEvent.objects.filter(datetime__year=today.year, datetime__month=today.month)
    usuarios=Miembro.objects.filter(state=True)
    viviendas= Vivienda.objects.filter(state=True)
    ultima = AlarmaEvent.objects.last()

    
    
    if request.method == "GET":
        addform=NewAlarmaVecinalForm()
    if request.method == "POST":
        if "addnew" in request.POST:
            addform = NewAlarmaVecinalForm(request.POST)
            if addform.is_valid():
                newgrupo = addform.save()
                return redirect('barrios')
            else:
                return HttpResponse("Something wrong with the form")
    context={
        "barrios": barrios,
        "addform": addform,
        "n_alertas": len(alertas),
        "n_usuarios": len(usuarios),
        "n_casas": len(viviendas),
        "ultima": ultima,

        "page_title":"Alarmas Vecinales"
    }
    return render(request, template_name, context)


@login_required
def barrio_delete(request, pk):
    barrio = get_object_or_404(AlarmaVecinal, id=pk)
    barrio.state = False
    barrio.save()
    return redirect('barrios')

############################################################################################################
########################### crud de viviendas ###########################

@login_required
def barrio_detail(request, pk): 
    template_name = 'sistema/barrios/barrio.html'
    
    barrio = get_object_or_404(AlarmaVecinal, id=pk)
    viviendas = Vivienda.objects.filter(state="Yes", alarma_vecinal = barrio)
    ultima = AlarmaEvent.objects.filter(miembro__vivienda__alarma_vecinal = barrio).last()
    
    emergencias = barrio.get_e
    if len(emergencias) != 0:
        emergencia = barrio.get_e[0]
        e_this_m = []
        for e in emergencias:
            if e.datetime.month == today.month and e.datetime.year == today.year:
                e_this_m.append(e)
    else:
        emergencia = None
        e_this_m = None
            

    soss = barrio.get_s
    if len(soss) != 0:
        sos = barrio.get_s[0]
        s_this_m = []
        for s in soss:
            if s.datetime.month == today.month and s.datetime.year == today.year:
                s_this_m.append(s)
    else:
        sos = None
        s_this_m = None
            
    fuegos = barrio.get_f
    if len(fuegos) != 0:
        fuego = barrio.get_f[0]
        f_this_m = []
        for f in fuegos:
            if f.datetime.month == today.month and f.datetime.year == today.year:
                f_this_m.append(f)
    else:
        fuego = None
        f_this_m = None
            
    
    if request.method == "GET":
        addform=NewViviendaForm()
    if request.method == "POST":
        if "addnew" in request.POST:
            addform = NewViviendaForm(request.POST)
            if addform.is_valid():
                vivienda = addform.save(commit=False)
                vivienda.alarma_vecinal=barrio
                vivienda.save()
                return redirect('barrio', pk=barrio.pk)
            else:
                return HttpResponse("Something wrong with the form")
    context={
        "viviendas": viviendas,
        "barrio":barrio,
        "addform": addform,
        "ultima": ultima,
        "page_title":f"Alarma Vecinal {barrio.nombre}",
        "emergencia": emergencia,
        "e_this_m": e_this_m,
        "sos": sos,
        "s_this_m": s_this_m,
        "fuego": fuego,
        "f_this_m": f_this_m,
    }
    return render(request, template_name, context)


@login_required
def vivienda_delete(request, pk):
    
    vivienda = get_object_or_404(Vivienda, id=pk)
    vivienda.state = False
    vivienda.save()
    return redirect('barrio', pk=vivienda.alarma_vecinal.pk)


@login_required
def vivienda_detail(request, pk):
    
    vivienda = get_object_or_404(Vivienda, id=pk)
    usuarios = vivienda.miembros.filter(state=True)
    alarmas = AlarmaEvent.objects.filter(miembro__vivienda= vivienda.pk)
    ultima = alarmas.last()
    e = alarmas.filter(tipo="Emergencia")
    f = alarmas.filter(tipo="Fuego")
    s = alarmas.filter(tipo="SOS")
    
    template_name= 'sistema/barrios/vivienda.html'
    addform=NewUsuarioForm()
         
        
    if request.method == "POST":
        if "addnew" in request.POST:
            addform = NewUsuarioForm(request.POST, request.FILES)
            if addform.is_valid():
                usuario = addform.save(commit=False)
                usuario.vivienda = vivienda
                if 'avatar' in request.FILES:
                    avatar = request.FILES['avatar']
                    filename = default_storage.save('profiles/' + avatar.name, avatar)
                    usuario.avatar = filename
                usuario.save()
                return redirect('vivienda', pk=vivienda.pk)
            
    context ={
        "vivienda" : vivienda,
        "usuarios": usuarios,
        "ultima": ultima,
        "e":e,
        "f":f,
        "s":s,
        "addform" : addform,
    }
    return render(request, template_name, context)





@login_required
def barrio_edit(request, pk):
    
    barrio = get_object_or_404(AlarmaVecinal, id=pk)
    template_name= 'sistema/barrios/barrioedit.html'
    editform=NewAlarmaVecinalForm(instance=barrio)
             
        
    if request.method == "POST":
            editform = NewAlarmaVecinalForm(request.POST, instance=barrio)
            if editform.is_valid():
                editform.save()
                return redirect('barrio', pk=barrio.pk)
            else:
                return HttpResponse("Something wrong with the form")
            
    context ={
        "barrio" : barrio,
        "editform" : editform,
    }
    return render(request, template_name, context)



@login_required
def vivienda_edit(request, pk):
    
    vivienda = get_object_or_404(Vivienda, id=pk)
    template_name= 'sistema/barrios/viviendaedit.html'
    editform=NewViviendaForm(instance=vivienda)
             
        
    if request.method == "POST":
            editform = NewViviendaForm(request.POST, instance=vivienda)
            if editform.is_valid():
                editform.save()
                return redirect('vivienda', pk=vivienda.pk)
            else:
                return HttpResponse("Something wrong with the form")
            
    context ={
        "vivienda" : vivienda,
        "editform" : editform,
    }
    return render(request, template_name, context)







############################################################################################################
####################################### USUARIOS GRAL ###########################





@login_required
def users_list(request, pk=None):
    
    
    if pk:
        barrio = get_object_or_404(AlarmaVecinal, id=pk)
        usuarios = Miembro.objects.filter(state="Yes", vivienda__alarma_vecinal=barrio)
        context ={
        "usuarios" : usuarios,
        "barrio": barrio,
        }
        
    else:
                
        
        usuarios = Miembro.objects.filter(state=True)
        context ={
        "usuarios" : usuarios,  
        }
        
        
    template_name= 'sistema/generic/usuarios.html'
            
    
    return render(request, template_name, context)



@login_required
def useradd(request):
    viviendas = Vivienda.objects.filter(state=True)
    alarmas = AlarmaVecinal.objects.filter(state=True)

    adduser = NewUser()
    
    if request.method == "POST":        
            
            
        if 'user' in request.POST: 
            print("############## USER")        

            post_data = request.POST.copy()
            print(post_data)

            if 'alarma_vecinal' in post_data:
                del post_data['alarma_vecinal']
                
            adduser = NewUser(post_data, request.FILES)
            print(adduser)
            
            
            if adduser.is_valid():
                
                user = adduser.save(commit=False)
                
                if 'avatar' in request.FILES:
                    avatar = request.FILES['avatar']
                    filename = default_storage.save('profiles/' + avatar.name, avatar)
                    user.avatar = filename

                
                user.vivienda = adduser.cleaned_data['vivienda']
                user.save()
                return redirect('usuarios')
           
        
        
    context ={
    "adduser": adduser,
    "alarmas": alarmas,
    "viviendas": viviendas,    
    }
        
        
    template_name= 'sistema/generic/useradd.html'
            
    
    return render(request, template_name, context)


@login_required
def viviendaadd(request):
    alarmas = AlarmaVecinal.objects.filter(state=True)

    addvivienda = NewVivienda()
    
    if request.method == "POST":
        if 'vivienda' in request.POST: 

            addvivienda = NewVivienda(request.POST)
            

                
            if addvivienda.is_valid():
                
                vivienda = addvivienda.save(commit=False)
                vivienda.alarma_vecinal = addvivienda.cleaned_data['alarma_vecinal']              
                vivienda.save()
                return redirect('useradd')
            else:
                print(addvivienda.errors)
                return HttpResponse(f"Something wrong with the form: {addvivienda.errors}")
            
            
        
    context ={
    "addvivienda": addvivienda, 
    "alarmas": alarmas,
    }
        
        
    template_name= 'sistema/generic/viviendaadd.html'
            
    
    return render(request, template_name, context)








@login_required
def barrioadd(request):

    addbarrio = NewAlarmaVecinalForm()
    
    if request.method == "POST":
        if 'addnew' in request.POST: 
            
            new = NewAlarmaVecinalForm(request.POST)
            if new.is_valid():
                
                new.save()
                return redirect('viviendaadd')
            else:
                print(new.errors)
                return HttpResponse(f"Something wrong with the form: {new.errors}")
            
            
        
    context ={
    "addform": addbarrio, 
    }
        
        
    template_name= 'sistema/generic/barrioadd.html'
            
    
    return render(request, template_name, context)
############################################################################################################
####################################### crud de usuarios dentro de vivievnda ###########################

@login_required
def usuario_detail(request, pk):
    
    usuario = get_object_or_404(Miembro, id=pk)
    template_name= 'sistema/barrios/usuario.html'
    editform=NewUsuarioForm(instance=usuario)
   
            
    if request.method == "POST":
        editform = NewUsuarioForm(request.POST, request.FILES, instance=usuario)
        if editform.is_valid():
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                filename = default_storage.save('profiles/' + avatar.name, avatar)
                usuario.avatar = filename
            usuario.save()
            return redirect('usuario', pk=usuario.pk)
        

            
    context ={
        "usuario" : usuario,
        "editform" : editform,
    }
    return render(request, template_name, context)



@login_required
def usuario_delete(request, pk):
    
    usuario = get_object_or_404(Miembro, id=pk)
    usuario.state = False
    usuario.save()
    return redirect('vivienda', pk=usuario.vivienda.pk)
########################################################################################################################








