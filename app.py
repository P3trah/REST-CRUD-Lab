from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Plant

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
db = SQLAlchemy(app)

@app.route('/plants', methods=['GET'])
def get_all_plants():
    plants = Plant.query.all()
    output = []
    for plant in plants:
        plant_data = {}
        plant_data['id'] = plant.id
        plant_data['name'] = plant.name
        plant_data['image'] = plant.image
        plant_data['price'] = plant.price
        plant_data['is_in_stock'] = plant.is_in_stock
        output.append(plant_data)
    return jsonify({'plants': output})

@app.route('/plants/<int:plant_id>', methods=['GET'])
def get_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    plant_data = {}
    plant_data['id'] = plant.id
    plant_data['name'] = plant.name
    plant_data['image'] = plant.image
    plant_data['price'] = plant.price
    plant_data['is_in_stock'] = plant.is_in_stock
    return jsonify({'plant': plant_data})

@app.route('/plants', methods=['POST'])
def create_plant():
    data = request.get_json()
    new_plant = Plant(name=data['name'], image=data['image'], price=data['price'], is_in_stock=data['is_in_stock'])
    db.session.add(new_plant)
    db.session.commit()
    return jsonify({'message': 'New plant created'}), 201

@app.route('/plants/<int:plant_id>', methods=['PATCH'])
def update_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    data = request.get_json()

    if 'name' in data:
        plant.name = data['name']
    if 'image' in data:
        plant.image = data['image']
    if 'price' in data:
        plant.price = data['price']
    if 'is_in_stock' in data:
        plant.is_in_stock = data['is_in_stock']

    db.session.commit()
    return jsonify({'plant': plant.to_dict()})

@app.route('/plants/<int:plant_id>', methods=['DELETE'])
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    db.session.delete(plant)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5555)