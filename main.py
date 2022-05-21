from requests import get
from lxml import html
from clint.textui import progress


def download(id, Quality):
    if(Quality not in ['720', '480', '240']):
        print('Invalid Quality')
    else:
        res = get(f"https://alaatv.com/c/{id}")
        tree = html.fromstring(res.content)
        link = tree.xpath(f'//source[@res="{Quality}p"]/@src')
        try:
            download_file_progress(link[0], f"{id}-{Quality}.mp4")
        except IndexError:
            print("No video found")


def download_file_progress(url, filename):
    with open(filename, 'wb') as f:
        r = get(url, stream=True)
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
        print("Finished")


id = input("Enter Id Video : ")
quality = input("Enter Quality ex(720,480,240) : ")
download(id, quality)
