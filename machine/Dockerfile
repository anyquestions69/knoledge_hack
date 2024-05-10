FROM python:3.9-slim

WORKDIR /machine 
RUN apt update && apt install -y build-essential libffi-dev python-dev libhdf5-dev 

RUN python -m pip install --upgrade pip

COPY . /machine
RUN pip3 install  setuptools wheel
RUN pip3 install --no-binary=h5py h5py
RUN pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow
RUN pip3 install -r ./requirements.txt --verbose

CMD [ "python3", "/machine/main.py" ]