# About COVID-19

This README file contains the description of work involved in doing the MiniProject for Cloud Computing.

The project supports an application that is developed in flask and python and is deployed on a docker. The data extracted from the application API is stored in a cassandra database.

The project implements an API ([API documentation](https://about-corona.net/documentation)) that gets the up-to-date statstics for given country code. The response from the source is in the form of JSON but displayed in human readble HTML format. The information of interest are number of virus cases confirmed,recovered,deaths and date the data got updated.country code entered as'id' is used as a unique PRIMAY KEY for the cassandra database. The project assumes that a table already exists in the database ( The table covid.stats is created in KEYSPACE covid using CQL)

The main application file is app.py. It begins by importing required libraries.Cluster is imported from cassandra.cluster. This is needed to communicate with a cassandra database. The project also imports flask, request, render_template and forms. 

## Running the application:

The following field has to be entered for the need: country code.

How To Install and Run the Project : Install the Dependencies using pip install -r requirements.txt.

Run the project using python3 app.py.

## Overview

Application demo

![img](/results.PNG)

## Cassandra 

Apache Cassandra is a database management system that replicates large amounts of data across many servers, avoiding a single point of failure and reducing latency.[Learn More.](https://cassandra.apache.org/)

To build image
```
sudo docker build . --tag=cassandrarest:v1
```
To run it as a service, exposing the deploment to get an external IP:
```
sudo docker run -p 80:80 cassandrarest:v1
```
## Creating RESTful Services

Please note: this REST API uses a self signed certificate for SSL encryption. The curl command doesn't like self signed certificates and will not allow any requests to be made. Therefore, in order be able to make a request run all the below commands using sudo and the command parameter -k.

To implement methods like GET,POST,PUT,DELETE.

1. GET method

The GET method is for retrieving information.Here to get the list of countries.
##### Request
```GET /
curl -k -i https://ec2-18-234-180-253.compute-1.amazonaws.com/countries
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 184
Server: Werkzeug/1.0.1 Python/3.7.7
Date: Sun, 19 Apr 2020 01:01:51 GMT
{
'Spain', 'Austria', 'Iran', 'Bahrain', 'Canada', 'China', 'Switzerland', 'India', 'France', 'USA', 'Germany', 'Pakistan', 'UK', 'Qatar', 'Poland', 'Afghanistan', 'Australia', 'Italy'
}
```
2. POST method

To add a new country info.

##### Request
```POST /
curl -k -i -H "Content-Type: application/json" -X POST -d '{"name":"Bahamas","confirmed":1234, "deaths":2, "recovered": 100}' https://ec2-18-234-180-253.compute-1.amazonaws.com/country
```
##### Response
```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 45
Server: Werkzeug/1.0.1 Python/3.7.7
Date: Sun, 19 Apr 2020 00:30:24 GMT

{
  "message": "created: /country/Bahamas"
}
```
3. PUT method

To update a country info.
##### Request
```PUT /
curl -k -i -H "Content-Type: application/json" -X PUT -d '{"name":"Bahamas","confirmed":55, "deaths":9, "recovered": 10}' https://ec2-18-234-180-253.compute-1.amazonaws.com/country
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 45
Server: Werkzeug/1.0.1 Python/3.7.7
Date: Sun, 19 Apr 2020 00:33:04 GMT

{
  "message": "updated: /country/Bahamas"
}
```
4. DELETE method

To delete a country.
##### Request
```DELETE/
curl -k -i -H "Content-Type: application/json" -X DELETE -d '{"name":"Bahamas"}' https://ec2-18-234-180-253.compute-1.amazonaws.com/country
```
##### Response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 45
Server: Werkzeug/1.0.1 Python/3.7.7
Date: Sun, 19 Apr 2020 00:33:32 GMT

{
  "message": "deleted: /country/Bahamas"
}
```
## Creating a Home page

Flask looks for template files inside the templates folder.Therefore,index.html file is created inside templates.Inorder to view the HTML file created,import render_template() from the flask framework which is used to render the template files.

## Running Flask Application Over HTTPS

Self signed certificates are generated in the command line.
```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

Generating a 4096 bit RSA private key
......................++
.............++
writing new private key to 'key.pem'
-----
About to be asked to enter information that will be incorporated
into the certificate request.This is called a Distinguished Name or a DN.
There are quite a few fields which can be leftblank
For some fields there will be a default value, enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:Oregon
Locality Name (eg, city) []:Portland
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Miguel Grinberg Blog
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:localhost
Email Address []:
```

This command writes a new certificate in cert.pem with its corresponding private key in key.pem, with a validity period of 365 days.
To use this new self-signed certificate in Flask application,ssl_context argument in app.run() is set with a tuple consisting of the certificate and private key files along with port=443.
[Learn more](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)

## Kuberenetes Load Balancing Implementation

To create an External Load Balancer,following steps are required:

Install Kubernetes
```
sudo snap install microk8s --classic
```

  1.cassandra-image need to be build and push to registry
  ```
  sudo microk8s enable registry #To install registry

  sudo docker build . -t localhost:32000/cassandra-test:registry #To build and tag

  sudo docker push localhost:32000/cassandra-test # To push it to the registry
  ```
  
  2.The new configuration should be loaded with a Docker daemon restart and restart cassandra-image again
  
  ````
  sudo systemctl restart docker 

  sudo docker start cassandra-test
  ````
  3.Configure the deployment.yaml file
  
  4.Deploy docker container image present in the registry 

  ```
  sudo microk8s.kubectl apply -f ./deployment.yaml # To deploy

  sudo microk8s kubectl expose deployment covidmyapp-deployment --type=LoadBalancer --port=443 --target-port=443
```
Notes:

 To see the pods and services created
 ```
 sudo microk8s.kubectl get all

 ```
 To delete 
 ```
 sudo microk8s.kubectl delete deployment covid2019app-deployment
 sudo microk8s.kubectl delete services covid2019app-deployment
 ```

To learn more about creating external load balancer.[link](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/)
