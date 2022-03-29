import tkinter as tk
import tkinter.scrolledtext as ScrolledText
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import threading
from tkinter import messagebox
from tkinter import filedialog

stop_or_not = 0;
def process(result,Input_user,Input_run_page,chromedriver_path,download_path):
    global stop_or_not
    stop_or_not=1

    try:
       browser = webdriver.Chrome(chromedriver_path)
    except:
       stop_or_not=0
    #browser = webdriver.Chrome(r'C:\Users\user\OneDrive\桌面\新增資料夾\chromedriver.exe')
    browser.get('https://www.ruten.com.tw/store/'+Input_user.get("1.0","end")+'/')
    maxpage =  browser.find_elements(By.XPATH,"//li[@class='page-num-info']")[0].text
    minpage = browser.find_elements(By.XPATH,"//li[@class='page-num-info']//span")[0].text
    time.sleep(5)

    if (len(Input_run_page)==1) and (Input_run_page.isdigit()==0):
      messagebox.askokcancel('Warning', '帳號'+Input_user.get("1.0","end")+'\n總共'+str(maxpage[len(minpage):])+'頁\n執行'+ str(maxpage[len(minpage):]) +'頁')
      maxpage = maxpage[len(minpage):]
    else:
      messagebox.askokcancel('Warning', '帳號 '+Input_user.get("1.0","end")+'\n總共'+str(maxpage[len(minpage):])+'頁\n執行'+ Input_run_page.replace("\n","") +'頁')
      maxpage = int(Input_run_page.replace("\n",""))
    index = 1
    all_item = {}
    item_index = 0
    while(index<=int(maxpage)):
        if stop_or_not==0:
           break
        browser.execute_script("""   
          (function () {   
            var y = document.body.scrollTop;   
            var step = 100;   
            window.scroll(0, y);   
  
  
            function f() {   
                if (y < document.body.scrollHeight) {   
                    y += step;   
                    window.scroll(0, y);   

                    setTimeout(f, 50);   
                }  
                else {   
                    window.scroll(0, y);   
                    document.title += "scroll-done";   
                }   
            }   
            setTimeout(f, 1000);   
        })();   
        """)  
        time.sleep(20)
        elems_url = browser.find_elements(By.XPATH, "//div[@class='rt-goods-list-item']")
        for e in elems_url:
           item_index = item_index +1
           all_item.update({str(item_index)+"_"+e.get_attribute('textContent').strip().split("\n")[0]+"_"+e.get_attribute('textContent').strip().split("\n")[1].strip():e.get_attribute('textContent').strip().split("\n")[2].strip()})
           result.insert('insert',str(item_index)+"_"+e.get_attribute('textContent').strip().split("\n")[0]+"_"+e.get_attribute('textContent').strip().split("\n")[1].strip()+" "+e.get_attribute('textContent').strip().split("\n")[2].strip()+"\n\n")
           
        if index<int(maxpage):
           browser.find_element(By.XPATH,"//li[@class='next']//a").click()
           #browser.find_element_by_xpath("//li[@class='next']//a").click()
        index = index+1
    if stop_or_not == 1:
        rank_1 = sorted(all_item.items(),key = lambda x:x[1],reverse = True)
        #f = open(r'C:\Users\user\OneDrive\桌面\新增資料夾\data.txt', 'w+', encoding='UTF-8')
        f = open(download_path+'\data.csv', 'w', encoding='UTF-8')
        f.write('商品名稱,銷售數,愛心\n')
        for key in range(len(rank_1)):
           f.write('"'+rank_1[key][0].split("_")[1]+'","'+rank_1[key][0].split("_")[2]+'","'+rank_1[key][1]+'"\n')
           f.flush()
        f.close()
    stop_or_not = 0
    messagebox.showinfo('Warning', '結束!!')

def start(result,Input_user,Input_run_page,window):
    global stop_or_not
    
    chromedriver_path = filedialog.askopenfilename(parent=window, title='選擇 chromedriver')
    download_path = filedialog.askdirectory(parent=window, title='設定下載資料 路徑')
      
    if stop_or_not ==0:
        MsgBox = tk.messagebox.askquestion('Warning','是否開始搜尋?')
        if MsgBox == 'yes':
           result.delete('1.0', 'end')
           t = threading.Thread(target=process,args=(result,Input_user,Input_run_page,chromedriver_path,download_path))
           t.start()
    else:
        messagebox.showinfo('Warning', '正在執行中!!請不要在執行一次')

def end():
    global stop_or_not
    MsgBox = tk.messagebox.askquestion('Warning','是否停止搜尋?')
    if MsgBox == 'yes':
       stop_or_not = 0
       print(stop_or_not)   

if __name__ == "__main__":
  window = tk.Tk()
  window.resizable(0,0)
  window.title('Ruten crawl')
  window.geometry("510x470+500+50")
  Input_user_label = tk.Label(window ,text='請輸入露天帳號',height=1,width=15)
  Input_user_label.place(x=28,y=50)
  Input_user = tk.Text(window,height=1,width=15)
  Input_user.place(x=130,y=52)
  
  Input_run_page_label = tk.Label(window ,text='尋找頁數',height=1,width=15)
  Input_run_page_label.place(x=235,y=50)
  Input_run_page = tk.Text(window,height=1,width=15)
  Input_run_page.place(x=320,y=52)
  Result= ScrolledText.ScrolledText(window, height=28,width=68,undo=True)
  Result.place(x=10,y=90)

  start_button = tk.Button(window,text = 'Start Search',command = lambda:start(Result,Input_user,Input_run_page.get("1.0","end"),window),height = 1,width = 20)
  start_button.place(x=10,y=10)
  stop_button = tk.Button(window,text = 'Stop Search',command = end,height = 1,width = 20)
  stop_button.place(x=350,y=10)
  window.mainloop()



