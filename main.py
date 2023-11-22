
app = Flask(__name__, template_folder=r"C:\Users\E-JFRANCOGON\Documents\Placas\templates", static_folder=r'C:\Users\E-JFRANCOGON\Documents\Placas\static')
app.secret_key = "cemex secret key"

@app.route('/ocr', methods=['GET','POST'])
def ocr():
    try:
        if request.method == "POST":
            placa = request.form['placa']
            img = request.files['img']
            # Define the directory where you want to save the image
            save_directory = r'C:\Users\E-JFRANCOGON\Documents\Placas\img'
            img.save(os.path.join(save_directory, img.filename))
            IMAGE_PATH = os.path.join(save_directory, img.filename)
            print(IMAGE_PATH)
            reader = easyocr.Reader(['en'],gpu=False)
            result = reader.readtext(IMAGE_PATH)
            print(result)
 
            top_left = tuple(map(int, result[0][0][0]))
            bottom_right = tuple(map(int, result[0][0][2]))
            text = result[0][1]
            font = cv2.FONT_HERSHEY_SIMPLEX
 
 
            img = cv2.imread(IMAGE_PATH)
            img = cv2.rectangle(img,top_left,bottom_right,(0,255,0),4)
            img = cv2.putText(img,text,top_left,font,2,(255,255,255),2,cv2.LINE_AA)
 
            output_name = "test.jpg"
            output_path = os.path.join(save_directory, output_name)
            cv2.imwrite(output_path, img)
 
            text2 = placa
            print("texto real: ",text2)
            text = text.replace(" ", "")
            text = text.lower()
            print("texto detectado: ",text)
 
            similitud = SequenceMatcher(None, text, text2).ratio() * 100
            print(f"El porcentaje de similitud entre las cadenas es: {similitud:.2f}%")
            length = 10
            alphabet = string.ascii_letters + string.digits  # Includes uppercase, lowercase letters, and digits
            token = ''.join(secrets.choice(alphabet) for _ in range(length))
            token = str(token)
 
            #return redirect(url_for('form_preoperacional_inspeccion_360',rannum=token))
            #return redirect(url_for('exito'))
            return send_file(output_path, mimetype='image/png')
        return render_template('ocr.html')          
    except Exception as e:
        return str(e)
    
if(__name__=="__main__"):
    app.run()
    