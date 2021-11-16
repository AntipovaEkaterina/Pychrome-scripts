from typing import Text
import subprocess
import time
import pychrome
from pychrome import tab

SEARCH_KLO_LOC = '[name="email"].big_text'            #локатор поля для ввода логина
SEARCH_KPA_LOC = '[name="pass"].big_text'             #локатор поля для ввода пароля
SEARCH_ENT_LOC = '.index_login_button'                #локатор для кнопки войти
SEARCH_MES_LOC = '[href="/im"]'                       #ссылка на переход в мессенджер
SEARCH_NAS_LOC = '.TopNavBtn__profileName'            #локатор для кнопки раскрывающее настройки
SEARCH_EXT_LOC = 'a#top_logout_link.top_profile_mrow' #локатор для кнопки выйти
SEARCH_COMMUN_LOC = '.im_editable'                    #локатор для пола ввода сообщения
SEARCH_SEND_LOC = '.im-send-btn.im-chat-input--send'  #локатора для кнопки отправить 

def fieldId(node_id, selector):  #нахождение элемента по ключу
    return tab.call_method("DOM.querySelector", nodeId=node_id, selector=selector)["nodeId"] 

def get_click_coords(node_id):
    box_model = tab.call_method("DOM.getBoxModel", nodeId=node_id)["model"]["content"]
    return box_model[0], box_model[1]

def mouseClick(tab, xCoord, yCoord):
    tab.call_method("Input.dispatchMouseEvent", type="mousePressed", x=xCoord, y=yCoord, button="left", clickCount=1)
    tab.call_method("Input.dispatchMouseEvent", type="mouseReleased", x=xCoord, y=yCoord, button="left", clickCount=1)

def findField(selector):
    tab.call_method("DOM.enable")#read
    id_root = tab.call_method("DOM.getDocument")["root"]["nodeId"] #getDocument возвращает корень всего документа 
    input_log = fieldId(node_id=id_root, selector=selector)
    input_field_box_model = get_click_coords(node_id=input_log)
    mouseClick(tab, input_field_box_model[0], input_field_box_model[1])

subprocess.Popen("C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir=remote-profile")  
time.sleep(5)

browser = pychrome.Browser(url='http://127.0.0.1:9222') 
tab = browser.new_tab()

tab.start()
tab.call_method("Network.enable")
tab.call_method("Page.navigate", url="https://vk.com/", _timeout=5) 
time.sleep(5)

#находим поле для ввода логина и пароля и вводим пароль
input_key_log = findField(selector=SEARCH_KLO_LOC)
tab.call_method("Input.insertText", text="****")
"""
input_key_log = fieldId(node_id=rootId, selector=SEARCH_KLO_LOC)
input_field_box_model = get_click_coords(node_id=input_key_log)
mouseClick(tab, input_field_box_model[0], input_field_box_model[1]) #мы нашли в странице поле ввода и кликнули тут на него 
tab.call_method("Input.insertText", text="****")
"""
#находим поле ввода логина и вводим пароль
input_key_pas = findField(selector=SEARCH_KPA_LOC)
tab.call_method("Input.insertText", text="***")
tab.wait(2)
#находим кнопку войти, нажимаем и должны войти в вк
input_entrance = findField(selector=SEARCH_ENT_LOC)
time.sleep(10)
#перейти в сообщения
input_mes = findField(selector=SEARCH_MES_LOC)
tab.wait(5)
#переходим в диалог
tab.call_method("Page.navigate", url="****", _timeout=5) 
time.sleep(5)
#отправляем 5 сообщений циклом
for i in range(2):
    #пишем сообщение 
    input_communication = findField(selector=SEARCH_COMMUN_LOC)
    tab.call_method("Input.insertText", text="это только ради науки")
    tab.wait(3)
    #нажимаем на кнопку отправить сообщение
    input_send = findField(selector=SEARCH_SEND_LOC)

tab.call_method("Network.clearBrowserCache")
"""
#ВОзвращяемся обратно в новостную ленту чтобы выйти из вк
tab.call_method("Page.navigate", url="https://vk.com/feed", _timeout=5) 
time.sleep(5)
#нажимаем на настройки чтобы выйти. 
input_nas = findField(selector=SEARCH_NAS_LOC)
tab.wait(2)
input_exit = findField(selector=SEARCH_EXT_LOC)

tab.wait(10)
#очистка кэша браузера
#tab.Network.clearBrowserCache()
#tab.call_method("Network.clearBrowserCache")
"""
tab.stop()
browser.close_tab(tab) #