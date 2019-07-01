#

docker build -t seba --build-arg mode=$1 .

docker run -p 7777:7777 -p 10000:10000 --name sebarunning seba