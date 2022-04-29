from crypto.models import Crypto

def update_crypto():
    queryset = Crypto.objects.all()

    for coin in queryset:
        try:
            oldPrice = coin.price
            coin.save()
            newPrice = coin.price
            print(f'updated {coin.name}! from {oldPrice} to {newPrice}')
        except:
            print('ERRO')