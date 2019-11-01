import manga_module as m #匯入自訂模組
import os
        
manga_name, manga_url = m.get_manga() #取得漫畫名稱與連結

if not os.path.exists(manga_name):
    os.mkdir(manga_name) #以漫畫名稱建立資料夾
    print("建立資料夾: " + manga_name)
else:
    print(manga_name + " 資料夾已存在")
        
chapter_name, chapter_url = m.get_chapter(manga_url) #取得章節名稱和連結

print("總共有", len(chapter_url), "個") #顯示章節總數
start_num = int(input("請問要從第幾個開始下載(請輸入數字): ")) 
end_num = int(input("請問要下載到第幾個(請輸入數字): "))
print("開始下載")
m.download_manga((start_num, end_num), manga_name, chapter_name, chapter_url) #下載漫畫
print("下載完畢")