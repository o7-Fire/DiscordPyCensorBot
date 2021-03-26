import traceback
import keep_alive
keep_alive.keep_alive()
import os
import discord
import unicodedata
import subprocess
import json
import sys
import urllib.request
import operator
import re


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


isSpamAllowed = 0
try:
    with open("spamsettings.txt", "r+") as f:
        isSpamAllowed = f.read()
except FileNotFoundError:
    print("gay")
print("VALUE OF ISSPAMALLOWED: " + str(isSpamAllowed))
print("fuck you faggots you niggers are gay")
TOKEN = os.getenv('BOT_TOKEN')  # for now use glitch api since volas having problem
##https://o7-api.glitch.me
##https://o7inc.ddns.net
o7API = "https://o7-api.glitch.me"  # choose your api
client = discord.Client()  # finally migrated to o7inc.ddns.net api
spam = {}
threshold = 0.7  # anything higher than this get vetoed
thresholdMinimizer = 0.25  # to sum up with other value
thresholdNeutralizer = 0.017  # round to 0 automatically
thresholdMaximizer = 0.81  # if the index above this and is safe dont delete
safeIndex = ["Neutral"]  # never trust Drawing
censored_words = ["suck me", "suck ne", "masterbat",
                  "horny", "lesbian", "bisexual", "vagina", "penis", "cock", "mastorbat",
                  "hentai", "henthai", "hxntai", "hormy", "fuck ne", "masturbat",
                  "sex", "porn", "daddy", "porm", "fuck me", "anal", "buttplug",
                  ":woozy_face:", ":flushed:", ":drooling_face:", "rape"]  # 343591759332245505
whitelisted_users = [7706075274265231707, 753874678220849174, 332394297536282634]
urlDiscordMedia = re.compile("((https|http):\/\/[0-9a-zA-Z\.\/_-]+.(png|jpg|gif|webm|mp4))")
#just ten more year we solved world hunger



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


def getClassification(img: str):
    content = urllib.request.urlopen(o7API + '//api/json/graphical/classification/' + img).read()#wow retard use double slash
    report = json.loads(content)
    reportActual: dict = {} 
    if type(report) is dict:
        return report["error"]
    for fe in report:
        reportActual[fe['className']] = float(fe['probability'])
    return reportActual

def checkvideotype(name, prefix):
  filename = name[-len(prefix)-1:]
  if filename==f'.{prefix}':
    return True

async def WarnUserVideoType(message, sta = {}): 
  att = message.attachments[0].filename
  if checkvideotype(att, 'mp4') or checkvideotype(att, 'webm'):
    await message.channel.send(
                "<@" + str(message.author.id) + "> bot detected that the attachment u posted is nsfw (definitely)\nAttachment type: " + "video\n" + sta[0] +
                sta[1] + sta[2] + sta[3])
  if checkvideotype(att, 'gif'): 
    await message.channel.send(
                "<@" + str(message.author.id) + "> bot detected that the attachment u posted is nsfw (definitely)\nAttachment type: " + "gif\n" + sta[0] +
                sta[1] + sta[2] + sta[3])
  elif checkvideotype(att, 'png') or checkvideotype(att, 'jpg'):
    await message.channel.send(
                "<@" + str(message.author.id) + "> bot detected that the attachment u posted is nsfw (definitely)\nAttachment type: " + "image\n" + sta[0] +
                sta[1] + sta[2] + sta[3])
def aboveLimit(val: float):
    return val > threshold


def neutralize(contents: dict, key: str, target: str):
    if contents[key] < thresholdNeutralizer:
        contents[target] = 0
    if contents[key] > 1 - thresholdNeutralizer:
        contents[target] = 0
    if contents[key] < thresholdMinimizer:
        contents[target] = contents[target] - thresholdMinimizer


async def checkVisual(message):
    if message.channel.nsfw:
        return
    urls: list = urlDiscordMedia.findall(message.content)
    done: list = []
    for img in message.attachments:
        if done.__contains__(img): continue
        done.append(img)
        if await checkVisualF(message, img.url):
            return True
    for u in urls:
        if done.__contains__(u[0]): continue
        done.append(u[0])
        if await checkVisualF(message, u[0]):
            return True
    return False


async def checkVisualF(message, img):
    try:
        ##get from api
        debug = "debug" in message.content
        contents = getClassification(img)  # ignorant is a bliss
        if not type(contents) is dict:
            if debug:
                await message.channel.send(contents)
            return True
        ##Test shit
        """
        top2: list = []
        top2Value: list = []
        top2Val: float
        top2Name: str = ""
        cont: list = sorted(contents.items(), key=operator.itemgetter(1), reverse=True)
        for i in range(2):
         #   top2.append(cont[i][0])
        #for i in range(2):
         #   top2Value.append(cont[i][1])
        #top2Val = top2Value[0] + top2Value[1]
        #contents["BorderlineHentai"] = (
        #        contents["Drawing"] * contents["Hentai"] * contents["Hentai"] / contents["Neutral"])
        # neutralize(contents, "Hentai", "BorderlineHentai")
        #contents["Digital"] = contents["Porn"] / 1.5 + contents["Neutral"] / 2 + contents["Drawing"] / 1.3
        # neutralize(contents, "Neutral", "Digital")
        #contents["Anime"] = (contents["Drawing"] - contents["Hentai"])
        # neutralize(contents, "Hentai", "BorderlineHentai")
        #contents["UntrustedDrawing"] = (
        #        (contents["Sexy"] + contents["Porn"] + contents["Hentai"] + contents["Drawing"]) / 1.5 - contents[
         #   "Neutral"])
        #neutralize(contents, "Sexy", "UntrustedDrawing")
        """
        sortedReport: list = sorted(contents.items(), key=operator.itemgetter(1), reverse=True)
        # print(sortedReport)
        if debug:##Print Details
            ss: str = ""
            for subject in sortedReport:  # mfw subject is tuple
                name: str = subject[0]
                if subject[1] > threshold:
                    name = "**Above-Threshold**-**" + name + "**"
                ss = ss + (name + ": " + str(subject[1])) + "\n"
            await message.channel.send(ss)

        for sf in safeIndex:
            if contents[sf] > thresholdMaximizer:
                return False #it prints out bot detected that the image u posted is nsfw (definitely) even though its video, not image
        ##Moderate by itzbenz
        #if contents["BorderlineHentai"] > threshold:
        #    await message.delete()
        #    await message.channel.send("<@" + str(message.author.id) + "> Borderline Hentai is not allowed")
        #    return True
        #if contents["Anime"] > threshold and debug:  # mfw use distance
         #   await message.channel.send("<@" + str(message.author.id) + "> is this anime ?")
        #if contents["Digital"] > threshold and debug:
            # await message.delete()
         #   await message.channel.send("<@" + str(message.author.id) + "> a digital generated image ?")
        # if contents["TransparentPorn"] > threshold:
        #     await message.delete()
        #     await message.channel.send("<@" + str(message.author.id) + "> Shady porn")
        #    return
        # report = json.loads(contents)
        # quick use contents['Drawing']/api/json/graphical/classification/
        
        ##Nexity shenanigans
        #std = subprocess.run(['curl', 'https://o7-api.glitch.me//api/json/graphical/classification/' + img],
         #                    capture_output=True, text=True)
        #sta = str(std.stdout).split(",")
        ##checkstring = sta[0] + sta[1] + sta[2] + sta[3]
        #if "Sexy" in sta[0] or "Porn" in sta[0] or "Hentai" in sta[0]:
        #    await message.delete()
        #    await WarnUserVideoType(message, sta)
        #elif "Sexy" in sta[2] or "Porn" in sta[2] or "Hentai" in sta[2]:
         #   a = float(sta[1].replace('"probability":', '').replace('}', ''))
         #   b = float(sta[3].replace('"probability":', '').replace('}', ''))
         #   if b > 0.25:
         #       await message.delete()
          #      await WarnUserVideoType(message, sta)
         ##       return True
        #    else:
         #       await WarnUserVideoType(message, sta)
         #       return True
        return False
    except Exception as e:
        print("no image found")
        traceback.print_exc()
        print("stackerror: " + str(e))
        return False

    # o hey it works @itzbenz


async def basicHandle(message):
    print("VV---------------------------------------------VV")
    print(message.author.name + ": " + message.content)
    try:
        img = message.attachments[0].url
        print(message.author.name + ": " + img)
    except:
        a = 0
    print("^^---------------------------------------------^^")
    if message.content == "test":
        await message.channel.send("aliven't")
    if message.author.id in whitelisted_users:
        if message.content == "restartbot":
            await message.channel.send("restarting")
            restart_program()
        return


async def checkSpam(message):
    global isSpamAllowed
    print("the spam : " + str(isSpamAllowed))
    # hey @itzbenz am I on crack or is it not returning and stil deleting
    # it shows the spam : 1 but it still deletes the message
    if isSpamAllowed == 1:
        return False
    try:
        if message.content.lower() == spam[message.author.id]:
            await message.delete()
            # channel = await message.author.create_dm()
            # await channel.send("stop spamming")
            # do i need to block the bots
            return True
    except:
        print("oh noes")
    finally:
        spam[message.author.id] = message.content.lower()
    return False


@client.event
async def on_message(message):
    global isSpamAllowed
    if message.author.id == 0:
      await message.delete()
    if message.author.bot:
        return
        # DONT DELETE
    await basicHandle(message)  # please dont delete this
    if message.content == "switchspam":
        if message.author.id in whitelisted_users or message.author.id == 343591759332245505:
            if isSpamAllowed:
                isSpamAllowed = 0
                with open("spamsettings.txt", "w+") as f:
                    f.write(str(isSpamAllowed))
                await message.channel.send("turned on antispam")
            else:
                isSpamAllowed = 1
                with open("spamsettings.txt", "w+") as f:
                    f.write(str(isSpamAllowed))
                await message.channel.send("turned off antispam")
    if "is AFK" in message.content and message.author.id == 155149108183695360:
        await message.delete()
    if message.author.id in whitelisted_users and not str(message.content).startswith("debug"):
        return
    if not message.content == "debug":
        if await checkSpam(message):
            return
    if await checkVisual(message):
        return
    for words in censored_words:
        if message.channel.nsfw:
            return
        msg = message.content.lower().replace("0", "o").replace("4", "a").replace("3", "e").replace("@", "o").replace(
            "1", "l").replace(".", "").replace(" ", "")
        if words in unicodedata.normalize('NFKC', msg):
            await message.delete()
            await message.channel.send("get censored")


if __name__ == '__main__':
    client.run(TOKEN)
