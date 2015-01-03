import json
import os
import pystache

class PackageManifestException(Exception):
    pass

def parse_package_manifest(package_manifest_json):
    manifest = {}
    parameters = {}
    try:
        manifest = json.loads(package_manifest_json)
    except ValueError:
        raise PackageManifestException('Invalid package manifest.')
    required_attributes = ['name', 'description']
    for required_attribute in required_attributes:
        if required_attribute not in manifest:
            raise PackageManifestException('Invalid package manifest. Missing {0} attribute.'.format(required_attribute))
    parameters['plugin_name'] = manifest['name'] or ''
    parameters['plugin_name_cc'] = manifest['name'].title() or ''
    parameters['plugin_description'] = manifest['description'] or ''
    return parameters

def substitute(content, parameters):
    return pystache.render(content, parameters)

def generate_files(package_json_path='package.json', dest_path='.'):
    package_manifest_content = open(package_json_path).read()
    parameters = parse_package_manifest(package_manifest_content)
    for root, dirs, files in os.walk('boilerplate'):
        new_root = root.replace('boilerplate', '')
        if new_root.startswith("/"):
            new_root = new_root[1:]
        new_path = os.path.join(dest_path, new_root)
        for file_ in files:
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            new_file_path = os.path.join(new_path, substitute(str(file_), parameters))
            old_file_path = os.path.join(root, str(file_))
            open(new_file_path, 'w').write(substitute(open(old_file_path).read(), parameters))
    new_json_manifest_path = os.path.join(dest_path, parameters['plugin_name'] + '.jquery.json')
    open(new_json_manifest_path, 'w').write(open(package_json_path).read())

def install_dependencies(dest_path):
    os.system('cd {0} && bower install qunit'.format(dest_path))
    os.system('cd {0} && bower install jquery'.format(dest_path))
    os.system('cd {0} && npm install'.format(dest_path))

def generate(package_json_path='jquery.json', dest_path='.'):
    try:
        generate_files(package_json_path, dest_path)
        install_dependencies(dest_path)
    except OSError as ex:
        print (ex)

generate(package_json_path='vimeoplaylist.jquery.json', dest_path='/build')
