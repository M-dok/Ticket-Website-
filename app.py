from flask import Flask,render_template,request,url_for,session,redirect,g
from flask_session import Session 
from werkzeug.security import generate_password_hash,check_password_hash
from database import get_db,close_db
from datetime import datetime
from flask_mail import Mail, Message
from form import RegistrationForm,Gig_regForm,GigForm,ReviewForm,LoginForm,ForgotForm,ResetForm,DeleteForm
from functools import wraps
 
'''
    forgot password
    Limited tickets '''

app= Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
app.config["SECRET_KEY"]="this-is-my-secret"
app.config['MAIL_SERVER']='smtp.office365.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'TicketSever536@outlook.com'
app.config['MAIL_PASSWORD'] = 'caProject2023'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.teardown_appcontext(close_db)
mail =Mail(app)
Session(app)

@app.before_request
def logged_in_user():
    g.user = session.get("username",None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login",next=request.url))
        return view(*args, **kwargs)
    return wrapped_view

    

@app.route("/")#Should have Admin version of this to show 
def home():
    db=get_db()
    gigs = db.execute(""" SELECT DISTINCT * FROM gigs 
                            ORDER BY RANDOM() LIMIT 6; """).fetchall()
    
    return render_template("Ticket_Sever.html",gigs=gigs)

@app.route("/register_account",methods=["GET","POST"]) #To register the account 
def register_account():
    form = RegistrationForm()
    message=""
    if form.validate_on_submit():
        username = form.username.data
        email=form.email.data
        password = form.password.data
        password2 = form.password2.data
        db=get_db()
        clashing_user = db.execute(""" SELECT * FROM user_info
                                        WHERE username = ? ;""",(username,)).fetchone()
        
        if clashing_user is not None:
            form.username.errors.append("Username is already taken")
        else:
            db.execute(""" INSERT INTO user_info(username,email,password)
                            VALUES (?,?,?); """ , (username,email,generate_password_hash(password)))
            db.commit()
        return redirect(url_for('login'))
        
    return render_template("register.html",form=form,message=message)

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password =form.password.data
        db =get_db()
        possible_user = db.execute(""" SELECT * FROM user_info WHERE username = ?; """,(username,)).fetchone()
        if possible_user is None:
            form.username.errors.append("Invalid username")
        elif not check_password_hash(possible_user["password"],password):
            form.password.errors.append("Invalid password")
        else:
            session.clear()
            session["username"]=username
            next_page = request.args.get("next")
            if not next_page:
                return redirect(url_for("home"))
    return render_template("login.html",form=form)



@app.route("/logout")
def logout():
    session.clear()
    return redirect (url_for("home"))

@app.route("/delete",methods=["GET","POST"])
def delete():
    form=DeleteForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        db=get_db()
        possible_user = db.execute(""" SELECT * FROM user_info
                                        WHERE username = ? ;""",(username,)).fetchone()
        
        if possible_user is None:
            form.username.errors.append("Username does not exist")
        else:
            db.execute("""DELETE FROM user_info 
                        WHERE username=?;""",(username,))
            db.commit()

            db.execute(""" DELETE from reviews WHERE username=?;""",(username,))
            db.commit()

            db.execute(""" DELETE FROM purchases WHERE username=?;""",(username,))
            db.commit()

            session.clear()
        return redirect(url_for("home"))
    return render_template("del.html",form=form)

 
@app.route("/register_gig",methods=["GET","POST"]) #Needs Work
@login_required
def GigRegistration():  #Register a gig in the db.
    form = Gig_regForm()
    message = ''
    if form.validate_on_submit():
        artist_name = form.artist_name.data
        gig_date=form.gig_date.data
        gig_venue=form.gig_venue.data
        num_of_tickets=form.num_of_tickets.data
        price = form.price.data
        genre=form.genre.data
        db=get_db()
        gig_date=gig_date.strftime('%Y-%b-%d')
        #Need to make sure that the user cannot insert a past date into the db 
        '''if gig_date <= datetime.now().date():
            form.gig_date.errors("Please insert a future date.")'''
        if num_of_tickets <= 0:
            form.num_of_tickets.errors.append("Invalid amount of tickets")
        elif price < 0:
            form.price.errors.append("Please set a price")
        elif form.gig_date.data <= datetime.now().date():
            form.gig_date.errors.append("Please insert a future date")

        else:
            clashing_gig= db.execute(""" SELECT * FROM gigs
                                        WHERE gig_date =? AND gig_venue=? AND artist_name =? ;""",(gig_date,gig_venue,artist_name)).fetchone()
            if clashing_gig is not None:
               form.gig_venue.errors.append("This gig clashes with another gig")

            else:
                db.execute(""" INSERT INTO gigs (artist_name,gig_date,gig_venue,genre,price,num_of_tickets)
                                VALUES (?,?,?,?,?,?);""",(artist_name,gig_date,gig_venue,genre,price,num_of_tickets))
                message="You have successfully created a gig"
                db.commit()
    return render_template("gig_reg.html",form=form,message=message)

@app.route("/gigs",methods=["GET","POST"])
def gigs():
    db=get_db()
    gigs = db.execute(""" SELECT * FROM gigs; """)
    form=GigForm()
    message=''
    
    if form.validate_on_submit():
        artist_name=form.artist_name.data
        genre =form.genre.data
        db=get_db()
        if artist_name==''and genre != 'None':
            gigs = db.execute(""" SELECT * FROM gigs WHERE genre =?;""",(genre,)).fetchall()
            if gigs ==[]:
                gigs = db.execute(""" SELECT DISTINCT * FROM gigs 
                            ORDER BY RANDOM() LIMIT 4; """).fetchall()
                message="Sorry we couldn't find your gig but we think you might like theses"
        elif artist_name != '' and genre == 'None':
            gigs = db.execute(""" SELECT * FROM gigs WHERE artist_name =?; """,(artist_name,)).fetchall()
            if gigs ==[]:
                gigs = db.execute(""" SELECT DISTINCT * FROM gigs 
                            ORDER BY RANDOM() LIMIT 4; """).fetchall()
                message="Sorry we couldn't find your gig but we think you might like theses"      
        elif artist_name =='' and genre == 'None':
            gigs = db.execute(""" SELECT * FROM gigs; """).fetchall()
            if gigs ==[]:
                gigs = db.execute(""" SELECT DISTINCT * FROM gigs 
                            ORDER BY RANDOM() LIMIT 4; """).fetchall()
                message="Sorry we couldn't find your gig but we think you might like theses"
        else:
            gigs = db.execute(""" SELECT * FROM gigs WHERE artist_name =? AND genre =?; """,(artist_name,genre)).fetchall()
            if gigs ==[]:
                gigs = db.execute(""" SELECT DISTINCT * FROM gigs 
                        WHERE genre =? ORDER BY RANDOM() LIMIT 4; """,(genre,)).fetchall()
                message="Sorry we couldn't find your gig but we think you might like theses"
    
    
    return render_template("gigs.html",form=form,gigs=gigs,message=message)

@app.route("/gig_info/<int:gig_id>",methods=["GET","POST"])
@login_required
def gig_info(gig_id):
    form = ReviewForm()
    db=get_db()
    gigs = db.execute(""" SELECT * FROM gigs WHERE gig_id =?;""",(gig_id,)).fetchone()
    reviews = db.execute(""" SELECT * FROM  reviews WHERE artist_name=?;""",(gigs['artist_name'],)).fetchall()
    if form.validate_on_submit():
        #artist_name = form.artist_name.data
        review = form.review.data
        score = form.score.data
        db=get_db()
        db.execute(""" INSERT INTO reviews(gig_id,username,artist_name,review,score) VALUES(?,?,?,?,?);""",(gig_id,session["username"],gigs['artist_name'],review,score))
        db.commit()
        return redirect(url_for("gig_info",gig_id=gig_id))
    return render_template("gig_info.html",gigs=gigs,reviews=reviews,form=form)

@app.route("/cart")    #Needs work
@login_required
def cart():
    if "cart" not in session:
        session["cart"]={}

    all_gigs = []
    db=get_db()
    message=''
    for gig_id in session["cart"]: #Error if nothing in cart
            if session["cart"]=={}:
                message="Your cart is empty"
            else:
                gig = db.execute(f""" SELECT * FROM gigs
                WHERE gig_id = {gig_id}""").fetchone()
                
                message="Item successfully purchased "
                all_gigs.append(gig)  
    return render_template("cart.html",all_gigs=all_gigs,message=message)

@app.route("/purchase/<int:gig_id>")
def purchase(gig_id):
    db=get_db()
    gig = db.execute(f""" SELECT * FROM gigs
                WHERE gig_id = {gig_id}""").fetchone()
    if gig["num_of_tickets"]<=0:
        return redirect(url_for("out_of_stock",gig_id=gig_id))
    else:
        db.execute(""" INSERT INTO purchases (username,gig_id,artist_name,gig_venue,gig_date,price) 
                    VALUES(?,?,?,?,?,?);""",(g.user,gig["gig_id"],gig["artist_name"],gig["gig_venue"],gig["gig_date"],gig["price"]))
        db.commit()

        db.execute(""" UPDATE gigs SET num_of_tickets = num_of_tickets - 1 WHERE gig_id=?;""",(gig_id,))
        db.commit()
        del session["cart"][gig_id]
        
        return redirect(url_for("account")) #Needs work. I want to send user to account or cart to see purchase or to purchase other tickets
@app.route("/remove_item_cart/<int:gig_id>")
def remove(gig_id):
    del session["cart"][gig_id]
    return redirect(url_for("cart"))

@app.route("/out_of_stock/<int:gig_id>")
def out_of_stock(gig_id):
    db=get_db()
    error_gig=db.execute(""" SELECT * FROM gigs WHERE gig_id=?;""",(gig_id,)).fetchone()
    recommended_gigs = db.execute(""" SELECT * FROM gigs WHERE genre=? AND NOT gig_id  = ?;""",(error_gig["genre"],gig_id)).fetchall()
    if recommended_gigs == []:
        recommended_gigs =db.execute(""" SELECT DISTINCT * FROM gigs 
        WHERE NOT  gig_id = ? AND num_of_tickets > 0 ORDER BY RANDOM() LIMIT 4; """,(gig_id,)).fetchall()
        
        del session["cart"][gig_id]
        
        return render_template("error.html",recommended_gigs=recommended_gigs,error_gig=error_gig)
    return render_template("error.html",recommended_gigs=recommended_gigs,error_gig=error_gig)

@app.route("/add_to_cart/<int:gig_id>") 
@login_required
def add_to_cart(gig_id):
    if "cart" not in session:
        session["cart"]={}
    if gig_id not in session["cart"]:
        session["cart"][gig_id]= 1
    else:
        session["cart"][gig_id] = session["cart"][gig_id] +1
    return redirect( url_for('cart') )


'''
@app.route("/email_sent/<email>",methods=["GET"])
def send_mail(email):
    msg_title="Rest Password"
    sender ='TicketServer536@gmail.com'
    msg =Message(msg_title,sender=sender,recipients=[email])
    msg_body="This is an email"
    msg_body="This is an email"
    data ={
        'app_name':"Ticket Server",
        'title':msg_title,
        'body':msg_body
    }
    msg.html = render_template("email.html",data=data)
    try:
        mail.send(msg)
        return "Email sent"
    except Exception as e:
        print(e)
        return f"Email was not sent{e}"
if __name__ == "__main__":
    app.run(debug=True )
'''

'''@app.route("/forgot",methods=["GET","POST"])    #Needs Work
def forgot():
    form =ForgotForm()
    db=get_db()
    if form.validate_on_submit():
        username = form.username.data
        email=form.email.data
        possible_user = db.execute(""" SELECT * FROM user_info WHERE username = ?; """,(username,)).fetchone()
        if possible_user is None:
            form.username.errors.append("Invalid username")
        else:
            redirect(url_for(f"send_mail({email})"))
    return render_template("forgot.html",form=form)'''

@app.route("/forgot",methods=["GET","POST"])    #Needs Work
def forgot():
    form= ForgotForm()
    db=get_db()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        possible_user = db.execute(""" SELECT * FROM user_info WHERE username=? AND email=?;""",(username,email)).fetchone()
        if possible_user == None:
            form.username.errors.append("Invalid username")
        else:
            return redirect(url_for('reset',user_id=possible_user['user_id']))
    return render_template("forgot.html",form=form)

@app.route("/reset_password/<int:user_id>",methods=["GET","POST"])
def reset(user_id):
    form= ResetForm()
    db=get_db()
    if form.validate_on_submit():
        password=form.password.data
        password2=form.password2.data
        db.execute(""" UPDATE user_info SET password=? WHERE user_id=?""",(generate_password_hash(password),user_id))
        db.commit()
        return redirect(url_for("login"))
    return render_template("password_reset.html",form=form)


        
@app.route("/account")
def account():
    db=get_db()
    reviews = db.execute(""" SELECT * FROM reviews WHERE username =?;""",(session["username"],)).fetchall()
    purchases = db.execute(""" SELECT * FROM purchases WHERE username =?;""",(session["username"],)).fetchall()
    return render_template("account.html",reviews=reviews,purchases=purchases)
    
@app.route("/delete_review/<int:review_id>")
def delete_review(review_id):
    db=get_db()
    db.execute("""DELETE FROM reviews WHERE review_id=?;""",(review_id,))
    db.commit()
    return redirect(url_for("account"))

@app.route("/refund/<int:purchase_id>")
def refund(purchase_id):
    db=get_db()
    refund = db.execute(""" SELECT * FROM purchases WHERE purchase_id=?""",(purchase_id,)).fetchone()
    db.execute("""DELETE FROM purchases WHERE purchase_id=?;""",(purchase_id,))
    print(refund)
    db.execute(""" UPDATE gigs SET num_of_tickets = num_of_tickets + 1 WHERE gig_id=?""",(refund["gig_id"],))
    db.commit()

    return redirect(url_for("account"))
