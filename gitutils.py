import os
import subprocess


def git_blame(path, line):
    '''
    Call the git blame command on specified file-line and return result
    path: file to blame
    line: line to blame
    return tuple(return code, return message)
    '''
    # startupinfo to prevent external console window appear
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    #path = path.replace('\\', '/')
    result = subprocess.run(['git', 'blame', os.path.basename(path), '-L', f'{line},{line}', '-p'], 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, cwd=os.path.dirname(path))
    return result.returncode, result.stdout if result.returncode == 0 else result.stderr                   
