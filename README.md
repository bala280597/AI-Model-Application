# AI-Model-Application


| Deployment | Type| Author |
| -------- | -------- |--------|
| Google Cloud,Github Action |Cloud  | BALAMURUGAN BASKARAN|

# Architechture

![Architechture](https://user-images.githubusercontent.com/47313756/165962407-489cded2-f8be-450b-99a4-355dde985c2c.jpg)
• CI/CD - Github Action
• Storage for Models & Data - Google Cloud Storage bucket and versioning is enabled for models. Helps to rollback models 
• Trigger CI/CD pipeline when new data arrives or Trained file updated in Google cloud storage - Google Cloud Functions
• Kubernetes - Flask application is hosted on Kubernetes with Horizontal Auto Scaling enabled. MYSQL Database is hosted as Statefulset and fully scallable.

# Application
• The application is a simple wrapper around an AI model that serve the model and bind a HTTP API to it, so that users can query the model and get back results.
• Users need to authenticate before using the application. Authentication is handled in the application by call to the MYSQL database.
• Users need to be registered before using application. Application supports users registration through api.
• User requests are logged into a database for later billing of the service (pay-per-request model).
![image](https://user-images.githubusercontent.com/47313756/165990340-13eb4ad3-e9a2-43a4-b47d-bfadf6622e75.png)


# Google Cloud Storage bucket
• Data for Model training and AI Models is stored in 2 seperate Google cloud bucket.
• Versioning is enabled for bucket in which AI Models stored.
• Maximum size of a single object can support upto 5 TiB. 
• No limit to the number of writes across an entire bucket
![GCS](https://user-images.githubusercontent.com/47313756/165990057-1703b91c-dc22-4fdb-ad53-6e5462951016.png)


