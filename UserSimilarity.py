#__author__ = 'leng'
# -*- coding: utf-8 -*
# 相似度函数
import math

# 余弦相似度，O(N*N)
def Cosine_Similarity(train):
	w = dict()
	for u in train.keys():
		w[u] = dict()
		for v in train.keys():
			if u == v:
				continue
			co_items = list(set(train[u]).intersection(set(train[v])))  # 用户u和用户v都产生行为的item，交集
			w[u][v] = len(co_items)
			w[u][v] /= math.sqrt(len(train[u]) * len(train[v]))
	return w


# 余弦相似度，倒排表实现
def InvertedIndex(train):
	# build inverted table for item_users，倒排表
	item_users = dict()
	for u, items in train.items():
		for i in items:
			if i not in item_users:
				item_users[i] = set()
			item_users[i].add(u)
	print("倒排表完成")
	# calculate co-rated items between users，计算用户u和用户v都产生行为的item的个数
	C = dict()
	N = dict()
	for i, users in item_users.items():
		for u in users:
			if u not in C:
				C[u] = dict()
			if u not in N:
				N[u] = 1
			else:
				N[u] += 1  # 记录每个用户的item个数
			for v in users:
				if u == v:
					continue
				if v not in C[u]:
					C[u][v] = 1
				else:
					C[u][v] += 1  # 记录用户u和用户v同时喜欢的物品的数量
	print("计算item个数完成")
	# calculate final similarity matrix W，计算相似度
	W = dict()
	for u, related_users in C.items():
		if u not in W:
			W[u] = dict()
		for v, cuv in related_users.items():
			W[u][v] = cuv / math.sqrt(N[u] * N[v])
	return W


# 改进的兴趣相似度计算公式
def ImprovedSimilarity(train):
	# build inverted table for item_users，倒排表
	item_users = dict()
	for u, items in train.items():
		for i in items:
			if i not in item_users:
				item_users[i] = set()
			item_users[i].add(u)

	# calculate co-rated items between users
	C = dict()
	N = dict()
	for i, users in item_users.items():
		for u in users:
			if u not in C:
				C[u] = dict()
			if u not in N:
				N[u] = 1
			else:
				N[u] += 1  # 记录每个用户的item个数
			for v in users:
				if u == v:
					continue
				if v not in C[u]:
					C[u][v] = 1 / math.log(1 + len(users))  # 惩罚用户u和用户v共同兴趣列表中热门物品对他们相似度的影响
				else:
					C[u][v] += 1 / math.log(1 + len(users))

	# calculate final similarity matrix W，计算相似度
	W = dict()
	for u, related_users in C.items():
		if u not in W:
			W[u] = dict()
		for v, cuv in related_users.items():
			W[u][v] = cuv / math.sqrt(N[u] * N[v])
	return W


# 基于距离的用户相似度
def Dist_Similarity(train, r):
	dist = dict()
	for u in train.keys():
		for v in train.keys():
			if v == u:
				continue
			else:
				co_items = list(set(train[u]).intersection(set(train[v])))  # 用户u和用户v都产生行为的item，交集
				item_lenth = len(co_items)
				if item_lenth == 0:
					continue
				else:
					if u not in dist:
						dist[u] = dict()
					tmp = 0
					maxdist = 0
					for item in co_items:
						tmp += (r[u][item] - r[v][item]) * (r[u][item] - r[v][item])
						if abs(r[u][item] - r[v][item]) > maxdist:
							maxdist = abs(r[u][item] - r[v][item])
					if maxdist == 0:
						dist[u][v] = 1
					else:
						dist[u][v] = 1 - math.sqrt(tmp) / math.sqrt(item_lenth * maxdist * maxdist)
	return dist


# 基于距离与余弦相似度结合的融合相似度
def FusionSimilarity(w, dist):
	Fusion_W = dict()
	for u, relate_user in w.items():
		if u not in Fusion_W:
			Fusion_W[u] = dict()
		for v, wuv in relate_user.items():
			Fusion_W[u][v] = wuv * dist[u][v]
	return Fusion_W
