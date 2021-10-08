from app import app
import unittest
from flask import jsonify




class FlaskTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        app.config['SERVER_NAME'] = 'localhost:5000'
        cls.client = app.test_client()

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_success(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1',
                            json={
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
                                "MonthlyCharges": [52.55],
                                "TotalCharges": [0]
                            })
        headers = ['0_probability', '1_probability', 'prediction']
        for i in range(len(headers)):
            self.assertIn(headers[i].encode(), response.data)
        
    def test_bad_keys(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1',
                               json={
                                   "THISWILLFAIL": ["Female"],
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
                                   "MonthlyCharges": [52.55],
                                   "TotalCharges": [0]
                               })
        self.assertEqual(response.status, "400 BAD REQUEST",
                         "Status should be 400, was %s" % response.status)
        
    def test_bad_numericals(self):
        tester = app.test_client(self)
        response = tester.post('/api/v1',
                            json={
                                "gender": ["Female"],
                                "SeniorCitizen": ["THIS WILL FAIL"],
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
                                })
        self.assertEqual(response.status, "400 BAD REQUEST",
                            "Status should be 400, was %s" % response.status)

if __name__ == '__main__':
    unittest.main()
