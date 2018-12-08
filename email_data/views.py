from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
import extract_msg
from django.core.files.storage import FileSystemStorage
import os, io, mimetypes
from django.conf import settings
import paramiko

def index(request, path=''):
    """
    The home page. This displays the single-page app.
    """
    return render(request, 'index.html')

@api_view(['POST'])
def connect(request):
    """
    Filter all tracks or artist id or release date.
    """
    # Command to get users
    # awk -F':' '{ print $1}' /etc/passwd
    # cut -d: -f1 /etc/passwd
    # compgen -u

    # Command to get user with root privileges
    # grep -Po '^sudo.+:\K.*$' /etc/group

    user_data = []
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        port = 80
        if request.data["port"] != None and request.data["port"] != "":
            port = request.data["port"]
        client.connect(hostname=request.data["host"], port=port, username=request.data["username"], password=request.data["password"])
        shell = client.invoke_shell()
        # Execute command and get results.
        stdin, stdout, stderr = client.exec_command("compgen -u")
        user_list = str(stdout.read()).replace("b\'", "").split("\\n")
        stdin, stdout, stderr = client.exec_command("grep -Po '^sudo.+:\K.*$' /etc/group")
        root_users = str(stdout.read()).replace("b\'", "").replace("\\n\'", "").split(",")
        # Close connection.
        shell.close()
        client.close()
        for user in user_list[0: len(user_list)-1]:
            isRoot = False
            if user in root_users:
                isRoot = True
            print(isRoot)
            user_data.append({
                "user": user,
                "isRootUser": isRoot
            })
        response = {
            "response": "SUCCESS",
            "message": "Connection Success!",
            "data": user_data
        }
    except:
        response = {
            "response": "FAIL",
            "message": "Cannot connect to the server!",
            "data": user_data
        }
    return Response(response)

@api_view(['POST'])
def extract(request):
    """
    Filter all tracks or artist id or release date.
    """
    try:
        files = request.FILES.getlist('myFile')
        msg_data = []
        fs = FileSystemStorage()
        for file in files:
            name = file.name.replace(" ", "_")
            # if os.path.exists(settings.MEDIA_ROOT + "\\" + file.name):
            #     os.remove(settings.MEDIA_ROOT + "\\" + file.name)
            fs.save(settings.MEDIA_ROOT + "\\" + name, file)
            msg = extract_msg.Message(settings.MEDIA_ROOT + "\\" + name)
            # for attachment in msg.attachments:
            #     fs.save(settings.MEDIA_ROOT + "\\" + attachment.longFilename, attachment.data)
            msg_data.append({
                # "mainProperties": msg.mainProperties,
                # "header": msg.header,
                # "attachments": msg.attachments,
                "filename": file.name,
                "filepath": "/media/" + name,
                "from": msg.sender,
                "to": msg.to,
                "cc": msg.cc,
                "subject": msg.subject,
                "date": msg.date,
                "body": msg.body,
            })
        response = {
            "response": "SUCCESS",
            "message": "File Uploaded!",
            "data": msg_data
        }
    except:
        response = {
            "response": "FAIL",
            "message": "Erorr in file uploading!",
            "data": msg_data
        }
    return Response(response)

def download(request, file):
    """Returns the requested file"""
    print(file)
    try:
        mimetypes.init()
        file_path = settings.MEDIA_ROOT + '/' + file
        fsock=None
        with open(file_path, "rb") as f:
            fsock = io.BytesIO(f.read())
        file_name = os.path.basename(file_path)
        mime_type_guess = mimetypes.guess_type(file_name)
        response = HttpResponse(fsock, content_type=mime_type_guess[0])
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        return response
    except:
        return not_found(request)
