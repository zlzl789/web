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
            soup = BeautifulSoup(reqe, 'html.parser', from_encoding='utf-8')  # url을 뷰티풀소프로 컴퓨터가 읽을수있는 html파일로 쪄버리기
            titles_by_select = soup.select('ol.lst_type > li') # a태그 선택하여 titles_by_select안에 담아요
            if not titles_by_select:  # a태그가 없으면(값) 멈춰라
                break



            for titl in titles_by_select:  # titles_by_select안에 titl가 있는동안 도라라
                link = titl.find('a',{'class':'lnk_tit'})
                link_r = link.get('href')
                te = link.text  # te안에 titl을 텍스트인것들(쇼핑몰 이름)을 담아라! 잘 담김=프린트해봄
                link2 = titl.find('a',{'class':'sub_tit'})


                if link2:
                    link2_r = link2.get('href') #두번째 타이틀의 주소
                    te2 = link2.text #두번째 타이틀
                else:
                    te2 = ""
                    link2_r=""


                img = titl.find('img',{'class':'image'})
                if  img:
                    iimg = img.get('src')#이미지가 있을 시 src뒤로붙은 주소가져오기
                else:
                    iimg = "None"

                url_r = titl.find('a', {'class': 'url'})
                f_url = url_r.get('href')
                f_req = requests.get(f_url).text
                s_url = url_r.text # 화면의 나오는 url



                p_title = titl.find_all('p', 'ad_dsc')
                if  p_title:
                    p_text = p_title[0].text
                else:
                    p_text= ""

                p_title2 = titl.find('em',{'class':'point'})
                if  p_title2:
                    ret = titl.find_all('p', 'promotion')
                    p_title = titl.find_all('p', 'ad_dsc')
                    p_text = p_title[1].text
                    p_text2 = ret[0].text

                else:
                    p_text2 = ""


                po = []
                item = titl.find('ul',{'class':'lst_link'})
                if item:
                    re = item.find_all('a','link')
                    for i1 in re:
                        re1 = i1.text
                        re11 = i1.get('href')

                        du = {'url':re11,'tit':re1}
                        po.append(du)
                else:
                    po = ""



                pi = []
                item2 = titl.find('ul',{'class':'lst_price'})
                if item2:
                    re2 = item2.find_all('a','link')
                    for i2 in re2:
                        re2 = i2.text
                        ree = i2.get('href')

                        d = {'url_1':ree,'tit_1':re2}
                        pi.append(d)
                else:
                    pi = ""



                il = titl.find_all('em','txt')
                ir = il[0].text #광고집행기간

                cur = connection.cursor()
                string = "select * from topic"
                cur.execute(string)
                see = cur.fetchall()

                post1 = []
                for t in see:  # 데이터베이스와 url 비교하는구문
                    if t[2] in f_req:
                        di = t[1]
                        post1.append(di)

                    dd = {'img':iimg,'site': te, 'site2':te2 ,'f_url':f_url , 'te':ir, 'p':p_text,'p_text2':p_text2, 'title': post1, 'link_k':link_r,'link2_r':link2_r,'s_url':s_url,'po':po,'pi':pi}



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
        url = 'http://search.daum.net/search?w=ad&q={}'.format(ke)  # 네이버 파워링크 url 뒤로 키워드값 넣기
        uurl = url + '&p={}'  # 페이지 수
        req = requests.get(url, headers=headers)  # 키워드넣은 값의 url을 갖고왔다
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        total = soup.select('body.daum')

        for at in total:
            art = at.text
            r = art.split('totalCount:')[1]
            d = r[1]+r[2]

            dew=int(d)
            gr = dew/20
            result = round(gr+1)

        for n in range(1,result):  # url페이지 수 100번 돌리기 포문
            print(n)

            u_url = uurl.format(n)  # url페이지 수 뒤로 n번만큼(100) 돌려라
            reqe = requests.get(u_url, headers=headers)  # 키워드넣은 값의 url을 갖고왔다

            html2 = reqe.text
            soup2 = BeautifulSoup(html2, 'html.parser')
            titles_by_select = soup2.select(' div.coll_cont > div > ul > li > div > div > div.wrap_tit.mg_tit > a')  # a태그 선택하여 titles_by_select안에 담아요

            for titl in titles_by_select:  # titles_by_select안에 titl가 있는동안 도라라
                te = titl.text  # te안에 titl을 텍스트인것들(쇼핑몰 이름)을 담아라! 잘 담김=프린트해봄
                f_url = titl.get('href')  # f_url안에 쇼핑몰의 주소를 담아라~ 프린트해봄!

                try:
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
                except:
                    pass

                post.append(dd)

        if forms.is_valid():  # 폼 검증 #얘는 if request.method == 'POST': 안에 있어야 함
            return render(request, 'hello_app/d_key.html', {'form': forms, 'post': post})

    else:  # 얘는 if request.method == 'POST': 얘랑 짝꿍이라 if request.method == 'POST':쟤 줄에 같이있어야한다
        forms = Key1()
        return render(request, 'hello_app/d_key.html', {'form': forms, })  # 템플릿 파일 경로 지정, 데이터 전달






