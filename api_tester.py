# import requests

# # Define the API endpoint
# student_id = 2  # Replace with the actual student ID
# url = f"http://127.0.0.1:8000/api/students/generate-certificate/{student_id}/"

# # Send the POST request
# response = requests.post(url)

# # Print the response
# print(f"Status Code: {response.status_code}")
# print(f"Response: {response.json() if response.status_code == 200 else response.text}")


import requests

# Define the API endpoint
course_id =1  # Replace with actual course ID
url = f"http://127.0.0.1:8000/api/students/upload/{course_id}/"

# Path to the Excel file
file_path = "students.xlsx"  # Replace with the actual file path

# Open the file in binary mode and send the request
with open(file_path, "rb") as file:
    files = {"file": (file_path, file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    

    response = requests.post(url, files=files)

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json() if response.status_code == 200 else response.text}")
