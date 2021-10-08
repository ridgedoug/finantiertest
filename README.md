# finantiertest

This repo contains a trained Neural Oblivious Decision Ensembles model that predicts the
 likelihood of customer defaulting on telco payment based on their telco data. NODE is a new deep learning architecture designed to work with tabular data.
 The architecture consists of differentiable oblivious decision trees (ODT) that are trained end-to-end by backpropagation. 
 To make the tree outputs differentiable, the authors used continuous counterparts to the splitting feature choice function and the Heaviside function, namely the entmax transformation. 
 NODE allows for multi-layer architecture design, where the outputs of each layer are concatenated with the outputs of the previous layers, and this in turn serves as the input to the next layer. 
 This allows for the learning of both shallow and deep decision rules.
 
 Link to the paper: https://arxiv.org/pdf/1909.06312.pdf
 
 The model was configured to train with 2 NODE layers and 1024 trees in each layer of depth 5. It obtained a test_accuracy of
 0.790, which is comparable to that of the Random Forest model used in the ipynb. For a more in depth EDA of the dataset, the cleaning
 process and model building and training, please refer to the .ipynb file. Do note that training the NODE model towards the end will require
 pytorch enabled with gpu and a CUDA compatible system. 
 
 The deployable model on the other hand is configured to run on cpu. To deploy the model locally in a container,
 make sure docker is installed, then clone this directory (use git clone. downloading the zip will not download the large model.cpkt file that's stored on git lfs. From the root folder where the Dockerfile resides, run the following commands:
 
 `docker build -t finantiertest .`
 
 `docker run -d -p 5000:5000 --name predictdefault finantiertest`
 
 The Dockerfile is configured to contain the necessary files and download the dependencies from requirements.txt during the building
 of the image. The first command builds the image and the second command runs the image in a container, mapping the host port 5000
 to the container port 5000 which is the default port used by Flask.
 
 Once the container is running, the model will run and can be pinged to predict a new customer instance for their likelihood of 
 defaulting. You can send a POST request to `localhost:5000/api/v1` with a json payload matching the format of the following example:
 
 `{
  "gender": ["Female"],
  "SeniorCitizen": [0],
  "Partner": ["Yes"],
  "Dependents": ["Yes"],
  "tenure": [0],
  "PhoneService": ["No"],
  "MultipleLines": ["No phone service"],
  "InternetService": ["DSL"],
  "OnlineSecurity": ["Yes"],
  "OnlineBackup": ["Yes"],
  "DeviceProtection": ["Yes"],
  "TechSupport": ["Yes"],
  "StreamingTV": ["Yes"],
  "StreamingMovies": ["Yes"],
  "Contract": ["Two year"],
  "PaperlessBilling": ["Yes"],
  "PaymentMethod": ["Bank transfer (automatic)"],
  "MonthlyCharges": [0],
  "TotalCharges": [0]
}`

Ensure that the keys and datatypes match the example above. The API checks for the correct format to pass into the model and will 
return a Bad Request describing the issue with the payload if a malformed payload is provided. The request will take around 10s to return a
response. As such, it is recommended to request a prediction for one customer at a time, although providing multiple instances in the payload is also
possible.

If the payload format is correct, the api will return a json response containing the 0_probability (no default), 1_probability (default) and
prediction. The response will look something like the following:

`{
    "0_probability": [
        0.7569267749786377
    ],
    "1_probability": [
        0.2430732250213623
    ],
    "prediction": [
        0
    ]
}`
