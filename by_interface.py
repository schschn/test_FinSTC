from flask import Flask, jsonify, make_response, request, redirect, render_template
import json

api = Flask(__name__)


@api.route('/html_create', methods=['GET', 'POST'])
def html_create():
    data = json.load(open('purchase_history.json'))

    if request.method == 'POST':
        vintage = 1 if request.form.get('vintage') == '1' else 0
        price = request.form.get('price')
        dealer_name = request.form.get('dealer_name')
        car_name = request.form.get('car_name')
        purchase_date = request.form.get('purchase_date')

        if any(len(i.strip()) < 1 for i in [price, dealer_name, car_name, purchase_date]):
            return render_template('404.html', msg='no one will fill in all the parameters for you, you should fix it')
        if price.isalpha() == True:
            return render_template('404.html', msg='do not write symbols in numerical data')

        new_data = {'id': len(data)+1, 'vintage': vintage, 'price': price,
                    'dealer_name': dealer_name, 'car_name': car_name, 'purchase_date': purchase_date}

        data.append(new_data)
        with open('purchase_history.json', 'w') as file:
            json.dump(data, file)
    return render_template('html_create.html', data=data)


@api.route('/html_retrieve', methods=['GET', 'POST'])
def html_retrieve():
    data = json.load(open('purchase_history.json'))
    data_dealers = set([i['dealer_name'] for i in data])
    data_cars = set([i['car_name'] for i in data])

    if request.method == 'POST':
        dealers = request.form.getlist('dealers')
        cars = request.form.getlist('cars')

        if dealers == []:
            data = [i for i in data if i['car_name'] in cars]
        elif cars == []:
            data = [i for i in data if i['dealer_name'] in dealers]
        else:
            data = [i for i in data if i['car_name'] in cars] + [i for i in data if i['dealer_name'] in dealers]
        return render_template('html_retrieve.html', data=data, dealers=data_dealers, cars=data_cars)

    return render_template('html_retrieve.html', data=data, dealers=data_dealers, cars=data_cars)


@api.route('/html_update', methods=['GET', 'POST'])
def html_update():
    data = json.load(open('purchase_history.json'))

    if request.method == 'POST':
        id_ = int(request.form.get('id'))
        vintage = 1 if request.form.get('vintage') == '1' else 0
        price = request.form.get('price')
        dealer_name = request.form.get('dealer_name')
        car_name = request.form.get('car_name')
        purchase_date = request.form.get('purchase_date')
        params = [id_, vintage, price, dealer_name, car_name, purchase_date]

        for row in data:
            if row['id'] == id_:
                for param, key in zip(params, row):
                    if param != '':
                        row[key] = param

        with open('purchase_history.json', 'w') as file:
            json.dump(data, file)

    return render_template('html_update.html', data=data)


@api.route('/html_delete', methods=['GET', 'POST'])
def html_delete():
    data = json.load(open('purchase_history.json'))
    data_ids = [i['id'] for i in data]
    if request.method == 'POST':
        id_ = int(request.form.get('id'))
        new_data = [i for i in data if i['id'] != id_]

        with open('purchase_history.json', 'w') as file:
            json.dump(new_data, file)

        return render_template('html_delete.html', data=new_data, data_ids=data_ids)

    return render_template('html_delete.html', data=data, data_ids=data_ids)


@api.route('/home', methods=['GET', 'POST'])
def home():
    data = json.load(open('purchase_history.json'))
    return render_template('home.html', data=data)


@api.route('/crud', methods=['GET', 'POST', 'PUT', 'DELETE'])
def crud():
    data = json.load(open('purchase_history.json'))

    if request.method == 'POST':
        vintage = 1 if request.args.get('vintage') == '1' else 0
        price = request.args.get('price')
        dealer_name = request.args.get('dealer_name')
        car_name = request.args.get('car_name')
        purchase_date = request.args.get('purchase_date')

        if any(len(i.strip()) < 1 for i in [price, dealer_name, car_name, purchase_date]):
            return make_response(jsonify({'error': 'one or many parameters are not specified'}), 400)
        if price.isalpha() == True:
            return make_response(jsonify({'error': 'price is not a num'}), 400)

        new_data = {'id': len(data) + 1, 'vintage': vintage, 'price': price,
                    'dealer_name': dealer_name, 'car_name': car_name, 'purchase_date': purchase_date}

        data.append(new_data)
        with open('purchase_history.json', 'w') as file:
            json.dump(data, file)
        return make_response(jsonify({'status': f'new row added: {new_data}'}), 200)


    if request.method == 'GET':
        dealers = request.args.getlist('dealers')
        cars = request.args.getlist('cars')

        if dealers == [] and cars == []:
            data = data
            return make_response(jsonify(data), 200)

        elif dealers != [] and cars != []:
            dealers = [i for i in data if i['dealer_name'] in dealers]
            cars = [i for i in data if i['car_name'] in cars]
            data = dealers + cars
            return make_response(jsonify(data), 200)

        elif dealers == []:
            data = [i for i in data if i['car_name'] in cars]
            return make_response(jsonify(data), 200)

        elif cars == []:
            data = [i for i in data if i['dealer_name'] in dealers]
            return make_response(jsonify(data), 200)


    if request.method == 'PUT':
        try:
            id_ = int(request.args.get('id'))
        except:
            return make_response(jsonify({'error': 'no id in request'}), 400)
        vintage = 1 if request.args.get('vintage') == '1' else 0
        price = request.args.get('price')
        dealer_name = request.args.get('dealer_name')
        car_name = request.args.get('car_name')
        purchase_date = request.args.get('purchase_date')
        params = [id_, vintage, price, dealer_name, car_name, purchase_date]

        for row in data:
            if row['id'] == id_:
                for param, key in zip(params, row):
                    if param != '' or param != None:
                        row[key] = param

        with open('purchase_history.json', 'w') as file:
            json.dump(data, file)
        return make_response(jsonify({'status': 'row updated'}), 200)


    if request.method == 'DELETE':
        try:
            id_ = int(request.args.get('id'))
        except:
            return make_response(jsonify({'error': 'use only numbers'}), 400)
        new_data = [i for i in data if i['id'] != id_]

        with open('purchase_history.json', 'w') as file:
            json.dump(new_data, file)
        return make_response(jsonify({'status': f'row {id_} deleted'}), 200)


@api.route('/')
def rdrct():
    return redirect('/home')

if __name__ == '__main__':
    api.run()
