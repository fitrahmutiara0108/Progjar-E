import os
import json
import base64
from glob import glob


class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self,params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self,params=[]):
        try:
            filename = params[0]
            if (filename == ''):
                return None
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def post(self,params=[]):
        if not (len(params) == 2):
            return False    
        filename = params[0]
        if os.path.exists(filename):
            return False
 
        file = base64.b64decode(params[1])
        fp = open(filename,'wb+')
        fp.write(file)
        fp.close()
        return dict(status='OK',data=f'File {filename} Succesfully Uploaded')
    
    def delete(self,params=[]):
        try:
            filename = params[0]
            if(filename == ''):
                return None
            os.remove(f"{filename}")
            return dict(status='OK')
        except Exception as e:
            return dict(status='ERROR',data=str(e))

if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    # print(f.get(['pokijan.jpg']))
