#__author__ = 'leng'
# -*- coding: utf-8 -*
# 评价指标

import math
from Recommend import GetRecommendation

# 召回率
def Recall(train, test, W, K, r, N):
	hit = 0
	n_recall = 0
	print("召回率计算开始")
	for user in train:
		tu = test[user]
		rank = GetRecommendation(user, train, W, K, r)
		rec_item = sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]  # 推荐感兴趣程度前N的item
		for item, pui in rec_item:
			if item in tu:
				hit += 1
		n_recall += len(tu)
	print("召回率计算完成")
	return hit / (n_recall * 1.0)


# 准确率
def Precision(train, test, W, K, r, N):
	hit = 0
	n_precision = 0
	for user in train:
		tu = test[user]
		rank = GetRecommendation(user, train, W, K, r)
		rec_item = sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]  # 推荐感兴趣程度前N的item
		for item, pui in rec_item:
			if item in tu:
				hit += 1
		n_precision += N
	return hit / (n_precision * 1.0)


# 覆盖率
def Coverage(train, test, W, K, r, N):
	recommend_items = set()
	all_items = set()
	for user in train:
		for item in train[user]:
			all_items.add(item)
		rank = GetRecommendation(user, train, W, K, r)
		rec_item = sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]  # 推荐感兴趣程度前N的item
		for item, pui in rec_item:
			recommend_items.add(item)
	return len(recommend_items) / (len(all_items) * 1.0)


# 新颖度，用平均流行度来衡量
def Popularity(train, test, W, K, r, N):
	item_popularity = dict()  # item的流行度
	for user in train:
		for item in train[user]:
			if item not in item_popularity:
				item_popularity[item] = 1
			else:
				item_popularity[item] += 1
	ret = 0
	n = 0
	for user in train:
		rank = GetRecommendation(user, train, W, K, r)
		rec_item = sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N]  # 推荐感兴趣程度前N的item
		for item, pui in rec_item:
			ret += math.log(1 + item_popularity[item])  # 物品流行度分布满足长尾分布，取对数后均值更加平稳
			n += 1
	ret /= (n * 1.0)
	return ret
