from flask import Flask, render_template, request
#from flask import Flask, render_template, session, copy_current_request_context
import os

template_path = os.path.abspath('./front_end')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

app = Flask(__name__, template_folder=template_path)

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

# @app.route('/',methods = ['POST'])
# def predict():
#   return render_template('../front_end/index.html', prediction_text="Newton Predicts {}".format(prediction[0]))


if __name__ == '__main__':
    app.run(debug=True)