import random
from threading import Thread
from datetime import datetime,timezone,timedelta

def tag(name,ctx): #標記
  conv=[
    '王子先生，王子先生\n要品茗嗎?\n茗就是茶阿!',
    '在古今中外的繪本裡阿，\n保護公主，\n就是王子先生的使命呦。',
    '早上，一睜開眼，\n首先要跟小鳥先生們，\n說聲早安呀~',
    '女孩子就是活在夢之國裡，\n做著夢的呀。\n命運的王子先生與夢之國~♪',
    f'{name}王子先生，有什麼事嗎？'
  ]
  if "讓我看看" in ctx:
    return "不要!"
  else:
    return random.choice(conv)

def conv_input(conv):
  print(conv)
  f = open('/home/evanlau/dc-bot/conv_log.txt','a')
  f.writelines(f"{str(conv)}\n")
  f.close()

def write_log(conv):
  write = Thread(target=conv_input(conv))
  write.start()

def feedback(conv):
  dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
  dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換台灣時區
  ticks = int(dt2.strftime("%H"))
  if ticks >= 5 and ticks <= 11:
    ctx=['早安~請問要來點甜蜜的早餐嗎？']
    return random.choice(ctx)
  if ticks >= 12 and ticks <= 18:
    ctx=['午安~要和我共進下午茶嗎？']
    return random.choice(ctx)
  if ticks >= 19 and ticks <= 23:
    ctx=['晚安~祝你有個美夢～']
    return random.choice(ctx)
  if ticks >= 0 and ticks <= 3:
    ctx=['今晚不讓你睡喔~♥王子大人']
    return random.choice(ctx)
  if ticks == 4 :
    ctx=['王子大人，啊……啊，不要這樣♥']
    return random.choice(ctx)

def gif(message):
  if '🎤' in str(message):
    return 'https://media.discordapp.net/attachments/903285693655162932/904025706286178334/1.gif'

  if 'mumei' in str(message):
    return 'https://i.imgur.com/xojG0xB.gif'

  if 'ina1' == str(message):
    return 'https://i.imgur.com/GfDvVdg.gif'

  if 'ina2' == str(message):
    return 'https://i.imgur.com/mNBAdoA.gif'

  if 'yagoo' in str(message):
    return 'https://i.imgur.com/DUM40wt.gif'
  return False

def print_ctx(message):
  dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
  dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換台灣時區
  ticks = dt2.strftime("%H:%M:%S")
  try:
    conv=str(message.author)+'於'+str(ticks)+'在'+str(message.guild.name)+'的'+str(message.channel)+'說:'+str(message.content)
  except:
    conv=str(message.author)+'於'+str(ticks)+'在'+str(message.channel)+'說:'+str(message.content)
  write_log(conv)

def print_cmd(message,cmd):
  dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
  dt2 = dt1.astimezone(timezone(timedelta(hours=8))) # 轉換台灣時區
  ticks = dt2.strftime("%H:%M:%S")
  try:
    conv=str(message.author)+'於'+str(ticks)+'在'+str(message.guild.name)+'的'+str(message.channel)+'用:'+str(cmd)
  except:
    conv=str(message.author)+'於'+str(ticks)+'在'+str(message.channel)+'用:'+str(cmd)
  write_log(conv)