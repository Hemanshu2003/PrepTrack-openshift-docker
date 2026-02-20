FROM nginx:alpine
# Copy the custom HTML file to the default Nginx public folder
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]