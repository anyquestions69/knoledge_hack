FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /machine 
RUN apt-get update && apt-get install -y build-essential libffi-dev python-dev-is-python3 libhdf5-dev libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg62-turbo-dev liblapack-dev libblas-dev gfortran
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN python -m pip install --upgrade pip

COPY . /machine
RUN pip3 install  setuptools wheel
#RUN pip3 install --no-binary=h5py h5py
RUN pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow
RUN pip3 install -r ./requirements.txt --verbose

CMD [ "python3", "/machine/main.py" ]