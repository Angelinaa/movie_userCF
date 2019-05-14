
import pandas as pd
if __name__ == "__main__":
    r = dict()
    try:
        #生成用户-电影矩阵，第一行是所有电影id，第一列是所有用户id，矩阵内是评分数据
        #r是第一列字典，即存储用户id的字典
        df = pd.read_csv("4.csv", encoding="utf-8")
        for row in df.itertuples():
            movie_id=getattr(row, 'movie_id')
            user_id = getattr(row, 'user_id')
            rate = getattr(row, 'rate')
            if user_id not in r:
                r[user_id] = dict()
            r[user_id][movie_id] = rate
        print("r矩阵：",r["58508076"])
    except IOError as err:
        print("IOError" + str(err))
    print("r原始长度：", len(r))
    re=r.copy()
    print("re原始长度：", len(re))
    for user, item in r.items():
        #print("用户id:",user)
        #print("该用户的数据条数为：",len(item.items()))
        #print("该用户的数据为：", item.items())

        if len(item.items())<5:
            print("用户id:", user)
            print("该用户的数据条数为：", len(item.items()))
            #for movie, rate in item.items():
                #r.pop(movie)
            re.pop(user)
    print("r删除后长度：", len(r))
    print("re删除后长度：", len(re))