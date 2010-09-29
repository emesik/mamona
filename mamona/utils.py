from django.conf import settings

def import_backend_modules(submodule=''):
	try:
		backends = settings.MAMONA_BACKENDS
	except AttributeError:
		backends = []
	modules = {}
	for backend_name in backends:
		fqmn = 'mamona.backends.%s' % backend_name
		if submodule:
			fqmn = '%s.%s' % (fqmn, submodule)
		mamona = __import__(fqmn)
		if submodule:
			module = getattr(getattr(mamona.backends, backend_name), submodule)
		else:
			module = getattr(mamona.backends, backend_name)
		modules[backend_name] = module
	return modules

