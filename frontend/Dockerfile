# Use the official unprivileged image
FROM nginxinc/nginx-unprivileged:alpine
 
# Copy your HTML file
COPY index.html /usr/share/nginx/html/index.html
 
# Expose port 8080 instead of 80 (non-root requirement)
EXPOSE 8080
 
CMD ["nginx", "-g", "daemon off;"]

