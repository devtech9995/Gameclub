from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import soundfile
import speech_recognition as sr
import os
import random
import urllib
import pandas as pd
import certifi
import math
from datetime import datetime, timedelta
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

flag_gameclub = False
flag_rmt = False
flag_rmt = False
list_bot = Flask(__name__)
CORS(list_bot)

@list_bot.route('/get-status', methods=["GET"])
def get_status():
    with open('status.txt','r',encoding="utf_8_sig") as file:
        status_text = file.read()
    # print(status_text)
    return jsonify({"status_text":status_text})
@list_bot.route('/get-status_rmt', methods=["GET"])
def get_status_rmt():
    with open('status_rmt.txt','r',encoding="utf_8_sig") as file:
        status_text_rmt = file.read()
    # print(status_text_rmt)
    return jsonify({"status_text_rmt":status_text_rmt})
@list_bot.route('/gameclub_close', methods=["GET", "POST"])
def gameclub_close():
    global flag_gameclub
    flag_gameclub = request.json['flag_gameclub']
    print("success", flag_gameclub)
    return jsonify({'success':True})
@list_bot.route('/rmt_close', methods=["GET", "POST"])
def rmt_close():
    global flag_gameclub
    flag_rmt = request.json['flag_rmt']
    print("success", flag_rmt)
    return jsonify({'success':True})
@list_bot.route('/gameclub', methods=["GET", "POST"])
def backend():
    global flag_gameclub
    mode = request.json['mode']
    startTime = request.json['startTime']
    endTime = request.json['endTime']
    switch = request.json['select']
    play_startTime = request.json['play_startTime']
    play_endTime = request.json['play_endTime']
    flag_gameclub = request.json['flag_gameclub']
    print(flag_gameclub)
    if flag_gameclub:
        end_obj = datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        # end_obj += timedelta(hours=9)
        start_obj = datetime.strptime(startTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        # start_obj += timedelta(hours=9)
        if switch == True:
            while True:
                current_obj = datetime.now()
                print(start_obj)
                print(end_obj)
                print(f"waiting...      {current_obj}")
                if (current_obj >= start_obj):
                    if start_obj <= end_obj:
                        break
                    else:
                        # try:
                            
                        # messagebox.showinfo("アラート", "稼働時間を正しく入力してください！")
                        # break
                        pass
        username = "rmt@k-andi.co.jp"
        password = "Ez9ubrcG"
        
        # Go to site
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome()
        with open('status.txt','w',encoding="utf_8_sig") as file:
            file.write("稼働を開始しました。")
        driver.get('https://gameclub.jp')

        # Press the sell button
        sell_button = driver.find_element("xpath", "//i[@class='fas fa-camera']")
        sell_button.click()

        with open('status.txt','w',encoding="utf_8_sig") as file:
            file.write("ログイン中です…")
        # Input email and password
        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys(username)
        time.sleep(2)
        pwd_input = driver.find_element(By.NAME, "password")
        pwd_input.send_keys(password)
        time.sleep(2)

        # Click the captcha button
        recaptcha = driver.find_element(By.XPATH, "//div[@class = 'g-recaptcha']")
        recaptcha.click()
        time.sleep(10)

        #Judge the status of check
        driver.switch_to.default_content()
        check_status = driver.find_element(By.XPATH, "//div[5]")
        status = check_status.value_of_css_property("visibility")
        print(status)

        if status != "hidden":
            with open('status.txt','w',encoding="utf_8_sig") as file:
                file.write("Captcha認証の突破中です…")
            
            # Get audio challenge
            driver.switch_to.default_content()
            frames=driver.find_element(By.XPATH, "//div[5]").find_elements(By.TAG_NAME, "iframe")
            driver.switch_to.frame(frames[0])
            driver.find_element(By.ID, "recaptcha-audio-button").click()

            # Click the play button
            driver.switch_to.default_content()   
            frames= driver.find_elements(By.TAG_NAME, "iframe")
            driver.switch_to.frame(frames[-1])
            time.sleep(2)
            driver.find_element(By.XPATH, "//div/div//div[3]/div/button").click()

            #get the mp3 audio file
            src = driver.find_element(By.ID, "audio-source").get_attribute("src")
            # print("[INFO] Audio src: %s"%src)   

            #download the mp3 audio file from the source
            file_path = os.path.join(os.getcwd(), "captcha.wav")
            # print(file_path)
            urllib.request.urlretrieve(src, file_path)

            data,samplerate=soundfile.read('captcha.wav')
            soundfile.write('new.wav',data,samplerate, subtype='PCM_16')
            r=sr.Recognizer()
            try:
                with sr.AudioFile("new.wav") as source:
                    audio_data=r.record(source)
                    text=r.recognize_google(audio_data)
            except:
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。")
                # print(text)

            # Click the verify button
            driver.find_element(By.ID, "audio-response").send_keys(text)
            driver.find_element(By.ID, "recaptcha-verify-button").click()

        time.sleep(5) 
        try:
            driver.switch_to.default_content()
            login_click = driver.find_element(By.XPATH,"//button[@class='btn btn-danger btn-registration']")
            login_click.click()
            print("login!")
            with open('status.txt','w',encoding="utf_8_sig") as file:
                file.write("ログインが完了しました。")
            
        except:
            with open('status.txt','w',encoding="utf_8_sig") as file:
                file.write("エラーが発生した。(captcha)")
            
        time.sleep(3)
        print(str(start_obj))
        print(str(end_obj))
        
        index11 = 0
        # flag = True
        while flag_gameclub:
            print(flag_gameclub)
            # end_obj = datetime.strptime(endTime, '%Y-%m-%dT%H:%M:%S.%fZ')
            # end_obj += timedelta(hours=9)
            current_obj = datetime.now()
            # print(end_obj)
            # print(current_obj)
            if current_obj >= end_obj:
                flag_gameclub = False
                print("The tool is closed")
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("設定してください。")
                break
            
            googlesheetid='1uXXG0LjOf6xIr3mqimVH6Kcwkj-tYZ_oLOpgYlQJAnA'
            sheetname='Gameclub.jp'
            url=f"https://docs.google.com/spreadsheets/d/{googlesheetid}/gviz/tq?tqx=out:csv&sheet={sheetname}"
            content=pd.read_csv(url)
            
            # mode setting
            if mode == 'automate':
                check_status = True
            else:
                check_status = content.iloc[index11, 0]
            
            # exhibit only when the check is activated   
            if not check_status:
                index11 += 1
                continue
            
            if math.isnan(content.iloc[index11, 1]):
                index11 = 0
                continue
            
            # index11 = 0
            with open('status.txt','w',encoding="utf_8_sig") as file:
                file.write("出品中です…")
            upload_Image = content.iloc[index11,2]
            # upload_Image = r"/Users/Superman/Downloads/10000.jpg"
            try:
                driver.find_element(By.XPATH, "//input[@type='file']").send_keys(upload_Image)
            except:
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(画像)")
            
            try:
                search = driver.find_element(By.ID, "btn-search-title")
            except:
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(title_button)")
            search.click()
            
            time.sleep(20)
            
            try:
                search_title = driver.find_element(By.ID, "search-title-input")
            except:
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(title_input)")
            search_title.send_keys(content.iloc[index11,3])

            time.sleep(5)
            try:
                item = driver.find_element(By.XPATH, "//div[@class='item']")
            except:
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。()")
            item.click()

            time.sleep(3)

            if content.iloc[index11,4] == "代行":
                try:
                    radio = driver.find_element(By.ID, "account-type-id-40")
                except:
                    with open('status.txt','w',encoding="utf_8_sig") as file:
                        file.write("エラーが発生した。(40)")
            else:
                try:
                    radio = driver.find_element(By.ID, "account-type-id-10")
                except:
                    with open('status.txt','w',encoding="utf_8_sig") as file:
                        file.write("エラーが発生した。(10)")
            radio.click()
            try:
                name = driver.find_element(By.NAME, "name")
            except:
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(name)")
            name.send_keys(content.iloc[index11,5])

            try:
                detail = driver.find_element(By.NAME, "detail")
            except:
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(detail)")
            detail.send_keys(content.iloc[index11,6])
            try:
                if not math.isnan(content.iloc[index11, 7]):
                    member = driver.find_element(By.NAME, "subcategory_unique_property_1_value")
                    member.send_keys(int(content.iloc[index11, 7]))
            except:
                print("登録時間を設定できません。")
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("設定してください。(property_1)")
                pass
            
            try:
                if not math.isnan(content.iloc[index11, 8]):
                    circle = driver.find_element(By.NAME, "subcategory_unique_property_2_value")
                    circle.send_keys(int(content.iloc[index11, 8]))
            except:
                print("再生回数を設定できません。")
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("設定してください。(property_2)")
                pass
            
            try:
                if not math.isnan(content.iloc[index11, 9]):
                    retry_time = driver.find_element(By.NAME, "subcategory_unique_property_3_value")
                    retry_time.send_keys(int(content.iloc[index11, 9]))
            except:
                print("再生時間を設定できません。")
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("設定してください。(property_3)")
                pass
            
            try:
                if not math.isnan(content.iloc[index11, 10]):
                    rate = driver.find_element(By.NAME, "subcategory_unique_property_4_value")
                    rate.send_keys(int(content.iloc[index11, 10]))
            except:
                print("高評価数を設定できません。")
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("設定してください。(property_4)")
                pass
            
            try:
                if not isinstance(content.iloc[index11, 11], (int, float)):
                    notice = driver.find_element(By.NAME, "notice_information")
                    notice.send_keys(content.iloc[index11,11])
            except:
                print("収益/月（直近）を設定できません。")
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("設定してください。(notice)")
                pass

            price_budget = int(content.iloc[index11, 12])
            try:
                price = driver.find_element(By.NAME, "price")
            except:
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(price)")
            price.send_keys(price_budget)

            try:
                confirm_button = driver.find_element(By.ID, "btn-confirm")
            except:
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(check_btn)")
            confirm_button.click()

            time.sleep(3)
            try:
                add_button = driver.find_element(By.ID, "btn-add")
            except:
                print("エラーが発生した。")
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(add_btn)")
                # pass
            add_button.click()
            with open('status.txt','w',encoding="utf_8_sig") as file:
                file.write("出品が完了しました。")
            time.sleep(3)
            try:
                close_button = driver.find_element(By.XPATH, "//*[@id='content-wrapper']/div/div[2]/div[8]/div/div[1]/i")
            except:
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(wrapper1)")
            close_button.click()
            
            current_obj = datetime.now()
            if current_obj >= end_obj:
                flag_gameclub = False
                print("The tool is closed")
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("設定してください。")
                break

            time1 = int(play_startTime) * 60
            time2 = int(play_endTime) * 60
            wait_time = random.uniform(time1, time2)
            print(wait_time)
            
            current_obj = datetime.now()
            wait_delta = timedelta(seconds=wait_time)
            if (current_obj+wait_delta) >= end_obj:
                flag_gameclub = False
                print("The tool is closed")
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("設定してください。")
                break
            
            with open('status.txt','w',encoding="utf_8_sig") as file:
                file.write("待機中です…")
            print(flag_gameclub)
            time.sleep(wait_time)
            print(flag_gameclub)
            
            try:
                return_button = driver.find_element(By.XPATH, "//*[@id='content-wrapper']/header/div/div[2]/div[2]/a[2]")
            except:
                print("エラーが発生した。")
                with open('status.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(wrapper2)")
            return_button.click()
            index11 = index11 + 1
            print(index11)
        
        with open('status.txt','w',encoding="utf_8_sig") as file:
            file.write("設定してください。")
        driver.quit()
        
        # Return the recognized text
        return jsonify({'mode': mode,
                        'starTime': startTime,
                        'endTime': endTime,
                        'switch': switch,
                        'play_startTime': play_startTime,
                        'play_endTime': play_endTime})

@list_bot.route('/rmt', methods=["GET", "POST"])
def backend_rmt():
    mode_rmt = request.json['mode']
    startTime_rmt = request.json['startTime']
    endTime_rmt = request.json['endTime']
    switch_rmt = request.json['select']
    play_startTime_rmt = request.json['play_startTime']
    play_endTime_rmt = request.json['play_endTime']
    flag_rmt = request.json['flag_rmt']
    print(flag_rmt)
    if flag_rmt:
        current_obj = datetime.now()
        end_obj = datetime.strptime(endTime_rmt, '%Y-%m-%dT%H:%M:%S.%fZ')
        # end_obj += timedelta(hours=9)
        start_obj = datetime.strptime(startTime_rmt, '%Y-%m-%dT%H:%M:%S.%fZ')
        # start_obj += timedelta(hours=9)
        if switch_rmt == True:
            print("start_obj", start_obj)
            print("end_obj", end_obj)
            while True:
                current_obj = datetime.now()
                print(f"waiting...      {current_obj}")
                if (current_obj >= start_obj):
                    if start_obj <= end_obj:
                        break
                    else:
                        # try:
                            
                        # messagebox.showinfo("アラート", "稼働時間を正しく入力してください！")
                        # break
                        pass
        username = "rmt@k-andi.co.jp"
        password = "FKrAd7kQk7sLPb"
        
        # Go to site
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome()
        with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
            file.write("稼働を開始しました。")
        driver.get('https://rmt.club/')

        # Press the sell button
        sell_button = driver.find_element("xpath", "//img[@class= 'top_slide_pc']")
        sell_button.click()

        with open('status_rmt).txt','w',encoding="utf_8_sig") as file:
            file.write("ログイン中です…")
        # Input email and password
        email_input = driver.find_element(By.NAME, "data[User][mail]")
        email_input.send_keys(username)
        time.sleep(1)
        pwd_input = driver.find_element(By.NAME, "data[User][password]")
        pwd_input.send_keys(password)
        time.sleep(3)

        # Click the captcha button
        recaptcha = driver.find_element(By.XPATH, "//div[@class = 'g-recaptcha']")
        recaptcha.click()
        time.sleep(10)

        #Judge the status of check
        div_elements = driver.find_elements(By.XPATH, "//body/div")
        # print(len(div_elements))
        check_status = div_elements[-1]
        status = check_status.value_of_css_property("visibility")
        # print(status)

        if status != "hidden":
            with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                file.write("Captcha認証の突破中です…")
            # Get audio challenge
            driver.switch_to.default_content()
            frames = driver.find_element(By.XPATH, "//div[3]/div[4]/iframe")
            driver.switch_to.frame(frames)
            driver.find_element(By.ID, "recaptcha-audio-button").click()

            # Click the play button
            driver.switch_to.default_content()   
            frames= driver.find_elements(By.TAG_NAME, "iframe")
            driver.switch_to.frame(frames[-1])
            time.sleep(2)
            driver.find_element(By.XPATH, "//div/div//div[3]/div/button").click()

            #get the mp3 audio file
            src = driver.find_element(By.ID, "audio-source").get_attribute("src")
            # print("[INFO] Audio src: %s"%src)

            #download the mp3 audio file from the source
            file_path = os.path.join(os.getcwd(), "captcha1.wav")
            # print(file_path)
            urllib.request.urlretrieve(src, file_path)

            data,samplerate=soundfile.read('captcha1.wav')
            soundfile.write('rmt.wav',data,samplerate, subtype='PCM_16')
            r=sr.Recognizer()
            with sr.AudioFile("rmt.wav") as source:
                audio_data=r.record(source)
                text=r.recognize_google(audio_data)
                print(text)
            time.sleep(5)

            # Click the verify button
            driver.find_element(By.ID, "audio-response").send_keys(text)
            time.sleep(2)
            driver.find_element(By.ID, "recaptcha-verify-button").click()

        time.sleep(2) 
        try:
            driver.switch_to.default_content()
            login_click = driver.find_element("xpath", "//input[@class='btn_type1 fade']")
            login_click.click()
            with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                file.write("ログインが完了しました。")
            
        except:
            with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                file.write("エラーが発生した。(type)")
            
        time.sleep(3)
        
        index11 = 1
        # flag = True
        while flag_rmt:
            print(flag_rmt)
            # end_obj = datetime.strptime(endTime_rmt, '%Y-%m-%dT%H:%M:%S.%fZ')
            # end_obj += timedelta(hours=9)
            # print(end_obj)
            # print(current_obj)
            if current_obj >= end_obj:
                flag_rmt = False
                print("The tool is closed")
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("設定してください。")
                break
            
            googlesheetid='1uXXG0LjOf6xIr3mqimVH6Kcwkj-tYZ_oLOpgYlQJAnA'
            sheetname='RMT.club'
            url=f"https://docs.google.com/spreadsheets/d/{googlesheetid}/gviz/tq?tqx=out:csv&sheet={sheetname}"
            content=pd.read_csv(url)
            
            # mode setting
            if mode_rmt == 'automate':
                check_status = True
            else:
                check_status = content.iloc[index11, 0]
            
            # exhibit only when the check is activated   
            if not check_status:
                index11 += 1
                continue
            
            print(math.isnan(content.iloc[index11, 1]), "code")
            if math.isnan(content.iloc[index11, 1]):
                index11 = 1
                continue
            
            # index11 = 0
            with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                file.write("出品中です…")
            try:
                display_button = driver.find_element("xpath", "//img[@class= 'top_slide_pc']")
            except:
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(list)")
            display_button.click()

            time.sleep(2)
            try:
                sale_button = driver.find_element("xpath", "//label[@for='DealRequest0']")
            except:
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(sale_btn)")
            sale_button.click()

            try:
                game_name = driver.find_element(By.NAME, "data[Deal][game_title]")
            except:
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(name)")
            game_name.send_keys(content.iloc[index11,2])

            try:
                publication_title = driver.find_element(By.NAME, "data[Deal][deal_title]")
            except:
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(title)")
            publication_title.send_keys(content.iloc[index11,3])

            try:
                tag = driver.find_element(By.NAME, "data[Deal][tag]")
            except:
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(tag)")
            tag.send_keys(content.iloc[index11,4])

            try:
                detail = driver.find_element(By.NAME, "data[Deal][info]")
            except:
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(detail)")
            detail.send_keys(content.iloc[index11,5])

            upload_Image = content.iloc[index11,6]
            # upload_Image = r"/Users/Superman/Downloads/10000.jpg"
            try:
                driver.find_element(By.XPATH, "//input[@type='file']").send_keys(upload_Image)
            except:
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(画像)")

            price_budget = int(content.iloc[index11,7])
            try:
                price = driver.find_element(By.NAME, "data[Deal][deal_price]")
            except:
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(price)")
            price.send_keys(price_budget)

            try:
                confirm_button = driver.find_element(By.NAME, "smt_confirm")
            except:
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(confirm)")
            confirm_button.click()

            time.sleep(8)
            try:
                agree_button = driver.find_element(By.NAME, "data[Deal][agreement]")
            except:
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(agree_btn)")
            agree_button.click()

            try:
                finish_button = driver.find_element(By.NAME, "smt_finish")
            except:
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("エラーが発生した。(finish_btn)")
            finish_button.click()
            with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                file.write("出品が完了しました。")
            
            current_obj = datetime.now()
            if current_obj >= end_obj:
                flag_rmt = False
                print("The tool is closed")
                with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                    file.write("設定してください。")
                break

            time1 = int(play_startTime_rmt) * 60
            time2 = int(play_endTime_rmt) * 60
            wait_time = random.uniform(time1, time2)
            # print(wait_time)
            
            current_obj = datetime.now()
            wait_delta = timedelta(seconds=wait_time)
            if (current_obj+wait_delta) >= end_obj:
                flag_rmt = False
                print("The tool is closed")
                break
            
            with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                file.write("待機中です…")
            time.sleep(wait_time)
            
            index11 = index11 + 1
            print(index11)
        
        with open('status_rmt.txt','w',encoding="utf_8_sig") as file:
                file.write("設定してください。")
        driver.quit()
        
        # Return the recognized text
        return jsonify({'mode': mode_rmt,
                        'starTime': startTime_rmt,
                        'endTime': endTime_rmt,
                        'switch': switch_rmt,
                        'play_startTime': play_startTime_rmt,
                        'play_endTime': play_endTime_rmt})

if __name__ == '__main__':
    # list_bot.run("localhost", 5000)
    list_bot.run("ec2-34-224-4-175.compute-1.amazonaws.com", 5000)