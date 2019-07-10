from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import connection
import requests
from .forms import PersonForm


def index(request):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}
    form = PersonForm(request.POST)
    url = form.data['site']
    req = requests.get(url,headers = headers ).text

    posts = []
    cursor = connection.cursor()
    query_string = "select * from topic"
    cursor.execute(query_string)
    se = cursor.fetchall()

    for ti in se:
        if ti[2] in req:

            dic = {'site': ti[1], 'url': ti[2]}
            posts.append(dic)

    return render(request, 'hello_app/index.html', {'posts': posts})





def form_test(request):
    form = PersonForm()
    return render(request, 'hello_app/form.html',{'form': form})





def confirm(request):
    form = PersonForm(request.POST)
    print(form.data['site'])
    if form.is_valid():
        return render(request, 'hello_app/confirm.html', {'form': form})


    return HttpResponseRedirect('/hello_app/form')


def test(request):
    if request.method == 'POST':

        url = request.POST.get('q')
        req = requests.request.get(url)

        posts = []
        cursor = connection.cursor()
        query_string = "select * from topic"
        cursor.execute(query_string)
        se = cursor.fetchall()

        for ti in se:
            if ti[2] in req:
                dic = {'site': ti[1], 'url': ti[2]}
                posts.append(dic)

        return render(request, 'hello_app/index.html', {'posts': posts})



def test1(request):
    if request.method == 'POST':

        form = PersonForm(request.POST)
        url = form.data['title']
        req = requests.get(url).text

        posts = []
        cursor = connection.cursor()
        query_string = "select * from topic"
        cursor.execute(query_string)
        se = cursor.fetchall()

        for ti in se:
            if ti[2] in req:
                dic = {'site': ti[1], 'url': ti[2]}
                posts.append(dic)


        if form.is_valid():  # 폼 검증
            return render(request, 'hello_app/test1.html', {'form': form, 'posts':posts})

    else:
        form = PersonForm()  # forms.py의 PostForm 클래스의 인스턴스
        return render(request, 'hello_app/test1.html', {'form': form})  # 템플릿 파일 경로 지정, 데이터 전달


