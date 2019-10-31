# USER/PICTURE_HANDLER.PY
import os
from PIL import Image
from flask import url_for, current_app


def add_profile_pic(pic_upload, username):
    
    filename = pic_upload.filename
    #Eg mypicture.jpg  spilt => mypicture . 'jpg'
    ext_type = filename.split('.')[-1]
    #Eg username.jpeg
    storage_filename = str(username)+'.'+ext_type
    # Save the image
    filepath = os.path.join(current_app.root_path,'static\profile_pics',storage_filename)
    # required image size
    output_size = (200,200)
    # Save image
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename