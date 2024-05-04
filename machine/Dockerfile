FROM python:3.10.4

WORKDIR /machine 

#RUN apt update -y
RUN python -m pip install --upgrade pip

COPY . /machine

RUN pip3 install -r ./requirements.txt --verbose

CMD [ "python3", "/machine/receive.py" ]