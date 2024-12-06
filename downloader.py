import requests

def download_pdf(link, dir='./', filename=None):
    response = requests.get(link)
    if filename is None:
        filename = f'article{time.time()}.pdf'
    with open(dir + filename, 'wb') as f:
        f.write(response.content)