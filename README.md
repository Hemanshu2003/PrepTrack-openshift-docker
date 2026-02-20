# PrepTrack-openshift-docker
PrepTrack is a cloud-native, multi-tier web application designed to track study goals, manage syllabuses, and store preparation notes. It is built using a microservices architecture and deployed on the Red Hat Developer Sandbox (OpenShift).

---
 
```markdown
# 📚 PrepTrack: 3-Tier Microservices Study Portal
 
![OpenShift](https://img.shields.io/badge/OpenShift-EE0000?style=for-the-badge&logo=redhat&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
 
## 🎯 Project Overview
PrepTrack is a cloud-native, 3-tier web application built to manage intensive study schedules and track preparation progress for competitive technical exams, such as GATE and BARC CS.
 
This project serves as a practical demonstration of containerization, microservices architecture, and Kubernetes/OpenShift fundamentals. It showcases the deployment of a frontend UI, a stateless REST API, and a stateful database, all communicating securely within an OpenShift cluster.
 
## 🏗️ Architecture
 
The application is broken down into three decoupled tiers:
 
1. **Frontend (Tier 1):** A lightweight HTML/JS web interface served by an Nginx container. It makes asynchronous REST calls to the backend.
2. **Backend API (Tier 2):** A Python (Flask) REST API that handles business logic and database connections.
3. **Database (Tier 3):** A PostgreSQL database utilizing a Persistent Volume Claim (PVC) to ensure study data survives pod restarts.
 
```text
[ Web Browser ]  ---> (OpenShift Route) ---> [ Nginx Frontend Pod(s) ]
                                                    |
                                                    v
[ Python Flask API Pod(s) ] <--- (Internal Service) +
            |
            v
[ PostgreSQL Pod ] ---> (Persistent Volume Claim)
 
```
 
## ⚙️ Prerequisites
 
To deploy this project, you will need:
 
* Access to an OpenShift Cluster (e.g., Red Hat Developer Sandbox).
* The OpenShift CLI (`oc`) installed and logged in.
* Docker installed locally (if building images from scratch).
 
---
 
## 🚀 Deployment Guide
 
Follow these steps to deploy the complete architecture to your OpenShift environment.
 
### Step 1: Clone the Repository
 
```bash
git clone [https://github.com/YOUR_USERNAME/preptrack-repo.git](https://github.com/YOUR_USERNAME/preptrack-repo.git)
cd preptrack-repo
 
```
 
### Step 2: Create a Dedicated OpenShift Project
 
We isolate our application resources in a dedicated namespace.
 
```bash
oc new-project preptrack-env --display-name="PrepTrack Study Portal"
 
```
 
### Step 3: Deploy the Database Tier (Stateful)
 
Security and storage are paramount for the database. We first create a Secret to keep our password out of the deployment configurations, then deploy PostgreSQL with persistent storage.
 
```bash
# 1. Create a Secret for the DB password
oc create secret generic db-credentials --from-literal=db-password=SuperSecret123
 
# 2. Deploy PostgreSQL using the OpenShift catalog
oc new-app postgresql-persistent \
  -p POSTGRESQL_USER=prepuser \
  -p POSTGRESQL_PASSWORD=SuperSecret123 \
  -p POSTGRESQL_DATABASE=preptrackdb \
  -p VOLUME_CAPACITY=1Gi \
  --name=postgres-db
 
```
 
*(Note: Once the database pod is running, use `oc rsh <postgres-pod-name>` to log in and execute the `database/init.sql` script to seed the initial study tasks).*
 
### Step 4: Deploy the Backend API Tier (Stateless)
 
The backend needs to know how to find the database. We use a ConfigMap to pass non-sensitive environment variables (like the DB host) to the pod.
 
```bash
# 1. Create a ConfigMap for DB connection routing
oc create configmap backend-config \
  --from-literal=DB_HOST=postgres-db \
  --from-literal=DB_PORT=5432 \
  --from-literal=DB_NAME=preptrackdb \
  --from-literal=DB_USER=prepuser
 
# 2. Deploy the Python Backend (Assuming the image is pushed to a public registry like Docker Hub)
# Replace 'YOUR_DOCKERHUB_USERNAME' with your actual username where you pushed the image
oc new-app YOUR_DOCKERHUB_USERNAME/preptrack-backend:v1 --name=api-backend
 
# 3. Inject the ConfigMap and Secret into the Backend Deployment
oc set env deployment/api-backend --from=configmap/backend-config
oc set env deployment/api-backend DB_PASS=SuperSecret123
 
```
 
### Step 5: Expose the Backend API
 
The frontend needs a URL to communicate with the backend. We expose the backend service to create a public Route.
 
```bash
oc expose svc/api-backend
oc get route api-backend
 
```
 
**Crucial Configuration:** Copy the URL output from the `oc get route` command. Open `frontend/index.html` and replace `BACKEND_OPENSHIFT_ROUTE_URL` with this actual URL before building your frontend image.
 
### Step 6: Deploy the Frontend UI Tier
 
With the API route configured in our HTML, we can deploy the Nginx frontend.
 
```bash
# 1. Deploy the Nginx Frontend
oc new-app YOUR_DOCKERHUB_USERNAME/preptrack-frontend:v1 --name=web-frontend
 
# 2. Scale the frontend to ensure high availability
oc scale deployment/web-frontend --replicas=2
 
# 3. Expose the frontend to the public internet
oc expose svc/web-frontend
 
```
 
## ✅ Verification
 
To view the live application, retrieve the frontend URL:
 
```bash
oc get route web-frontend
 
```
 
Click the generated link. You should see the PrepTrack dashboard successfully fetching your study tasks from the PostgreSQL database via the Python API!
 
## 🧹 Cleanup
 
To tear down the entire project and free up cluster resources:
 
```bash
oc delete project preptrack-env
 
```
 
