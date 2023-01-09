PROJECT= ExcelUpload


all: start


start: remove get venv req


remove:
	rm -r ${PROJECT} -f

get:
	git clone https://github.com/NickJoyce/${PROJECT}


venv:
	python3.8 -m venv ${PROJECT}/venv
	

req: 
	. venv/bin/activate && pip install -r ${PROJECT}/requirements.txt
