# -*- coding: utf-8 -*-
from apiclient import errors
from colorama import init,Fore,Back,Style
from termcolor import colored
from apiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
import os
import sys
import re
import time

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

def main():
    """
    Clone shared folder to your drive.
    """

    # use Colorama to make Termcolor work on Windows too
    init()
    # now, to clear the screen
    cls()
    print colored('  ________________        .__               _________ .__                        ', 'blue')
    print colored(' /  _____/\______ \_______|__|__  __ ____   \_   ___ \|  |   ____   ____   ____  ', 'blue')
    print colored('/   \  ___ |    |  \_  __ \  \  \/ // __ \  /    \  \/|  |  /  _ \ /    \_/ __ \ ', 'magenta')
    print colored('\    \_\  \|    `   \  | \/  |\   /\  ___/  \     \___|  |_(  <_> )   |  \  ___/ ', 'magenta')
    print colored(' \______  /_______  /__|  |__| \_/  \___  >  \______  /____/\____/|___|  /\___  >', 'cyan')
    print colored('        \/        \/                    \/          \/                 \/     \/ ', 'cyan')
    print colored('===================================================================================', 'white')
    print colored('                                    Version: ', 'yellow'), (1.0)
    print colored('                                    Author : ', 'yellow'), ('Blavk')
    print colored('                                    Github : ', 'yellow'), ('https://github.com/duytran1406/gdriveclone')
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    print colored('[*] GDrive Folder/File ID: ','blue')
    folder_id = raw_input("   - ID  : ")
    while not folder_id:
        folder_id = raw_input("   - ID  : ")
    type(folder_id)

    try:
        folder = service.files().get(fileId=folder_id).execute()
        folder_name = normalizeName(folder[u'name'])
        print folder_name
        index_folder(service, folder_id, folder_name)
    except errors.HttpError, error:
        print 'An error occurred: {}'.format(error)

def index_folder(service, folder_id, folder_name, parent_id = None):
    #create folder
    if parent_id == None:
        mFolder = service.files().create(body={"name": folder_name,"mimeType": "application/vnd.google-apps.folder"}).execute()
    else:
        mFolder = service.files().create(body={"name": folder_name,"mimeType": "application/vnd.google-apps.folder","parents": [parent_id]}).execute()
    try:
        result = []
        files = service.files().list(
                q="'{}' in parents".format(folder_id),
                fields='files(id, mimeType, name)').execute()
        result.extend(files['files'])
        result = sorted(result, key=lambda k: k[u'name'])

        total = len(result)
        if total == 0:
            print colored('Folder is empty!', 'red')
        else:
            print colored('[*] START COPY FOLDER %s!' % mFolder[u'name'], 'yellow')
            current = 1
            for item in result:
                file_id = item[u'id']
                filename = normalizeName(item[u'name'])
                mime_type = item[u'mimeType']
                print '- ', colored(filename, 'cyan'), colored(mime_type, 'cyan')
                if mime_type == 'application/vnd.google-apps.folder':
                    index_folder(service, file_id, filename, mFolder[u'id'])
                else:
                    copy_file(service,file_id,filename, mFolder[u'id'])
                current += 1
                print colored('DONE!', 'yellow')
    except errors.HttpError, error:
        print 'An error occurred: {}'.format(error)

def copy_file(service, origin_file_id, copy_title, parent_id):
   try:
       print colored('[*] Copying file: %s' %copy_title, 'green')
       return service.files().copy(fileId=origin_file_id, body={"name": copy_title,"parents": [parent_id]}).execute()
   except errors.HttpError, error:
       print 'An error occurred: %s' % error
   return None

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
def normalizeName(s):
    #s = s.decode('utf-8', errors='ignore')
    s = re.sub(u'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(u'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(u'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(u'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(u'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(u'[ìíịỉĩ]', 'i', s)
    s = re.sub(u'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(u'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(u'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(u'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(u'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(u'[Đ]', 'D', s)
    s = re.sub(u'[đ]', 'd', s)
    s = re.sub('[^A-Za-z0-9 .]+', '', s)
    return s.encode('utf-8')

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %05s seconds ---" % (time.time() - start_time))
