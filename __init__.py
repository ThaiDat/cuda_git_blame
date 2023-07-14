import cudatext as app
from cudatext import ed
from cudax_lib import get_translation
from .gitutils import git_blame, git_log, git_shortlog
from .parser import parse_blame_one_line, parse_blame_analysis, parse_formatted_log
from .settings import gsettings


_ = get_translation(__file__)  # I18N


class Command:
    def __init__(self):
        pass

    def log_output(self, msgs, clear=True, show=True):
        '''
        Log messages to output panel
        msgs: list of messages
        clear: clear the panel first if true
        '''
        if clear:
            app.app_log(app.LOG_CLEAR, '', panel=app.LOG_PANEL_OUTPUT)
        for msg in msgs:
            app.app_log(app.LOG_ADD, msg, panel=app.LOG_PANEL_OUTPUT)
        if show:
            app.app_proc(app.PROC_BOTTOMPANEL_ACTIVATE, 'Output')

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
        result = parse_blame_one_line(*git_blame(fn, line))
        # print result to output panel
        self.log_output(['{file_name} : {line}'.format(file_name=fn, line=line)] + result)

    def do_blame_analyze(self):
        '''
        Handle Blame Analyze command
        '''
        fn = ed.get_filename()
        result = parse_blame_analysis(*git_blame(fn))
        self.log_output([fn] + result)
        
    def do_see_file_history(self):
        '''
        Handle See file history command
        '''
        fn = ed.get_filename()
        result = parse_formatted_log(*git_log(fn, gsettings['pretty_log_format']))
        self.log_output([fn] + result)
        
    def do_see_file_history_by_commiter(self):
        '''
        Handle See file history by committer command
        '''
        fn = ed.get_filename()
        result = parse_formatted_log(*git_shortlog(fn))
        self.log_output([fn] + result)