from wish import app, db
from flask import render_template, request, url_for, redirect, flash
from sqlalchemy import text

@app.route('/')
def home_page():
    cookie = request.cookies.get('name')
    print("<>home_page()")
    return render_template('home.html', cookie=cookie)



@app.route('/login', methods=['GET', 'POST'])
def login_pages():
    print("login was called")

    if request.method == 'POST':
        print("->login_pages()")
        username = request.form.get('Username')
        password = request.form.get('Password')
        print("Here the Data!!!")
        print(username)
        print(password)

        if (username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            print("not valid")
            flash(f"Username is not valid", category='warning')
            return render_template('login.html', cookie=None)

        if (password is None or
                isinstance(password, str) is False or
                len(password) < 3):
            print("something with password")
            flash(f"Password is not valid", category='warning')
            return render_template('login.html', cookie=None)

        query_stmt=f"select username from wishusers where username = '{username}' and password = '{password}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))

        user = result.fetchall()
        print("select:")
        print(user)
        if not user:
            flash(f"Try again", category='warning')
            return render_template('login.html', cookie=None)
        flash(f"'{user}', you are logged in ", category='success')

        resp = redirect('/wishes')
        resp.set_cookie('name', username)
        print("<-login(), go to wishes_pages")
        return resp
    return render_template('login.html', cookie=None)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        print("->register_page()")

        username = request.form.get('Username')
        email = request.form.get('Email')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        print(username)
        print(email)
        print(password1)
        print(password2)

        if(username is None or
                isinstance(username, str) is False or
                len(username) < 3):
            flash("Username not valid", category='danger')
            print("<-register_page(), username invalid")
            return render_template('register.html', cookie=None)

        if(email is None or
                isinstance(email, str) is False or
                len(email) < 3):
            print("<-register_page(), email not valid")
            flash("Email not valid", category='danger')
            return render_template('register.html', cookie=None)

        if(password1 is None or
                isinstance(password1, str) is False or
                len(password1) < 3 or
                password1 != password2):
            print("<-register_page(), password1 not valid")
            flash("Password1 not valid", category='danger')
            return render_template('register.html', cookie=None)

        query_stmt = f"select * from wishusers where username = '{username}'"
        print(query_stmt)
        result = db.session.execute(text(query_stmt))
        item = result.fetchone()
        print(item)

        if item is not None:
            flash("Username exists, try again")
            print("Username exists")
            return render_template('register.html', cookie=None)

        query_insert = f"insert into wishusers (username, email_address, password) values ('{username}', '{email}', '{password1}')"
        print(query_insert)
        db.session.execute(text(query_insert))
        db.session.commit()
        flash("You are registered", category='success')
        resp = redirect('/wishes')
        resp.set_cookie('name', username)
        print("<-register_page(), go to wishes_pages")
        return resp

    return render_template('register.html')

@app.route('/wishes')
def wishes_pages():

    cookie = request.cookies.get('name')
    print("->wishes_pages()", cookie)
    if not request.cookies.get('name'):
        print("<-wishes_pages(), no cookie")
        return redirect(url_for('login_pages'))

    query_stmt = f"select * from wishitems"
    result = db.session.execute(text(query_stmt))
    itemsquery = result.fetchall()

    print(itemsquery)
    print("<-wishes_pages()=", cookie)
    return render_template('wishes.html', items=itemsquery, cookie=cookie)


@app.route('/logout')
def logout():
    resp = redirect('/')
    resp.set_cookie('name', '', expires=0)
    return resp


@app.route('/wish_entry', methods=['GET', 'POST'])
def wish_entry():

    cookie = request.cookies.get('name')
    print("->wish_entry()", cookie)
    if not cookie:
        print("no cookie")
        return redirect(url_for('login'))

    if request.method == 'POST':
        priority = request.form.get('Priority')
        username = request.form.get('Username')
        item = request.form.get('Item')
        quantity = request.form.get('Quantity')

        query_insert = f"insert into wishitems (priority, username, item, quantity) values ({priority}, '{username}', '{item}', '{quantity}')"
        print(query_insert)
        db.session.execute(text(query_insert))
        db.session.commit()
        print("hey erfolgreich")
        resp = redirect('/wishes')
        resp.set_cookie('name', cookie)
        return resp

    return render_template('wish_entry.html', cookie=cookie)

@app.route('/wish_item/<int:item_id>', methods=['GET'])
def wish_item(item_id):
    print("->wish_item()")
    query_stmt = f"select * from wishitems where id={item_id}"

    result = db.session.execute(text(query_stmt))
    item = result.fetchone()
    print(query_stmt)
    if not item:
        print("item not existing")
        # error handling ....

    cookie = request.cookies.get('name')

    return render_template('wish_item.html', items=item, cookie=cookie)


