import requests

# Function to make POST request for each IP and question
def make_post_requests(ip_list, question_list):
    for ip in ip_list:
        for question in question_list:
            payload = {
                'question': question,
                'contest':"16c24"
            }
            try:
                response = requests.post(f"http://{ip}/core/getTestcase/", json=payload)
                if response.status_code == 200:
                    print(f"Successfully sent request to {ip} for question '{question}'")
                else:
                    print(f"Failed to send request to {ip} for question '{question}', Status Code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error sending request to {ip} for question '{question}': {e}")

# Example IP list and question list
ip_list = ["20.197.15.252:9000", "20.197.11.21:9000"]
"""
b3202
3930c
70e1e
dadef
65073
addae
0ef76
"""
# question_list = ["b3202","3930c","70e1e","dadef","65073","addae","0ef76","2b4d6","3e9e3","2c2cb"]
question_list = ["addae"]

# Example URL endpoint where you want to make the POST request

# Call the function to make requests
make_post_requests(ip_list, question_list)
