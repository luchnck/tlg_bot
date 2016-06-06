"""
	Хелперы для обработки данных логики
"""

"""
	Генерация списков заданий на лету, в зависимости от количества участников 
	генератор возвращает в каждой итерации список сдвинутый на автоматически рассчитанный шаг
"""
def generateTaskLists(list,teams):
    interval = int(round(len(list)/teams));i=0
    while i < teams:
        yield list[i*interval:len(list)]+list[0:i*interval]
        i+=1

