import RPCServer as rs, inspect, json
import subprocess

RESOURCES = 'http://0.0.0.0:9090/master-{version}.zip'

class Engine:
	def query(self, options):
		VERSION = sorted( subprocess.Popen(['ls', 'resources'], stdout=subprocess.PIPE).communicate()[0].split() )[-1].split('-')[-1].split('.z')[0]
		if options == 'version':
			result = VERSION
		elif options == 'pull':
			result = RESOURCES.replace('{version}', VERSION)

		return json.dumps({
			"service" : inspect.currentframe().f_code.co_name,
			"result" : result
		})

rs.start(Engine, ("0.0.0.0", 3333))