import requests, json, datetime, time, re, threading
from discord_webhook import DiscordWebhook, DiscordEmbed

itemDetails = None
cookie = 'put your roblox cookie here' # needed for grabbing price from roblox.com requires cookie
webhook = 'put your discord webhook here'

def itemInfo():
    global itemDetails
    while True:
        itemDetails = json.loads(
                re.search('item_details = (.*?);', requests.get('https://www.rolimons.com/itemtable').text).group(1)
            )
        time.sleep(180)

threading.Thread(target=itemInfo).start()
time.sleep(3)

def checkMarket():
    checked = []
    while True:
        try:
            response = json.loads(
                re.search('initial_activity = (.*?);', requests.get('https://www.rolimons.com/marketactivity').text).group(1)
            )
            for sale in response: # assetId, oldRap, newRap = sale[1], sale[3], sale[4]
                if sale[-1] not in checked:
                    checked.append(sale[-1])
                    salePrice = round(sale[3] - (sale[3] - sale[4])*10)

                    averagePrice = int(requests.get(f'https://www.roblox.com/catalog/{sale[1]}', cookies = {'.ROBLOSECURITY': cookie}).text.split('expected-price="')[1].split('"')[0])

                    if salePrice <= averagePrice*0.7 or salePrice >= sale[3]*2:

                        webhook = DiscordWebhook(
                            url=webhook
                        )

                        embed = DiscordEmbed(
                            title=f"{itemDetails[str(sale[1])][0]}",
                            url=f'https://www.rolimons.com/item/{sale[1]}',
                            color='aa70e6'
                        )

                        embed.add_embed_field(name='Sale Price', value=salePrice, inline=True)
                        embed.add_embed_field(name='\u200b', value='\u200b', inline=True)
                        embed.add_embed_field(name='Normal Price', value=averagePrice, inline=True)
                        embed.add_embed_field(name='New RAP', value=str(sale[4]), inline=True)
                        embed.add_embed_field(name='Old RAP', value=str(sale[3]), inline=True)
                        embed.set_thumbnail(url=f"{itemDetails[str(sale[1])][-1]}")

                        webhook.add_embed(embed)
                        response = webhook.execute()
            time.sleep(60)
        except:
            time.sleep(15)
            pass



checkMarket()
