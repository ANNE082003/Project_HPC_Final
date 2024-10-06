from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from chat import get_response
from flask import jsonify
# Generate a salt for password hashing

db = SQLAlchemy()
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/files'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///faq.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'your_secret_key' 
# initialize the app with the extension
db.init_app(app)


class Faq(db.Model):
    sno=db.Column(db.Integer ,primary_key=True)
    question=db.Column(db.String(200) ,nullable=False)
    answer=db.Column(db.String(500) ,nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # category = db.relationship('Category')
    status = db.Column(db.Boolean,default=True)
  # Add status column

    def __repr__(self) -> str:
        return f"{self.sno}-{self.question}"
    
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120))
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False, unique=True)
#     date_created=db.Column(db.DateTime,default=datetime.utcnow)
#     status = db.Column(db.Boolean,default=True)
   


    
def add_initial_admin():
    
    admin = Admin(username='admin', password='password123')  # Replace with desired credentials
    db.session.add(admin)
    db.session.commit()

# # database for users
class User(db.Model):
    sno=db.Column(db.Integer ,primary_key=True)
    username=db.Column(db.String(200) ,nullable=False)
    email=db.Column(db.String(500) ,nullable=False)
    password=db.Column(db.String(500) ,nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __init__(self,email,password,username):
        self.username = username
        self.email = email
        self.password =password
    
with app.app_context():
    def __repr__(self) -> str:
        return f"{self.sno}-{self.username}"
    



    
with app.app_context():
    db.create_all()

@app.route('/')
def home(): 
    if 'email' not in session:
       email=''
    else:

       email=session['email']
    return render_template('home.html',email=email)

    
@app.route('/software')
def software(): 
    if 'email' not in session:
       email=''
    else:

       email=session['email']
    return render_template('software.html',email=email)
@app.route('/resource')
def resource(): 
    if 'email' not in session:
       email=''
    else:

       email=session['email']
    return render_template('resource.html',email=email)    


# Admin's Faq page
@app.route('/admin/faq')
def admin_faq(): 

    
    allFaq= Faq.query.all()   
    return render_template('admin/faq.html', faqs=allFaq)
    # return 'Hello, World!'

# admin faq session
@app.route('/delete/<int:sno>')
def delete(sno): 
    
    faq= Faq.query.filter_by(sno=sno).first()  
    db.session.delete(faq)
    db.session.commit()
    return redirect(url_for('admin_faq'))

@app.route('/update_faq_status/<int:faq_id>/<status>')
def update_faq_status(faq_id, status):
    faq = Faq.query.get_or_404(faq_id)
    faq.status = int(status)  # Convert status to integer (0 or 1)
    db.session.commit()
    flash('FAQ status updated successfully')
    return redirect(url_for('admin_faq'))


@app.route('/add_faq', methods=['POST'])
def add():
    allFaq = Faq.query.all()   
    question = request.form.get('question')
    answer= request.form.get('answer')
    
    # Create a new FAQ object
    faq = Faq(question=question, answer=answer)
   
    db.session.add(faq)
    db.session.commit()
    #  # Create a new FAQ object
    # admin = Admin(username='admin', password='password123')  # Replace with desired credentials
    # db.session.add(admin)
    # db.session.commit()
   
    return redirect(url_for('admin_faq'))

@app.route('/admin/faq/update_faq/<int:sno>',methods=['POST'])
def update_faq(sno):
    faq= Faq.query.filter_by(sno=sno).first()  
    # return redirect(url_for('admin_faq'))
    return render_template('admin/update_faq.html', faq=faq)
@app.route("/faqs")
def faqs():
    
    all_faqs = Faq.query.filter_by(status=1)
    if 'email' not in session:
       email=''
    else:

       email=session['email']
    return render_template("faq_user.html", faqs=all_faqs,email=email)


@app.route('/user_registration')
def register():
    return render_template('register.html')

@app.route('/adduser', methods=['POST'])
def add_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Create a new user object
    user = User(username=username, email=email, password=password)

    db.session.add(user)
    db.session.commit()
    flash('User registered successfully!')
    return redirect(url_for('login'))

    


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        
        email = request.form['email']
        password = request.form['password']

        count = User.query.filter_by(email=email,password=password).count()
        print(count)
        
        if count==1:
            user = User.query.filter_by(email=email,password=password).first()
            session['email'] = user.email
            session['user_id'] = user.sno
            return redirect('/')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/admin',methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        count = Admin.query.filter_by(username=username,password=password).count()
        
        
        if count==1:
            admin = Admin.query.filter_by(username=username,password=password).first()
            session['username'] = admin.username
           
            return redirect('/admin/faq')
        else:
            return render_template('admin/login.html',error='Invalid user')
    else:
        return render_template('admin/login.html')
    
@app.route('/adminlogout')
def admin_logout():
    session.clear()
    return redirect('/admin')


@app.route('/admin/listuser')
def view_users():
    # Fetch all users (customize query if needed)
    users = User.query.all()

    return render_template('admin/listuser.html', users=users)
@app.route('/deleteuser/<int:sno>')
def deleteuser(sno): 
    
    user= User.query.filter_by(sno=sno).first()  
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('view_users'))

# @app.route('/admin/categories')
# def admin_categories():
#     category = Category.query.all()
#     return render_template('admin/category.html', category=category)

# @app.route('/update_category_status/<int:faq_id>/<status>')
# def update_category_status(category_id, status):
#     category = Category.query.get_or_404(category_id)
#     category.status = int(status)  # Convert status to integer (0 or 1)
#     db.session.commit()
    
#     return redirect(url_for('admin_categories'))


# @app.route('/add_category', methods=['POST'])
# def add_category():
#     category = Category.query.all()   
#     name = request.form.get('name')
   
#     # Create a new FAQ object
#     category = Category(name=name)
   
#     db.session.add(category)
#     db.session.commit()
    
   
#     return redirect(url_for('admin_categories'))
@app.route('/predict', methods=['POST'])
def predict():
    text=request.get_json().get("message")
    response=get_response(text)
    message={"answer":response}
    return jsonify(message)


if __name__=="__main__":
    app.run(debug=True ,port=8000)
