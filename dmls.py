import os
from textwrap import wrap
import discord
import time
import base64
TOKEN = "Put your token here"
intents = discord.Intents.all()
client = discord.Client(intents=intents)
#you need read message history i guess
print('Please compress files before uploading them.')
idd = int(input('Channel id:\n')) #channel with data stored
readmode = input('(R)ead or (W)rite:\n')
if readmode == 'w':
    filetosend = input('Full file path:\n')
 
@client.event
async def on_ready():
    if readmode == 'r':
        data = ''
        filename = 'unknown.bin'
        channel = client.get_channel(idd)
        messages = channel.history(limit=50000, oldest_first=True)
        starttime = time.time()
        async for msg in messages:
            if msg.content.startswith('data:'):
                data+=msg.content[5:].replace("b'", "").replace("'","")
                print(f'data found, {msg.id}, {msg.content[:30]}...')
            if msg.content.startswith('meta:'):
                filename=msg.content[5:]
                print('found meta')
        endtime = time.time()
        newdata = base64.b64decode(data)
        print(f'KB/s: {(len(newdata)/1024)/(endtime-starttime)}')
        f = open(filename, 'wb+')
        f.write(newdata)
        f.close()
    else:
        f = open(filetosend, 'rb')
        filesize = os.path.getsize(filetosend)/1024
        fart = str(base64.b64encode(f.read()))
        n = 1993
        x = wrap(fart, n)
        channel = client.get_channel(idd)
        starttime = time.time()
        print('Sending')
        for datar in x:
            await channel.send(f'data:{datar}')
        print('Done')
        endtime = time.time()
        print(f'KB/s: {filesize/(endtime-starttime)}')
        await channel.send(f'Uploading speed (approximately) KB/s: {filesize/(endtime-starttime)}. Thats {(filesize/1024)/(endtime-starttime)} MB/s or {(filesize/1024/1024)/(endtime-starttime)} GB/s.')
        
client.run(TOKEN)
