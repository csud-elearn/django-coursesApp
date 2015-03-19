# http://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
from django.core.management.base import BaseCommand, CommandError
import subprocess
import os 
import signal
from optparse import make_option

from django.conf import settings

class Command(BaseCommand):
    args = '<specs>'
    help = 'Run the tests'
    option_list = BaseCommand.option_list + (
        make_option('--app',
            dest='directory',
            default="courses",
            help='Specify the app to run the tests'),
        )

    def handle(self, *args, **options):
        try:
            os.environ['WEBMATH_ENV'] = 'test'

            # check if the directory exists
            directory = options['directory']
            if directory not in settings.INSTALLED_APPS:
                raise CommandError("App '{}' does not exist".format(directory))

            # check if the file exists
            if args and not os.path.isfile("{}/spec/{}".format(directory, args[0])): 
                raise CommandError("Spec '{}' does not exist".format(args[0]))

            self.stdout.write('\nrun the tests in the {} directory (use the option --app to change that behavior)\n'.format(directory))

            # launch django and webdriver servers
            server = subprocess.Popen(["python3", "manage.py", "runserver", "3333"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
            webdriver = subprocess.Popen(["webdriver-manager", "start"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
            self.stdout.write('\n# SERVERS: Django and Webdriver servers launched\n')

            # create the test database
            self.stdout.write('\n# DATABASE\n\n')
            subprocess.call(["python3", "manage.py", "migrate", "--database=test"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.stdout.write('database created\n')

            # create the demo data
            subprocess.call(["python3", "manage.py", "seed"])

            # run the tests
            self.stdout.write('\n# TESTS\n\n')
            cmd = ["protractor", directory + "/spec/conf.js"]
            # run if a specific test file if given
            if args:
                cmd = cmd + ["--specs", "{}/spec/{}".format(directory, args[0])]
            subprocess.call(cmd)

            # remove the test database
            subprocess.call(["rm", "test.sqlite3"])
            self.stdout.write('\n# DATABASE: cleaned\n')

            # close django and webdriver servers
            os.killpg(webdriver.pid, signal.SIGTERM)
            os.killpg(server.pid, signal.SIGTERM)
            self.stdout.write('\n# SERVERS: Django and Webdriver servers closed\n\n')

            os.environ['WEBMATH_ENV'] = 'development'
        # ensure a clean interruption
        except KeyboardInterrupt:
            self.stdout.write('\n\n...Tests interrupted...')

            os.environ['WEBMATH_ENV'] = 'development'

            # close the servers
            if webdriver:
                os.killpg(webdriver.pid, signal.SIGTERM)
            if server:
                os.killpg(server.pid, signal.SIGTERM)
            self.stdout.write('\n# SERVERS: Django and Webdriver servers closed\n')

            # remove the test database
            if os.path.isfile("test.sqlite3"): 
                subprocess.call(["rm", "test.sqlite3"])
                self.stdout.write('\n# DATABASE: cleaned\n')