import json
import ast
from datetime import datetime, timedelta
import pandas
print('topic,username,join_time,leave_time,ptype,fc')
monitoruserlist = []
datalist = []
with open('monitorlist.txt') as f:
    content = f.readlines()
    content = [x.strip() for x in content]
    monitoruserlist = content

for line in open('nohup.out'):
    if ('meeting.participant_left' in line) | ('meeting.participant_joined' in line):
        data = ast.literal_eval(line)
        topic = data['payload']['object']['topic']
        username = data['payload']['object']['participant']['user_name']
        try: 
            join_time = data['payload']['object']['participant']['join_time']
            join_time = datetime.strftime(datetime.strptime(join_time,'%Y-%m-%dT%H:%M:%SZ')+timedelta(hours=7),'%Y-%m-%d %H:%M:%S')
        except: join_time = ''
        try: 
            leave_time = data['payload']['object']['participant']['leave_time']
            leave_time = datetime.strftime(datetime.strptime(leave_time,'%Y-%m-%dT%H:%M:%SZ')+timedelta(hours=7),'%Y-%m-%d %H:%M:%S')
        except: leave_time = ''
        ptype = 'Left' if 'meeting.participant_left' in line else 'Join'
        fc = 'Faculty' if username.strip().lower() in monitoruserlist else 'Student'
        datalist.append([topic,username,join_time,leave_time,ptype,fc])
        #print('{},{},{},{},{},{}'.format(topic,username,join_time,leave_time,ptype,fc))

for line in open('logs.json'):
    if ('meeting.participant_left' in line) | ('meeting.participant_joined' in line):
        data = ast.literal_eval(line)
        data = ast.literal_eval(data['log'])
        topic = data['payload']['object']['topic']
        try: username = data['payload']['object']['participant']['user_name']
        except: continue;
        try: 
            join_time = data['payload']['object']['participant']['join_time']
            join_time = datetime.strftime(datetime.strptime(join_time,'%Y-%m-%dT%H:%M:%SZ')+timedelta(hours=7),'%Y-%m-%d %H:%M:%S')
        except: join_time = ''
        try: 
            leave_time = data['payload']['object']['participant']['leave_time']
            leave_time = datetime.strftime(datetime.strptime(leave_time,'%Y-%m-%dT%H:%M:%SZ')+timedelta(hours=7),'%Y-%m-%d %H:%M:%S')
        except: leave_time = ''
        ptype = 'Left' if 'meeting.participant_left' in line else 'Join'
        fc = 'Faculty' if username.strip().lower() in monitoruserlist else 'Student'
        datalist.append([topic,username,join_time,leave_time,ptype,fc])
        #print('{},{},{},{},{},{}'.format(topic,username,join_time,leave_time,ptype,fc))

df = pandas.DataFrame(data=datalist,columns='topic,username,join_time,leave_time,ptype,fc'.split(','))
df1 = df[df['ptype']=='Join']
df1 = df1[['topic','username','fc','join_time']].groupby(['topic','username','fc'])['join_time'].min()
df2 = df[df['ptype']=='Left']
df2 = df2[['topic','username','fc','leave_time']].groupby(['topic','username','fc'])['leave_time'].max()

df = pandas.merge(df1,df2,how='outer',on=['topic','username','fc'])
df = df.sort_values(['join_time',], ascending=[True,])
df.to_csv('lichhoc_sorted.csv')
#df.to_json('lichhoc_sorted.json',orient='index',index=True)
#df = df.reindex(columns=['topic','username','fc','join_time','leave_time'])
def getjsondata():
    df = pandas.read_csv('lichhoc_sorted.csv')
    return df.to_json(orient='records',index=True)
