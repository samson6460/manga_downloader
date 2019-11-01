import requests
from bs4 import BeautifulSoup
import re
import os
import threading

def download_pic(url, path):
    pic = requests.get(url) #使用GET 對圖片路徑發出請求
    f = open(path,'wb') #以設定好的名稱建立一個檔案
    f.write(pic.content) #將回應物件的content寫入檔案中
    f.close() #關閉檔案

def get_manga():
    manga_name = input("請輸入要下載的漫畫名稱: ")
    url = "https://www.98comic.com/list/wd-" + manga_name + "/" #設定url
    html = requests.get(url) #GET請求
    html.encoding = 'utf-8' #指定編碼為utf-8

    bs = BeautifulSoup(html.text, 'lxml') #解析網頁
    manga_list = bs.find_all('a', {'class': 'bcover'}) 
    #搜尋所有標籤為a, class為'bcover'的元素
    if len(manga_list) == 0:
        print("無搜尋結果")
        return None, None
    else:
        for i in range(len(manga_list)):
            print(i+1, manga_list[i].get('title'))
    num = int(input("請問要下載哪個(請輸入數字): "))
    while(num <= 0 or num > len(manga_list)):
        num=int(input("超出範圍, 請再輸入一次: "))
    manga_name = manga_list[num-1].get('title')
    manga_url = "https://www.98comic.com" + manga_list[num-1].get('href')
    return manga_name, manga_url

def get_chapter(manga_url):
    html = requests.get(manga_url) #GET請求
    html.encoding = 'utf-8'
    bs = BeautifulSoup(html.text, 'lxml')
    print("目前更新至:"+bs.find('a', {'class': 'blue'}).text) #顯示漫畫更新進度   
    chapter_list = bs.find_all('a', {'class': 'status0'}) 
    #搜尋所有標籤為a, class為'status0'的元素
    chapter_name = []
    chapter_url = []
    for i in chapter_list:
        chapter_name.append(i.get('title'))
        chapter_url.append("https://www.98comic.com" + i.get('href'))
    return chapter_name, chapter_url

def download_chapter(manga_name, chapter_name, chapter_url):
    if not os.path.exists(manga_name + os.sep + chapter_name):
        os.mkdir(manga_name + os.sep + chapter_name)
        print("建立資料夾: " + chapter_name)
    else:
        print(chapter_name + " 資料夾已存在")
    html = requests.get(chapter_url) #GET請求
    html.encoding ='utf-8'
    bs = BeautifulSoup(html.text, 'lxml')
    
    script = bs.find_all('script') #搜尋所有標籤為script元素
    script = str(script) #將script轉為字串
    script = re.sub(r'[\s]', '', script) #去除所有空白字元
    cid = re.search(r'cid\':(.*),\'ncid', script) #搜尋cid的位置
    cid = cid.group(1) #取出要保留的文字
    fs = re.search(r'fs\':\[(.*)\],\'fc', script) #搜尋fs的位置
    download_list=fs.group(1).split(',')#取出要保留的文字並轉成list
    for i in range(len(download_list)):
        pic_url = "https://www.98comic.com/g.php?" + cid + "/" + download_list[i][1:-1] #設定圖片的下載路徑
        pic_path = manga_name + os.sep + chapter_name + os.sep + str(i+1) + ".jpg" #設定圖片的名稱和儲存路徑
        if not os.path.exists(pic_path):
            download_pic(pic_url, pic_path) #下載圖片
            
def download_manga(ran, manga_name, chapter_name, chapter_url):
    threads = []
    for i in range(ran[0]-1,ran[1]):
        threads.append(threading.Thread(target = download_chapter, args = (manga_name, chapter_name[i], chapter_url[i])))
        threads[i-(ran[0]-1)].start()                
    for i in threads:
        i.join()
