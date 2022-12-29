import requests, random

updateWebhook = ''
significantWebhook = ''

class Bot:

    def __init__(self, proxies):
        self.proxies = proxies
        self.rap = self.rapDict()
        self.constants()

    def rapDict(self):
        cursor, arr = '', {}
        while cursor != None:
            try:
                resp = requests.get(
                    f'https://inventory.roblox.com/v1/users/1/assets/collectibles?sortOrder=Asc&limit=100&cursor={cursor}',
                    proxies = {'https': f'http://{random.choice(self.proxies)}'}, timeout = 5
                ).json()
                for item in resp['data']:
                    arr[str(item['assetId'])] = item['recentAveragePrice']
                cursor = resp['nextPageCursor']
            except:
                pass
        return arr

    def constants(self):
        while True:
            cursor = ''
            while cursor != None:
                try:
                    resp = requests.get(
                        f'https://inventory.roblox.com/v1/users/1/assets/collectibles?sortOrder=Asc&limit=100&cursor={cursor}',
                        proxies = {'https': f'http://{random.choice(self.proxies)}'}, timeout = 5
                    ).json()
                    for item in resp['data']:
                        assetId = str(item['assetId'])
                        if assetId in self.rap:
                            currentRap, previousRap = item['recentAveragePrice'], self.rap[assetId]
                            if currentRap != previousRap:
                                self.sendWebhook(assetId, item['name'], currentRap, previousRap, round(previousRap - ((previousRap-currentRap)*10)))
                                self.rap[assetId] = currentRap
                    cursor = resp['nextPageCursor']
                except:
                    pass

    def grabImage(self, assetId):
        while True:
            try:
                resp = requests.get(
                    f'https://thumbnails.roblox.com/v1/assets?assetIds={assetId}&returnPolicy=0&size=250x250&format=Png&isCircular=false',
                    proxies = {'https': f'http://{random.choice(self.proxies)}'}, timeout = 3
                ).json()
                if 'data' in resp:
                    return resp['data'][0]['imageUrl']
            except:
                pass

    def sendWebhook(self, assetId, assetName, currentRap, previousRap, salePrice):
        if previousRap*0.5 < salePrice < previousRap*2: webhook = updateWebhook
        else: webhook = significantWebhook
        if previousRap < currentRap: color = '1DC321'
        else: color = 'C31D1D'

        requests.post(
            webhook,
            json = {
                'embeds': [{
                    'author': {
                        'name': f'{assetName}',
                        'url': f'https://www.rolimons.com/item/{assetId}'
                    },
                    'thumbnail': {
                        'url': self.grabImage(assetId)
                    },
                    'fields': [
                        {'name': 'Old RAP', 'value': f'{"{:,}".format(previousRap)}', 'inline':True},
                        {'name': 'New RAP', 'value': f'{"{:,}".format(currentRap)}', 'inline':True},
                        {'name': 'Sale Price', 'value': f'{"{:,}".format(salePrice)}', 'inline':True},
                    ],
                    'color': int(color,16)
                }
            ]}
        )

Bot(
    open('proxies.txt').read().splitlines()
)
