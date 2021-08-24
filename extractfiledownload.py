import json
import ast
for line in open('nohup.out'):
    if 'download_token' in line:
        #print(ast.literal_eval(line))
        data = ast.literal_eval(line)
        #print(line)
        #data = json.loads(line)
        download_token = data['download_token']
        topic = data['payload']['object']['topic']
        files = data['payload']['object']['recording_files']
        for fi in files:
            download_url = fi['download_url']+'?access_token='+download_token
            rec_type = fi['recording_type']
            print('{} - {}: {}'.format(topic,rec_type,download_url))

