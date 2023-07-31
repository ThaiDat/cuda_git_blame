import os
import subprocess
from .settings import gsettings


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
    result = subprocess.run(params, capture_output=True, startupinfo=startupinfo, cwd=cwd)
    return result.returncode, result.stdout if result.returncode == 0 else result.stderr

def git_blame(path, line=None):
    '''
    Call the git blame command on specified file-line
    path: file to blame
    line: line to blame
    return tuple(return code, return message)
    '''
    params = ['git', 'blame', '--line-porcelain', '--root', os.path.basename(path)]
    if line is not None:
        params.extend(['-L', '{line},{line}'.format(line=line)])
    return __git(params, cwd=os.path.dirname(path))

def git_log(path, fmt=None):
    '''
    Call git log command on specified file
    path: file to blame
    fmt: pretty format
    return tuple(return code, return message)
    '''
    params = ['git', 'log', '--date=format:'+gsettings['datetime_format']]
    if fmt is not None:
        params.append('--pretty=format:' + fmt)
    params.append(os.path.basename(path))
    return __git(params, cwd=os.path.dirname(path))


def git_shortlog(path):
    '''
    Call git shortlog command on specified file
    path: file to blame
    return tuple(return code, return message)
    '''
    params = [
        'git', 'shortlog', 'HEAD', '-n', '-c', '-e', '-w0,4,8',
        '--date=format:'+gsettings['datetime_format'],
        '--pretty=format:%cd %s',
        os.path.basename(path)
    ]
    return __git(params, cwd=os.path.dirname(path))


def git_show(path, commit):
    '''
    Show file content at specified commit
    path: file to blame
    commit: specified commit hash
    return tuple(return code, return message)
    '''
    # git show require an explicit path after :
    params = ['git', 'show', commit+':./'+os.path.basename(path)]
    return __git(params, cwd=os.path.dirname(path))