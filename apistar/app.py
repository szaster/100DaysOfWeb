import json
from typing import List

from apistar import App, Route, types, validators # Validators -
from apistar.http import JSONResponse


# helpers

def _load_cars_data():
    with open('cars.json') as f:
        cars = json.loads(f.read())
        return {car["id"]: car for car in cars}


cars = _load_cars_data() # data structure - lowercase
VALID_MANUFACTURERS = set([car["manufacturer"] # constant
                          for car in cars.values()])
CAR_NOT_FOUND = 'Car not found'  # constant


# definition


class Car(types.Type):
    id = validators.Integer(allow_null=True)  # assign in POST
    manufacturer = validators.String(enum=list(VALID_MANUFACTURERS))
    model = validators.String(max_length=50) #car model length name <50 characters
    year = validators.Integer(minimum=1900, maximum=2050)
    vin = validators.String(max_length=50, default='')


# API methods

def list_cars() -> List[Car]:
    return [Car(car[1]) for car in sorted(cars.items())]
 #Car(car[1]) is a serialization



def create_car(car: Car) -> JSONResponse:
    car_id = len(cars) + 1
    car.id = car_id
    cars[car_id] = car
    return JSONResponse(Car(car), status_code=201)


def get_car(car_id: int) -> JSONResponse:
    car = cars.get(car_id)
    if not car:
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    return JSONResponse(Car(car), status_code=200)


def update_car(car_id: int, car: Car) -> JSONResponse:
    if not cars.get(car_id):
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    car.id = car_id
    cars[car_id] = car
    return JSONResponse(Car(car), status_code=200)


def delete_car(car_id: int) -> JSONResponse:
    if not cars.get(car_id):
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del cars[car_id]
    return JSONResponse({}, status_code=204)


routes = [
    Route('/', method='GET', handler=list_cars), #read all the cars
    Route('/', method='POST', handler=create_car), #create
    Route('/{car_id}/', method='GET', handler=get_car), #get individual cars
    Route('/{car_id}/', method='PUT', handler=update_car), #update
    Route('/{car_id}/', method='DELETE', handler=delete_car), #delete
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)