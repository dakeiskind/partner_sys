__author__ = 'wangwei'

from django.shortcuts import render_to_response
from django.template import RequestContext
import pysftp


class Uploader(object):
    def __init__(self, remote, username, password, port=21):
        self.remote = remote
        self.username = username
        self.password = password
        self.port = port

    def handle_uploaded_file(self, localPath, remotePath):
        try:
            sftp = pysftp.Connection(host=self.remote, username=self.username,
                password=self.password)

            # To upload the file, simple replace get with put.
            sftp.put(localPath, remotePath)
        except Exception as err:
            print(err)
            raise Exception('sftp put error')
        finally:
            # Closes the connection
            sftp.close()

        return remotePath

    def upload(self, files, src='tmp/', dest='/home/dake/pics/'):
        urls = []
        for file in files:
            src = src + file.name
            dest = dest + file.name
            try:
                temp = open(src, 'wb+')
                for chunk in file.chunks():
                    temp.write(chunk)
            except Exception as err:
                print(err)
                raise Exception('chunk write error')
            finally:
                temp.close()

            try:
                url = self.handle_uploaded_file(src, dest)
                urls.append('ftp://' + self.remote + '/' + url)
            except Exception as err:
                print(err)
                raise Exception

        return urls

if __name__ == '__main__':
    u = Uploader('16.158.49.75', 'dake', '123qwe!@#')
    u.handle_uploaded_file('C:/workspace/pycharm/partner_sys/tmp/CentOS-Base.repo', '/home/dake/pics/CentOS-Base.repo')