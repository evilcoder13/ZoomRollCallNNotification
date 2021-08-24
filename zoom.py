import json
import datetime
from pytz import timezone
from zoomus import ZoomClient

# test acc
#client = ZoomClient('-rMnKsK0RMW35qzOS7G63Q', 'Rp52K4ycDmf5CIDru6ANWB851UtvhC0r1u9r')

# acc
client = ZoomClient('0bI5VZ6aR1qs2z4NGw6btg', 'iMAivEWGfMLZlF3hdvmdAY7x9xzI1laLgyme')

user_list_response = client.user.list()
user_list = json.loads(user_list_response.content)
# print(user_list)
# meet = client.meeting.create(user_id="me",host_id="Test-123", topic="Test meeting", type=2, start_time=datetime.datetime(2021,7,20,16,15,0,0,timezone('Asia/Ho_Chi_Minh')).astimezone(timezone('UTC')),duration=120)
# meet = json.loads(meet.content)
#for user in user_list['users']:
#    user_id = user['id']
#    print(json.loads(client.meeting.list(user_id=user_id).content))
#response = client.meeting.update(id=meet['id'], settings={ 'alternative_hosts':"thangdm1@vnpt.vn" })
#print(response.content)
for user in user_list['users']:
    user_id = user['id']
    recording_list = json.loads(client.recording.list(user_id=user_id).content)
    #print(recording_list)
    for meeting in recording_list['meetings']:
        record = json.loads(client.recording.get(meeting_id=meeting['id']).content)
        print(record)
    # meeting_list = json.loads(client.meeting.list(user_id=user_id).content)
    # #print(meeting_list)
    # for meeting in meeting_list['meetings']:
    #     print(meeting)
    #     regs_list = json.loads(client.meeting.list_registrants(id=meeting['id']).content)
    #     print(regs_list)