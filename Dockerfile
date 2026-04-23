FROM ubuntu:24.04 AS builder
RUN apt-get update && apt-get install -y wget git && rm -rf /var/lib/apt/lists/*
RUN wget -qO /tmp/hugo.tar.gz https://github.com/gohugoio/hugo/releases/download/v0.147.4/hugo_extended_0.147.4_linux-amd64.tar.gz \
    && tar xzf /tmp/hugo.tar.gz -C /usr/local/bin hugo \
    && rm /tmp/hugo.tar.gz
WORKDIR /src
COPY . .
RUN hugo --minify

FROM nginx:alpine
COPY --from=builder /src/public /usr/share/nginx/html
EXPOSE 80
