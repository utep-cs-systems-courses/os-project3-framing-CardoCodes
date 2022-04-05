
def archive(file_name): #encode file
    with open(file_name, "rb") as file: #open file in binary format for reading
        byteArray = bytearray() #setup bytearray object (i.e. array of bytes) - mutable sequence of integers 
        byteArray += file.read()  #add file to bytearray
        return byteArray
        

def unarchive(file_name, encoded_data): #decode encoded file
        with open(file_name, "wb") as file: #open file in bnary format for writing
            file.write(encoded_data) #write encoded data to file 

encoded = archive("sockets.txt")