FROM python:3.6

RUN apt update

RUN pip3 install soba

RUN git clone https://github.com/gsi-upm/soba.git

WORKDIR soba/projects/seba

EXPOSE 10000

EXPOSE 7777

CMD python3 run.py -v -s
