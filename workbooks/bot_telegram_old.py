from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor 
from datetime import datetime


import os 

TOKEN="6802410302:AAGx_fgsySpTy5yCtZN35weSp-gnpFaV2pc"
user1 = {
    	 'money': 0,
		 'reason': ''
		 }

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def echo_send(message : types.Message):
	
	dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	for i in message.text.split():
		try:
			user1['money'] += int(i)
		except Exception as e:
			user1['reason'] += 'Other' if len(user1['reason']) == 0 else i

	print(f"{dt_string}: {message.from_user.full_name} said '{message.text}'")
	print(f"Money: {user1['money'] }")
	print(f"Payment reason: {user1['reason']}")	

	skip_message = False
	if message.text.lower() == 'Hi'.lower():
		txt = 'You too'
	elif message.text.lower() == 'total'.lower():
		txt = f"Total money: {user1['money']}"
	else:
		skip_message = True

	if not skip_message:
		await message.answer(txt)
		await message.reply(message.text)
		await bot.send_message(message.from_user.id, message.text)		


executor.start_polling(dp, skip_updates=True)
