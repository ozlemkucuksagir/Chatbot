import sqlite3

class HRChatbotDB:
    def __init__(self, db_name='hr_chatbot.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
    
    def create_skill_level_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS skill_level (
                                id INTEGER PRIMARY KEY,
                                level_name TEXT
                            )''')
        levels = [('Junior',), ('Mid',), ('Senior',)]
        self.cursor.executemany('INSERT INTO skill_level (level_name) VALUES (?)', levels)
        self.conn.commit()
    
    def create_language_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS language (
                                id INTEGER PRIMARY KEY,
                                language_name TEXT
                            )''')
        languages = [('ENG (US)',)]
        self.cursor.executemany('INSERT INTO language (language_name) VALUES (?)', languages)
        self.conn.commit()
    
    def create_job_titles_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS job_titles (
                                id INTEGER PRIMARY KEY,
                                job_title_name TEXT
                            )''')
        job_titles = [('Software Engineer',), ('Software Developer',), ('Front End Developer',),
                      ('Network Engineer',), ('Android Developer',), ('Salesforce Developer',),
                      ('IOS Developer',), ('SQL Developer',), ('.NET Developer',), ('Python Developer',),
                      ('Game Developer',), ('Data Engineer',), ('Full Stack Developer',), ('React Developer',),
                      ('UI Developer',)]
        self.cursor.executemany('INSERT INTO job_titles (job_title_name) VALUES (?)', job_titles)
        self.conn.commit()
    
    def create_evaluator_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS evaluator (
                                id INTEGER PRIMARY KEY,
                                evaluator_type_name TEXT
                            )''')
        evaluator_type = [('App',), ('Expert',)]
        self.cursor.executemany('INSERT INTO evaluator (evaluator_type_name) VALUES (?)', evaluator_type)
        self.conn.commit()
    
    def create_categories_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                                id INTEGER PRIMARY KEY,
                                category_name TEXT
                            )''')
        category = [('Technical',)]
        self.cursor.executemany('INSERT INTO categories (category_name) VALUES (?)', category)
        self.conn.commit()
    def get_skill_levels(self):
        self.cursor.execute('SELECT * FROM skill_level')
        return self.cursor.fetchall()
    
    def get_languages(self):
        self.cursor.execute('SELECT * FROM language')
        return self.cursor.fetchall()
    
    def get_job_titles(self):
        self.cursor.execute('SELECT * FROM job_titles')
        return self.cursor.fetchall()
    
    def get_evaluator_types(self):
        self.cursor.execute('SELECT * FROM evaluator')
        return self.cursor.fetchall()
    
    def get_categories(self):
        self.cursor.execute('SELECT * FROM categories')
        return self.cursor.fetchall()

# Kullanım örneği:
hr_db = HRChatbotDB()
hr_db.connect()

print("Skill Levels:")
print(hr_db.get_skill_levels())

print("\nLanguages:")
print(hr_db.get_languages())

print("\nJob Titles:")
print(hr_db.get_job_titles())

print("\nEvaluator Types:")
print(hr_db.get_evaluator_types())

print("\nCategories:")
print(hr_db.get_categories())

hr_db.disconnect()