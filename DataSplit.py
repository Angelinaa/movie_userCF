#__author__ = 'leng'
# -*- coding: utf-8 -*
#Split Dataset，将每个用户的记录分成5份，3份训练集，1份交叉验证集，1份测试集
def SplitData(data):
	train = dict()  # 训练集
	cv = dict()  # 交叉验证集
	test = dict()  # 测试集
	for user, item in data.items():
		num = 0
		for movie, rate in item.items():
			if num == 3:
				if user not in cv:  # 交叉验证集中没有该用户
					cv[user] = set()
				cv[user].add(movie)
				num += 1
			elif num == 4:
				if user not in test:  # 测试集中没有该用户
					test[user] = set()
				test[user].add(movie)
				num += 1
			else:
				if user not in train:  # 训练集中没有该用户
					train[user] = set()
				train[user].add(movie)
				num += 1
			if num == 5:
				num = 0
	return train, cv, test
