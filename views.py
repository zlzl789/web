from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

from .forms import Key

def index(request):
    return render(request, 'poll/main.html')

def key_total(request):
    post = []  # 데이터베이스 안의 내용들이 한번씩 돌때마다 쌓여 담겨있어요 (포문안에쓰면 리셋되어 마지막꺼만 나옴)
    post_m=[] #모바일

    if request.method == 'POST':  # 포스트로 받은 값이 있다면
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}


        forms = Key(request.POST)  # HTTP가 인식하는 포스트의 모든값
        ke = forms.data['keyword']  # POST안에 있는 키 값
        Ke2 = forms.data['url']
        ab112 = ke.split('\r\n')



        for i123 in ab112:
            url = 'https://ad.search.naver.com/search.naver?where=ad&query={}'.format(i123)  # url 뒤로 i['pw']=키워드 값 넣기
            m_url = 'https://m.ad.search.naver.com/search.naver?where=m_expd&query={}'.format(i123)  # url 뒤로 i['pw']=키워드 값 넣기

            uurl = url + '&pagingIndex={}'  # 페이지 수

            if url:
                for n2 in range(1, 20):  # url페이지 수 100번 돌리기 포문
                    u_url = uurl.format(n2)  # url페이지 수 뒤로 n번만큼(100) 돌려라
                    reqe = requests.get(u_url, headers=headers).text  # 키워드넣은 값의 url을 갖고왔다
                    soup = BeautifulSoup(reqe, 'lxml', from_encoding='utf-8')  # url을 뷰티풀소프로 컴퓨터가 읽을수있는 html파일로 쪄버리기
                    titles_by_select = soup.select('ol.lst_type > li')  # a태그 선택하여 titles_by_select안에 담아요
                    if not titles_by_select:  # a태그가 없으면(값) 멈춰라
                        break

                    for titl in titles_by_select:
                        n = titl.get('num')  # 순위값
                        n1 = int(n)+1

                        title1 = titl.find('a', {'class': 'lnk_tit'})   # 사이트이름find
                        te = title1.text # 사이트이름

                        link = titl.find('a', {'class': 'url'})  # 화면상 url find
                        li = link.text # 화면상 url


                        if Ke2 in li:

                            dd={'num_b':n1,'tiel_b':te,'u_url':n2}
                            post.append(dd)

            if m_url:
                m_reqe = requests.get(m_url, headers=headers).text  # 키워드넣은 값의 url을 갖고왔다
                m_soup = BeautifulSoup(m_reqe, 'lxml', from_encoding='utf-8')  # url을 뷰티풀소프로 컴퓨터가 읽을수있는 html파일로 쪄버리기
                m_titles_by_select = m_soup.select('#contentsList > li > div')  # a태그 선택하여 titles_by_select안에 담아요


                for m_titl in m_titles_by_select:

                    n_m = m_titl.find('a', {'class': 'tit'})
                    n1_m = n_m.get('onclick')  # 순위값# 순위값
                    m_num = n1_m.split(',')[3]
                    m_num_b = m_num[:-2]



                    title1_m = m_titl.find('a', {'class': 'tit'})   # 사이트이름find
                    te_m = title1_m.text # 사이트이름

                    link_m = m_titl.find('cite', {'class': 'url'})  # 화면상 url find
                    li_m = link_m.text # 화면상 url


                    if Ke2 in li_m:

                        mm={'te_m':te_m,'m_num_b':m_num_b}
                        post_m.append(mm)


        if forms.is_valid():  # 폼 검증 #얘는 if request.method == 'POST': 안에 있어야 함
            return render(request, 'poll/key.html', {'form': forms, 'post': post,'post_m':post_m})


    else:  # 얘는 if request.method == 'POST': 얘랑 짝꿍이라 if request.method == 'POST':쟤 줄에 같이있어야한다
        forms = Key()
        return render(request, 'poll/key.html', {'form': forms })  # 템플릿 파일 경로 지정, 데이터 전달
