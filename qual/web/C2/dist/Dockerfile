FROM golang:1.24
RUN adduser c2
USER c2
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN GOOS=linux go build -o main .
EXPOSE 8080
CMD ["./main"]