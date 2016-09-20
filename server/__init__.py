import os
import re
import sys

from flask import Flask
from routes import MODULES

app = Flask(__name__, static_folder="../site", template_folder="../site")


def start():
    load_config()
    register_modules()

    if app.config["DEBUG"]:
        app.debug = True

    app.run(host=app.config["HOST"], port=app.config["PORT"])


def load_config():
    app.config.from_object("config")


def register_modules():
    app_dir = os.path.abspath(__file__)
    sys.path.append(os.path.dirname(app_dir) + "/modules")

    for module in MODULES:
        module_router = "%s.router" % module["name"]
        register = False
        try:
            router = __import__(module_router, globals(), locals(), [], 0)
        except ImportError:
            print(module["name"] + " can not be loaded")
        else:
            url = None
            if "url" in module:
                url = module["url"]
            if app.config["DEBUG"]:
                print("[MODULE] Registered module router in %s to URL %s" % (module_router, url))
            if url == "/":
                url = None
            app.register_module(router.module, url_prefix=url)
        finally:
            load_module_dependencies(app, module)


def load_module_dependencies(app, module):
    if 'models' in module and module['models'] == False:
        return

    name = module["name"]
    if app.config["DEBUG"]:
        print("[MODEL] loding model %s" % name)

    models = "%s.models" % name

    try:
        models = __import__(models, globals(), locals(), [], 0)
    except ImportError as ex:
        if re.match(r'No module named', ex.msg):
            print('[MODEL] Unable to load the model for %s: %s' % (models, ex.msg))
        else:
            print('[MODEL] Other(%s): %s' % (models, ex.msg))
        return False
    return True
