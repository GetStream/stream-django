import os
from mock import patch
from fabric.api import local

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def parse_version(version):
	mj, mi, pa = version.split('.')
	return [int(mj), int(mi), int(pa)]

def increase_version(type, version):
	if type == 'major':
		nversion = [version[0] + 1, 0, 0]
	elif type == 'minor':
		nversion = [version[0], version[1] + 1, 0]
	elif type == 'patch':
		nversion = [version[0], version[1], version[2] + 1]
	else:
		raise Exception('Input Exception')

	return nversion

@patch('setuptools.setup')
def get_version(type, _setup):
	execfile(os.path.join(PROJECT_ROOT, 'setup.py'))
	_, kwargs = _setup.call_args

	version = parse_version(kwargs['version'])
	return version, increase_version(type, version)

def version(type):
	unstaged_changes = local('git status --porcelain')

	if unstaged_changes != '':
		print 'Clean your git working directory'
		return

	old_version, version = get_version(type)

	old_string = "version='%s'" % '.'.join([ str(n) for n in old_version ])
	new_string = "version='%s'" % '.'.join([ str(n) for n in version ])

	fin = open('setup.py')
	content = fin.read()
	fin.close()

	if old_string in content:
		content = content.replace(old_string, new_string)
		fout = open('setup.py', 'w')
		fout.write(content)
		fout.flush()
		fout.close()

	local('git add setup.py')
	local('git commit -m "new version"')
	local('git tag v%s' % '.'.join([ str(n) for n in version ])

def publish():
	unstaged_changes = local('git status --porcelain')

	if unstaged_changes != '':
		print 'Clean your git working directory'
		return

	version, _ = get_version('patch')

	local('git push origin --tags')

	local('python setup.py sdist')
	local('python setup.py bdist_wheel')
	local('python setup.py upload')