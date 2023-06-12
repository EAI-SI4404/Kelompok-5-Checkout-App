from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from functools import wraps
import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'order'

mysql = MySQL(app)


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM CHECKOUT")

        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        # return jsonify(data)
        return jsonify({'status': 'success', 'message': 'Data retrieved successfully',
                        'timestamp': str(datetime.datetime.now()), 'data': data})

        cursor.close()

    elif request.method == 'POST':

        order_id = request.json['order_id']
        barang_id = request.json['barang_id']
        quantity = request.json['quantity']
        customer_id = request.json['customer_id']
        price = request.json['total_price']
        metode = request.json['metode_pembayaran']
        status = request.json['status_order']
        tgl = request.json['date_pemesanan']


        cursor = mysql.connection.cursor()
        sql = "INSERT INTO CHECKOUT (order_id, barang_id, quantity, customer_id, total_price, metode_pembayaran, status_order, date_pemesanan ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (order_id, barang_id, quantity, customer_id, price, status, metode, tgl)
        cursor.execute(sql, val)

        mysql.connection.commit()

        return jsonify({'status': 'success', 'message': 'Data added successfully',
                        'timestamp': str(datetime.datetime.now()), 'data': val})
        cursor.close()




@app.route('/editorder', methods=['PUT'])

def editorder():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE checkout SET  barang_id=%s, quantity=%s, customer_id=%s, total_price=%s, metode_pembayaran=%s, status_order=%s, date_pemesanan=%s WHERE order_id = %s"
        val = (data["barang_id"], data["quantity"], data["customer_id"], data["total_price"], data["metode_pembayaran"], data["status_order"],
                data["date_pemesanan"], request.args['id'],)
        cursor.execute(sql, val)

        mysql.connection.commit()
        return jsonify({'status': 'success', 'message': 'Data added successfully',
                        'timestamp': str(datetime.datetime.now()), 'data': val})
        cursor.close()


@app.route('/deleteorder', methods=['DELETE'])
def deleteorder():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM checkout WHERE order_id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)

        mysql.connection.commit()

        return jsonify({'status': 'success', 'message': 'Data deleted successfully',
                        'timestamp': str(datetime.datetime.now()), 'data': val})

        cursor.close()

@app.route('/detailorder')
def detailorder():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM checkout WHERE order_id = %s"
        val = ((request.args['id']),)
        cursor.execute(sql, val)

        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        return jsonify({'status': 'success', 'message': 'Data retrieved successfully',
                        'timestamp': str(datetime.datetime.now()), 'data': data})

        cursor.close()


    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=100, debug=True)