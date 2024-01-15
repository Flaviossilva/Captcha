## Install 

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ nohup python3 server.py

## Call API

#### Post to your ip server port 5000 in path /images and include a body with captcha image, call this file as image. Response is decoded phrase is: text decoded