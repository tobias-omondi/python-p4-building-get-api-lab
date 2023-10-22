#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakery_list = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "bakery_id": bakery.id,
            "created_at": bakery.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "id": bakery.id,
            "name": bakery.name,
            "price": bakery.price,
            "updated_at": bakery.updated_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.updated_at else None
        }
        bakery_list.append(bakery_dict)
    r = make_response(
        jsonify(bakery_list),
        200
    )
    return r

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    bakery_dict = {
        "bakery_id": bakery.id,
        "created_at": bakery.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "id": bakery.id,
        "name": bakery.name,
        "price": bakery.price,
        "updated_at": bakery.updated_at.strftime('%Y-%m-%d %H:%M:%S') if bakery.updated_at else None,
        "baked_goods": []
    }
    for baked_good in bakery.baked_goods:
        baked_good_dict = {
              "baked_good_id": baked_good.id,
            "created_at": baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "updated_at": baked_good.updated_at.strftime('%Y-%m-%d %H:%M:%S') if baked_good.updated_at else None
        }
    
        bakery_dict["baked_goods"].append(baked_good_dict)
        res = make_response(
            jsonify(bakery_dict),
            200
        )
    return res

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_list = []
    for baked_good in BakedGood.query.order_by(BakedGood.price.desc()).all():
        baked_good_dict = {
            "baked_good_id": baked_good.id,
            "created_at": baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "updated_at": baked_good.updated_at.strftime('%Y-%m-%d %H:%M:%S') if baked_good.updated_at else None
        }

        baked_goods_list.append(baked_good_dict)
        RES = make_response(
            jsonify(baked_goods_list),
            200
        )
    return RES

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    baked_good_dict = {
      "baked_good_id": baked_good.id,
        "created_at": baked_good.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "id": baked_good.id,
        "name": baked_good.name,
        "price": baked_good.price,
        "updated_at": baked_good.updated_at.strftime('%Y-%m-%d %H:%M:%S') if baked_good.updated_at else None
    }
    return jsonify(baked_good_dict)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
