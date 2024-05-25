# Internet Server Application Programming Interface (ISAPI)
# ISAPI ref: https://github.com/loozhengyuan/hikvision-sdk/tree/master/resources
# Sending HTTP requests
# XML command
import requests
from requests.auth import HTTPDigestAuth
import re

camera_ip = '192.168.1.64'
username = 'admin'
password = 'a_123456'

preSet = {"HIKZERO" : 1, "SHOBEYRI" : 2, "MOHEBI" : 3, "ALLZERO" : 4}

def relative_move_command(pan, tilt, zoom, duration = 500):
    # duration is the time in milliseconds for which the command is executed
    PTZ_CONTROL_URL = f'http://{camera_ip}/ISAPI/PTZCtrl/channels/1/Momentary'
    xml_payload = f'''  <PTZData>
                        <pan>{pan}</pan>
                        <tilt>{tilt}</tilt>
                        <zoom>{zoom}</zoom>
                        <Momentary>
                            <duration>{duration}</duration>
                        </Momentary>
                    </PTZData>'''
    
    response = requests.put(PTZ_CONTROL_URL, auth=HTTPDigestAuth(username=username, password=password), data=xml_payload)

    if response.status_code == 200:
        print('PTZ command sent successfully')
    else:
        print(f'Failed to send PTZ command: {response.status_code}')
    
def move_to_preset(PRESET):
    PreSet_URL = f'http://{camera_ip}/ISAPI/PTZCtrl/channels/1/presets/{PRESET}/goto'
    xml_payload = f'<PTZData><PresetID>{PRESET}</PresetID></PTZData>'

    response = requests.put(PreSet_URL, auth=HTTPDigestAuth(username, password), data=xml_payload, headers={'Content-Type': 'application/xml'})

    if response.status_code == 200:
        print('Moved to preset successfully')
    else:
        print(f'Failed to move to preset: {response.status_code}')

def go_to_position(pan, tilt, zoom):
    GoToURL = f'http://{camera_ip}/ISAPI/PTZCtrl/channels/1/absolute'
    xml_payload = f'''<PTZData>
                        <AbsoluteHigh>
                            <elevation>{10*tilt}</elevation>
                            <azimuth>{10*pan}</azimuth>
                            <absoluteZoom>{zoom}</absoluteZoom>
                        </AbsoluteHigh>
                      </PTZData>'''
    # <AbsoluteHigh><!--high-accuracy positioning which is accurate to one decimal place-->

    response = requests.put(GoToURL, auth=HTTPDigestAuth(username, password), data=xml_payload)
    if response.status_code == 200:
        print('Moved to PTZ successfully')
    else:
        print(f'Failed to move to PTZ: {response.status_code}')

def get_position():
    StatusURL = f'http://{camera_ip}/ISAPI/PTZCtrl/channels/1/status'
    response = requests.get(StatusURL, auth=HTTPDigestAuth(username, password))
    
    if response.status_code == 200:
        print('Status recived successfully')
        patern = r"<[absoluteZoom,azimuth,elevation]+>\d+</[absoluteZoom,azimuth,elevation]+>"
        ptzData = re.findall(patern, response.text)
        # print(ptzData)
        
        tilt_position = int(re.findall(r"\d+", ptzData[0])[0])//10 # elevation
        pan_position  = int(re.findall(r"\d+", ptzData[1])[0])//10 # azimuth        
        zoom_position = int(re.findall(r"\d+", ptzData[2])[0])//10 # zoom
    else:
        print(f'Failed to move to PTZ: {response.status_code}')

    return pan_position, tilt_position, zoom_position
    
# relative_move_command(pan=100, tilt=0, zoom=0, duration = 5000)
# move_to_preset(preSet["ALLZERO"])
# go_to_position(pan=0, tilt=0, zoom=1)

pan, tilt, zoom = get_position()
print(f'pan: {pan} | tilt: {tilt} | zoom: {zoom}')


# Other useful functions
# Date&Time, substream vs mainstream