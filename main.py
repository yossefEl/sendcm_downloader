import requests
import os
from bs4 import BeautifulSoup


def download_video(link, title):
    print("Downloading: {}".format(title))
    r = requests.get(link, stream=True)
    with open(title, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return


def scrap_link(link):
    print(link)
    r = requests.get(link)
    print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    i = 0
    for link in soup.find_all('tr'):

        if(i > 0):
            link_to_video = link.find('a').get('href')
            title_of_video = link.find('a').text

            r = requests.get(link_to_video)
            soup_details_page = BeautifulSoup(r.text, 'html.parser')
            link_to_video = soup_details_page.find('source').get('src')
            # check if the file already exists
            if not os.path.exists(title_of_video):
                download_video(link_to_video, title_of_video)

        i += 1


def create_folder_and_download(links, course_name):

    if not os.path.exists(course_name):
        os.makedirs(course_name)
    os.chdir(course_name)
    for link in links:
        scrap_link(link)


links = [
    # links here |Go to the files list page and click Next to get the pagination link and edit it to be something like this 🙂
  "https://send.cm/?sort_order=down&sort_field=file_created&id=17Q&op=user_public&page=1",
  "https://send.cm/?sort_order=down&sort_field=file_created&id=17Q&op=user_public&page=2"
]

course_name = "Ionic4"
course_name = course_name.replace(" ", "_")

create_folder_and_download(links, course_name)
