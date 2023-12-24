import cudatext as app


gsettings = {
    'datetime_format': '%m-%d-%Y',
    'pretty_log_format': '%>(17)%cn <%><(30)%ce> %cd: %s',
}


def load_ops(config_file):
    '''
    Load options from config file and stored in gsettings
    config_file: path to confile file
    '''
    gsettings['datetime_format'] = app.ini_read(config_file, 'op', 'datetime_format', gsettings['datetime_format'])
    
def save_ops(config_file):
    '''
    Save options from gsettings to config file
    config_file: path to config file
    '''
    app.ini_write(config_file, 'op', 'datetime_format', gsettings['datetime_format'])