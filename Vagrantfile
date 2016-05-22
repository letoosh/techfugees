#  vim: set ft=ruby ts=2 sw=2 tw=0 fdm=marker :
Vagrant.configure('2') do |config| config.vm.box = 'ubuntu/trusty64'

  config.vm.define "local", primary: true do |local|
    local.vm.network :forwarded_port, guest: 8000, host: 8000
    local.vm.synced_folder ".", "/srv/techfugees", owner: "vagrant", group: "vagrant"

    local.ssh.forward_agent = true

    local.vm.provision "ansible" do |ansible|
      ansible.host_key_checking = false
      ansible.playbook = "deploy/ansible/vagrant.yml"
      ansible.extra_vars = {
        ansible_ssh_user: 'vagrant',
        ansible_ssh_pass: 'vagrant',
        ansible_ssh_args: '-o ForwardAgent=yes',
        vagrant: true,
      }
      ansible.verbose = "vvvv"
      ansible.groups = {
        "webservers" => ["local"],
      }
    end
  end

  config.vm.define "staging", autostart: false do |staging|
    staging.vm.network :forwarded_port, guest: 80, host: 8080
    staging.ssh.forward_agent = true

    staging.vm.provision "ansible" do |ansible|
      ansible.host_key_checking = false
      ansible.playbook = "deploy/ansible/staging.yml"
      ansible.extra_vars = {
        ansible_ssh_user: 'vagrant',
        ansible_ssh_pass: 'vagrant',
        ansible_ssh_args: '-o ForwardAgent=yes'
      }
      ansible.verbose = "vvvv"
      ansible.groups = {
        "webservers" => ["staging"],
      }
    end
  end
end
