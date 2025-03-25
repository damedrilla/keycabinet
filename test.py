import requests
import json
BASE_API_URL = "https://keycabinet.cspc.edu.ph/api/"
def getIDholder(uid):
    req = requests.get(BASE_API_URL + "faculty")
    result = req.json()
    
    for _faculty in range(len(result)):
        if(str(uid) == result[_faculty]['rfid_uid']):
            return 200, result[_faculty]["faculty_id"]
        else:
            continue
    return 404, None


print(getIDholder("9d3dda2xdb"))