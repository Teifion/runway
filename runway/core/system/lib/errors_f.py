import inspect
import linecache
import os
import pydoc
import sys
import traceback
import cgitb
from datetime import datetime
import transaction
import json
import re

from pyramid.renderers import render_to_response
from pyramid.renderers import get_renderer

from uuid import uuid4

_instance_uuid = uuid4()
_startup_time = datetime.now()

# from ...communique import send as com_send

def com_send(*args, **kwards):
    pass

from ...base import DBSession
from ..models import ExceptionLog

graceful_images = {
    "default": "xkcd_computer_problems",
    "Permissions": "sandwich",
    "Input": "labyrinth_puzzle",
    "Not implemented": "compiling",
    "No data": "cell_phones",
    "Not found": "1_to_10",
    "Process": "workflow",
    "Password": "passwords",
    # "Integrity": ""
    # "Already done": "",
}

from ...lib import common
# GracefulException = common.GracefulException
        
styles = {
    "frame":            "font-family:monospace;padding:10px;border-top:1px solid #AAA;background-color:#EEE;color:#000;",
    "highlighted_row":  "background-color: #CCC;",
    "grey_text":        "color:#222;",
}

traceback_info = """The above is a description of an error in a Python program, formatted
for a Web browser because the 'cgitb' module was enabled.  In case you
are not reading this in a Web browser, here is the original traceback:"""

def log_error(exc, request, description="", context=5, extra_html=""):
    if not hasattr(request, "user") or request.anonymous:
        request.user = DudUser()
    
    error_output = html_render(sys.exc_info(), context=context, request=request) + extra_html
    
    # exception_type = str(sys.exc_info()[0]).replace("<class '", "").replace("'>", "")
    path = request.matched_route.pattern.format(**request.matchdict)
    
    if request.host[-5:] != ":6543" or "dev_log_anyway" in request.params:
        with transaction.manager:
            u = None
            if hasattr(request, "user"):
                if request.user.id > 0:
                    u = request.user.id
            
            # Param data
            data = {}
            for k in request.params:
                if k in ("password", "password1", "password2"): continue
                v = request.params[k]
                if len(v) < 200:
                    data[k] = v
            
            stmt = """INSERT INTO runway_exceptions
                ("timestamp", "path", "user", description, traceback, hidden, data) VALUES
                (:timestamp, :path, :user, :description, :traceback, :hidden, :data);"""
            
            args = dict(
                timestamp   = datetime.today(),
                path        = path,
                user        = u,
                description = description,
                traceback   = error_output,
                hidden      = False,
                data        = json.dumps(data),
            )
            
            # For some reason it won't let us use DBSession.add()
            # I would assume this is because we're breaking out
            # of the normal transaction block
            DBSession.execute(stmt, args)
            DBSession.execute("COMMIT")
    
    # with transaction.manager:
    #     exception_id = DBSession.query(ExceptionLog.id).order_by(ExceptionLog.id.desc()).first()[0]
    #     com_send(1, "core.exception", "There's been an exception", str(exception_id))
    
    return error_output

def log_error_without_request(exc, agent, path="", description="", data={}, context=5):
    error_output = html_render(sys.exc_info(), context=context)
    
    with transaction.manager:
        stmt = """INSERT INTO runway_exceptions
            ("timestamp", "path", "user", description, traceback, hidden, data) VALUES
            (:timestamp, :path, :user, :description, :traceback, :hidden, :data);"""
        
        args = dict(
            timestamp   = datetime.today(),
            path        = path,
            user        = agent,
            description = description,
            traceback   = error_output,
            hidden      = False,
            data        = json.dumps(data),
        )
        
        # For some reason it won't let us use DBSession.add()
        # I would assume this is because we're breaking out
        # of the normal transaction block
        DBSession.execute(stmt, args)
        DBSession.execute("COMMIT")
    
    # with transaction.manager:
    #     exception_id = DBSession.query(ExceptionLog.id).order_by(ExceptionLog.id.desc()).first()[0]
    #     com_send(1, "core.exception", "There's been an exception", str(exception_id))
    
    return error_output

# Used so we can grab it when testing
cache = {"traceback":""}

def html_render(einfo=None, context=5, request=None):
    """Copied from cgitb.html() and altered to suit my needs and preferences."""
    
    # If no info passed, grab it from the sys library
    if einfo == None:
        einfo = sys.exc_info()
    
    etype, evalue, etb = einfo
    if isinstance(etype, type):
        etype = etype.__name__
    
    indent = str(('&nbsp;' * 6))
    frames = []
    records = inspect.getinnerframes(etb, context)
    
    final_file, final_line = "", 0
    
    for frame, the_file, lnum, func, lines, index in records:
        if the_file:
            file_path = os.path.abspath(the_file)
            final_file = file_path
            link = '<a href="file://{}">{}</a>'.format(file_path, pydoc.html.escape(file_path))
        else:
            the_file = link = '?'
        
        args, varargs, varkw, locals = inspect.getargvalues(frame)
        call = ''
        if func != '?':
            call = 'in <strong>' + func + '</strong>' + \
                inspect.formatargvalues(args, varargs, varkw, locals,
                    formatvalue=lambda value: '=' + pydoc.html.repr(value))
        
        highlight = {}
        
        def reader(lnum=[lnum]):
            highlight[lnum[0]] = 1
            try: return linecache.getline(the_file, lnum[0])
            finally: lnum[0] += 1
        vars = cgitb.scanvars(reader, frame, locals)
        
        rows = []
        if index is not None:
            i = lnum - index
            for line in lines:
                num = "<span style='font-size:0.8em;'>" + '&nbsp;' * (5-len(str(i))) + str(i) + '</span>&nbsp;'
                if i in highlight:
                    final_line = i
                    line = '=&gt;%s%s' % (num, pydoc.html.preformat(line))
                    rows.append('<div style="{}">{}</div>'.format(styles['highlighted_row'], line))
                else:
                    line = '&nbsp;&nbsp;%s%s' % (num, pydoc.html.preformat(line))
                    rows.append('<div style="%s">%s</div>' % (styles['grey_text'], line))
                i += 1

        done, dump = {}, []
        for name, where, value in vars:
            if name in done: continue
            done[name] = 1
            if value is not cgitb.__UNDEF__:
                if where in ('global', 'builtin'):
                    name = ('<em>%s</em> ' % where) + "<strong>%s</strong>" % name
                elif where == 'local':
                    name = "<strong>%s</strong>" % name
                else:
                    name = where + "<strong>" + name.split('.')[-1] + "</strong>"
                dump.append('%s&nbsp;= %s' % (name, pydoc.html.repr(value)))
            else:
                dump.append(name + ' <em>undefined</em>')

        rows.append('<div style="{};font-size:0.9em;">{}</div>'.format(styles['grey_text'], ', '.join(dump)))
        
        frames.append('''
        <div style="{styles[frame]}">
            {link} {call}
            {rows}
        </div>'''.format(
            styles = styles,
            link = link,
            call = call,
            rows = '\n'.join(rows)
        ))
        
        final_file, final_line
    
    exception = ['<br><strong>%s</strong>: %s' % (pydoc.html.escape(str(etype)),
                                pydoc.html.escape(str(evalue)))]
    for name in dir(evalue):
        if name[:1] == '_': continue
        value = pydoc.html.repr(getattr(evalue, name))
        exception.append('\n<br>%s%s&nbsp;=\n%s' % (indent, name, value))
    
    path = "NO PATH"
    referrer = "No request"
    
    if request != None:
        referrer = request.referrer
    
    output = """
    <div class="panel panel-danger">
        <div class="panel-heading">
            <i class="fa fa-exclamation-triangle fa-fw"></i>
            Traceback
        </div>
        
        <div class="panel-body">
            <h2>{etype}</h2>
            <table class="table table-striped table-condensed">
                <tr>
                    <td style="text-align:right;">UUID:</td>
                    <td>{_instance_uuid}</td>
                </tr>
                <tr>
                    <td style="text-align:right;">Exception type:</td>
                    <td>{etype}</td>
                </tr>
                <tr>
                    <td style="text-align:right;">Exception value:</td>
                    <td><pre style="background-color:inherit;border-width:0;padding:0;margin:0;">{evalue}</pre></td>
                </tr>
                <tr>
                    <td style="text-align:right;">Exception location:</td>
                    <td>{location}</td>
                </tr>
                <tr>
                    <td style="text-align:right;">Referrer:</td>
                    <td>{referrer}</td>
                </tr>
                <!--
                <tr>
                    <td style="text-align:right;">Python executable:</td>
                    <td>{python_exe}</td>
                </tr>
                -->
                <tr>
                    <td style="text-align:right;">Python version:</td>
                    <td>{pyver}</td>
                </tr>
                <tr>
                    <td style="text-align:right;vertical-align: top;">Python path:</td>
                    <td>{pypath}</td>
                </tr>
                <tr>
                    <td style="text-align:right;">Server time:</td>
                    <td>{server_time}</td>
                </tr>
            </table>
            
    </div>""".format(
        styles      = styles,
        
        url         = path,
        location    = final_file + ", line %d" % final_line,
        etype       = pydoc.html.escape(str(etype)),
        referrer    = referrer,
        evalue      = pydoc.html.escape(str(evalue)),
        pyver       = sys.version.split()[0],
        python_exe  = sys.executable,
        pypath      = "<br>".join(sys.path),
        server_time = datetime.now().strftime("%A, %d of %b %Y %H:%M:%S %Z"),
        file_path   = path,
        _instance_uuid = _instance_uuid,
        
        # Takes file path and removes the root/system path from it
        short_file_path = path.replace(sys.path[0], ""),
    )
    
    cache['traceback'] = ''.join(traceback.format_exception(etype, evalue, etb))
    
    # return output + ''.join(frames) + ''.join(exception) + '''
    return output + ''.join(frames) + '''</div>


<!-- %s

%s
-->

''' % (traceback_info, pydoc.html.escape(
          ''.join(traceback.format_exception(etype, evalue, etb))))


_get_field_number = re.compile(r'could not pack parameter \$([0-9]+)::')
_get_query = re.compile(r'INSERT INTO (.+) RETURNING ')
def decipher_alchemy_error(exc):
    output = []
    
    if exc.args[0][0:42] == "(ParameterError) could not pack parameter ":
        field_number = int(_get_field_number.search(exc.args[0]).groups()[0])
        field_number -= 1
        query = _get_query.search(exc.args[0])
        
        if query != None:
            query = query.groups()[0]
            the_field = query.split(",")[field_number]
            output = [the_field, "<br />", str(field_number), "<br />", query]
        else:
            output = ["No match found"]
    else:
        output = ["No match found"]
    
    return """
    <div style="background-color:#5A5; padding:15px; color:#000;">
        %s
    </div>
    
    """ % "".join(output)
