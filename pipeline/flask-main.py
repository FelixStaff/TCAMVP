from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return 'main'

@app.route('/run')
def run():
    from kedro.framework.context import load_context

    context = load_context('./')
    ouptut = context.run()
    return f'Pipeline run completed: {ouptut}'

if __name__ == '__main__':
    app.run(host='0.0.0.0')