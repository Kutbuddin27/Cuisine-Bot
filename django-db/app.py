from flask import Flask, render_template,request,redirect, url_for
import mysql.connector
from datetime import date,datetime

app = Flask(__name__)

@app.route('/')
def display_data():
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='Rasa_database',
        password='Kutub@123',
        database='rasa'
    )

    # Create a cursor to execute SQL queries
    cursor = connection.cursor(dictionary=True)
    # Delete rows where TimeStamp is not equal to today's date
    # current_date = date.today()
    # cursor.execute('DELETE FROM information WHERE DATE(TimeStamp) != %s', (current_date,))

    # Execute a SELECT query to get data from the database
    cursor.execute('SELECT * FROM information')

    # Fetch all rows
    data = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    connection.close()

    # Render the HTML template with the data
    return render_template('index.html', data=data)

@app.route('/delete_row', methods=['POST'])
def delete_row():
    # Get the orderId from the form submission
    order_id = request.form['orderId']

    connection = mysql.connector.connect(
        host='localhost',
        user='Rasa_database',
        password='Kutub@123',
        database='rasa'
    )
    cursor = connection.cursor(dictionary=True)
    # Delete the row from the database
    cursor.execute('DELETE FROM information WHERE orderId = %s', (order_id,))
    connection.commit()

    return redirect(url_for('display_data'))

@app.route('/menu', methods=['GET', 'POST'])
def display_menu():
    if request.method == 'POST':
        # Get form data
        food_item = request.form.get('food_item')
        price = request.form.get('price')
        category = request.form.get('category')
        
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='Rasa_database',
            password='Kutub@123',
            database='rasa'
        )

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        if 'add' in request.form:
            # Check if the food item already exists in the database
            cursor.execute('SELECT * FROM menu WHERE food_items = %s', (food_item,))
            existing_item = cursor.fetchone()

            if existing_item:
                # If the item exists, update the price
                cursor.execute('UPDATE menu SET price = %s, categories = %s WHERE food_items = %s', (price, category, food_item))
            else:
                # If the item does not exist, insert a new record
                cursor.execute('INSERT INTO menu (food_items, price, categories) VALUES (%s, %s, %s)', (food_item, price, category))
        elif 'delete' in request.form:
            # Delete the row with the given food item
            cursor.execute('DELETE FROM menu WHERE food_items = %s', (food_item,))

        # Commit changes and close the cursor and database connection
        connection.commit()
        cursor.close()

    # Connect to the MySQL database (again to fetch updated data)
    connection = mysql.connector.connect(
        host='localhost',
        user='Rasa_database',
        password='Kutub@123',
        database='rasa'
    )

    # Create a cursor to execute SQL queries
    cursor = connection.cursor(dictionary=True)

    # Execute a SELECT query to get data from the menu
    cursor.execute('SELECT * FROM menu')

    # Fetch all rows
    menu_data = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    connection.close()

    # Render the HTML template with the menu data
    return render_template('menu.html', menu_data=menu_data)

if __name__ == '__main__':
    app.run(debug=True)