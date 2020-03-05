from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import traceback
import pandas as pd
import pickle
import math
app = Flask(__name__)
CORS(app)

def format_prices(value):
    return math.floor(math.floor(value) / 100)

@app.route('/predict/', methods=['GET'])
def predict(id):
    json_ = request.json
    print(json_)

    valid_users = [18790, 22104]
    if id == 22104:
        df_results = results_22104
    else:
        df_results = results_18790

    if df_results.empty == False:
        try:
            df_results = model.copy()
            df_results = df_results.fillna(0)
            df_results['sales'] = df_results['sales'] + df_results['pred_value']
            df_results = df_results.drop(['pred_value', 'index'],axis=1)
            df_results['date'] = pd.to_datetime(df_results['date'], unit='ms')
            df_results.set_index('date')
            df_results['sales'] = df_results['sales'].map(format_prices)​
            df_list = df_results.values.tolist()
            return jsonify(df_list)
        except:
            return jsonify({'trace': traceback.format_exc()})
    else:
        print('Train the model first')
        return ('No model here to use')
​
if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line input
    except:
        port = 5000 # If you don't provide any port the port will be set to 12345
    with open('./18790.pkl', 'rb') as fout:
        results_18790 = pickle.load(fout) # Load "model.pkl"
    with open('./22104.pkl', 'rb') as fout:
        results_22104 = pickle.load(fout) # Load "model.pkl"

    print('Model loaded')
    app.run(port=port, debug=True)