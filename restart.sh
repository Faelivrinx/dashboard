
docker rm -f dashboard-python

docker rmi dashboard-python

docker build -t dashboard-python .

docker run -it --rm --name dashboard-python -d dashboard-python
