#__author__ = 'leng'
# -*- coding: utf-8 -*

def GetRecommendation(user, train, W, K, r):
	rank = dict()
	interacted_items = train[user]  # 用户产生行为的item
	for v, wuv in sorted(W[user].items(), key=lambda x: x[1], reverse=True)[0:K]:  # 取与用户u最相似的K个用户
		for i in train[v]:
			if i in interacted_items:  # 过滤掉已经产生行为的item
				continue
			if i not in rank:
				rank[i] = wuv * r[v][i]  # 计算用户u对推荐item的感兴趣程度，用户u和用户v的相似度*用户v对item的感兴趣程度
			else:
				rank[i] += wuv * r[v][i]
	return rank
