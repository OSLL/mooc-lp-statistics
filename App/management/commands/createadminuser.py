from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Initial create superuser'

    def add_arguments(self, parser):
        #Positional arguments
        #parser.add_argument('poll_id', nargs='+', type=int)
        parser.add_argument('--login', help='login')
        parser.add_argument('--email', help='email')
        parser.add_argument('--password', help='password')
        # Named (optional) arguments
        #parser.add_argument('--delete', action='store_true', dest='delete', default=False, help='Delete poll instead of closing it')

    def handle(self, *args, **options):      
    #    self.stdout.write(options['login'])
    #    self.stdout.write(options['email'])
    #    self.stdout.write(options['password'])

        if options['login'] is not None \
          and options['password'] is not None \
          and options['email'] is not None \
          and len(options['login']) > 0 \
          and len(options['password']) > 0 \
          and len(options['email']) > 0:

            username = options['login']
            password = options['password']
            email = options['email']

            if not (User.objects.filter(username=username).exists()):
                user = User.objects.create_user(username, email, password)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.stdout.write("Superuser has been added")
                self.stdout.write(username)
                self.stdout.write("Password is:")
                self.stdout.write(password)

            else:
                self.stdout.write('Looks like this username already exists')


        else:
            self.stdout.write("One of the arguments is missed: (--login, --email or --password)")
