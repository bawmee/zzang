import datetime
from datetime import time
from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import SchMst
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'index.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST' :

        name    = request.POST['username']
        pw      = request.POST['password']
        user    = auth.authenticate(request, username = name, password = pw)


        if user is not None :
                auth.login(request, user)
                return redirect(listsch)
        else :
                return render(request, 'index.html', {'error':'이름 비밀번호 확인'})

    else :
        return render(request, 'index.html')
    


@login_required(login_url = '/')
def listsch(reqeust):

    today = date.today()
    start_date = datetime.datetime.strptime(str(today.year)+" "+str(today.month)+" "+str(today.day) ,'%Y %m %d')
    end_date = datetime.datetime.strptime(str(today.year)+" "+str(today.month)+" "+str(today.day)+" 23:59", '%Y %m %d %H:%M')

    try:
        tmpdata = SchMst.objects.get(date__range=[start_date, end_date])
    except SchMst.DoesNotExist:
        tmpdata = None

    if tmpdata is None :
        isTodayOnWork = 0
    else :
        isTodayOnWork = 1

    schlist = SchMst.objects.all().order_by('-date')

    return render(reqeust, 'workOn.html', {'schlist' : schlist, 'isTodayOnWork' : isTodayOnWork})

def oncreate(request):

    today = date.today()
    start_date = datetime.datetime.strptime(str(today.year)+" "+str(today.month)+" "+str(today.day) ,'%Y %m %d')
    end_date = datetime.datetime.strptime(str(today.year)+" "+str(today.month)+" "+str(today.day)+" 23:59", '%Y %m %d %H:%M')

    try:
        tmpdata = SchMst.objects.get(date__range=[start_date, end_date])
    except SchMst.DoesNotExist:
        tmpdata = None

    if tmpdata is None :

        schMst          = SchMst()
        schMst.isOnWork = True
        schMst.date     = timezone.datetime.now()
        schMst.save()

        messages.info(request, '출근 완')
        return redirect(listsch)
    else :
        messages.info(request, '이미 출근했삼')
        return redirect(listsch)

    
@login_required(login_url = '/')
def delete(request, chul_id):
    chul = get_object_or_404(SchMst, pk = chul_id)
    chul.delete()

    messages.info(request, '삭제 완료 ! 주의 깊게 하시라구요 ! ')
    return redirect(listsch)