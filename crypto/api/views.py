from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from ..models import Crypto, url
from .serializers import CryptoSerializer, ConvertCryptoSerializer
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework import serializers



class OverallAV(APIView):

    # GETS A LIST OF CRYPTO REGISTERED ON THE DATABASE
    
    def get(self, request):
        queryset = Crypto.objects.all()
        serializer = CryptoSerializer(queryset, many=True)
        return Response(serializer.data)

    # REGISTER A NEW CRYPTO ON THE DATABASE

    def post(self, request):
        # CHECKS LENGTH OF CRYPTO'S IN DB
        if Crypto.objects.all().count() == 5:
            return Response({'message': "You can only have 5 crypto's in your dashboard. "}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = CryptoSerializer(data=request.data)
        if serializer.is_valid():

            # VERIFIES IF THE CRYPTO EXISTS

            coin = str(serializer.validated_data['name']).lower()
            response = requests.get(url.format(coin))
            if response.status_code == 200:

                # ADDS CRYPTO TO THE DASHBOARD
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response({'name': ["there is no crypto with this name"]}, status=response.status_code)

        return Response(serializer.errors)


class CryptoDetailAV(APIView):

    # GET A SPECIFIC CRYPTO FROM THE DB

    def get(self, request, *args, **kwargs):


        url = 'https://rest.coinapi.io/v1/exchangerate/{}/USD?apikey=E50B331F-56FA-4839-BE72-9DDC3EB657DA&time={}'

        slug = self.kwargs['slug']
        if not Crypto.objects.filter(slug=slug).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cryptoObj = Crypto.objects.get(slug=slug)
        
        # 1. check if the parameters to specific years where passed:
        fromDate = self.request.query_params.get('from')
        toDate = self.request.query_params.get('to')

        # 2. if so, get the prices from those dates using coinAPI
        if fromDate is not None:
            responseFromDate = requests.get(url.format(cryptoObj.symbol, fromDate))
            if responseFromDate.status_code == 200:

                jsonFromDate = responseFromDate.json()
                firstPrice = round(jsonFromDate['rate'], 2)

                # 2.1. checks if 'to' parameter was given: if so, do the request; if not, uses the actual price usind the DB price
                if toDate is not None:
                    responseToDate = requests.get(url.format(cryptoObj.symbol, toDate))
                    if responseToDate.status_code == 200:
                        jsonToDate = responseToDate.json()
                        secPrice = round(jsonToDate['rate'], 2)
                    else:
                        return Response({'time': "invalid parameter time 'to'"}, status=responseToDate.status_code)
                else:
                    toDate = cryptoObj.date
                    secPrice = cryptoObj.price

                #2.2. calculates the percent change and returns the data
                percent_change = round(((secPrice * 100) / firstPrice) - 100, 2)

                data = {
                    'crypto': cryptoObj.name,
                    'symbol': cryptoObj.symbol,
                    'dateI': fromDate,
                    'priceI': firstPrice,
                    'dateII': toDate,
                    'priceII': secPrice,
                    'percent_change': percent_change
                }

                return Response(data)

            # 3. in case the parameter 'from' is wrong
            return Response({'time': "invalid parameter time 'from'"}, status=responseFromDate.status_code)
        
        # 4. if no param was passed, just return the current crypto
        serializer = CryptoSerializer(cryptoObj)
        return Response(serializer.data)

    # DELETE CRYPTO FROM THE DATABASE

    def delete(self, request, *args, **kwargs):
        queryset = Crypto.objects.all()
        cryptocoin = get_object_or_404(queryset, slug=self.kwargs['slug'])
        cryptocoin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ConvertAV(APIView):

    def get(self, request):
        return Response({
            'fromCoin': 'Coin name that you wanna convert. ',
            'toCoin': 'Coin name that you wanna get in exchange. ',
            'amount': 'Amount of coins that wil be used to do the conversion. ',
        })
    
    def post(self, request, *args, **kwargs):
        serializer = ConvertCryptoSerializer(data=request.data)
        if serializer.is_valid():
            queryset = Crypto.objects.all()
            # CHECKS IF THESE COINS EXIST IN THE DATABASE
            coinI = get_object_or_404(queryset, name=serializer.validated_data['fromCoin'].lower())
            coinII = get_object_or_404(queryset, name=serializer.validated_data['toCoin'].lower())
            amount = serializer.validated_data['amount']

            # CONVERT COINS VALUES
            convertion = (coinI.price * amount) / coinII.price

            return Response({
                'status': 'Coins succesfully converted!',
                'message': f'{amount} coin of {coinI} is the same as {convertion} coins of {coinII}'
            })
        return Response(serializer.errors)