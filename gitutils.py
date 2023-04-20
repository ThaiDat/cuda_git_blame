import os
import subprocess


def git_blame(path, line=None):
    '''
    Call the git blame command on specified file-line and return result
    path: file to blame
    line: line to blame
    return tuple(return code, return message)
    '''
    # startupinfo to prevent external console window appear
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    params = ['git', 'blame', os.path.basename(path), '--line-porcelain']
    if line is not None:
        params.extend(['-L', f'{line},{line}'])
    result = subprocess.run(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, cwd=os.path.dirname(path))
    return result.returncode, result.stdout if result.returncode == 0 else result.stderr                   
