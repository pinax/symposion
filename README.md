# Symposion

A conference management solution from Eldarion.

Built with the generous support of the Python Software Foundation.

See http://eldarion.com/symposion/ for commercial support, customization and hosting

## Usage
### Prerequisites
- python 
- pip
 - `curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python`
- build-essential (debian) or `yum groupinstall "Development Tools"; yum install gcc;` (centos)
- install git, git clone this repository, and cd into it.

### Quickstart
- `pip install -r requirements.txt`
- `python manage.py syncdb`
- `python manage.py loaddata fixtures/*`
 
## Development
### Getting the code
- Get an account with GitHub
- Click "Fork" on this page to create a fork (copy) of this repository
- Go to the resulting repo and copy the git url
- `git clone $url`
- `cd symposian`
- Now you can work on this code, commit and push to your own github repository

### Pushing the feature to Upstream
- Make sure your repo is in sync with upstream
 - `git remote add origin git://github.com/pinax/symposion.git`
 - `git fetch origin `
 - `git rebase origin master`
 - `git push origin master`
- Go to your github fork and click *pull request*.
 - The base repo should pinax/symposion and branch master. The head repo should be your fork and whatever branch you'd like to request pull from.
 - Leave a useful comment about the commit or a title and click *send pull request*
- Your feature will be merged it whenever the repo owners see fit.

## Deployment
### Development
- `python manage.py runserver localhost`
- Point your browser to localhost and it should load the project.

