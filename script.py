import requests

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
# ip_list = ["20.197.15.252:9000", "20.197.11.21:9000"]
ip_list = ["4.186.40.64:9000","20.198.17.214:9000"]


"""
7d187 70fec 09640 586fd b6f59 e4e5e f67b7

rc: 58567 09b33 eae63 8d635
"""
question_list = ["7d187" ,"70fec", "09640", "586fd", "b6f59", "e4e5e", "f67b7"]
# question_list = ["58567", "09b33", "eae63", "8d635","74a59","1d650","95f53"]
# question_list = ["addae"]
# 

make_post_requests(ip_list, question_list)
