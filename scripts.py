import os

def check_file_access(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print("File does not exist.")
        return False

    # Check for read permission
    if not os.access(file_path, os.R_OK):
        print("File is not readable.")
        return False

    # Check for write permission if needed
    if not os.access(file_path, os.W_OK):
        print("File is not writable.")
        return False
    print("File is accessible and ready to be used.")
    return True
print(os.path.abspath("./test.pdf"))
file_path = '/Users/mouayadmouayad/Desktop/jobbAI/test.pdf'
check_file_access(file_path)