import subprocess

result = subprocess.run([ 'echo', 'hello' ], capture_output=True)
print(result.returncode)
print(result.stdout.decode())
print(result.stderr.decode())
