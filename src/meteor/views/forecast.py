from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from core.utils import parse_coordinates 
from ..repositories.stations import station_repository 
from ..repositories.models import models_repository

class Forecast(APIView):
    def get(self, request):
        # parâmetros
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')
        service = request.query_params.get('service')
        date_from_array = request.query_params.get('from').split('-')
        date_to_array = request.query_params.get('to').split('-')
        mean = request.query_params.get('mean')
        date_from = datetime(int(date_from_array[0]), int(date_from_array[1]), int(date_from_array[2]), 0, 0, 0)
        date_to = datetime(int(date_to_array[0]), int(date_to_array[1]), int(date_to_array[2]), 0, 0, 0)
        reftime = request.query_params.get('reftime')

        if reftime:  
            reftime_array = request.query_params.get('reftime').split('-')
            reftime = datetime(int(reftime_array[0]), int(reftime_array[1]), int(reftime_array[2]), int(reftime_array[3]), int(reftime_array[4]), int(reftime_array[5]))

        # a ordem é longitude e latitude
        coordinates = parse_coordinates([longitude, latitude])
        
        # pega os dados de stations com base nos parâmetros
        stations = station_repository.handle_data(coordinates, date_from, date_to, service, mean) or []

        # pega os dados de models com base nos parâmetros
        models = models_repository.handle_data(coordinates, date_from, date_to, service, mean, reftime) or []

        # pega o tamanho de stations e models
        stationsLen = len(stations)
        modelsLen = len(models)

        # cria um array de datas com base no maior array
        dates = []

        def getDates(data):
            return data['date']

        if stationsLen > modelsLen:
            dates = map(getDates, stations)

        else:
            dates = map(getDates, models)


        # preenche os dados que faltaram para o menor array com zeros
        models_filled_array = []
        stations_filled_array = []

        if stationsLen > modelsLen:
            for index in range(modelsLen, stationsLen):
                models_filled_array.append({
                    'date': stations[index]['date'],
                    'value': 0
                })

        elif modelsLen > stationsLen: 
            for index in range(stationsLen, modelsLen):
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