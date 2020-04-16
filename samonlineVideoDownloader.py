import urllib
import bs4
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError
import validators
import os
import pathlib
from tqdm import tqdm


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, file_name, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=file_name) as t:
        urllib.request.urlretrieve(
            url, filename=output_path, reporthook=t.update_to)


def download_all_videos(video_links, video_names, complete_file_path):
    for link, video_name in zip(video_links, video_names):
        # video_name = link.split('/')[-1]
        print("\nDownloading file: %s" % video_name)
        download_url(link, video_name, complete_file_path+video_name)
        # urllib.request.urlretrieve(link, complete_file_path+video_name)
        print("%s Downloaded!" % video_name)

    print("All videos has been downloaded successfully!")


def download_selected_videos(video_links, video_names, complete_file_path):
    for link, video_name in zip(video_links, video_names):
        print("\nDownloading file: %s" % video_name)
        download_url(link, video_name, complete_file_path+video_name)
        print("%s Downloaded!" % video_name)

    print("All videos has been downloaded successfully!")


save_path = os.path.join(os.path.expanduser('~'), 'Downloads')

input_urlName = str(input('Give SamOnline Video Url:: '))
ftp_url = input_urlName.split('SAM')[0]

ext = (".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv",
       ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg",
                        ".rm", ".swf", ".vob", ".wmv")

if validators.url(input_urlName):
    req = Request(input_urlName)
else:
    exit()

try:
    with urlopen(req) as uClient:
        the_page = uClient.read()
        soup = BeautifulSoup(the_page, 'html.parser')
        uClient.close()
except URLError as e:
    if hasattr(e, 'reason'):
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    elif hasattr(e, 'code'):
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
else:
    container = soup.find('div', id="fallback")
    videos = container.find_all('td', {"class": "fb-n"})

    video_links = [ftp_url+video.a['href']
                   for video in videos if video.a['href'].endswith(ext)]

    video_names = [
        video.a.next_element for video in videos if video.a['href'].endswith(ext)]

    complete_file_path = os.path.join(save_path, 'Video/')
    pathlib.Path(complete_file_path).mkdir(parents=True, exist_ok=True)

    total_video = len(video_links)
    choice = str(input('Download all '+str(total_video) +
                       ' videos type for Yes=\'y\'; No=\'n\':: '))

    selected_video_links = []
    selected_video_names = []

    if choice == 'y' or choice == 'Y':
        download_all_videos(video_links, video_names, complete_file_path)
    elif choice == 'n' or choice == 'N':
        for link, video_name in zip(video_links, video_names):
            print("\nDownloading file: %s" % video_name)
            choice = str(
                input('\nDownload selected videos type for Select=\'s\'; No=\'n\':: '))
            if choice == 's' or choice == 'S':
                selected_video_links.append(link)
                selected_video_names.append(video_name)
                print('Video has been selected for downloading')
            elif choice == 'n' or choice == 'N':
                continue

        download_selected_videos(selected_video_links,
                                 selected_video_names, complete_file_path)
