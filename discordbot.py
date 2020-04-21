import discord 
import os
import asyncio
from discord.ext import tasks
import datetime
import re
import random
from func import diceroll
import urllib.request
import json

#トークン
TOKEN = os.environ['DISCORD_BOT_TOKEN']

CHANNEL_ID = 676738177062535168
great_owner_id = 459936557432963103
CHANNEL_ID3 = 664098210264121374
CHANNEL_ID_ALL = 668861946434682890
ksi_ver = '6.0.1'
discord_py_ver = '3.7.3'
g_set = 'voice-log'

url = "https://api.p2pquake.net/v1/human-readable?limit=1"
resp = urllib.request.urlopen(url).read()
resp = json.loads(resp.decode('utf-8'))

# 接続に必要なオブジェクトを生成
client = discord.Client()

#起動メッセージ
@client.event
async def on_ready():
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('----------------')
    print('Hello World,リマインドbotプログラム「project-RRN」、起動しました')
    channel = client.get_channel(CHANNEL_ID)
    await channel.purge()
    await channel.send(f'名前:{client.user.name}')  # ボットの名前
    await channel.send(f'ID:{client.user.id}')  # ボットのID
    await channel.send(f'Discord ver:{discord.__version__}')  # discord.pyのバージョン
    await channel.send('----------------')
    await channel.send('状態：BOT再起動しました。')
    await client.change_presence(status=discord.Status.idle,activity=discord.Game(name='創成の女神'))

@client.event
async def on_voice_state_update(member, before, after): 
    channels = client.get_all_channels()
    # channelsはbotの取得できるチャンネルのイテレーター
    global_channels = [ch for ch in channels if ch.name == g_set]
    # global_channelsは issue-global の名前を持つチャンネルのリスト
    for schannel in global_channels:
        if before.channel != after.channel:
            # before.channelとafter.channelが異なるなら入退室
            if after.channel and len(after.channel.members) == 1:
                # もし、ボイスチャットが開始されたら
                await schannel.send(f"{member.name}さんが通話を開始しました。\n場所：<#{after.channel.id}>(←クリックすると直接入れます)")

            if before.channel and len(before.channel.members) == 0:
                # もし、ボイスチャットが終了したら
                await schannel.send(f"{member.name}さんが通話を終了しました。\n場所：{before.channel.name}")

@client.event
async def on_message(message):

    url_re = r"https://discordapp.com/channels/(\d{18})/(\d{18})/(\d{18})"
    url_list  = re.findall(url_re,message.content)
    
    for url in url_list:
        guild_id,channel_id,message_id = url
        channel = client.get_channel(int(channel_id))

        if channel is not None:
            got_message = await channel.fetch_message(message_id)

            if got_message is not None:
                await message.channel.send(embed=open_message(got_message))
 

    if message.author.bot:  # ボットを弾く。
        return 

    if message.content == "json":
        await message.channel.send(resp)

    if client.user in message.mentions: # 話しかけられたかの判定
        hensin = random.choice(('よんだ？', 'なにー？', 'たべちゃうぞー！', 'がおー！', 'よろしくね', '！？'))
        reply = f'{message.author.mention} さん' + hensin + '```\n 私の機能が分からなかったら「ヘルプ」と打ってね☆```' #返信メッセージの作成
        await message.channel.send(reply) # 返信メッセージを送信

    if message.content.startswith("おはよ"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.author.id == great_owner_id:
            await message.channel.send('おはようございます！マスターさん！今日も一日頑張って下さい！') 
        if not message.author.id == great_owner_id:
            await message.channel.send(f"{message.author.mention} さん。おはようございます。") 

    if message.content.startswith("おやす"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.author.id == great_owner_id:
            await message.channel.send('おやすみなさい！マスターさん！今日も一日お疲れさまでした！') 
        if not message.author.id == great_owner_id:
            await message.channel.send(f"{message.author.mention} さん。おやすみなさい。") 

    if message.content == "ジャンケン":

        await message.channel.send( "最初はグー、じゃんけん" )
        
        def jankencheck(m):
            return m.content == "グー" or "チョキ" or "パー" and m.author == message.author
        try:
            reply = await client.wait_for( "message" , check = jankencheck , timeout = 10.0 )
        except asyncio.TimeoutError:
            await message.channel.send( "後出しはいけませんよ！\nあなたの負け！" )
        else:
            if reply.content == "チョキ":
                result = "グー"

            elif reply.content == "パー":
                result = "チョキ"

            elif reply.content == "グー":
                result = "パー"
     
            elif not reply.content == "グー" or reply.content == "チョキ" or reply.content == "パー":
                await message.channel.send("不適切な返事です。\nあなたの負け！")
                return

            await message.channel.send( result + "を出しました \nあなたの負け！" )

    if message.content == "おみくじ":
        # Embedを使ったメッセージ送信 と ランダムで要素を選択
        embed = discord.Embed(title="おみくじ", description=f"{message.author.mention}さんの今日の運勢は！",
                              color=0x2ECC69)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="[運勢] ", value=random.choice(('大吉', '中吉', '小吉', '吉', '半吉', '末吉', '末小吉', '凶', '小凶', '半凶', '末凶', '大凶')), inline=False)
        await message.channel.send(embed=embed)
        
    #運勢
    if message.content == '運勢':
        prob = random.random()
    
        if prob < 0.3:
            await message.channel.send('凶です……外出を控えることをオススメします')
           
        elif prob < 0.65:
            await message.channel.send('吉です！何かいい事があるかもですね！')
        
        elif prob < 0.71:
            await message.channel.send('末吉……どれくらい運がいいんでしょうね？•́ω•̀)?')
        
        elif prob < 0.76:
            await message.channel.send('半吉は吉の半分、つまり運がいいのです！')
        
        elif prob < 0.80:
            await message.channel.send('小吉ですね！ちょっと優しくされるかも？')
        
        elif prob < 0.83:
            await message.channel.send('吉の中で1番当たっても微妙に感じられる……つまり末吉なのです( ´･ω･`)')
       
        elif prob <= 1.0:
            await message.channel.send('おめでとうございます！大吉ですよ！(๑>∀<๑)♥')   
        

    if message.content == '御神籤':
        await asyncio.sleep(0.1)
        prob = random.random()
    
        if prob < 0.02: #大凶
            await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655056313637666816/20191213233945.jpg')
        
        elif prob < 0.10: #凶
            await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655055945659056134/20191213233816.jpg')
        
        elif prob < 0.35: #吉
            await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655055610441891840/20191213233638.jpg')
        
        elif prob < 0.55: #半吉
            await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655054936773754890/20191213233418.jpg')
        
        elif prob < 0.75: #小吉
            await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655054736638345238/20191213233326.jpg')
        
        elif prob < 0.95: #末吉
            await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655054481956012046/20191213233205.jpg')
       
        elif prob <= 1.0: #大吉
            await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655051678499995651/20191213232052.jpg')   
        

    if message.content == 'ステータス':
        if message.author.guild_permissions.administrator or message.author.id == great_owner_id:
            embed = discord.Embed(title="この鯖のステータス",description="Embed式")
            embed.add_field(name="サーバー名",value=f'{message.guild.name}',inline=False)
            embed.add_field(name="現オーナー名",value=f'{message.guild.owner}',inline=False)
            guild = message.guild
            member_count = sum(1 for member in guild.members if not member.bot) 
            bot_count = sum(1 for member in guild.members if member.bot) 
            all_count = (member_count) + (bot_count)
            embed.add_field(name="総人数",value=f'{all_count}',inline=False)
            embed.add_field(name="ユーザ数",value=f'{member_count}',inline=False)
            embed.add_field(name="BOT数",value=f'{bot_count}',inline=False)
            embed.add_field(name="テキストチャンネル数",value=f'{len(message.guild.text_channels)}個',inline=False)
            embed.add_field(name="ボイスチャンネル数",value=f'{len(message.guild.voice_channels)}個',inline=False)
            embed.set_thumbnail(url=message.guild.icon_url)
            await message.channel.send(embed=embed)

        else:
            await message.channel.send('貴方は管理者権限がありません。 \n You do not have admin roles !!')

        #年月日
    if message.content == '何日？':
        date = datetime.datetime.now()
        await message.channel.send(f'今日は{date.year}年{date.month}月{date.day}日です！')    
    if message.content == '何時？':
        date = datetime.datetime.now()
        await message.channel.send(f'今は{date.hour}時{date.minute}分{date.second}秒だよ！')
    if message.content == '時計':
        weekdays = datetime.date.today().weekday()
        if weekdays == 0:
            weekday_name = "月曜日"
        elif weekdays == 1:
            weekday_name = "火曜日"
        elif weekdays == 2:
            weekday_name = "水曜日"
        elif weekdays == 3:
            weekday_name = "木曜日"
        elif weekdays == 4:
            weekday_name = "金曜日"
        elif weekdays == 5:
            weekday_name = "土曜日"
        elif weekdays == 6:
            weekday_name = "日曜日"
        else:
            weekday_name = "エラー"
        date = datetime.datetime.now()
        embed = discord.Embed(title="時計", description="TimeZone(Japan)",color=random.choice((0,0x1abc9c,0x11806a,0x2ecc71,0x1f8b4c,0x3498db,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0x95a5a6,0x607d8b,0x979c9f,0x546e7a,0x7289da,0x99aab5)))
        embed.add_field(name="日付", value=f'{date.year}年{date.month}月{date.day}日{weekday_name}', inline=False)
        embed.add_field(name="時間", value=f'{date.hour}時{date.minute}分{date.second}秒', inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/688986679956340804/690461569854996490/180half_f.gif")
        await message.channel.send(embed=embed)
        
 
    if message.content == 'nrestart': 
        if message.author.id == great_owner_id:
            await message.channel.send('再起動します')
            await asyncio.sleep(0.5)
            await client.logout()  
            os.execv(sys.executable,[sys.executable, os.path.join(sys.path[0], __file__)] + sys.argv[1:])  
        if not message.author.id == great_owner_id:
            await message.channel.send('貴方にこのコマンドの使用権限はありません')   

    if message.content == 'nclear': 
        if message.author.id == great_owner_id:
            await message.channel.purge()  
        if not message.author.id == great_owner_id:
            await message.channel.send('貴方にこのコマンドの使用権限はありません')   

    if not message.author.id == 664880378481213473:
        prob = random.random()
    
        if prob < 0.02:
            if not message.content.startswith("スロット"): 
                await message.add_reaction('💝')

    if message.content == "スロット": 
        suroto=random.choice(('０', '１', '２', '３', '４', '５', '６', '７', '８', '９'))
        suroto1=random.choice(('０', '１', '２', '３', '４', '５', '６', '７', '８', '９'))
        suroto2=random.choice(('０', '１', '２', '３', '４', '５', '６', '７', '８', '９'))
        await asyncio.sleep(0.1)
        my_message = await message.channel.send('スロット結果がここに表示されます！')
        await asyncio.sleep(3)
        await my_message.edit(content='？|？|？')
        await asyncio.sleep(1)
        await my_message.edit(content=suroto + '|？|？')
        await asyncio.sleep(1)
        await my_message.edit(content=suroto + '|' + suroto1 + '|？')
        await asyncio.sleep(1)
        await my_message.edit(content=suroto + '|' + suroto1 + '|' + suroto2)
        if suroto == suroto1 == suroto2:
            await my_message.edit(content=suroto + '|' + suroto1 + '|' + suroto2 + '\n 結果：大当たり！！')
        elif suroto == suroto1 or suroto == suroto2 or suroto1 == suroto2:
            await my_message.edit(content=suroto + '|' + suroto1 + '|' + suroto2 + '\n 結果：リーチ！')
        else:
            await my_message.edit(content=suroto + '|' + suroto1 + '|' + suroto2 + '\n 結果：ハズレ')
        
    if message.content.startswith("!dc"):
        # 入力された内容を受け取る
        say = message.content 

        # [!dc ]部分を消し、AdBのdで区切ってリスト化する
        order = say.strip('!dc ')
        cnt, mx = list(map(int, order.split('d'))) # さいころの個数と面数
        dice = diceroll(cnt, mx) # 和を計算する関数(後述)
        await message.channel.send(dice[cnt])
        del dice[cnt]

        # さいころの目の総和の内訳を表示する
        await message.channel.send(dice)
     
    if message.content == 'coin sn1' or message.content == 'coin sn2':
        if message.author.id == great_owner_id:
            coin=random.choice(('●', '○'))
            if message.content == 'coin sn1':
                my_message = await message.channel.send('コイントスをします！')
                await asyncio.sleep(3)
                await my_message.edit(content='定義：○は表、●は裏')
                await asyncio.sleep(3)
                await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：　```定義：○は表、●は裏```')
                await asyncio.sleep(2)
                await my_message.edit(content='　結果：' + coin + '```定義：○は表、●は裏 \n adid:sn1```')
                return
            elif message.content == 'coin sn2':
                my_message = await message.channel.send('コイントスをします！')
                await asyncio.sleep(3)
                await my_message.edit(content='定義：●は表、○は裏')
                await asyncio.sleep(3)
                await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：　```定義：●は表、○は裏```')
                await asyncio.sleep(2)
                await my_message.edit(content='　結果：'+ coin + '```定義：●は表、○は裏 \n adid:sn2```')
                return
        await message.channel.send('Error:You cannot use this command')  
        return

    if message.content == 'coin':
        coin=random.choice(('●', '○'))
        coin1=random.choice(('1', '2'))
        await asyncio.sleep(0.1)
        if coin1 == '1':
            my_message = await message.channel.send('コイントスをします！')
            await asyncio.sleep(3)
            await my_message.edit(content='定義：○は表、●は裏')
            await asyncio.sleep(3)
            await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：　```定義：○は表、●は裏```')
            await asyncio.sleep(2)
            await my_message.edit(content='　結果：' + coin + '```定義：○は表、●は裏 \n adid:sn' + coin1 + '```')
            
            return
        elif coin1 == '2':
            my_message = await message.channel.send('コイントスをします！')
            await asyncio.sleep(3)
            await my_message.edit(content='定義：●は表、○は裏')
            await asyncio.sleep(3)
            await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
            await asyncio.sleep(0.5)
            await my_message.edit(content='抽選中：　```定義：●は表、○は裏```')
            await asyncio.sleep(2)
            await my_message.edit(content='　結果：'+ coin + '```定義：●は表、○は裏 \n adid:sn' + coin1 + '```')
            
            return
        await message.channel.send('Error')

    if message.content == 'ヘルプ':
        page_count = 0 #ヘルプの現在表示しているページ数
        page_content_list = [">>> **ノアコマンド一覧(ページ1)**\n\n**何時？**：今の時間を教えてくれます！(何時何分何秒)\n**何日？**：何日か教えてくれます！(何月何日)\n\n➡絵文字を押すと次のページへ",
            ">>> **ノアコマンド一覧(ページ2)**\n\n**!dc XdY**：Y面のダイスをX回振ります！\n**coin**：コイントスを行います。\n**スロット**：あなたは大当たりを引けるのか!？\n\n➡絵文字で次のページ\n⬅絵文字で前のページ",
            ">>> **ノアコマンド一覧(ページ3)**\n\n**おみくじ**or**御神籤**：おみくじが引けます！\n**運勢**：貴方の運勢は！\n\n➡絵文字で次のページ\n⬅絵文字で前のページ",
            ">>> **ノアコマンド一覧(ページ4)**\n\n以下のコマンドは__管理者権限__が必要\n**ステータス**：この鯖のステータスです。\n\n➡絵文字で次のページ\n⬅絵文字で前のページ",
            ">>> **このBOT詳細情報(ページ5)**\n\nBOT名前：" + f"{client.user.name}" + "\nBOT ID：" + f"{client.user.id}" + "\nDiscord.pyバージョン：" + f"{discord.__version__}" + "\npythonバージョン：" + discord_py_ver + "\n開発バージョン：" + ksi_ver + "\n開発者：<@459936557432963103>\n\n⬅絵文字で前のページ"] #ヘルプの各ページ内容] #ヘルプの各ページ内容
        
        send_message = await message.channel.send(page_content_list[0]) #最初のページ投稿
        await send_message.add_reaction("➡")

        def help_react_check(reaction,user):
            '''
            ヘルプに対する、ヘルプリクエスト者本人からのリアクションかをチェックする
            '''
            emoji = str(reaction.emoji)
            if reaction.message.id != send_message.id:
                return 0
            if emoji == "➡" or emoji == "⬅":
                if user != message.author:
                    return 0
                else:
                    return 1

        while not client.is_closed():
            try:
                reaction,user = await client.wait_for('reaction_add',check=help_react_check,timeout=60.0)
            except asyncio.TimeoutError:
                await send_message.clear_reactions()
                msg_end = '\n ```State:Stop```'
                await send_message.edit(content=page_content_list[page_count] + msg_end)
                return #時間制限が来たら、それ以降は処理しない
            else:
                emoji = str(reaction.emoji)
                if emoji == "➡" and page_count < 4:
                    page_count += 1
                if emoji == "⬅" and page_count > 0:
                    page_count -= 1

                await send_message.clear_reactions() #事前に消去する
                msg_act = '\n ```State:Active```'
                await send_message.edit(content=page_content_list[page_count] + msg_act)

                if page_count == 0:
                    await send_message.add_reaction("➡")
                elif page_count == 1:
                    await send_message.add_reaction("⬅")
                    await send_message.add_reaction("➡")
                elif page_count == 2:
                    await send_message.add_reaction("⬅")
                    await send_message.add_reaction("➡")
                elif page_count == 3:
                    await send_message.add_reaction("⬅")
                    await send_message.add_reaction("➡")
                elif page_count == 4:
                    await send_message.add_reaction("⬅")
                    #各ページごとに必要なリアクション

def open_message(message):
    """
    メッセージを展開し、作成した埋め込みに各情報を添付し返す関数

    Args:
        message (discord.Message) : 展開したいメッセージ

    Returns:
        embed (discord.Embed) : メッセージの展開結果の埋め込み
    """
    color_code = random.choice((0,0x1abc9c,0x11806a,0x2ecc71,0x1f8b4c,0x3498db,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0x95a5a6,0x607d8b,0x979c9f,0x546e7a,0x7289da,0x99aab5))
    embed = discord.Embed(title=message.content,description=f"[メッセージリンク]({message.jump_url})",color=color_code)

    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url) #メッセージ送信者
    embed.set_footer(text=message.guild.name, icon_url=message.guild.icon_url) #メッセージのあるサーバー
    embed.timestamp = message.created_at #メッセージの投稿時間

    if message.attachments:
        embed.set_image(url=message.attachments[0].url) #もし画像があれば、最初の画像を添付する
    return embed

logch_id = 673412099350855702

@client.event
async def on_member_join(member):
    guild = member.guild 
    member_count = sum(1 for member in guild.members if not member.bot)
    bot_count = sum(1 for member in guild.members if member.bot)
    logch = client.get_channel(logch_id)
    msg = [
        f"鳥だ！飛行機だ！いや{member.mention}",
        f"綺麗な月と{member.mention}ですね……",
        f"まぶしい朝には{member.mention}を一杯！うまい！",
        f"{member.mention}がご降臨なさった！崇め敬え奉れ！",
        f"にげろ！{member.mention}だ！",
        f"{member.mention}生きとったんかワレ！",
        f"うるせえ{member.mention}なげるぞ！",
        f"あ！{member.mention}だ！",
        f"予期されていたかのように{member.mention}が現れた……",
        f"野生の{member.mention}が現れた！",
        f"綺麗な夕日と{member.mention}に乾杯"
    ]
    embed = discord.Embed(
        title = "ようこそ！",
        description = random.choice(msg) + f"\n現在のメンバーは**{str(member_count)}**人です。\nBotは**{str(bot_count)}**個です。",
        color = random.choice((0,0x1abc9c,0x11806a,0x2ecc71,0x1f8b4c,0x3498db,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0x95a5a6,0x607d8b,0x979c9f,0x546e7a,0x7289da,0x99aab5))
    )
    embed.timestamp = datetime.now(JST) 
    await logch.send(embed=embed) 
    
@client.event
async def on_member_remove(member):
    guild = member.guild 
    member_count = sum(1 for member in guild.members if not member.bot)
    bot_count = sum(1 for member in guild.members if member.bot)
    logch = client.get_channel(logch_id)
    msg = [
        f"森へおかえり、{member.mention}",
        f"僕は全てを失った。金も、名誉も、{member.mention}も",
        f"だれだゴミ箱に{member.mention}を入れたのは",
        f"ねえマミー、僕の{member.mention}はどこー？",
        f"さようならっ{member.mention}！",
        f"{member.mention}\nあいつは良い奴だったよ",
        f"{member.mention}は星になったのさ"
    ]
    embed = discord.Embed(
        title = "さようなら(´;ω;｀)！",
        description = (
            random.choice(msg) + 
            f"\n現在のメンバーは**{str(member_count)}**人です。\nBotは**{str(bot_count)}**個です。"
        ),
        color = random.choice((0,0x1abc9c,0x11806a,0x2ecc71,0x1f8b4c,0x3498db,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0x95a5a6,0x607d8b,0x979c9f,0x546e7a,0x7289da,0x99aab5))
    )
    embed.timestamp = datetime.now(JST)  
    await logch.send(embed=embed) 
    
client.run(TOKEN)

#ノア
