FROM python:3.6

RUN apt update

RUN pip3 install soba

RUN git clone https://github.com/gsi-upm/soba.git

WORKDIR soba/projects/seba

ARG mode

ENV mode ${mode}

EXPOSE 10000 7777

CMD python3 run.py -${mode} -s