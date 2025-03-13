import base64

with open("/Users/sydulamin/Desktop/running pro/Friendsbook-Metro/download.png", "rb") as img_file:
    encoded_string = base64.b64encode(img_file.read()).decode("utf-8")
    print(encoded_string)