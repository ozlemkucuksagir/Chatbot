from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import sqlite3

# SQLite veritabanı bağlantısı oluşturma
conn = sqlite3.connect('interview_questions3.db')
c = conn.cursor()

# Veritabanı tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS interview_questions
             (id INTEGER PRIMARY KEY, job_title TEXT, difficulty TEXT, category TEXT, question_type TEXT, language TEXT, question TEXT, answer TEXT)''')

# Selenium WebDriver'ı başlatma
driver = webdriver.Chrome()  # veya diğer tarayıcıları kullanabilirsiniz

# Web sitesine gidin
driver.get("https://recooty.com/tools/interview-question-generator/")  # WEBSITE_URL'i kendi web sitesinin URL'si ile değiştirin


def select_option_by_text(select_element, option_text):
    for option in select_element.find_elements(By.TAG_NAME, 'option'):
        if option.text.strip() == option_text:
            option.click()
            break

def scrape_and_save(job_title, difficulty, category, language=None):
    # Job title'i giriş kutusuna yazma


    job_title_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div.styles_input__9RnCm.undefined.styles_JTInput__flMU5.styles_wide__QYOEu > input')))
    job_title_input.click()
    job_title_input.send_keys(job_title)
    
    # Zorluk seviyesini seçme
    difficulty_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div:nth-child(2) > select')))
    select_option_by_text(difficulty_select, difficulty)
    
    # Soru tipini seçme
    category_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div:nth-child(3) > select')))
    select_option_by_text(category_select, category)
    
    # Dil seçeneğini belirleme (varsa)
    if language:
        language_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div.styles_SelectMenuWrapper__onWBr.styles_LangSelect__DbruI > div.styles_input__Xoi8Y.undefined > input[type=text]')))
        select_option_by_text(language_select,language)
    
    
    # Generate butonuna tıklama
    generate_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > button')))
    generate_button.click()


    show_answers_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo.styles_IC_expanded__paAaR > div.styles_Container__EnYDl.styles_ContainerActive__-e3Z6.styles_contentBody__56j3w > div.styles_MainHeading__AV-pn > div > div')))
    show_answers_button.click()
    
    # Soru ve cevapları bulma
    question_elements = driver.find_elements(By.XPATH, "//span[@class='styles_Question__FRNnc']")
    answer_elements = driver.find_elements(By.XPATH, "//p[@class='styles_AnswerText__Y1oHC']")
    
    # Soru ve cevapları ekrana yazdırma
    for question, answer in zip(question_elements, answer_elements):
        # Soru tipini belirleme

        question_heading = question.find_element(By.XPATH, "./ancestor::div[@class='styles_Topic__oDaCh']/div[@class='styles_Heading__FSyPb']")

        question_type_text = question_heading.find_element(By.TAG_NAME, 'h2').text
        if "Opening" in question_type_text:
            question_type = "Opening Questions"
            question_text = question.text.split(". ", 1)[1]  # Soru numarasını kaldır
            answer_text = ""
        elif "Technical" in question_type_text:
            question_type = "Technical Questions"
            question_text = question.text.split(". ", 1)[1]  # Soru numarasını kaldır
            answer_text = answer.text.split(": ", 1)[1]  # Cevap başlığını kaldır
        elif "Closing" in question_type_text:
            question_type = "Closing Questions"
            question_text = question.text.split(". ", 1)[1]  # Soru numarasını kaldır
            answer_text = ""
        else:
            question_type = "Unknown"
            question_text = question.text.split(". ", 1)[1]  # Soru numarasını kaldır
            answer_text = answer.text.split(": ", 1)[1]  # Cevap başlığını kaldır
        print("Soru:", question_text)
        print("Cevap:", answer_text)
        print("Question Type:", question_type)
        print()
        # Veritabanına kaydetme
        c.execute("SELECT * FROM interview_questions WHERE question=? AND answer=?", (question_text, answer_text))
        existing_record = c.fetchone()
        if not existing_record:
            c.execute("INSERT INTO interview_questions (job_title, difficulty, category, question_type, language, question, answer) VALUES (?, ?, ?, ?, ?, ?, ?)", (job_title, difficulty, category, question_type, language, question_text, answer_text))
            conn.commit()
# Kullanıcıdan girdileri alma ve işlemi gerçekleştirme


job_title = input("Job Title: ")
difficulty = input("Difficulty: ")
category = input("Category: ")
language = input("Language (optional): ")

scrape_and_save(job_title, difficulty, category, language)

# Veritabanı bağlantısını kapatma
conn.close()

# WebDriver'ı kapatma
driver.quit()
