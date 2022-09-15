from nextcord import Interaction, Embed
import typing

class botInteraction(Interaction):
    async def send_spamSMS_embed(self, *, phone: int, counts: typing.List[int], status: int):
        embed = Embed(title="ส่งสแปม SMS", description="กำลังส่ง SMS ไปที่เบอร์ {phone}".format(phone=phone))
        embed.add_field(name="ทั้งหมด/สำเร็จ/ล้มเหลว", value="{}/{}/{}".format(counts[0], counts[1], counts[2]), inline=True)
        embed.add_field(name="สถานะ", value="{}".format("รอการทำงาน" if status == 0 else "กำลังโจมตี" if status == 1 else "หยุดทำงาน"), inline=True)
        sendMsg = await self.send(embed=embed)
        return sendMsg
    async def edit_spamSMS_embed(self, *, interaction, phone: int, counts: typing.List[int], status: int):
        embed = Embed(title="ส่งสแปม SMS", description="กำลังส่ง SMS ไปที่เบอร์ {phone}".format(phone=phone))
        embed.add_field(name="ทั้งหมด/สำเร็จ/ล้มเหลว", value="{}/{}/{}".format(counts[0], counts[1], counts[2]), inline=True)
        embed.add_field(name="สถานะ", value="{}".format("รอการทำงาน" if status == 0 else "กำลังโจมตี" if status == 1 else "หยุดทำงาน"), inline=True)
        sendMsg = await interaction.edit(embed=embed)
        return sendMsg
