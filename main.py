#__author__ = 'leng'
# -*- coding: utf-8 -*
from DataSplit import *
from UserSimilarity import *
from Index import *
import pandas as pd
from Recommend import GetRecommendation
import numpy as np

if __name__ == "__main__":
	r = dict()
	try:
		#生成用户-电影矩阵，第一行是所有电影id，第一列是所有用户id，矩阵内是评分数据
		#r是第一列字典，即存储用户id的字典
		df = pd.read_csv("3.csv", encoding="utf-8")
		for row in df.itertuples():
			movie_id=getattr(row, 'movie_id')
			user_id = getattr(row, 'user_id')
			rate = getattr(row, 'rate')
			if user_id not in r:
				r[user_id] = dict()
			r[user_id][movie_id] = rate
		#print("r矩阵：",r["abin520918"])
		"""ratings = open('ratings.dat')
		for each_line in ratings:
			try:
				(userID, movieID, rate, timestamp) = each_line.split('::')
				if userID not in r:
					r[userID] = dict()
				r[userID][movieID] = int(rate)  # 记录一个用户给一部电影的评分
			except ValueError as err:
				print('ValueError' + str(err))"""
	except IOError as err:
		print("IOError" + str(err))

	re = r.copy()
	print("re原始长度：", len(re))
	for user, item in r.items():
		if len(item.items()) < 5:
			#print("用户id:", user)
			#print("该用户的数据条数为：", len(item.items()))
			re.pop(user)
	print("re删除后长度：", len(re))
	r=re
	print("r删除后长度：", len(r))

	print("切分数据集开始")
	(train, cv, test) = SplitData(r)  # 将数据集分为训练集、交叉验证集和测试集，3:1:1
	print("切分数据集完成")
	print("训练集：", len(train))
	print("测试集：", len(test))
	print("交叉验证集：", len(cv))
	#print("测试集：",test["abin520918"])
	print("相似性计算开始")
	# UserCF，用户相似度选择
	W = InvertedIndex(train)  # 余弦相似度，倒排表实现
	#	W = ImprovedSimilarity(train)  # 改进的余弦相似度
	#W = Dist_Similarity(train, r)  # 基于距离的相似度
	#	W = FusionSimilarity(w, dist)   # 基于距离和余弦相似度的加权相似度
	#	W = FusionSimilarity(w, dist)   # 基于距离和改进余弦相似度的加权相似度
	print("相似性计算完成")
	N=10
	K=40
	for user in train:
		user_recommend=[]
		recommend_items = set()
		rank = GetRecommendation(user, train, W, K, r)
		rec_item = sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]
		for item, pui in rec_item:
			recommend_items.add(item)
		#print("recommend_items",recommend_items)
		user_recommend.append(user)
		user_recommend.extend(recommend_items)
		df2 = pd.DataFrame(user_recommend)
		df2=df2.T
		#print(df2)
		df2.to_csv('result.csv',mode='a',header=False,index=False)
		#print("user_recommend",user_recommend)
		#print("shape:",np.array(user_recommend).shape)

"""

	listN = [20, 40, 60]  # 给用户u推荐的item个数
	listK = [20, 40, 80, 160]  # 与用户u兴趣最相似的K个用户
	max_F = 0  # 最优F值
	optim_K = 0  # 最优K值
	optim_N = 0  # 最优N值
	for N in listN:
		for K in listK:
			recall = Recall(train, cv, W, K, r, N)  # 召回率
			precision = Precision(train, cv, W, K, r, N)  # 准确率
			coverage = Coverage(train, cv, W, K, r, N)  # 覆盖率
			popularity = Popularity(train, cv, W, K, r, N)  # 新颖度
			F = 2 * precision * recall / (precision + recall)  # F值
			if F > max_F:
				max_F = F
				optim_K = K
				optim_N = N
			try:
				with open('analysis.txt', 'a') as anafile:
					print(N, K, file= anafile)
					print(recall * 100, file=anafile)
					print(precision * 100, file=anafile)
					print(coverage * 100, file=anafile)
					print(popularity, file=anafile)
					print(F * 100, file=anafile)
			except IOError as err:
				print('File Error: ' + str(err))

	print('The optimal N and K are: ')
	print(optim_N, optim_K)
	recall = Recall(train, test, W, optim_K, r, optim_N)  # 召回率
	precision = Precision(train, test, W, optim_K, r, optim_N)  # 准确率
	coverage = Coverage(train, test, W, optim_K, r, optim_N)  # 覆盖率
	popularity = Popularity(train, test, W, optim_K, r, optim_N)  # 新颖度
	F = 2 * precision * recall / (precision + recall)  # F值
	print('%s: %.2f%%' % ('Recall', recall * 100))
	print('%s: %.2f%%' % ('Precision', precision * 100))
	print('%s: %.2f%%' % ('Coverage', coverage * 100))
	print('%s: %.2f' % ('Popularity', popularity))
	print('%s: %.2f%%' % ('F_value', F * 100))
"""