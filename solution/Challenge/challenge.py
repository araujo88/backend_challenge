import unittest
import requests
from pprint import pprint

URL = "http://127.0.0.1:8000/api/"


class Setup(unittest.TestCase):

    def test_create_car(self):
        r = requests.post(f"{URL}create-car/")
        response = r.json()
        pprint(response)
        self.assertEqual(response['capacity'], 65.0)

    def test_create_tyres(self):
        r = requests.get(f"{URL}get-cars/")
        response = r.json()
        car = response[-1]
        car_id = car['id']
        data = {"id": car_id}
        car_tyres = 0
        for i in range(0, 4):
            r = requests.post(f"{URL}create-tyre/", data=data)
            response = r.json()
            pprint(response)
            car_tyres += 1
        r = requests.get(f"{URL}get-car-status/{car_id}")
        response = r.json()
        pprint(response)
        num_tyres = response['num_tyres']
        self.assertEqual(car_tyres, num_tyres)

    def test_fill_tank(self):
        r = requests.get(f"{URL}get-cars/")
        response = r.json()
        car = response[-1]
        car_id = car['id']
        data = {"gas": 65.0}
        r = requests.post(f"{URL}refuel/{car_id}", data=data)
        response = r.json()
        pprint(response)
        gas = response['gas']
        self.assertEqual(gas, 65.0)


class Trip(unittest.TestCase):

    def test_trip(self):
        total_distance = 10000
        step = 100

        r = requests.get(f"{URL}get-cars/")
        response = r.json()
        car = response[-1]
        car_id = car['id']
        for distance in range(0, total_distance, step):
            r = requests.post(f"{URL}refuel/{car_id}", data={"gas": 65.0})
            r = requests.post(f"{URL}maintenance/{car_id}")
            r = requests.post(f"{URL}trip/{car_id}",
                              data={"distance": step})
        response = r.json()
        pprint(response)

    def test_check_tyres(self):
        r = requests.get(f"{URL}get-cars/")
        response = r.json()
        car = response[-1]
        pprint(car)
        num_tyres = car['num_tyres']
        self.assertEqual(num_tyres, 4)

    def test_check_fuel(self):
        r = requests.get(f"{URL}get-cars/")
        response = r.json()
        car = response[-1]
        pprint(car)
        current_gas = car['current_gas']
        self.assertGreaterEqual(current_gas, 0)


if __name__ == '__main__':
    unittest.main()
