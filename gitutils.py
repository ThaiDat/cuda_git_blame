import os
import subprocess


def __git(params, cwd=None):
    '''
    Prepare environment and call git command given params.
    params: list of params to send to shell, must contain 'git' at the beginning
    cwd: current working directory
    return tuple(return code, return message)
    '''
    # startupinfo to prevent external console window appear
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    result = subprocess.run(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, cwd=cwd)
    return result.returncode, result.stdout if result.returncode == 0 else result.stderr

def git_blame(path, line=None):
    '''
    Call the git blame command on specified file-line and return result
    path: file to blame
    line: line to blame
    return tuple(return code, return message)
    '''
    params = ['git', 'blame', '--line-porcelain', '--root', os.path.basename(path)]
    if line is not None:
        params.extend(['-L', '{line},{line}'.format(line=line)])
    return __git(params, cwd=os.path.dirname(path))