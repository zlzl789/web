from django.shortcuts import render
from django.db import connection
import requests

from bs4 import BeautifulSoup


from .forms import PersonForm
from .forms import Key
from .forms import Key1




def index(request):
    return render(request, 'hello_app/main.html')




def urls(request):

    if request.method == 'POST':
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}

        form = PersonForm(request.POST)
        url = form.data['title']
        req = requests.get(url, headers=headers).text
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
            return render(request, 'hello_app/urls.html', {'form': form, 'posts':posts,'url':url})

    else:
        form = PersonForm()  # forms.py의 PostForm 클래스의 인스턴스
        return render(request, 'hello_app/urls.html', {'form': form})  # 템플릿 파일 경로 지정, 데이터 전달








def key(request):  # key 라는 함수(그룹) 만들겠다고 def로 선언했어

    post = []  # 데이터베이스 안의 내용들이 한번씩 돌때마다 쌓여 담겨있어요 (포문안에쓰면 리셋되어 마지막꺼만 나옴)

    if request.method == 'POST':  # 포스트로 받은 값이 있다면
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}

        forms = Key(request.POST)  # HTTP가 인식하는 포스트의 모든값
        ke = forms.data['keyword']  # POST안에 있는 키 값
        url = 'https://ad.search.naver.com/search.naver?where=ad&sm=svc_nrs&query={}'.format(ke)  # 네이버 파워링크 url 뒤로 키워드값 넣기
        uurl = url + '&pagingIndex={}'  # 페이지 수



        for n in range(1, 100):  # url페이지 수 100번 돌리기 포문

            u_url = uurl.format(n)  # url페이지 수 뒤로 n번만큼(100) 돌려라
            reqe = requests.get(u_url, headers=headers).text  # 키워드넣은 값의 url을 갖고왔다
            soup = BeautifulSoup(reqe, 'html.parser')  # url을 뷰티풀소프로 컴퓨터가 읽을수있는 html파일로 쪄버리기
            titles_by_select = soup.select('ol.lst_type > li > div.inner') # a태그 선택하여 titles_by_select안에 담아요


            if not titles_by_select:  # a태그가 없으면(값) 멈춰라
                break


            for titl in titles_by_select:  # titles_by_select안에 titl가 있는동안 도라라

                link = titl.find('a')
                te = link.text  # te안에 titl을 텍스트인것들(쇼핑몰 이름)을 담아라! 잘 담김=프린트해봄
                f_url = link.get('href')  # f_url안에 쇼핑몰의 주소를 담아라~ 프린트해봄!
                f_req = requests.get(f_url, headers=headers).text  #

                il = titl.find_all('em','txt')
                ir = il[0].text

                cur = connection.cursor()
                string = "select * from topic"
                cur.execute(string)
                see = cur.fetchall()

                post1 = []
                for t in see:  # 데이터베이스와 url 비교하는구문
                    if t[2] in f_req:
                        di = t[1]
                        post1.append(di)

                dd = {'site': te, 'title': post1, 'url': f_url , 'te':ir}

                post.append(dd)




        if forms.is_valid():  # 폼 검증 #얘는 if request.method == 'POST': 안에 있어야 함
            return render(request, 'hello_app/key.html', {'form': forms, 'post': post})


    else:  # 얘는 if request.method == 'POST': 얘랑 짝꿍이라 if request.method == 'POST':쟤 줄에 같이있어야한다
        forms = Key()
        return render(request, 'hello_app/key.html', {'form': forms, })  # 템플릿 파일 경로 지정, 데이터 전달





def d_key(request):





    post = []  # 데이터베이스 안의 내용들이 한번씩 돌때마다 쌓여 담겨있어요 (포문안에쓰면 리셋되어 마지막꺼만 나옴)


    if request.method == 'POST':  # 포스트로 받은 값이 있다면
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}


        forms = Key1(request.POST)  # HTTP가 인식하는 포스트의 모든값
        ke = forms.data['keyword1']  # POST안에 있는 키 값
        url = 'https://search.daum.net/search?w=ad&q={}'.format(ke)  # 네이버 파워링크 url 뒤로 키워드값 넣기



        for n in range(1, 5):  # url페이지 수 100번 돌리기 포문

            reqe = requests.get(url, headers=headers).text  # 키워드넣은 값의 url을 갖고왔다
            soup = BeautifulSoup(reqe, 'html.parser')  # url을 뷰티풀소프로 컴퓨터가 읽을수있는 html파일로 쪄버리기
            titles_by_select = soup.select(' div.coll_cont > div > ul > li > div > div > div.wrap_tit.mg_tit > a')  # a태그 선택하여 titles_by_select안에 담아요


            if not titles_by_select:  # a태그가 없으면(값) 멈춰라
                break

            for titl in titles_by_select:  # titles_by_select안에 titl가 있는동안 도라라
                te = titl.text  # te안에 titl을 텍스트인것들(쇼핑몰 이름)을 담아라! 잘 담김=프린트해봄
                f_url = titl.get('href')  # f_url안에 쇼핑몰의 주소를 담아라~ 프린트해봄!
                f_req = requests.get(f_url, headers=headers).text  #

                cur = connection.cursor()
                string = "select * from topic"
                cur.execute(string)
                see = cur.fetchall()

                post1 = []
                for t in see:  # 데이터베이스와 url 비교하는구문
                    if t[2] in f_req:
                        di = t[1]
                        post1.append(di)

                    dd = {'site': te, 'title': post1, 'url': f_url}

                post.append(dd)


        if forms.is_valid():  # 폼 검증 #얘는 if request.method == 'POST': 안에 있어야 함
            return render(request, 'hello_app/d_key.html', {'form': forms, 'post': post})


    else:  # 얘는 if request.method == 'POST': 얘랑 짝꿍이라 if request.method == 'POST':쟤 줄에 같이있어야한다
        forms = Key1()
        return render(request, 'hello_app/d_key.html', {'form': forms, })  # 템플릿 파일 경로 지정, 데이터 전달




