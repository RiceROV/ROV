% Matlab Code Example for sending IMU Data
% Define the URL of the Flask server endpoint
url = 'http://localhost:5000/data';

% Define the headers
options = weboptions('MediaType','application/json');

% Create an array of data
data = [1, 2, 3];

% Convert the MATLAB array to a JSON formatted string
jsonData = jsonencode(data);

% Send the data as a POST request to the Flask server
response = webwrite(url, jsonData, options);

% Display the server response
disp(response);
