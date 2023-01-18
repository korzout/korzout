import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
	"""
	Наивный прогноз возраста пользователя по возрасту его друзей.

	Возраст считается как медиана среди возраста всех друзей пользователя

	:param user_id: Идентификатор пользователя.
	:return: Медианный возраст пользователя.
	"""
	# собираем информацию о друзьях пользователля
	friends = get_friends(user_id).items
	ages = []
	# создаем переменную, содержащую текущий год
	now = dt.datetime.now().year
	for friend in friends:
		try:
			# вычисляем возраст друзей пользователя, используя дату рождения
			ages.append(int(now - int(friend['bdate'][5:])))
		except:
			pass
	# сортируем список возрастов и возвращаем медиану
	ages.sort()
	if len(ages) == 0:
		return None
	return ages[len(ages)//2]
