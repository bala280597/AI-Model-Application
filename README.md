# AI-Model-Application


| Deployment | Type| Author |
| -------- | -------- |--------|
| Google Cloud,Github Action |Cloud  | BALAMURUGAN BASKARAN|

# Architecture
![Architechture](https://user-images.githubusercontent.com/47313756/165962407-489cded2-f8be-450b-99a4-355dde985c2c.jpg)

1) CI/CD - Github Action - Automate Model training and Application Deployment 
2) Storage for Models & Data - Google Cloud Storage bucket and versioning is enabled for models. Helps to rollback models 
3) Trigger CI/CD pipeline when new data arrives or Trained file updated in Google cloud storage - Google Cloud Functions
4) Kubernetes - Flask application is hosted on Kubernetes with Horizontal Auto Scaling enabled. MYSQL Database is hosted as Statefulset and fully scalable.

# Key Benifits:
1) Decoupling Architecture - Model training(Heavy Computational) and Flask application(Light Weight) is decoupled.
2) Micro Service Architecture + Serverless + Cloud Storage + Containerized Architecture.
3) I had solved 3 pain points which is mentioned in Challenge,
         1) When New Data arrives, Pipeline will be triggered.
         2) Versioning in object storage aids rollback of AI Models.
         3) User Requests can be throttled by enabling Horizontal Autoscaling for Pods.
         4) I had workaround SSL certificates which I had mentioned below under TLS certificate.
# Application
1) The application is a simple wrapper around an AI model that serves the model and binds a HTTP API to it, so that users can query the model and get back results.
2) Users need to authenticate before using the application. Authentication is handled in the application by a call to the MYSQL database.
3) Users need to be registered before using the application. Application supports users registration through api.
4) User requests are logged into a database for later billing of the service (pay-per-request model).
![image](https://user-images.githubusercontent.com/47313756/165990340-13eb4ad3-e9a2-43a4-b47d-bfadf6622e75.png)

# Google Cloud Storage bucket
1) Data for Model training and AI Models is stored in 2 seperate Google cloud bucket.
2) Versioning is enabled for bucket in which AI Models are stored.
3) Maximum size of a single object can support upto 5 TiB. 
4) No limit to the number of writes across an entire bucket.
![GCS](https://user-images.githubusercontent.com/47313756/165990057-1703b91c-dc22-4fdb-ad53-6e5462951016.png)

# Google Cloud Function
1) When new data arrives to the cloud bucket, Cloud function is triggered which invokes Github Action Pipeline which trains Data sets and uploads Model to another bucket.
2) When Model is updated in bucket, Cloud function triggers Github Action Pipeline which deploy the Flask application into Kubernetes Cluster.
![image](https://user-images.githubusercontent.com/47313756/165994033-05e91886-b746-470c-9f73-c6386fd4396e.png)

# Google Kubernetes Engine
1) Flask application is deployed in Google Kubernetes Engine and Load Balancer is created to route traffic.
2) Horizontal Auto Scaling is enabled by creating Horizontal Pod AutoScaler which Scales pod based on CPU utilisation. So User Requests can be throttled.
3)  MYSQL Database is hosted as a Stateful Set in Kubernetes. User Authentication credentials are verified with the User registration table in MYSQL Database.  
4) Each User request for model output is updated in MYSQL database for later billing of the service.
![Resource](https://user-images.githubusercontent.com/47313756/165997485-7329e48e-184f-4e33-8961-1c189a7d6f4c.png)
![Service](https://user-images.githubusercontent.com/47313756/165997528-b0d972f5-667c-4b23-ba57-2412e1b8dcb0.png)

# CI/CD Pipeline:
1) 2 Pipeline is consumed one for training model  and other for Application Deployment.
2) Training model Pipeline is triggered when new data arrives in a storage bucket .Pipeline performs model training and uploads a .pkl file to another storage bucket.
3) Application Deployment Pipeline is triggered when the developer updates the code or when a .pkl file is updated in the bucket. Pipeline builds Docker image and Deployed to Kubernetes Cluster 
![image](https://user-images.githubusercontent.com/47313756/165998381-6e4b53e4-61ab-45ec-b97a-36d95137ba68.png)

# TLS Certificate
1) In Kubernetes, To enable HTTPS for application, we need Domain name with SSL certificate and create Ingress(L7 Load Balancer),because Pods(server where app is running) in kubernetes are not permanent resource so self signed certificates is not a good practise.
2) In this challenge, I do not have a custom domain , So I created a Load Balancer Service( L4 Load Balancer) which routes based on TCP/UDP protocols.
3) My application currently supports HTTP endpoint only. But I can also enable HTTPS endpoints if a custom domain is provided.
