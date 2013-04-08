# -*- coding:utf8 -*-
from django.http import HttpResponse
from django.http import QueryDict
from django.http import Http404
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import render, render_to_response, redirect
from recorder.models import LoginUsers, LoginRecord
from datetime import datetime, timedelta

def index(request):
    # return render(request, 'recorder/index.html')
    return redirect('/recorder/login')


def login(request):
    if request.method == 'POST':
        un = request.POST.get('workid', None)
        pw = request.POST.get('password', None)
        print un, pw
        if un and pw:
            try:
                print 'success'
                user = LoginUsers.objects.get(user_name=un, passwd=pw)
                request.session['userid'] = user.id
                return redirect('/recorder/welcome/')
            except Exception, e:
                pass
        message = u"登陆错误！"

    return render_to_response('recorder/index.html', locals(), context_instance=RequestContext(request))

def welcome(request):
    '''welcome page'''
    try:
        userid = request.session['userid']
        user = LoginUsers.objects.get(id=userid)
        record = user.get_last_record()
        print 'vvvv', record
        if record:
            now = datetime.now()
            delta = record.stop_time - now.replace(tzinfo=record.stop_time.tzinfo)
            context = {'username': user.user_name, 'state':record.state, \
            'seconds':delta.total_seconds()}
        else:
            context = {'username': user.user_name, 'state':False, 'seconds':0}
        # welcome同时显示登陆与取消登陆2种选择，取决于state
        return render(request, 'recorder/welcome.html', context)
    except Exception, e:
        print e
        raise Http404 

def regist(request):
    if request.method == 'POST':
        un = request.POST.get('username', None)
        pw = request.POST.get('password', None)
        wi = request.POST.get('workid', None)
        print un, pw
        if un and pw and wi:
            try:
                user = LoginUsers.objects.get(user_name=un)
                return HttpResponse("%s has been registed!"%un)
            except Exception, e:
                user = LoginUsers(user_name=un, passwd=pw, work_id=wi)
                user.save()
                pass

    return render_to_response('recorder/regist.html', context_instance=RequestContext(request))

def start(request):
    '''启用自动登陆'''
    userid = request.session['userid']
    user = LoginUsers.objects.get(id=userid)
    start_time = datetime.now()
    stop_time = start_time + timedelta(days=1)
    record = LoginRecord(work_id=user.work_id, state=True, start_time=start_time, stop_time=stop_time)
    record.save() # 新建一个记录
    print "start:", record
    return redirect('/recorder/welcome/')

def stop(request):
    '''禁用自动登陆'''
    userid = request.session['userid']
    user = LoginUsers.objects.get(id=userid)
    start_time = datetime.now()
    stop_time = start_time + timedelta(days=1)
    record = LoginRecord(work_id=user.work_id, state=False, start_time=start_time, stop_time=stop_time)
    record.save() # 禁用一个记录
    return redirect('/recorder/welcome/')

def api_query(request):
    try:
        username = request.GET.get('un', None)
        user = LoginUsers.objects.get(user_name=username)
        record = user.get_last_record()
        return HttpResponse(record)
    except Exception, e:
        pass
