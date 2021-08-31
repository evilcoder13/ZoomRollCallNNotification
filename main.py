from fastapi import Request, FastAPI
from fastapi.staticfiles import StaticFiles
import json
import asyncio
import requests
import os
import urllib.parse
from zoomus import ZoomClient

app = FastAPI()
app.mount("/zoom/view", StaticFiles(directory="src"), name="src")
appapi = 'aua6bn1fdoueyqqjw9ss9p5i7bhhaw'
userapi = 'uyrtbe36bs47c3sma4grm7jxfjjidv'
#msg = 'Test msg API Zoom'
#msg = urllib.parse.quote('Test msg API Zoom')
#x = requests.post('https://api.pushover.net/1/messages.json', data = {'token':appapi,'user':userapi,'message':msg})
#print(x.content)

@app.get("/zoom")
async def root():
    return {"message": "Hello World"}

@app.post("/zoom")
async def proot(request: Request):
    data = await request.json()
    print(data)
    try:
        status = data['event']
        if status=='recording.completed':
            download_token = data['download_token']
            topic = data['payload']['object']['topic']
            files = data['payload']['object']['recording_files']
            for fi in files:
                download_url = fi['download_url']+'?access_token='+download_token
                rec_type = fi['recording_type']
                #resp = requests.post('https://api.pushover.net/1/messages.json', data = {'token':appapi,'user':userapi,'message':"Topic: "+topic+ ', Type: '+rec_type+', Download: ' +download_url,'url_title':rec_type,'url':download_url}) #Push Over
                #resp = requests.post('https://api.pushover.net/1/messages.json', data = {'token':appapi,'user':userapi,'message':"Topic: "+topic+ ', Type: '+rec_type+', Download: ' +download_url}) #Push Over
                print('{} - {}: {}'.format(topic,rec_type,download_url))
            return { 'message': 'OK' }
        joineduser = data['payload']['object']['participant']['email']
        joinedusername = data['payload']['object']['participant']['user_name']
        joineduser = joineduser.lower()
        joinedusername = joinedusername.lower()
        status = ' joined ' if status == 'meeting.participant_joined' else status
        status = ' left ' if status == 'meeting.participant_left' else status
        monitoruserlist = await listusr()
        monitoruserlist = monitoruserlist['userlist']
        if (joineduser in monitoruserlist) | (joinedusername in monitoruserlist): 
            joineduser = joinedusername + ' '+joineduser
            #print("Found user "+joineduser)
            await sendNotification("Found user "+joineduser) #One signal
            resp = requests.post('https://api.pushover.net/1/messages.json', data = {'token':appapi,'user':userapi,'message':"Zoom found user "+status+ ' ' +joineduser}) #Push Over
            #print(x.content)
            #return {"message":"Found user "+joineduser}
            return {"message":resp.content}
    except: pass
    return {"message": "Hello World"}

@app.get("/zoom/list")
async def listusr():
    with open('monitorlist.txt') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    monitoruserlist = content
    #print(content)
    return { 'userlist': content }

@app.get("/zoom/timesheet")
async def timesheet():
    import extractinoutinfo
    return extractinoutinfo.getjsondata()

def download(url,filename):
    get_response = requests.get(url,stream=True)
    file_name = filename
    if not(filename): file_name = url.split("/")[-1]
    with open(file_name, 'wb') as f:
        for chunk in get_response.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

@app.post("/zoom/download")
async def zoomdownload(request: Request):
    data = await request.json()
    download(data['url'],data['filename'])
    return {"message":"Downloading "+data['filename']}

@app.post("/zoom/change")
async def changeusr(request: Request):
    data = await request.json()
    with open('monitorlist.txt', 'w') as f:
        for l in data:
            f.write("%s\n" % l)
    return {"message": "OK, done!"}

@app.get("/zoom/recordings")
async def listrecordings():
    apis = [{'key':'0bI5VZ6aR1qs2z4NGw6btg','secret':'iMAivEWGfMLZlF3hdvmdAY7x9xzI1laLgyme'},{'key':'nbpTOiVXTT2nuYs9HZMipw','secret':'cctbgI6WnFWlsEoba2SpSbfS1lx5fjm6'},{'key':'w0zHIsVbQiu5XU5vdasw','secret':'qM5d12g3sqMuSlUDzY2ajbD57Sds7vHa'},{'key':'yYPQuTXkTX6FELMmn_rEQQ','secret':'DJ2LPUk7j63hUzX8PydHy3ufV5E6nKGQ'},{'key':'GMp2ipgJTd2lH8lWxOoaA','secret':'2syevJpGN4WxORe15OR4WPO76vAnQ3dO'}]
    records = []
    return {'data':records}
    for api in apis:
        client = ZoomClient(api['key'], api['secret'])
        user_list = json.loads(client.user.list().content)
        print(user_list)
        for user in user_list['users']:
            user_id = user['id']
            recording_list = json.loads(client.recording.list(user_id=user_id).content)
            # print(recording_list)
            for meeting in recording_list['meetings']:
                record = json.loads(client.recording.get(meeting_id=meeting['id']).content)
                #print(record)
                records.append(record)
    return { 'data':records }

async def sendNotification(msg):
    
    header = {"Content-Type": "application/json; charset=utf-8",
            "Authorization": "Basic YmE2NmI3MTgtODg1ZS00M2Q2LWFkZjQtZDk2ZWEwMDJkMTM0"}

    payload = {"app_id": "4a57b71f-39ef-466c-b3fe-b01e42b4cf89",
            "included_segments": ["Subscribed Users"],
            "contents": {"en": msg}}
    
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
    
    print(req.status_code, req.reason)