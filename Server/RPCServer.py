import SimpleHTTPServer, SocketServer, inspect

instanceMachine, specMachine, nameMachine = None, None, None

def setWorker(Worker):
    global instanceMachine 
    global specMachine
    global nameMachine

    nameMachine = Worker.__name__.lower()
    instanceMachine = Worker()
    specMachine = {
		el: inspect.getargspec(getattr(instanceMachine, el)).args[1:]
		for el in dir(instanceMachine) 
		if (type(getattr(instanceMachine, el)).__name__ == 'instancemethod')
	}

def getSpecMachine(method):
    global specMachine
    return specMachine[method]

def parseArgument(method, params):
    argList = getSpecMachine(method.im_func.func_name)
    rawParams = {v[0] : v[1] for v in [el.split("=") for el in params.strip(" &").split("&")] if (len(v) == 2 and (v[0] in argList))}
    return [rawParams[k] for k in argList] if (len(rawParams) == len(argList)) else None
    

def getMachine():
    return instanceMachine

def execute(method, params):
    instance = getMachine()

    try:
        if (hasattr(instance, method)):
            method = getattr(instance, method) 
            argList = parseArgument(method, params)
            return method(*argList)
    except:
        return False

class RPCServer(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()
        
    def do_GET(self):
        if self.path.startswith('/{}/'.format(nameMachine)):
            service, argv = self.path.strip()[len(nameMachine)+2:].strip('/').split('?')
            self.wfile.write(execute(service, argv))
        else:
            self.wfile.write('{} server started'.format(nameMachine))

machine = None
def start(handler, server):
    setWorker(handler)

    machine = SocketServer.TCPServer(server, RPCServer);
    try:
        print 'Server (http://{}/) started'.format(':'.join(map(str, list(server))))
        machine.serve_forever()
    except KeyboardInterrupt:
        machine.shutdown()