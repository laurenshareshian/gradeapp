Instructions for setting up simple grading app on OSU's server:

I got most of my instructions from [here](https://github.com/knightsamar/CS340_starter_flask_app).


Set up your VPN.

Log in to flip2:
ssh {username}@flip2.engr.oregonstate.edu

git clone https://github.com/laurenshareshian/gradeapp.git

cd gradeapp
bash
virtualenv venv -p $(which python3) 
source ./venv/bin/activate
pip3 install --upgrade pip
pip install -r requirements.txt


source ./venv/bin/activate
export FLASK_APP=main.py

Change 8042 to your favorite four digit number:
python -m flask run -h 0.0.0.0 -p 8042 --reload

Go to http://flip2.engr.oregonstate.edu:8042/ in your browser (change 8042 if necessary)

Type in "Jane Doe" or "John Doe" and you should see the classes they teach.