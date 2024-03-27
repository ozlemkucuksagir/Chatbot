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
conn = sqlite3.connect('interview_questions.db')
c = conn.cursor()

# Veritabanı tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS interview_questions
             (id INTEGER PRIMARY KEY, job_title TEXT, skill_level TEXT, category TEXT, evaluator TEXT , question_type TEXT, language TEXT, question TEXT, answer TEXT)''')

# Selenium WebDriver'ı başlatma
driver = webdriver.Chrome()

# Web sitesine gidin
driver.get("https://recooty.com/tools/interview-question-generator/")

def select_option_by_text(select_element, option_text):
    for option in select_element.find_elements(By.TAG_NAME, 'option'):
        if option.text.strip() == option_text:
            option.click()
            break

def scrape_and_save(job_title, skill_level, category, language=None):
    # Job title'i giriş kutusuna yazma



    try:
        job_title_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div.styles_input__9RnCm.undefined.styles_JTInput__flMU5.styles_wide__QYOEu > input')))
        job_title_input.click()
        job_title_input.clear()
        job_title_input.send_keys(job_title)
    except ElementClickInterceptedException:
        print("Element tıklanabilir değil, sayfa yenileniyor...")
        driver.refresh()
        try:
            close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.styles_SmallButton__v-MHQ.CloseButton')))
            close_button.click()
            job_title_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div.styles_input__9RnCm.undefined.styles_JTInput__flMU5.styles_wide__QYOEu > input')))
            job_title_input.click()
            job_title_input.clear()
            job_title_input.send_keys(job_title)
        except TimeoutException:
            print("Element tıklanabilir değil, işlem gerçekleştirilemiyor.")
    
    # Zorluk seviyesini seçme
    skill_level_select = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo > div.styles_InputGrid__UgoNG > div:nth-child(2) > select')))
    select_option_by_text(skill_level_select, skill_level)
    
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
    
    #  Show Answers butonuna sadece ilk iterasyonda tıklama
    show_answers_button = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.BodyContainer > div:nth-child(4) > div.styles_IslandContainer__Q1LMo.styles_IC_expanded__paAaR > div.styles_Container__EnYDl.styles_ContainerActive__-e3Z6.styles_contentBody__56j3w > div.styles_MainHeading__AV-pn > div > div')))
    if scrape_and_save.first_iteration:
        show_answers_button.click()
        scrape_and_save.first_iteration = False
    
    # Soru ve cevapları bulma
    question_elements = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//span[@class='styles_Question__FRNnc']")))
    answer_elements = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//p[@class='styles_AnswerText__Y1oHC']")))
    
    # Soru ve cevapları ekrana yazdırma
    for question, answer in zip(question_elements, answer_elements):
        # Soru tipini belirleme

        question_heading = question.find_element(By.XPATH, "./ancestor::div[@class='styles_Topic__oDaCh']/div[@class='styles_Heading__FSyPb']")
        question_type_text = question_heading.find_element(By.TAG_NAME, 'h2').text
        if "Opening" in question_type_text:
            question_type = "Opening Questions"
            question_text = question.text.split(". ", 1)[1]  # Soru numarasını kaldır
            evaluator = "Expert"
            answer_text = "Personal answer"
        elif "Closing" in question_type_text:
            question_type = "Closing Questions"
            question_text = question.text.split(". ", 1)[1]  # Soru numarasını kaldır
            evaluator = "Expert"
            answer_text = "Personal answer"
            
        else:
            question_type = question_type_text
            question_text = question.text.split(". ", 1)[1]  # Soru numarasını kaldır
            answer_text = answer.text.split(": ", 1)[1]  # Cevap başlığını kaldır
            evaluator = "App"
        # Veritabanına kaydetme
        c.execute("SELECT * FROM interview_questions WHERE question=? AND answer=?", (question_text, answer_text))
        existing_record = c.fetchone()
        if not existing_record:
            c.execute("INSERT INTO interview_questions (job_title, skill_level, category, question_type, evaluator, language, question, answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (job_title, skill_level, category, question_type, evaluator,language, question_text, answer_text))
            conn.commit()
# İlk iterasyon için bir bayrak oluşturma
scrape_and_save.first_iteration = True
# Kullanıcıdan girdileri alma ve işlemi gerçekleştirme
iterations = 27 # Yapılacak işlem sayısı
for _ in range(iterations):

    
    job_title = "Backend Developer"
    skill_level = "Junior"
    category = "Technical"
    language = "ENG (US)"
    #job_title = input("Job Title: ")
    #skill_level = input("Skill level: ")
    #category = input("Category: ")
    #language = input("Language : ")

    scrape_and_save(job_title, skill_level, category, language)

# Veritabanı bağlantısını kapatma
conn.close()

# WebDriver'ı kapatma
driver.quit()
