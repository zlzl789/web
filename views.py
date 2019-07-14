from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import connection
import requests
from .forms import PersonForm
from .forms import Key
from bs4 import BeautifulSoup


def key(request): # key 라는 함수(그룹) 만들겠다고 def로 선언했어

    post = []  # 데이터베이스 안의 내용들이 한번씩 돌때마다 쌓여 담겨있어요 (포문안에쓰면 리셋되어 마지막꺼만 나옴)


    if request.method == 'POST': #포스트로 받은 값이 있다면
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}

        forms = Key(request.POST) #폼에서 받아온 키워드로
        ke = forms.data['keyword'] #key안에 넣고
        url = 'https://ad.search.naver.com/search.naver?where=ad&sm=svc_nrs&query={}'.format(ke) #네이버 파워링크 url 뒤로 키워드값 넣기
        uurl = url+'&pagingIndex={}'#페이지 수



        for n in range(1, 100): #url페이지 수 100번 돌리기 포문


            u_url = uurl.format(n) #url페이지 수 뒤로 n번만큼(100) 돌려라
            reqe = requests.get(u_url, headers=headers).text #키워드넣은 값의 url을 갖고왔다
            soup = BeautifulSoup(reqe, 'html.parser') #url을 뷰티풀스프로 컴퓨터가 읽을수있는 html파일로 쪄버리기
            titles_by_select = soup.select('ol.lst_type > li > div.inner > a.lnk_tit') #a태그 선택하여 titles_by_select안에 담아요

            if not titles_by_select: #a태그가 없으면(값) 멈춰라
                break


            for titl in titles_by_select: #titles_by_select안에 titl가 있는동안 도라라
                te = titl.text #te안에 titl을 텍스트인것들(쇼핑몰 이름)을 담아라! 잘 담김=프린트해봄
                f_url = titl.get('href') # f_url안에 쇼핑몰의 주소를 담아라~ 프린트해봄!
                f_req = requests.get(f_url, headers=headers).text #

                cur = connection.cursor()
                string = "select * from topic"
                cur.execute(string)
                see = cur.fetchall()

                post1 = []
                for t in see: #데이터베이스와 url 비교하는구문
                    if t[2] in f_req:
                        di = {'site': t[1],'title':te}
                        post1.append(di)
                post.append(post1)

            print(post)
            if forms.is_valid():  # 폼 검증 #얘는 if request.method == 'POST': 안에 있어야 함
                return render(request, 'hello_app/key.html', {'form':forms,'post': post, 'title': te})


    else: #얘는 if request.method == 'POST': 얘랑 짝꿍이라 if request.method == 'POST':쟤 줄에 같이있어야한다
        forms = Key()
        return render(request, 'hello_app/key.html', {'form': forms,})  # 템플릿 파일 경로 지정, 데이터 전달
