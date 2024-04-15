from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import sqlite3
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException

# SQLite veritabanı bağlantısı oluşturma
conn = sqlite3.connect('hr_chatbot.db')
c = conn.cursor()

# Veritabanı tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS questions
             (id INTEGER PRIMARY KEY, job_title_id TEXT, skill_level_id TEXT, category_id TEXT, evaluator_id TEXT , question_type TEXT, language_id TEXT, question TEXT, answer TEXT)''')

# Veritabanından dil, iş pozisyonu, beceri seviyesi ve kategori bilgilerini çekme
c.execute("SELECT id, job_title_name FROM job_titles")
job_titles = c.fetchall()

c.execute("SELECT id, level_name FROM skill_level")
skill_levels = c.fetchall()

c.execute("SELECT id, category_name FROM categories")
categories = c.fetchall()

c.execute("SELECT id, evaluator_type_name FROM evaluator")
evaluators = c.fetchall()

c.execute("SELECT id, language_name FROM language")
languages = c.fetchall()

def select_option_by_text(select_element, option_text):
    for option in select_element.find_elements(By.TAG_NAME, 'option'):
        if option.text.strip() == option_text:
            option.click()
            break


def scrape_and_save():
    # Job title'i giriş kutusuna yazma
    for job_title_id, job_title_name in job_titles:
        for skill_level_id, skill_level_name in skill_levels:
            for category_id, category_name in categories:
                for evaluator_id, evaluator_name in evaluators:
                    for language_id, language_name in languages:
                        try:
                            job_title_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div.styles_input__9RnCm.undefined.styles_JTInput__flMU5.styles_wide__QYOEu > input')))
                            job_title_input.click()
                            job_title_input.clear()
                            job_title_input.send_keys(job_title_name)
                        except ElementClickInterceptedException:
                            print("Element tıklanabilir değil, sayfa yenileniyor...")
                            driver.refresh()
                            try:
                                close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.styles_SmallButton__v-MHQ.CloseButton')))
                                close_button.click()
                                job_title_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div.styles_input__9RnCm.undefined.styles_JTInput__flMU5.styles_wide__QYOEu > input')))
                                job_title_input.click()
                                job_title_input.clear()
                                job_title_input.send_keys(job_title_name)
                            except TimeoutException:
                                print("Element tıklanabilir değil, işlem gerçekleştirilemiyor.")
                        
                        # Zorluk seviyesini seçme
                        skill_level_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div:nth-child(2) > select')))
                        select_option_by_text(skill_level_select, skill_level_name)
                        
                        # Soru tipini seçme
                        category_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div:nth-child(3) > select')))
                        select_option_by_text(category_select, category_name)
                        
                        # Dil seçeneğini belirleme (varsa)


                        if language_name:
                            language_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div.styles_SelectMenuWrapper__onWBr.styles_LangSelect__DbruI > div.styles_input__Xoi8Y.undefined > input[type=text]')))
                            select_option_by_text(language_select,language_name)
                        
                        
                        # Generate butonuna tıklama
                        generate_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > button')))
                        generate_button.click()
                        
                        #  Show Answers butonuna sadece ilk iterasyonda tıklama
                        try :
                            show_answers_button = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo.styles_IC_expanded__paAaR > div.styles_Container__EnYDl.styles_ContainerActive__-e3Z6.styles_contentBody__56j3w > div.styles_MainHeading__AV-pn > div > div')))
                            if scrape_and_save.first_iteration:
                                    show_answers_button.click()
                                    scrape_and_save.first_iteration = False
                                
                        except Exception as e:
                            print("Generate butonuna tıklanırken bir hata oluştu:", str(e) ,"Yeniden generate ediliyor.")
                            # Generate butonuna tıklama
                            generate_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > button')))
                            generate_button.click()
                            try :
                                show_answers_button = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo.styles_IC_expanded__paAaR > div.styles_Container__EnYDl.styles_ContainerActive__-e3Z6.styles_contentBody__56j3w > div.styles_MainHeading__AV-pn > div > div')))
                                if scrape_and_save.first_iteration:
                                    show_answers_button.click()
                                    scrape_and_save.first_iteration = False
                            except Exception as e:
                                    print("Show Answers butonu bulunamadı veya tıklanabilir değil.")


                        # Soru ve cevapları bulma
                        question_elements = WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.XPATH, "//span[@class='styles_Question__FRNnc']")))
                        try:
                            answer_elements = WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.XPATH, "//p[@class='styles_AnswerText__Y1oHC']")))
                        except Exception as e:
                            print("Answers bulunamadı veya Show answers tekrar tıklandı.")
                            show_answers_button.click()
                            scrape_and_save.first_iteration = False
                            answer_elements = WebDriverWait(driver, 100).until(EC.visibility_of_all_elements_located((By.XPATH, "//p[@class='styles_AnswerText__Y1oHC']")))

                        # Soru ve cevapları ekrana yazdırma
                        for question, answer in zip(question_elements, answer_elements):
                            # Soru tipini belirleme

                            question_heading = question.find_element(By.XPATH, "./ancestor::div[@class='styles_Topic__oDaCh']/div[@class='styles_Heading__FSyPb']")
                            question_type_text = question_heading.find_element(By.TAG_NAME, 'h2').text
                            if "Opening" in question_type_text:
                                question_type = "Opening Questions"
                                question_text = question.text.split(". ", 1)[1]  # Soru numarasını kaldır
                                evaluator_id = 2
                                answer_text = ""
                            elif "Closing" in question_type_text:
                                question_type = "Closing Questions"
                                question_text = question.text.split(". ", 1)[1]  # Soru numarasını kaldır
                                evaluator_id = 2
                                answer_text = ""
                                
                            else:
                                question_type = question_type_text
                                question_text = question.text.split(". ", 1)[1]  # Soru numarasını kaldır
                                answer_text = answer.text.split(": ", 1)[1]  # Cevap başlığını kaldır
                                evaluator_id = 1
                            # Veritabanına kaydetme
                            c.execute("SELECT * FROM questions WHERE job_title_id=? AND skill_level_id=? AND question=?", (job_title_id, skill_level_id, question_text))
                            existing_record = c.fetchone()
                            if not existing_record:
                                c.execute("INSERT INTO questions (job_title_id, skill_level_id, category_id, question_type, evaluator_id, language_id, question, answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (job_title_id, skill_level_id, category_id, question_type, evaluator_id,language_id, question_text, answer_text))
                                conn.commit()
    
    

# Kullanıcıdan girdileri alma ve işlemi gerçekleştirme
iterations = 23 # Yapılacak işlem sayısı
innerIter= 4
#job_titles=["Software Engineer","Software Developer","Front End Developer","Network Engineer","Android Developer","Salesforce Developer","IOS Developer","SQL Developer",".NET Developer","Python Developer","Game Developer","Data Engineer","Full Stack Developer","React Developer","UI Developer"]
#skill_levels=["Junior","Mid-level","Senior"]


for _ in range(iterations):
    # Selenium WebDriver'ı başlatma
    driver = webdriver.Chrome()
    # Web sitesine gidin
    driver.get("https://recooty.com/tools/interview-question-generator/")
    # İlk iterasyon için bir bayrak oluşturma
    scrape_and_save.first_iteration = True
    for i in range (innerIter):
        scrape_and_save()
        print("i: ",i)
    # Mevcut driver'ı kapat
    driver.quit()
    print("_: ",_)
# Veritabanı bağlantısını kapatma
conn.close()
