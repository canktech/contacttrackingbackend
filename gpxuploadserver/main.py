from fastapi import FastAPI, File, UploadFile

upload_folder="/gpxfiles"
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Coronavirus"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile=File(...)):
    global upload_folder
    print(file.filename) 
    file_object = file.file 
    #create empty file to copy the file_object to 
    upload_location = open(os.path.join(upload_folder, file.filename), 'wb+') 
    shutil.copyfileobj(file_object, upload_location) 
    upload_location.close()
    return {'filename': file.filename} 

#POST from client to 95.216.149:106:8000/uploadfile/
    
