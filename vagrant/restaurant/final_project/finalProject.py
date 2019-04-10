from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake Restaurants
#restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
#restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
#items = [{'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'}]
#item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


# JSON API Endpoints
@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def menuJSON(restaurant_id):
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


@app.route('/')
@app.route('/restaurants')
def showRestaurants(): # READ
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant(): # CREATE
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("Restaurant Successfully Created!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id): # UPDATE
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        flash("Restaurant Successfully Edited!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=editedRestaurant)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id): # DELETE
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        flash("Restaurant Successfully Deleted!")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=deletedRestaurant)


@app.route('/restaurants/<int:restaurant_id>')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id): # READ
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant_id=restaurant_id, restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id): # CREATE
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("Menu Item Successfully Created!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id): # UPDATE
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash("Menu Item Successfully Edited!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id): # DELETE
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Menu Item Successfully Deleted!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key' # flask will use this to create sessions for our users
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
