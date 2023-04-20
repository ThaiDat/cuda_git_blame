import cudatext as app
from cudatext import ed
from cudax_lib import get_translation
from cuda_git_blame.gitutils import git_blame


_ = get_translation(__file__)  # I18N


class Command: 
    def __init__(self):
        pass
    
    def log_output(self, msgs, clear=True):
        '''
        Log messages to output panel
        msgs: list of messages
        clear: clear the panel first if true
        '''
        if clear:
            app.app_log(app.LOG_CLEAR, '', panel=app.LOG_PANEL_OUTPUT)
        for msg in msgs:
            app.app_log(app.LOG_ADD, msg, panel=app.LOG_PANEL_OUTPUT)
    
    def do_blame_current_line(self):
        '''
        Handle command Blame current line
        '''
        # get current line
        carets = ed.get_carets()
        if len(carets) != 1:
            app.msg_status(_('Git Blame: Multiple carets not supported'))
        x0, y0, x1, y1 = carets[0]
        if y1 >= 0 and y1 != y0:
            app.msg_status(_('Git Blame: Multiple lines not supported'))
        line = y0 + 1
        # call git blame
        fn = ed.get_filename()
        result = git_blame(fn, line)
        # print result to output panel
        self.log_output(result)
        app.app_proc(app.PROC_BOTTOMPANEL_ACTIVATE, 'Output')