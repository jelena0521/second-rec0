import os
import json
import random
import math
class FirstRec:
    def __init__(self,path,seed,k,n_item):
        self.path=path
        self.seed=seed
        self.users_1000=self.get_sample_data()
        self.train_data,self.test_data=self.split_data()
        self.n_item=n_item
        self.k=k
    def get_sample_data(self):
        print('随机选择1000个用户')
        users=[]
        if os.path.exists('data/train.json') and os.path.exists('data/test.json'):
            return list()
        else:
            for file in os.listdir(self.path):
                one_path='{}/{}'.format(self.path,file)
                #print('{}'.format(one_path))
                with open(one_path) as f:
                    for line in f.readlines():
                        if line.strip().endswith(':'):
                            continue
                        u,_,_=line.split(',')
                        users.append(u)
        users_1000=random.sample(list(set(users)),1000)
        return users_1000
    def split_data(self):
        train_data={}
        test_data={}
        if os.path.exists('train.json') and os.path.exists('test.json'):
            train_data=json.load('train.json')
            test_data=json.load('test.json')
            print('加载训练集和测试集完成')
        else:
            random.seed(self.seed)
            for file in os.listdir(self.path):
                one_path='{}/{}'.format(self.path,file)
                with open(one_path) as f:
                    movieid=f.readline().split(':')[0]
                    for line in f.readlines():
                        if line.strip().endswith(':'):
                            continue
                        userid,rate,_=line.split(',')
                        if userid in self.users_1000:
                            if random.randint(1,50)==1:
                                test_data.setdefault(userid,{})[movieid]=int(rate)
                            else:
                                train_data.setdefault(userid,{})[movieid]=int(rate)
            json.dump(train_data,open('train.json','w'))
            json.dump(test_data,open('test.json','w'))
            print('数据生成完毕')
        return train_data,test_data
    def person(self,rating1,rating2):
        sum_xy=0
        sum_x=0
        sum_y=0
        sum_power_x=0
        sum_power_y=0
        n=0
        for key in rating1.keys():
            if key in rating2.keys():
                n=n+1
                x=rating1[key]
                y=rating2[key]
                sum_xy=sum_xy+x*y
                sum_x=sum_x+x
                sum_y=sum_y+y
                sum_power_x=sum_power_x+x*x
                sum_power_y=sum_power_y+y*y
        if n==0:
            return 0
        elif sum_power_x-sum_x*sum_x/n==0:
            return 0
        elif sum_power_y-sum_y*sum_y/n==0:
            return 0
        r=(sum_xy-sum_x*sum_y/n)/(math.sqrt(sum_power_x-sum_x*sum_x/n)*math.sqrt(sum_power_y-sum_y*sum_y/n))
        return r
    def recommend(self,userid):
        neighbor={}
        for user in self.train_data.keys():
            if userid !=user:
                r=self.person(self.train_data[userid],self.train_data[user])
                neighbor[user]=r
        sorted_neighbor=sorted(neighbor.items() ,key=lambda k:k[1],reverse=True)
        movies={}
        for sim_user,sim in sorted_neighbor[:self.k]:
            for movieid in self.train_data[sim_user].keys():
                movies[movieid] +=sim*self.train_data[sim_user][movieid]
        newmovies=sorted(movies.items(),key=lambda k:k[1],reverse=True)
        return newmovies
    def evaluate(self,num=30):
        random.seed(9)
        hit=0
        p=[]
        for user in random.sample(self.test_data.keys(),num):
            result=self.recommend(user)[:self.n_item]
            for item,_ in result:
                if item in self.test_data[user]:
                    hit=hit+1
            p.append(hit/self.n_item)
        return sum(p)/p.__len__()

if __name__=='__main__':
    path='training_set'
    k=15
    n_item=20
    seed=10
    f_rec=FirstRec(path,seed,k,n_item)
    result=f_rec.recommend('1')
    print('为用户1推荐的电影为{}'.format(result))
    print('算法的准确性为{}'.format(f_rec.evaluate()))
















