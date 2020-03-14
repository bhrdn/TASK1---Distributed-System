#!/usr/bin/python
import sys, os, json
import subprocess

URL = 'http://0.0.0.0:3333/engine/query?options='

if len(sys.argv) < 2:
	print 'Usage: {} {}'.format(sys.argv[0].split('/')[-1], 'pull')

options = sys.argv[1]

if options == 'pull':
	version = open('version').read().strip()
	p = subprocess.Popen(['curl', '{}{}'.format(URL, 'version')], stdout=subprocess.PIPE)
	_ = json.loads(p.communicate()[0])['result']
	if _ != version:
		print '[INFO] version {} deprecated'.format(version)
		p = subprocess.Popen(['curl', '{}{}'.format(URL, 'pull')], stdout=subprocess.PIPE)
		_ = json.loads(p.communicate()[0])['result']

		print '[INFO] pull files from server..'
		os.system('wget {}; unzip -v -o *.zip; rm *.zip'.format(_))

		print '[INFO] task completed !!'
	else:
		print '[INFO] all files are up to date !!'
elif options == 'push':
	try:
		version = open('version').read().strip()
		print '[INFO] push files to server..'
		os.system('zip ../resources/master-{}.zip * 2>&1 >/dev/null'.format(version))
		print '[INFO] task completed !!'
	except Exception as e:
		pass
