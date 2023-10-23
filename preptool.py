from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    # Receive data from the frontend
    data = request.get_json()
    uploaded_file = data['file']

    # Perform data cleaning, transformation, and integration using Pandas
    # Example:
    data = pd.read_csv(uploaded_file)
    
    # Additional data processing options
    if 'scale' in data:
        data = data * data['scale']
    if 'one_hot_encode' in data:
        data = pd.get_dummies(data, columns=data['one_hot_encode'])
    
    # Data visualization (bar chart)
    if 'plot_column' in data:
        plt.figure(figsize=(8, 6))
        data[data['plot_column']].value_counts().plot(kind='bar')
        plt.xlabel(data['plot_column'])
        plt.ylabel('Count')
        plt.title('Bar Chart')
        
        # Save the plot to a base64 encoded image
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        img_data = base64.b64encode(img_buffer.read()).decode()
        plt.close()

    # Return the processed data as JSON
    processed_data = data.to_dict(orient='records')
    
    return jsonify({'processed_data': processed_data, 'plot_image': img_data if 'plot_column' in data else None})

if __name__ == '__main__':
    app.run(debug=True)
