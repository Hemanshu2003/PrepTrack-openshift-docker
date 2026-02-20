FROM nginx:alpine
# Copy the custom HTML file to the default Nginx public folder
#RUN rm /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]

