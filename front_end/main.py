from flask import Flask, render_template, request, redirect
import sys
import os
import cv2
import denoise_image.denoise_document as d
import read_image.detect_text as dt
from read_image.helper import cleanup_text

uploads_dir = os.path.dirname(os.path.realpath(__file__)) + '/uploads'
template_path = os.path.abspath('./front_end')
all_text = []

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

app = Flask(__name__, template_folder=template_path)

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		if request.files:
  		# get the image
			image = request.files['image']
			# save the image
			image.save(os.path.join(uploads_dir, image.filename))
			#clean = d.denoise(os.path.join(uploads_dir, image.filename))
			# save the clear image
			#cv2.imwrite(os.path.join(uploads_dir, 'clean.jpg'), clean)
			# detect the text
			results = dt.detect(os.path.join(uploads_dir, image.filename))
			results = sorted(results, key=lambda y: y[0][0][1])

			img = cv2.imread(os.path.join(uploads_dir, image.filename))

			for (box, text) in results:
				text = cleanup_text(text)
				all_text.append(text)
			
			#print(all_text)
			return redirect(request.url)
			
	# convert list to a string		
	str_text = ' '.join(all_text)
	return render_template("index.html", data=str_text)

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True)