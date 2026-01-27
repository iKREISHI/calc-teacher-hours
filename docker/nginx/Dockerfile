FROM docker.io/library/nginx:1.29.3-alpine

RUN rm /etc/nginx/conf.d/default.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]