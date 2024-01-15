from flask import Flask
from flask import request
from decoder import process_image

app = Flask(__name__)

    
@app.route("/images",methods=["POST","GET"])
def main():
    try:
        if request.method=='POST':
            # print("request",request.form)
            image=request.files['image']
            image_name=image.filename
            image.save(image_name)
            if '.jpg' in image_name:
                decoded_phrase = process_image(image_name)

                return {"response": decoded_phrase.replace("\n", "").replace("\f", "")}
            
            elif '.jpeg' in image_name: 
                image.save(image_name)

                return {"response":"file saved successfully in your current durectory"}
            else:
                return {"error":"select you image file"}
    except Exception as e:
        return {"error":str(e)}

    
if __name__=="__main__":
    app.run("0.0.0.0",debug=True)
