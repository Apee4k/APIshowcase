from asyncio.windows_events import NULL
from datetime import datetime
from math import nan
from flask import render_template, request, redirect, url_for, session, jsonify
from FlaskWebProject1222 import app
import sqlite3 
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
app.secret_key = 'your_secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



products = [
    (1, 'Agreement management', 'img/agreement.png',
     'API соглашений предоставляет стандартизированный механизм управления соглашениями, особенно в контексте партнерских отношений между партнерами. API позволяет создавать, обновлять и запрашивать экземпляры соглашения, а также создавать, обновлять и запрашивать спецификации соглашения, служащие шаблонами для экземпляров соглашения.',
     1, '', 1000, 0, 'api_card_1'),
    (2, 'Agreement management', 'img/agreement.png',
     'API соглашений предоставляет стандартизированный механизм управления соглашениями, особенно в контексте партнерских отношений между партнерами. API позволяет создавать, обновлять и запрашивать экземпляры соглашения, а также создавать, обновлять и запрашивать спецификации соглашения, служащие шаблонами для экземпляров соглашения.',
     1, '', 5000, 0, 'api_card_1'),
    (3, 'Agreement management', 'img/agreement.png',
     'API соглашений предоставляет стандартизированный механизм управления соглашениями, особенно в контексте партнерских отношений между партнерами. API позволяет создавать, обновлять и запрашивать экземпляры соглашения, а также создавать, обновлять и запрашивать спецификации соглашения, служащие шаблонами для экземпляров соглашения.',
     1, '', 10000, 0, 'api_card_1'),
    (4, 'Customer management', 'img/cust.png',
     'API управления клиентами предоставляет стандартизированный механизм для управления клиентами и учетными записями клиентов, например, создание, обновление, извлечение, удаление и уведомление о событиях. Клиентом может быть человек, организация или другой поставщик услуг, который покупает продукты у предприятия. API управления клиентами позволяет управлять идентификационной и финансовой информацией о нем.',
     1, '', 1000, 0, 'api_card_2'),
     (5, 'Customer management', 'img/cust.png',
     'API управления клиентами предоставляет стандартизированный механизм для управления клиентами и учетными записями клиентов, например, создание, обновление, извлечение, удаление и уведомление о событиях. Клиентом может быть человек, организация или другой поставщик услуг, который покупает продукты у предприятия. API управления клиентами позволяет управлять идентификационной и финансовой информацией о нем.',
     1, '', 5000, 0, 'api_card_2'),
     (6, 'Customer management', 'img/cust.png',
     'API управления клиентами предоставляет стандартизированный механизм для управления клиентами и учетными записями клиентов, например, создание, обновление, извлечение, удаление и уведомление о событиях. Клиентом может быть человек, организация или другой поставщик услуг, который покупает продукты у предприятия. API управления клиентами позволяет управлять идентификационной и финансовой информацией о нем.',
     1, '', 10000, 0, 'api_card_2'),
    (7, 'Document management', 'img/document.png',
     'Основная цель API программного обеспечения системы управления документами Folderit или API облачного хранилища — позволить компании-партнеру создать гибкое функциональное приложение. API позволяет легко и быстро получить все функции, которые включает в себя Folderit DMS.',
     1, '', 1000, 0, 'api_card_3'),
     (8, 'Document management', 'img/document.png',
     'Основная цель API программного обеспечения системы управления документами Folderit или API облачного хранилища — позволить компании-партнеру создать гибкое функциональное приложение. API позволяет легко и быстро получить все функции, которые включает в себя Folderit DMS.',
     1, '', 5000, 0, 'api_card_3'),
     (9, 'Document management', 'img/document.png',
     'Основная цель API программного обеспечения системы управления документами Folderit или API облачного хранилища — позволить компании-партнеру создать гибкое функциональное приложение. API позволяет легко и быстро получить все функции, которые включает в себя Folderit DMS.',
     1, '', 10000, 0, 'api_card_3'),
    (10, 'Payment management', 'img/paymant.png',
     'API управления платежами включает определение модели, а также все доступные операции для платежей и возвратов. Этот API позволяет выполнять следующие операции: уведомление о выполненном платеже, получение списка платежей, отфильтрованных по заданным критериям, получение отдельного выполненного платежа, уведомление о выполненном возврате, получение списка возвратов, отфильтрованных по заданным критериям, получение отдельного выполненного возврата.',
     1, '', 1000, 0, 'api_card_4'),
    (11, 'Payment management', 'img/paymant.png',
     'API управления платежами включает определение модели, а также все доступные операции для платежей и возвратов. Этот API позволяет выполнять следующие операции: уведомление о выполненном платеже, получение списка платежей, отфильтрованных по заданным критериям, получение отдельного выполненного платежа, уведомление о выполненном возврате, получение списка возвратов, отфильтрованных по заданным критериям, получение отдельного выполненного возврата.',
     1, '', 5000, 0, 'api_card_4'),
    (12, 'Payment management', 'img/paymant.png',
     'API управления платежами включает определение модели, а также все доступные операции для платежей и возвратов. Этот API позволяет выполнять следующие операции: уведомление о выполненном платеже, получение списка платежей, отфильтрованных по заданным критериям, получение отдельного выполненного платежа, уведомление о выполненном возврате, получение списка возвратов, отфильтрованных по заданным критериям, получение отдельного выполненного возврата.',
     1, '', 10000, 0, 'api_card_4'),
    (13, 'Product catalog management', 'img/catalog.png',
     'API управления каталогом продуктов позволяет управлять всем жизненным циклом элементов каталога, консультироваться с элементами каталога во время нескольких процессов, таких как процесс заказа, управление кампанией, управление продажами. Эта версия спецификации API управления каталогом продуктов Rest включает функционал Engage Party Migration.',
     1, '', 1000, 0, 'api_card_5'),
    (14, 'Product catalog management', 'img/catalog.png',
     'API управления каталогом продуктов позволяет управлять всем жизненным циклом элементов каталога, консультироваться с элементами каталога во время нескольких процессов, таких как процесс заказа, управление кампанией, управление продажами. Эта версия спецификации API управления каталогом продуктов Rest включает функционал Engage Party Migration.',
     1, '', 5000, 0, 'api_card_5'),
    (15, 'Product catalog management', 'img/catalog.png',
     'API управления каталогом продуктов позволяет управлять всем жизненным циклом элементов каталога, консультироваться с элементами каталога во время нескольких процессов, таких как процесс заказа, управление кампанией, управление продажами. Эта версия спецификации API управления каталогом продуктов Rest включает функционал Engage Party Migration.',
     1, '', 10000, 0, 'api_card_5')
]



def is_logged_in():
    return 'email' in session

global logs_actions
logs_actions = {1:'User added product',
                2:'User deleted product', 
                3:'User edited product',
                4:'User registred',
                5:'User logged in',
                6:'User added product to cart',
                7:'User deleted product from cart',
                8:'User purchased product',
                9:'User cleared the cart'}

conn = None
try:
    conn = sqlite3.connect('APIshowcase.db', isolation_level='DEFERRED', check_same_thread= False)
    db = conn.cursor()
    db.execute('''
    CREATE TABLE IF NOT EXISTS USERS(
        USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        EMAIL CHAR(320) NOT NULL UNIQUE,
        PASSWORD CHAR(600) NOT NULL,
        ACCESS CHAR(200) DEFAULT NULL,
        SUPERUSER BOOLEAN DEFAULT FALSE
        )''')
    conn.commit()
    db.execute('''CREATE TABLE IF NOT EXISTS PRODUCTS(
        PRODUCT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PRODUCT_NAME VARCHAR(100) NOT NULL DEFAULT '',
        PICTURE BLOB,
        API_DESCRIPTION VARCHAR(1500),
        RATE INTEGER DEFAULT 1,
        RATE_DESCRIPTION VARCHAR(500),
        PRICE INTEGER NOT NULL DEFAULT 0,
        REQUESTS INTEGER NOT NULL DEFAULT 0,
        LINK VARCHAR(100) NOT NULL,
        CREATOR INTEGER DEFAULT 1
        )''')
    conn.commit()
    db.execute('''CREATE TABLE IF NOT EXISTS OPERATIONS(
        OPERATION_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USER INTEGER,
        PRODUCT INTEGER,
        STATUS VARCHAR,
        FOREIGN KEY (USER) REFERENCES USERS(USER_ID) ON DELETE NO ACTION ON UPDATE NO ACTION,
        FOREIGN KEY (PRODUCT) REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE NO ACTION ON UPDATE NO ACTION
        )''')
    conn.commit()
    db.execute('''CREATE TABLE IF NOT EXISTS LOGS(
        LOG_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ACTION INTEGER,
        USER INTEGER,
        PRODUCT INTEGER,
        FOREIGN KEY (USER) REFERENCES USERS(USER_ID) ON DELETE NO ACTION ON UPDATE NO ACTION,
        FOREIGN KEY (PRODUCT) REFERENCES PRODUCTS(PRODUCT_ID) ON DELETE NO ACTION ON UPDATE NO ACTION
        )''')
    print("sucsess!")
        
except:
    print("conect fail")

product_ids = [1, 2, 3, 4, 5]
db.executemany('DELETE FROM PRODUCTS WHERE PRODUCT_ID = ?', [(product_id,) for product_id in product_ids])

for product in products:
    db.execute('''INSERT INTO PRODUCTS (PRODUCT_NAME, PICTURE, API_DESCRIPTION, RATE, RATE_DESCRIPTION, PRICE, REQUESTS, LINK) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', product[1:])

conn.commit()


class User(UserMixin):
    def __init__(self, user_id, email, password, access, superuser):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.access = access
        self.superuser = superuser

    @staticmethod
    def find_user_by_email(email):
        db.execute('''SELECT * FROM USERS WHERE EMAIL = ? ''', (email,))
        user_data = db.fetchone()
        if user_data:
            return User(*user_data) 
        return None
    
    def totuple(self):
        list_of_att = []
        list_of_att.append(self.user_id)
        list_of_att.append(self.email)
        list_of_att.append(self.password)
        list_of_att.append(self.access)
        list_of_att.append(self.superuser)
        return tuple(list_of_att)

    def logs(self):
        user_id = self.user_id
        db.execute('SELECT ACTION FROM LOGS WHERE USER = ? ',(user_id,))
        user_logs = db.fetchall()
        user_logs = [user_log[0] for user_log in user_logs]
        print(user_logs)
        if user_logs:
            return user_logs
        return None
    
    def get_id(self):
        return str(self.user_id)
    

def users_cart(user_id):
    db.execute('SELECT PRODUCT FROM OPERATIONS WHERE (USER, STATUS)= (?,?)', (user_id, 'in_cart',))
    accesses = db.fetchall()
    product_ids = [access[0] for access in accesses]
    return product_ids

def final_cost(product_ids):
    placeholders = ', '.join(['?'] * len(product_ids))
    query = f'SELECT PRICE FROM PRODUCTS WHERE PRODUCT_ID IN ({placeholders})'
    
    db.execute(query, product_ids)
    
    product_prices = db.fetchall()
    final_price = 0
    for price in product_prices:
        final_price+=price[0]
    return final_price




@login_manager.user_loader
def load_user(user_id):
    db.execute('SELECT * FROM USERS WHERE USER_ID = ?', (user_id,))
    user_data = db.fetchone()
    if user_data:
        return User(*user_data)
    return None


user_list = []

#Добавление суперюзера в БД
superuser = User(user_id=None, email = 'qwerty12345@mail.ru', password = generate_password_hash("123456789"), access=None, superuser=True)
db.execute('INSERT OR IGNORE INTO USERS(USER_ID, EMAIL, PASSWORD, ACCESS, SUPERUSER) VALUES (?, ?, ?, ?, ?)', superuser.totuple())
conn.commit()

def picture_to_binlist(pic_path):
    with open(pic_path, 'rb') as file:
        image_data = file.read()
    return sqlite3.Binary(image_data)

class Product:

    def __init__(self, product_id, product_name, picture, API_description, rate, rate_description, price, requests, link, creator):
        self.product_id = product_id
        self.product_name = product_name
        self.picture = picture
        self.API_description = API_description
        self.rate = rate
        self.rate_description = rate_description
        self.price = price
        self.requests = requests
        self.link = link
        self.creator = creator

    def get_atts_list(self):
        list_of_atts = ['product_id', 'product_name', 'picture', 'API_description', 'rate', 'rate_description', 'price', 'requests','link','creator']
        return list_of_atts

    @staticmethod
    def product_by_name(name):
        db.execute('''SELECT * FROM PRODUCTS WHERE PRODUCT_NAME = ? ''', (name,))
        product_data = db.fetchone()
        if product_data:
            return Product(*product_data) 
        return None
    
    @staticmethod
    def get_product(product_id):
        db.execute('SELECT * FROM PRODUCTS WHERE PRODUCT_ID = ?',(product_id,))
        product_data = db.fetchone()
        if product_data:
            return Product(*product_data)
        return None
    
    @staticmethod
    def get_prices(product_id):
        product_ids = [product_id,product_id+1,product_id+2]
        placeholders = ', '.join(['?'] * len(product_ids))
        query = f'SELECT PRICE FROM PRODUCTS WHERE PRODUCT_ID IN ({placeholders})'
    
        db.execute(query, product_ids)
    
        product_data = db.fetchall()
        bprice = product_data[0][0]
        aprice = product_data[1][0]
        eprice = product_data[2][0]
        return bprice, aprice, eprice

@app.route('/')
def index():
    if current_user.is_authenticated:
        is_superuser = current_user.superuser 
    else:
        is_superuser = False 
    return render_template('index.html', is_superuser=is_superuser)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.find_user_by_email(email=email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            db.execute('''
                        INSERT INTO LOGS(LOG_ID, ACTION, USER, PRODUCT) VALUES (?, ?, ?, ?)''', 
                        (None, logs_actions[5], user.user_id, 0))
            conn.commit()
            return redirect(url_for('index')) 
        else:
            return "Wrong E-mail or password"

    return render_template('login.html')

@app.route('/logout')
def logout():
    db.execute('''INSERT INTO LOGS(LOG_ID, ACTION, USER, PRODUCT) VALUES (?, ?, ?, ?)''', (None, logs_actions[5], current_user.user_id, 0))
    conn.commit()
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password == confirm_password:
            try:
                user = User.find_user_by_email(email=email)
                if user is None: 
                    password_hash = generate_password_hash(password)
                    db.execute('''
                        INSERT INTO USERS(USER_ID, EMAIL, PASSWORD, ACCESS, SUPERUSER) VALUES (?, ?, ?, ?, ?)''', 
                        (None, email, password_hash, None, False))
                    conn.commit()
                    user = User.find_user_by_email(email)
                    db.execute('''
                        INSERT INTO LOGS(LOG_ID, ACTION, USER, PRODUCT) VALUES (?, ?, ?, ?)''', 
                        (None, logs_actions[4], user.user_id, 0))
                    conn.commit()
                else:
                    print('User already exists')
                    return 'User with this email already exists'  

            except Exception as e:
                print(f"Error saving user: {e}")
                return 'Error saving user to database'
            
            
            return redirect(url_for('index'))
        else:
            return 'Passwords do not match'

    return render_template('register.html')

@app.route('/account')
def account():
    print(current_user.logs())
    if current_user.logs() == None:
        logs = []
    else:
        logs = current_user.logs()
    cart_ids = users_cart(current_user.user_id) 
    cart = [Product.get_product(product_id) for product_id in cart_ids]
    return render_template('account.html',logs=logs,cart=cart)



@app.route('/add-api', methods=['POST'])
def add_api():
    api_name = request.form['api-name']
    api_description = request.form['api-description']
    api_image = request.files['api-image']
    api_basic_price = request.form['api-basic-price']
    api_advanced_price = request.form['api-advanced-price']
    api_enterprise_price = request.form['api-enterprise-price']
    api_documentation = request.files['api-documentation']
    api_prices = [api_basic_price, api_advanced_price, api_enterprise_price]
    #api_requests = request.form['api-requests']
    api_requests = 10

    api_id = None
    api_name = api_name.replace(" ", "_").lower()
    api_link = f"api_card_{api_name}"
    img_dir = os.path.join('FlaskWebProject1222','FlaskWebProject1222', 'static', 'img')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    image_filename = f"{api_name}.png"
    image_path = os.path.join(img_dir, image_filename)

    api_image.save(image_path)

    docs_dir = os.path.join('FlaskWebProject1222','FlaskWebProject1222', 'static', 'docs')
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    documentation_filename = f"{api_name}_documentation.pdf"
    documentation_path = os.path.join(docs_dir, documentation_filename)
    api_documentation.save(documentation_path)
       
    rate_desciptions = ['basic','advanced','enterprise']
    for i in range(3):
        db.execute('INSERT INTO PRODUCTS VALUES (?,?,?,?,?,?,?,?,?,?)', (api_id, 
                                                                        api_name, 
                                                                        picture_to_binlist(image_path),
                                                                        api_description,
                                                                        i+1,
                                                                        rate_desciptions[i],
                                                                        api_prices[i],
                                                                        api_requests,
                                                                        api_link,
                                                                        current_user.user_id))
    conn.commit()
    product = Product.product_by_name(api_name)
    db.execute('''INSERT INTO LOGS(LOG_ID, ACTION, USER, PRODUCT) VALUES (?, ?, ?, ?)''', 
        (None, logs_actions[1], current_user.user_id, product.product_id))
    conn.commit()
    create_api_page(product.product_id, api_name, api_description, api_basic_price, api_advanced_price, api_enterprise_price, documentation_filename)
    return redirect(url_for('view_api_card', title=api_name,product_id = product.product_id))

def create_api_page(api_id, title, description, basic_price, advanced_price, enterprise_price, documentation_filename):
    output_dir = 'FlaskWebProject1222/FlaskWebProject1222/templates'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    html_content = render_template('api_card_template.html', title=title, description=description,
                                   basic_price=basic_price, advanced_price=advanced_price, enterprise_price=enterprise_price,
                                   documentation_filename=documentation_filename,api_id_1=api_id,api_id_2=api_id+1, api_id_3 = api_id+2)
    
    html_file_path = os.path.join(output_dir, f'api_card_{title}.html')
    
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/api_card/<title>/', methods=['GET'])
def view_api_card(title):
    
    product_id = request.args.get('product_id')

    if product_id is None:
        return "Product ID is required", 400

    try:
        product_id = int(product_id)
    except ValueError:
        return "Invalid Product ID", 400

    product = Product.get_product(product_id)
    
    if not product:
        return "API не найдено", 404

    basic_price, advanced_price, enterprise_price = Product.get_prices(product_id)
    api_id_1=product.product_id
    api_card_2 = product.product_id + 1
    api_card_3 = product.product_id + 2


    return render_template(
        'api_card_template.html',
        title=product.product_name,
        description=product.API_description,
        basic_price=basic_price,
        advanced_price=advanced_price,
        enterprise_price=enterprise_price,
        documentation_filename=f'{title}_documentation.pdf',
        api_id_1=api_id_1,
        api_id_2 = api_card_2,
        api_id_3 = api_card_3,
        creator_id=product.creator
    )




@app.route('/api/products', methods=['GET'])
def get_products(): 
    db.execute('''SELECT PRODUCT_ID, 
       PRODUCT_NAME, 
       API_DESCRIPTION, 
       LINK, 
       GROUP_CONCAT(RATE, ", ") 
    FROM PRODUCTS 
    GROUP BY PRODUCT_NAME''')
    products = db.fetchall()
    product_list = []
    
    for product in products:
        product_dict = {
            'id': product[0],  # PRODUCT_ID
            'title': product[1],  # PRODUCT_NAME
            'description': product[2],  # API_DESCRIPTION
            'link': url_for('view_api_card', title=product[1].replace(" ", "_").lower(), product_id=product[0]),  # Передаем product_id
            'image': url_for('static', filename=f'img/{product[1]}.png')  # Путь к изображению
        }

        product_list.append(product_dict)

    conn.commit()
    return jsonify(product_list)


@app.route('/delete_product/<int:product_id>', methods=['POST'])
@login_required 
def delete_product(product_id):
    db.execute('DELETE FROM PRODUCTS WHERE PRODUCT_ID >= ? AND PRODUCT_ID <= ?', (product_id,product_id+2,))
    conn.commit()
    db.execute('''INSERT INTO LOGS(LOG_ID, ACTION, USER, PRODUCT) VALUES (?, ?, ?, ?)''', 
                    (None, logs_actions[2], current_user.user_id, 0))
    conn.commit()

    return redirect(url_for('index')) 

@app.route('/add_to_cart', methods=['POST'])
@login_required  # Убедитесь, что пользователь аутентифицирован
def add_to_cart():
    product_id = request.form.get('product_id')
    
    if not product_id:
        return "Product ID is required", 400

    try:
        product_id = int(product_id)
    except ValueError:
        return "Invalid Product ID", 400

    user_id = current_user.user_id  # Получаем ID текущего пользователя

    # Проверяем, существует ли операция с таким продуктом и пользователем
    existing_operation = db.execute('SELECT * FROM OPERATIONS WHERE USER = ? AND PRODUCT = ? AND STATUS = ?', 
                                     (user_id, product_id, 'in_cart')).fetchone()

    if existing_operation:
        return "Товар уже в корзине", 409  # Код 409 Conflict


    # Добавляем товар в "корзину"
    db.execute('INSERT INTO OPERATIONS (USER, PRODUCT, STATUS) VALUES (?, ?, ?)', (user_id, product_id, 'in_cart'))
    conn.commit()

    db.execute('''INSERT INTO LOGS(LOG_ID, ACTION, USER, PRODUCT) VALUES (?, ?, ?, ?)''', 
                    (None, logs_actions[6], current_user.user_id, 0))
    conn.commit()

    return render_template('index.html')






@app.route('/cart', methods=['GET'])
@login_required  # Убедитесь, что пользователь аутентифицирован
def view_cart():
    user_id = current_user.user_id
    operations = db.execute('SELECT PRODUCT FROM OPERATIONS WHERE USER = ? AND STATUS = ?', 
                            (user_id, 'in_cart')).fetchall()

    products_in_cart = []
    
    for operation in operations:
        product = db.execute('SELECT * FROM PRODUCTS WHERE PRODUCT_ID = ?', (operation[0],)).fetchone()
        if product:
            products_in_cart.append(product)

    return render_template('cart.html', products=products_in_cart)


@app.route('/remove_from_cart', methods=['POST'])
@login_required
def remove_from_cart():
    product_id = request.form.get('product_id')

    if not product_id:
        return "Product ID is required", 400

    try:
        product_id = int(product_id)
    except ValueError:
        return "Invalid Product ID", 400

    user_id = current_user.user_id

    # Удаляем операцию из "корзины"
    db.execute('DELETE FROM OPERATIONS WHERE USER = ? AND PRODUCT = ? AND STATUS = ?', 
               (user_id, product_id, 'in_cart'))
    conn.commit()

    db.execute('''INSERT INTO LOGS(LOG_ID, ACTION, USER, PRODUCT) VALUES (?, ?, ?, ?)''', 
                    (None, logs_actions[7], current_user.user_id, 0))
    conn.commit()

    return redirect(url_for('view_cart'))  # Перенаправляем обратно на страницу корзины


@app.route('/clear_cart', methods=['POST'])
@login_required
def clear_cart():
    user_id = current_user.user_id

    db.execute('DELETE FROM OPERATIONS WHERE USER = ? AND STATUS = ?', (user_id, 'in_cart'))
    conn.commit()
    db.execute('''INSERT INTO LOGS(LOG_ID, ACTION, USER, PRODUCT) VALUES (?, ?, ?, ?)''', 
                    (None, logs_actions[9], current_user.user_id, 0))
    conn.commit()

    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    user_id = current_user.user_id
    
    # Здесь вы можете добавить логику для обработки заказа
    # Например, получение всех товаров в корзине
    operations = db.execute('SELECT PRODUCT FROM OPERATIONS WHERE USER = ? AND STATUS = ?', 
                            (user_id, 'in_cart')).fetchall()

    products_in_cart = []
    
    for operation in operations:
        product = db.execute('SELECT * FROM PRODUCTS WHERE PRODUCT_ID = ?', (operation[0],)).fetchone()
        if product:
            products_in_cart.append(product)
    product_ids = users_cart(current_user.user_id)
    final_price = final_cost(product_ids)

    if request.method == 'POST':
        # Логика оформления заказа (например, создание записи в таблице заказов)
        # После успешного оформления можно очистить корзину
        db.execute('DELETE FROM OPERATIONS WHERE USER = ? AND STATUS = ?', (user_id, 'in_cart'))
        conn.commit()
        db.execute('''INSERT INTO LOGS(LOG_ID, ACTION, USER, PRODUCT) VALUES (?, ?, ?, ?)''', 
                    (None, logs_actions[8], current_user.user_id, 0))
        conn.commit()
        return redirect(url_for('index'))  # Перенаправление на страницу подтверждения заказа

    return render_template('checkout.html', products=products_in_cart, final_cost=final_price)
