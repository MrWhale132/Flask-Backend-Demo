from __future__ import annotations

from flask import Flask, request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy import select

from varname import nameof


app=Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"]="postgres://postgres:admin@localhost:5432/test"
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mydb.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFIER_MODIFICATIONS"]=False
db = SQLAlchemy(app)
migrate=Migrate(app,db)
ma=Marshmallow(app)


class Product(db.Model):
    __tablename__="product"
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, nullable=True)
    
    def __init__(self, name:str):
        self.name=name


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =Product
        load_instance =True



@app.route("/product",methods=["GET"])
def getall():
    query=select(Product)
    daos=db.session.scalars(query).all()
        
    response=ProductSchema(many=True).dump(daos)
    
    return response,200



@app.route("/product/<id>",methods=["GET"])
def getsingle(id:int):
    query=select(Product).where(Product.id==id)
    dao=db.session.scalars(query).one()
    
    response=ProductSchema().dump(dao)
    
    return response, 200



@app.route("/product",methods=["POST"])
def create():
    body =request.json
    
    name=body["name"]
    
    product=Product(name=name)
    
    db.session.add(product)
    db.session.commit()
    
    response=jsonify({
        "id":product.id
    })
    
    return response,201



@app.route("/product/<id>",methods=["DELETE"])
def delete(id:int):
    user=db.session.get(Product,id)
    
    db.session.delete(user)
    db.session.commit()

    return "",204



@app.route("/product/<id>",methods=["PATCH"])
def update(id:int):
    body=request.json
    
    user=db.session.get(Product,id)
    
    if nameof(Product.name) in body:
        name =body["name"]
        user.name=name
        
    db.session.commit()
    
    return "",204
    


if __name__=="__main__":
    app.run(debug=True)
