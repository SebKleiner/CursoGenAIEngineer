## How to run the services

In the terminal:

1. install colima ```brew install colima```
2. start colima ```colima start```
3. go to the backend folder and choose the relevant service ```cd backend```
4. build the image: ```docker build -t fastapi-app .```
5. run the container: ```docker run -d --name fastapi-app -p 8000:8000 fastapi-app```
6. open logs: ```docker logs -f fastapi-app```
7. open the browser and go to: ```http://localhost:8000/docs```
8. Test -> using test_api.py file
9. Stop the container: ```docker stop fastapi-app```
10. Remove the container: ```docker rm fastapi-app```

**Shortcuts**

Start API
```
docker stop fastapi-app
docker rm fastapi-app
docker build -t fastapi-app .
docker run -d --name fastapi-app -p 8080:8080 fastapi-app
docker logs -f fastapi-app
```


## How to Deploy the services

1. install google cloud sdk ```brew install google-cloud-sdk```
2. login to google cloud ```gcloud auth login```
3. set the project ```gcloud config set project glossy-reserve-452115-v2```
4. build the image: ```gcloud builds submit --tag us-docker.pkg.dev/glossy-reserve-452115-v2/curso-ai-backend/test .```
5. deploy the service from the UI