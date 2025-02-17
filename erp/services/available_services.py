from setup.db import erp_connection
from setup.utils import parse_bson

class AvailableServicesService: 
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def get_coordinates(self):
        production = erp_connection.get_collection('production')
        
        query = {
            'customer_id': int(self.customer_id)
        }

        production_data_by_customer_id = production.find_one(query)

        production_data_by_customer_id = list(map(lambda x: list(reversed(x)), production_data_by_customer_id['services'][0]['locations']))

        return parse_bson(production_data_by_customer_id)
