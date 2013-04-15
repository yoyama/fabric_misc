from fabric.api import run, env, sudo, parallel
from fabric.operations import open_shell
from fabric.contrib.files import append, exists


def install_chefsolo():
    '''
    Install chef-solo via opscode repository
    Target OS: Ubuntu 12.04
    '''
    opscode_list = "/etc/apt/sources.list.d/opscode.list"
    if not exists(opscode_list):
        cmd = 'echo "deb http://apt.opscode.com/ ' +\
        '`lsb_release -cs`-0.10 main"' +\
        ' > /etc/apt/sources.list.d/opscode.list'
        sudo(cmd)

    gpg_dir = "/etc/apt/trusted.gpg.d"
    if not exists(gpg_dir):
        sudo("mkdir %s" % (gpg_dir))
    sudo("gpg --keyserver keys.gnupg.net --recv-keys 83EF826A")
    sudo("gpg --export packages@opscode.com > " +\
         "/etc/apt/trusted.gpg.d/opscode-keyring.gpg")
    sudo("apt-get update")
    sudo("apt-get install -y opscode-keyring")
    sudo("env DEBIAN_FRONTEND=noninteractive apt-get install -y chef")
    sudo("/etc/init.d/chef-client stop")
    sudo("update-rc.d -f chef-client remove")
