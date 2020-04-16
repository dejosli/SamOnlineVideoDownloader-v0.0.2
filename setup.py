from cx_Freeze import setup, Executable
import os

path = os.path.abspath("./samonlineVideoDownloader.py")

executables = [Executable(path)]

'''
packages = [""]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}
'''

setup(
    name = 'SamOnline Video Downloader',
    #options = options,
    version = '0.0.2.0',
    description = 'Download videos from SamOnline FTP Server by giving the URL of the video location',
    executables = executables
)
