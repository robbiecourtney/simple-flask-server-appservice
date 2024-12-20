from quart import Quart, Blueprint, render_template, request
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
import os
import logging

logger = logging.getLogger('app_log')
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(levelname)s : %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

bp = Blueprint("routes", __name__, static_folder="static")

@bp.route("/favicon.ico")
async def favicon():
   return await bp.send_static_file("faficon.ico")

@bp.route('/')
async def index():
  return await render_template('index.html')

@bp.route('/hello')
async def hello():
  return await render_template('hello.html', name=request.args.get('name'))

# Create a quart app
app = Quart(
  __name__,
  template_folder='templates',
  static_folder='static'
)
app.register_blueprint(bp)

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    logger.info("APPLICATIONINSIGHTS_CONNECTION_STRING is set, enabling Azure Monitor")
    configure_azure_monitor()
else:
   logger.info("APPLICATIONINSIGHTS_CONNECTION_STRING is NOT set, NOT enabling Azure Monitor")

if __name__ == '__main__':
  # Run the quart app
  app.run(host='0.0.0.0', debug=True, port=8080)