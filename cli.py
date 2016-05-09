"""
This is the command line interface entry point for the Runway application.
"""

import os
import sys
import argparse
import unittest
from collections import namedtuple
from runway.core.cli.lib import cli_f

config = dict(
    db_host     = "localhost",
    db_username = "runway",
    db_name     = "runway",
    db_password = "123456",
    
    mock_db_host     = "localhost",
    mock_db_username = "postgres",
    mock_db_name     = "runway",
    mock_db_password = "123456",
    
    test_db_host     = "localhost",
    test_db_username = "postgres",
    test_db_name     = "runway_testing",
    test_db_password = "123456",
    
    backup_path      ='/path/to/backup/folder',
    
    api_path         = "http://localhost:6543/api/",
    dev_path         = "/path/to/dev/folder",
    
    # Typically the name of the system (e.g. "runway") within the dev folder
    folder_path      = '/path/to/dev/folder/folder',
    
    # Where are the PG binaries located if not on the path
    pgbin = "/usr/bin",
    
    # System name
    name = "runway",
)

def bootstrap(production = False):
    from pyramid.paster import bootstrap
    return bootstrap('{}/production.ini'.format(config['dev_path']))

def backup(options):
    from runway.core.system.lib import backup_f
    return backup_f.perform_backup(config)

def dev_app(options):
    os.system("cd {}; ../venv/bin/pserve development.ini --reload;".format(config['dev_path']))
    return ""

def new_plugin(options):
    from runway.core.system.lib import files_f
    
    import pathlib
    vals = options.vals
    
    if len(vals) != 2:
        return cli_f.shell_text("Required run command: [b]$ runway new_plugin[/b] name label")
    
    name, label = options.vals
    
    # Check to see if it exists
    p = pathlib.Path('{dev_path}/runway/plugins/{name}/__init__.py'.format(
        name = name,
        dev_path = config['dev_path'],
    ))
    
    if p.exists():
        return cli_f.shell_text("[r]This plugin already exists[/r]")
    
    os.system("cp -r {dev_path}/empty_module {dev_path}/runway/plugins/{name}".format(
        name = name,
        dev_path = config['dev_path'],
    ))
    
    folder_path = "{dev_path}/runway/plugins/{name}".format(
        name = name,
        dev_path = config['dev_path'],
    )
    
    def file_func(fpath, f):
        if f[0] in (".",):
            return
        
        if ".cpython" in f:
            return
        
        the_file = "{}/{}".format(fpath, f)
        
        with open(the_file, 'r', encoding="utf8") as f:
            contents = f.read()
        
        contents = contents.replace("{{name}}", name)
        contents = contents.replace("{{label}}", label)
        
        with open(the_file, 'w', encoding="utf8") as f:
            f.write(contents)
    
    for fpath, f in files_f.iter_tree(folder_path):
        file_func(fpath, f)
    
    return ""

def replicate_for_test(options):
    from runway.core.base import (
        DBSession,
        Base
    )
    
    pg_password = 'export PGPASSWORD="{}"'.format(config['mock_db_password'])
    
    # First we backup the live one
    # file_path = "{}/test.sql".format(config["backup_path"])
    
    args = "--host={host} --username={user} {db}".format(
        host = config["mock_db_host"],
        user = config["mock_db_username"],
        db   = config["mock_db_name"]
    )
    
    print("Saving data")
    
    file_path = "/tmp/runway_dupe.sql"
    os.system("{}/pg_dump --file={} {}".format(config['pgbin'], file_path, args))
    
    connect_string = "-h {host} -U {user}".format(
        host    = config["test_db_host"],
        user    = config["test_db_username"],
    )
    
    # Update user passwords
    with open(file_path, 'a') as f:
        f.write("\n")
        f.write("""UPDATE runway_users
        SET password = '$5$rounds=110000$A1vz94RZAKWk6mzf$mqMkuKbzKrNOddYhVnnElAPG0KQImtds6kQX1iSThf6';""")
        f.write("""DELETE FROM runway_security_checks;""")
        f.write("""UPDATE runway_settings SET value = 'True' WHERE "name" LIKE 'runway.modules.%'""")
    
    # Now we drop the mock one
    print("Dropping test database")
    # os.system("/library/PostgreSQL/bin/dropdb {} {}".format(connect_string, config["mock_db_name"]))
    os.system("{}; {}/dropdb {} {}".format(pg_password, config["pgbin"], connect_string, config["test_db_name"]))
    
    # Create a new one
    print("Creating new test database")
    # os.system("/library/PostgreSQL/bin/createdb {} {}".format(connect_string, config["mock_db_name"]))
    os.system("{}; {}/createdb {} {}".format(pg_password, config["pgbin"], connect_string, config["test_db_name"]))
    
    print("Installing SQL")
    os.system("{pgbin}/psql {conn} -d {db_name} -f {path}".format(
        pgbin   = config["pgbin"],
        conn    = connect_string,
        db_name = config["test_db_name"],
        path    = file_path,
    ))
    
    # Wipe PGPASSWORD
    os.system('export PGPASSWORD="\'Password not set\'"')
    
    # Now to install modules
    bootstrap()
    
    engine = DBSession.get_bind()
    Base.metadata.create_all(engine)
    
    return "Duplication complete"

def run_tests(options):
    from sqlalchemy.exc import SAWarning
    import warnings
    warnings.simplefilter('error', SAWarning)
    
    # Call the CLI as a new process so we don't cause session issues
    if not options.no_duplicate and not options.quick:
        os.system("{0}/../venv/bin/python {0}/cli.py replicate_for_test".format(config['dev_path']))
    
    if options.coverage:
        os.system("cd {}/runway; ../../venv/bin/nosetests --cover-package=runway --cover-erase --with-coverage --cover-html --cover-html-dir=../../coverage --cover-xml --cover-xml-file=../../coverage.xml".format(config['dev_path']))
        
        """
        Some other options for nosetests that may be of interest:
        
        https://nose.readthedocs.org/en/latest/usage.html
        
            --failed
        Run only the tests that failed last time
        
        ../bin/nosetests --failed
        """
    else:
        suite = unittest.TestLoader()
        
        verbosity = 1
        if options.verbose: verbosity += 1
        
        # -qf
        if options.quick:
            suite = suite.discover("%s/runway/core/testing/" % config['dev_path'], pattern="one_test_file.py")
            unittest.TextTestRunner(verbosity=verbosity).run(suite)
            
        else:
            verbosity += 1
            suite = suite.discover("%s/runway/" % config['dev_path'], pattern="*_tests.py", top_level_dir=config['dev_path'])
            unittest.TextTestRunner(verbosity=verbosity).run(suite)
            
        return "Use --cover to run with coverage information"
    
    return ""

def run_build(options):
    if not options.quick:
        suite = unittest.TestLoader()
        
        if not options.no_duplicate:
            os.system("{0}/../venv/bin/python {0}/cli.py replicate_for_test".format(config['dev_path']))
        
        suite = suite.discover("%s/runway/" % config['dev_path'], pattern="*_tests.py", top_level_dir=config['dev_path'])
        
        test_program = unittest.TextTestRunner().run(suite)
        
        if test_program.failures != [] or test_program.errors != []:
            return cli_f.shell_text("[r]The test suite failed, the build script was not run. To override this use the -f (force) argument[/r]")
    
    os.system("cd {}; sh build.sh".format(config['dev_path']))
    return ""

def cron(options):
    bootstrap(production=True)
    
    from runway.core.cron.lib import cron_f
    cron_f.background_process(config)
    return ""

def uninstall(options):
    bootstrap(production=False)
    
    if len(options.vals) < 1:
        module_name = input("Please name the module you wish to demo: ")
    else:
        module_name = options.vals[0]
    
    from runway.core import plugins
    from runway.core.plugins.lib import find
    
    for plugin_name in find.scan_for_plugins(config['folder_path']):
        if module_name == plugin_name:
            exec("from runway.plugins import %s" % plugin_name, plugins.__dict__)
            the_plugin = plugins.__dict__[plugin_name]
            
            if hasattr(the_plugin, "uninstall"):
                the_plugin.uninstall()
                return "{} successfully uninstalled".format(module_name)
            return "{} has no uninstaller".format(module_name)
    
    return "No plugin by the name of {}".format(module_name)

def demo(options):
    bootstrap(production=False)
    
    if len(options.vals) < 1:
        module_name = input("Please name the module you wish to demo: ")
    else:
        module_name = options.vals[0]
    
    from runway.core import plugins
    from runway.core.plugins.lib import find
    
    for plugin_name in find.scan_for_plugins(config['folder_path']):
        if module_name == plugin_name:
            exec("from runway.plugins import %s" % plugin_name, plugins.__dict__)
            the_plugin = plugins.__dict__[plugin_name]
            
            if hasattr(the_plugin, "demo"):
                the_plugin.demo()
                return "{} successfully setup for demo".format(module_name)
            return "{} has no demo mode".format(module_name)
    
    return "No plugin by the name of {}".format(module_name)

def sql(options):
    bootstrap(production=False)
    
    results = cli_f.sql(*options.vals)
    
    for i, query in enumerate(results):
        print("")
        print(options.vals[i])
        if query.returns_rows:
            for row in query:
                print(row)
        print("")
    return ""

def quick_test(options):
    bootstrap(production=False)
    
    from runway.core.system.jobs.prune_logs import PruneLogsJob
    j = PruneLogsJob()
    j.perform_job(None)
    
    return ""

def devel(options):
    py_path = "{d}/../venv/bin/python".format(d=config['dev_path'])
    
    os.system("rm -r {d}/runway.egg-info;".format(d=config['dev_path'], py=py_path))
    os.system("{py} {d}/setup.py develop".format(d=config['dev_path'], py=py_path))
    
    return ""

def cli_help(options):
    return """
$ runway <command> <options>

Useful commands:
  commands: Lists commands implemented by the system
    """

func_dict = {
    ("default", "dev_app"):             (dev_app, "Run development tool (pserve --reload)"),
    ("test", "tests"):                  (run_tests, "Run test suite"),
    ("replicate_for_test",):            (replicate_for_test, "Replicate for a test database"),
    ("build"):                          (run_build, "Run the build script"),
    ("backup"):                         (backup, "Run backup tool"),
    ("new_plugin"):                     (new_plugin, "Create a new plugin"),
    ("dupe", "duplicate", "replicate"): (replicate, "Duplicate the live data into the mock database"),
    # ("cron"):                           (cron, "Runs the cron script"),
    
    ("devel"):                          (devel, "Run the dev init scripts"),
    ("q"):                              (quick_test, "Run the quick test function"),
    ("?"):                              (cli_help, "Show CLI help information"),
    ("uninstall"):                      (uninstall, "uninstall a module"),
    ("demo"):                           (demo, "setup a demo mode for a module"),
    
    ("sql"):                            (sql, "run some sql"),
}

def main():
    parser = argparse.ArgumentParser(description='Runway command line interface.', prog="Runway")
    parser.add_argument('m', help='the mode being run with, list modes with mode set to "list"')
    parser.add_argument('vals', nargs="*")
    
    parser.add_argument('-v', dest="verbose", action="store_true", help='Verbose mode')
    parser.add_argument('-q', dest="quick", action="store_true", help='Asks the process to try and skip some steps', required=False)
    
    parser.add_argument('--no-duplicate', dest="no_duplicate", action="store_true")
    parser.add_argument('--coverage', dest="coverage", action="store_true", help="Used in testing, uses coverage rather than the built in testing")
    
    if len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        args = namedtuple('args', ['m'])(m='default')
    
    # Try the func dict
    for keys, the_function in func_dict.items():
        if isinstance(keys, str): keys = [keys]
        
        if args.m.lower() in keys:
            f, info = the_function
            print(f(args))
            sys.exit()
    
    # No mode found from the hard coded, check commands
    from runway.core.commands import execute_command
    
    try:
        bootstrap(production=False)
        r = execute_command(args.m.lower(), *getattr(args, "vals", []))
        
        if r != None:
            print(cli_f.shell_text(r))
        
        return
    
    except KeyError as e:
        if e.args[0][:24] == "Command by the name of '":
            print(cli_f.shell_text("[y]{}[/y]".format(e.args[0])))
        else:
            raise

if __name__ == '__main__':
    main()
