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
			clean = d.denoise(os.path.join(uploads_dir, image.filename))
			# save the clear image
			cv2.imwrite(os.path.join(uploads_dir, 'clean.jpg'), clean)
			# detect the text
			results = dt.detect(os.path.join(uploads_dir, 'clean.jpg'))
			results = sorted(results, key=lambda y: y[0][0][1])

			img = cv2.imread(os.path.join(uploads_dir, image.filename))

			for (box, text) in results:
				
				cv2.polylines(img, [box], True, (0,255,0), 3)
				cv2.putText(img, text, (box[0][0], box[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
				output = img.copy()
				cv2.polylines(output, [box], True, (0, 255, 0), 2)

				text = cleanup_text(text)
				all_text.append(text)
				
				(x, y, w, h) = cv2.boundingRect(box)
				cv2.putText(output, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
				cv2.imshow('Text Detection', output)
				cv2.waitKey(0)
			cv2.destroyAllWindows(1)

			return redirect(request.url)

	return render_template("index.html")

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True)