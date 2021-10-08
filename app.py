from flask import Flask
from flask import request
from flask_cors import CORS
import numpy as np
import pandas as pd
from pytorch_tabular import TabularModel
import torch

app = Flask(__name__)
CORS(app)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
saved = TabularModel.load_from_checkpoint('NODEresults', map_location='cpu')


@app.route('/api/v1', methods=['POST'])
def Predict():
    if request.method == "POST":
        data = request.json
        holder = [*data]
        holder.sort()
        
        if holder != sorted([
            'gender', 'SeniorCitizen',
            'Partner', 'Dependents', 'tenure',
            'PhoneService', 'MultipleLines', 'InternetService',
            'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
            'TechSupport', 'StreamingTV', 'StreamingMovies',
            'Contract', 'PaperlessBilling', 'PaymentMethod',
            'MonthlyCharges', 'TotalCharges'
        ]):
            return 'Bad Request: Keys are not correct', 400
        test = pd.DataFrame.from_dict(data)
        datatypes = test.dtypes
        test_categorical = test.drop(
            columns=['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges']).astype('object')
        test_numerical = test[['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges']]
        numerical_features = test_numerical.dtypes.values
        for dtype in numerical_features.tolist():
            if dtype not in ['int64', 'float64']:
                return 'Bad Request: Numerical variables are of the wrong datatype', 400
        test = test_categorical.join(test_numerical)
        result = saved.predict(test)
        to_ret = result[['0_probability', '1_probability',
                         'prediction']].to_dict('list')
        return to_ret

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
