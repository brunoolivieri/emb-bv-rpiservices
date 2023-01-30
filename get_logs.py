import requests
import os
import urllib.request 
import time
import progressbar

# Configs
#ADDRESS = "http://201.49.23.53:3000"  # This is the virtual drone online for debuging
ADDRESS = "http://10.0.2.100:3000"  # This is the defatul address for real drones
ABOUTSERVER_ROUTE = "/api/softwareinfo"
LOGS_ROUTE = "/api/logfiles"
FILES_ROUTE = " /logdownload/"


class MyProgressBar():
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


def get_drone_id():
    try:
        r = requests.get(ADDRESS + ABOUTSERVER_ROUTE)
        hostname_data = (r.json())['hostname']
        return hostname_data
    except Exception as e: 
        print('get_hostname() failure ...')
        print(e)


def check_folders(drone_id):
    try:
        if not os.path.exists(drone_id):
            os.makedirs(drone_id)
        if not os.path.exists(os.path.join(drone_id, 'tlogs')):
            os.makedirs(os.path.join(drone_id, 'tlogs'))
        if not os.path.exists(os.path.join(drone_id, 'kmzlogs')):
            os.makedirs(os.path.join(drone_id, 'kmzlogs'))
    except Exception as e: 
        print('check_folders() failure ...')
        print(e)


def list_logs(log_type):
    try:
        r = requests.get(ADDRESS + LOGS_ROUTE)
        server_json = r.json()[log_type]
        for item in server_json:
            print('File found:  ' + item["key"]) 
        return server_json
    except Exception as e: 
        print('list_logs() failure ...')
        print(e)


def download_logs(drone_id, logs):
    for item in logs:
        try:
            print('Downloading: ' + item["key"])               
            urllib.request.urlretrieve((ADDRESS + FILES_ROUTE + item['key']), os.path.join(drone_id, item['key']), MyProgressBar())
            time.sleep(2) # to avoid HTTP 429 from NodeJS protection.
        except Exception as e: 
            print('download_logs() failure ...')
            print(e)




if __name__ == "__main__":
    drone_id = get_drone_id()
    print("Drone ID: " + drone_id)
    check_folders(drone_id)

    tlogs = list_logs('TlogFiles')
    download_logs(drone_id, tlogs)

    kmzs = list_logs('KMZlogFiles')
    download_logs(drone_id, kmzs)