import asyncio

from os import getenv
from time import time
from httpx import AsyncClient

summer_start = 1622491200
summer_end = 1630440000
summer_ended = False
text_preset = 'Прошло уже {0:.2f}% лета.'
text_ended = 'Лето прошло, а ты так ничего и не сделал.'

async def main():
	global summer_ended

	VK_TOKEN = getenv('VK_TOKEN')
	owner_id = getenv('owner_id')

	if not all([VK_TOKEN, owner_id]):
		return

	client = AsyncClient(
		base_url = 'https://api.vk.com/method/',
		params = {
			'owner_id': owner_id,
			'v': 5.131,
			'access_token': VK_TOKEN
		})

	while not summer_ended:
		old_post_id = (
			await client.get('wall.get', params = {
				'count': 1, 
				'extended': 0, 
				'filter': 'owner'
				})
			).json()['response']['items'][0]['id']

		await client.get('wall.delete', params = {'post_id': old_post_id})

		percent = ((int(time()) - summer_start) / (summer_end - summer_start)) * 100

		if percent >= 100:
			summer_ended = True

		await client.get('wall.post', params = {'message': (text_preset.format(percent)) if not summer_ended else text_ended})

		await asyncio.sleep(900) # 15 minutes

	await client.aclose()	

if __name__ == '__main__':
	asyncio.run(main())