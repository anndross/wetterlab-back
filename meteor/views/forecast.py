from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from core.utils import parse_coordinates 
from ..repositories.stations import station_repository 
from ..repositories.models import models_repository
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class Forecast(APIView):
    @method_decorator(cache_page(86400)) # Cache por 1 dia

    def get(self, request):
        # TODO: adicionar validações e retornar status

        # parâmetros
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')
        service = request.query_params.get('service')
        mean = request.query_params.get('mean')
        reftime = request.query_params.get('reftime')
        reftime_array = request.query_params.get('reftime').split('-')
        reftime = datetime(int(reftime_array[0]), int(reftime_array[1]), int(reftime_array[2]), int(reftime_array[3]), int(reftime_array[4]), int(reftime_array[5]))

        # a ordem é longitude e latitude
        coordinates = parse_coordinates([longitude, latitude])
        
        # pega os dados de models com base nos parâmetros
        models = models_repository.handle_data(coordinates, service, mean, reftime) or []

        models_len = len(models)

        if models_len > 0:
            date_from = models[0]['date']
            date_to = models[models_len - 1]['date']

            # pega os dados de stations com base nos parâmetros
            stations = station_repository.handle_data(coordinates, date_from, date_to, service, mean) or []
        else:
            return Response({
                'dates': [], 
                'stations': [], 
                'models': []
            })

        # pega o tamanho de stations e models
        stations_len = len(stations)

        # cria um array de datas com base no maior array
        def get_dates(data):
            return data['date']

        dates = map(get_dates, models)


        # preenche os dados que faltaram para o menor array com zeros
        models_filled_array = []
        stations_filled_array = []

        if models_len > stations_len: 
            for index in range(stations_len, models_len):
                stations_filled_array.append({
                    'date': models[index]['date'],
                    'value': 0
                })

        response_data = {
            'dates': dates, 
            'stations': stations + stations_filled_array, 
            'models': models + models_filled_array
        }

        mapped_stations = [
            {
                "x": [],
                "y": []
            },
            {
                "x": [],
                "y": []
            },
            {
                "x": [],
                "y": []
            }
        ]
        

        def push_stations_axle_x_and_y(data): 
            mapped_stations[0]['x'].append(data['date'])
            mapped_stations[0]['y'].append(data['value'])

            mapped_stations[1]['x'].append(data['date'])
            if data['value'] == 0:
                mapped_stations[1]['y'].append(data['value'])
            else: 
                mapped_stations[1]['y'].append(data['value'] / 1.2)

            mapped_stations[2]['x'].append(data['date'])
            if data['value'] == 0:
                mapped_stations[2]['y'].append(data['value'])
            else: 
                mapped_stations[2]['y'].append(data['value'] * 1.2)



        for data in response_data['stations']:
            push_stations_axle_x_and_y(data)

        mapped_models = [
            {
                "x": [],
                "y": []
            },
            {
                "x": [],
                "y": []
            },
            {
                "x": [],
                "y": []
            }
        ]
        def push_models_axle_x_and_y(data): 
            mapped_models[0]['x'].append(data['date'])
            mapped_models[0]['y'].append(data['value'])

            mapped_models[1]['x'].append(data['date'])
            if data['value'] == 0:
                mapped_models[1]['y'].append(data['value'])
            else: 
                mapped_models[1]['y'].append(data['value'] / 1.2)

            mapped_models[2]['x'].append(data['date'])
            if data['value'] == 0:
                mapped_models[2]['y'].append(data['value'])
            else: 
                mapped_models[2]['y'].append(data['value'] * 1.2)


        for data in response_data['models']:
            push_models_axle_x_and_y(data)

        response_data['stations'] = mapped_stations
        response_data['models'] = mapped_models

        return Response(response_data)
