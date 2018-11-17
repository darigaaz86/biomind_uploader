import requests
import json

class Orthanc():
    def __init__(self, host='localhost', port=8042):
        port = int(port)
        self._url  = 'http://%s:%d' % (host, port)   
        self._instance_url    = '%s/instances' % self._url
        self.errorfilelist = []

    def get_url(self):
        print(self._url)

    def get_instances(self):
        return self._getRequest(self._instance_url)
        
    def delete_all_instances(self):
        lis2del = self.get_instances()
        if lis2del != None:
            for instance in lis2del:
                self.deleteInstance(instance)

    def delete_all_patients(self):
        patients = self._getRequest("%s/patients" % self._url)
        for patientId in patients:
            url = "%s/%s" % (self._patients_url, patientId)
            print(self._deleteRequest(url))
       

    def uploadInstance(self, filePath):
        url = self._instance_url
        headers = { 'content-type' : 'application/dicom'}
        f = open(filePath, "rb")
        content = f.read()
        f.close()
        count = 3 
        while count > 0:
            if count < 3:
                print("Retry %d %s"%(count, filePath))
            response = self._postRequest(url, headers=headers, data=content)
            if response:
                if response['Status'] == "Success" or response['Status'] == "AlreadyStored":
                    return response
                else:
                    count = count - 1
            else:
                count = count - 1
        self.errorfilelist.append(filePath)
        return response

    def deleteInstance(self, instanceId):
        url = "%s/%s" % (self._instance_url, instanceId)
        return self._deleteRequest(url)

    def _getRequest(self, url):
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                if "application/json" in response.headers.get('content-type'):
                    return json.loads(response.text)
                else:
                    return response.text
            else:
                print("Unknown error message. GET request failed")
                print(json.loads(response.content))
        except Exception as e:
            print('GET Request failed %s' % e)
        return None

    def _postRequest(self, url, **kwargs):
        try:
            response = requests.post(url, timeout=10, **kwargs)
            if response.status_code == 200:
                if "application/json" in response.headers.get('content-type'):
                    return json.loads(response.text)
                else:
                    return response.text
            else:
                print("Unknown error message. POST request failed")
                print(response.text)
        except Exception as e:
            print('POST Request failed %s' % e)
        return None

    def _deleteRequest(self, url):
        response = requests.delete(url)
        if response.status_code == 200:
            return True
        else:
            return False


