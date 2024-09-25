from car_visualizer.app import db

# Define the Car model
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=True)
    engine_capacity = db.Column(db.Float, nullable=True)
    horse_power = db.Column(db.Float, nullable=True)
    cylinder = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Car {self.id}: {self.price}, {self.engine_capacity}, {self.horse_power}>"
