try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
import sys
import requests
import time
import json

pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'


def ocr_core(filename):

    # text = pytesseract.image_to_string(Image.open(filename))
    # print(os.path.getsize('static/uploads/' + filename.filename))
    # print(filename.filename)
    # return text

    subscription_key = os.environ['SECRET_KEY']
    endpoint = os.environ['API_ENDPOINT']
    image_url = os.environ['URL'] + 'static/uploads/' + filename.filename
    api_url = endpoint + 'vision/v3.2/read/analyze'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    data = {'url': image_url}
    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()
    operation_url = response.headers["Operation-Location"]

    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(response.headers["Operation-Location"],
                                      headers=headers)
        analysis = response_final.json()
        p = analysis

        # print(json.dumps(analysis, indent=4))

        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False

    l = []
    for x in p["analyzeResult"]["readResults"][0]["lines"]:

        l.append(x["text"])

    # print(l)
    return '\n'.join(l)
