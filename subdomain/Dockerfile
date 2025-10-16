FROM golang:1.17


WORKDIR /go/src/hakrawler
COPY docker_hakraw.py .
COPY . .

RUN go get -d -v ./...
RUN go install -v ./...

ENTRYPOINT ["hakrawler"]
