import discord
import os
import requests
import json
import random
from replit import db
from keep_up import keep_alive

my_secret = os.environ['bot']

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry"]

starter_enc = ["Cheer up!", "Hang in there.", "Super si!", "Dovolj igranja minecrafta @Beber Biber Bober#7778!"]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)


def update_enc(enc_msg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(enc_msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [enc_msg]

def delete_enc(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))



@client.event
async def on_message(message):
  msg = message.content

  if message.author == client.user:
    return
  if msg.startswith("$zivijo"):
    await message.channel.send("Cao!")
  if msg.startswith("$inspire"):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_enc
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])
  
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$dodaj"):
    enc_msg = msg.split("$dodaj ", 1)[1]
    update_enc(enc_msg)
    await message.channel.send("Dodana nova poved!")
  if msg.startswith("$izbrisi"):
    enc = []
    if "encouragements" in db.keys():
      index = int(msg.split("$izbrisi ", 1)[1])
      delete_enc(index)
      enc = list(db["encouragements"])
    await message.channel.send(enc)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = list(db["encouragements"])
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responing is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responing is off.")

keep_alive()
client.run(my_secret)
