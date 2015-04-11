#Filename iOSAutoDistribute.py
import os,sys,getopt,subprocess
import requests
import json
'''
    http://www.pgyer.com/
'''
UserKey        = ""
APIKey         = ""
pgyerRequestBaseURL = "http://www.pgyer.com/apiv1/app/upload"
downBaseURL = "http://www.pgyer.com"


def changeDir(directory):
    print("project dir %s" % directory)
    os.chdir(directory)

def xcbuild(targetName, directory="./build/"):
    print("target %s, configuration %s" % (targetName, ""))

    exportIpaPath =  directory + "/" + targetName + ".ipa"

    archiveCmd = "xcodebuild -scheme " + targetName + " archive -archivePath " + directory +"/" + targetName + ".xcarchive"
    ipaCmd = "xcodebuild -exportArchive -exportFormat ipa" + " -archivePath " + directory + "/" + targetName + ".xcarchive" + " -exportPath " + exportIpaPath

    print("archive cmd %s, ipa cmd %s" % (archiveCmd, ipaCmd))

    process = subprocess.Popen(archiveCmd, shell=True)
    process.wait()

    process = subprocess.Popen(ipaCmd, shell=True)
    output = process.communicate()
    print output
    uploadIPAToPgyer(exportIpaPath)

'''
    upload ipa to  http://www.pgyer.com/
'''

def resultJson(jsonResult):
    resultCode = jsonResult['code']
    if resultCode == 0:
      downUrl = downBaseURL +"/"+jsonResult['data']['appShortcutUrl']
      print "Upload Success"
      print "DownUrl is:"+downUrl
    else:
        print "Upload Fail!"
        print "Reason:"+jsonResult['message']


def uploadIPAToPgyer(ipaDirectory):
    uploadUrl = pgyerRequestBaseURL+"?"+"uKey="+UserKey+"&"+"_api_key="+APIKey+"&"+"publishRange="+"2"+"&"+"isPublishToPublic="+"2"
    print "fff:"+ipaDirectory
    print "hhh:"+uploadUrl
    files = {'file': open(ipaDirectory, 'rb')}
    headers = {'enctype':'multipart/form-data'}
    payload = {'uKey':UserKey,'_api_key':APIKey,'publishRange':'2','isPublishToPublic':'2'}
    print "uploading...."
    r = requests.post(uploadUrl,data = payload ,files=files,headers=headers)
    if r.status_code == requests.codes.ok:
         result = r.json()
         resultJson(result)
    else:
        print 'HTTPError,Code:'+r.status_code

    #print r.json()

def main():
    try:
        print("start")
        opts, args = getopt.getopt(sys.argv[1:], "x", ["target=", "config="])

        print(opts)

        print("change dir")
        #swtich to project directory
        changeDir(args[0])

        print("xcodebuild opts %s" % opts)

        #execute xcodebuile
        xcbuild(opts[0][1],args[1])
    except getopt.GetoptError as e:
        # usage()
        print("error %s" % e)
        sys.exit(2)


if __name__ == '__main__':
    main()
