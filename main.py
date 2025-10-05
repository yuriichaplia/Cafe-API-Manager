from os import environ
from random import randint
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound
from sqlalchemy import Integer, String, Boolean
from flask import Flask, jsonify, render_template, request
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()

app = Flask(__name__)

class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random", methods=["GET"])
def random():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    random_index = randint(0, len(cafes))
    random_cafe = cafes[random_index].to_dict()

    return jsonify(cafe=random_cafe)

@app.route("/all_cafes", methods=["GET"])
def all_cafes():
    cafes = db.session.execute(db.select(Cafe)).scalars().all()
    all_elements = []
    for element in cafes:
        all_elements.append(element.to_dict())

    return jsonify(cafes=all_elements)

@app.route("/search", methods=["GET"])
def search():
    location = request.args.get('loc')
    all_cafes_in_loc = (db.session.execute(db.select(Cafe).where(Cafe.location == location))
                            .scalars().all())
    if len(all_cafes_in_loc) == 1:
        return jsonify(cafe=all_cafes_in_loc.to_dict())
    elif len(all_cafes_in_loc) > 1:
        all_elements = []
        for element in all_cafes_in_loc:
            all_elements.append(element.to_dict())
        return jsonify(cafes=all_elements)
    else:
        error = {
            'Not Found': "Sorry, we don't have a cafe at that location."
        }
        return jsonify(error=error)

@app.route("/add", methods=["GET", "POST"])
def add():
    cafe = Cafe(name=request.form['name'],
                map_url = request.form['map_url'],
                img_url=request.form['img_url'],
                location=request.form['location'],
                seats=request.form['seats'],
                has_toilet=bool(request.form['has_toilet']),
                has_wifi=bool(request.form['has_wifi']),
                has_sockets=bool(request.form['has_sockets']),
                can_take_calls=bool(request.form['can_take_calls']),
                coffee_price=request.form['coffee_price']
    )
    db.session.add(cafe)
    db.session.commit()
    response = {
        "success": "Successfully added the new cafe. "
    }
    return jsonify(response=response)

@app.route("/update-price/<int:cafe_id>", methods=["GET", "PATCH"])
def update_price(cafe_id):
    try:
        cafe_to_update = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar_one()
        new_price = request.args.get('new_price')
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        response = {
            "success": "Successfully updated price. "
        }
        return jsonify(response=response)
    except (AttributeError, NoResultFound):
        response = {
            "Not Found": "Sorry, a cafe with that id was not found in our cafe database. "
        }
        return jsonify(response=response)

@app.route("/report-closed/<int:cafe_id>", methods=["GET", "DELETE"])
def delete(cafe_id):
    api_key = request.args.get('api_key')
    if api_key == environ.get('API_KEY'):
        try:
            cafe_to_delete = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar_one()
            db.session.delete(cafe_to_delete)
            db.session.commit()
            response = {
                "Success": "That cafe was deleted from our cafe database. "
            }
            return jsonify(response=response)
        except NoResultFound:
            response = {
                "Not Found": "Sorry, a cafe with that id was not found in our database. "
            }
            return jsonify(error=response)
    else:
        response = {
            "Error": "Sorry, that's not allowed. You must have correct API Key. "
        }
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
