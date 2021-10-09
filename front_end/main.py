from flask import Flask, render_template, request, redirect
import os

template_path = os.path.abspath('./front_end')

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
			image = request.files['image']
			print(image)
			image.save(image.filename)
			return redirect(request.url)

	return render_template("index.html")

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True)