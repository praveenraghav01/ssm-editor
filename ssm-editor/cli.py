import boto3
import tempfile
import os
import subprocess
from tabulate import tabulate

def fetch_parameters_by_path(path):
    """Fetch all parameters from AWS SSM by path."""
    ssm = boto3.client('ssm')
    parameters = {}
    next_token = None

    while True:
        kwargs = {'Path': path, 'Recursive': True, 'WithDecryption': True}
        if next_token:
            kwargs['NextToken'] = next_token
        response = ssm.get_parameters_by_path(**kwargs)

        for param in response.get('Parameters', []):
            parameters[param['Name'].split(path)[1]] = param['Value']

        next_token = response.get('NextToken')
        if not next_token:
            break

    return parameters


def edit_parameters_in_editor(parameters, editor):
    """Write parameters to a temp file as key=value, open in editor, and return updated values."""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".txt") as tmp:
        tmp_file = tmp.name
        for k, v in parameters.items():
            tmp.write(f"{k}={v}\n")

    if editor == "code":
        subprocess.Popen([editor, tmp_file])
        print(f"\nFile opened in VS Code: {tmp_file}")
        input("Press Enter after saving and closing the file in VS Code...")
    else:
        subprocess.call([editor, tmp_file])

    updated_data = {}
    with open(tmp_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or '=' not in line:
                continue
            key, value = line.split('=', 1)
            updated_data[key.strip()] = value.strip()

    os.unlink(tmp_file)
    return updated_data


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Edit AWS SSM parameters in your favorite editor.")
    parser.add_argument("--path", required=True, help="SSM path (e.g., /dev/pimcore/)")
    parser.add_argument("--editor", default="code", help="Editor to use (default: code)")
    args = parser.parse_args()

    path = args.path
    print(f"Fetching parameters from {path} ...")
    params = fetch_parameters_by_path(path)

    print(f"\nFetched {len(params)} parameters. Opening editor...")
    updated_params = edit_parameters_in_editor(params, args.editor)

    print("\nChanged values:")
    changes = []
    ssm = boto3.client('ssm')

    for k, v in updated_params.items():
        if params.get(k) != v:
            changes.append([k, params[k], v])
            try:
                ssm.put_parameter(
                    Name=path + k,
                    Value=v,
                    Type='SecureString',
                    Overwrite=True
                )
            except Exception as e:
                print(f"❌ Failed to update {k}: {e}")

    if not changes:
        print("No changes were made.")
    else:
        print(tabulate(changes, headers=["Parameter", "Old Value", "New Value"], tablefmt="grid"))
        print("\nAll changes have been updated in SSM.")