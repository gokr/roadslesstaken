---
title: Going virtual from CLI
date: '2013-01-21'
categories:
- VirtualBox
- Linux
- Ubuntu
- Computing
---
Recently when I automated a development process I looked deeper at managing virtual environments and ended up using two really nice tools complementing [VirtualBox](http://www.virtualbox.org) in a slick way - [Vagrant](http://www.vagrantup.com) and [Veewee](https://github.com/jedi4ever/veewee). A lot of us use VirtualBox of course, but getting a new Ubuntu box up is still a bit of blablablabla... What if it could be done *all from the command line and easily automated*?

<!--more--> 

Instead of talking, let me show you how you can get a Ubuntu 12.10 box (as an example) up and running. Note that this should work on **Ubuntu 12.10 (Quantal)** and probably 12.04 too:

```bash Installing the tools
# Base needed to get going, hope I didn't miss anything important
sudo apt-get install squashfs-tools genisoimage libxml2-dev zlib1g-dev libxslt1-dev ruby1.9.3

# New VirtualBox 4.2.0 (the one in Ubuntu proper is 4.1.x), it seems linux-headers are needed.
wget -q http://download.virtualbox.org/virtualbox/debian/oracle_vbox.asc -O- | sudo apt-key add -
sudo sh -c 'echo "deb http://download.virtualbox.org/virtualbox/debian quantal contrib" >> /etc/apt/sources.list'
sudo apt-get update && sudo apt-get install linux-headers-generic virtualbox-4.2

# Vagrant and Veewee from gems, used to build Ororo basebox and appliance
sudo gem1.9.3 install vagrant
sudo gem1.9.3 install veewee
```

As you can see I am installing VirtualBox 4.2.0, but 4.1.x probably works fine too. Ok, now that we have VirtualBox, Vagrant and Veewee we can get cracking. Veewee is a tool that adds some sub commands to Vagrant and automates the creation the VirtualBox instance from a vanilla OS ISO file that Vagrant then can control. Vagrant can then be used to bring such a box up, down and ssh into it and install lots of more software on it etc.

Let's pretend we are running a 64 bit Ubuntu on our machine but suddenly we want to compile some 32 bit libraries and the simplest way to do it is to just get a 32 bit virtual Ubuntu:

```bash Create an empty Ubuntu 12.10 32 bit basebox that we can reuse
mkdir quantal32
cd quantal32
vagrant basebox define quantal32 ubuntu-12.10-server-i386
vagrant basebox build quantal32
vagrant basebox validate quantal32
vagrant basebox export quantal32
vagrant box add quantal32 quantal32.box
```
The steps:

1. Pick a template. Veewee offers lots of templates we can use and you can list them using ```veewee vbox templates``` (just run ```veewee``` for more commands). We picked **ubuntu-12.10-server-i386**.
2. Build the box. You will see how VirtualBox pops up to life but everything is automated so don't touch!
3. Validate the box. This makes Veewee run a bunch of quick tests to check that the few things Veewee installed are all OK. The stuff installed can easily be inspected if you take a look in the sub dir definitions etc, it all has to do with making Vagrant happy for further provisioning etc.
3. Export the box as a single file called **quantal32.box** that we could share if we wanted to.
4. Add this exported box as a known basebox in Vagrant. This last step makes this basebox available to clone using Vagrant.

Okidoki, so now we have progressed from a downloaded ISO file of vanilla unmodified Ubuntu to a preconfigured VirtualBox. Of course, if you think the above is too much work :) then you can find [prebuilt baseboxes here](http://www.vagrantbox.es). Let's now create one of these puppies to use:

```
mkdir mynewbox
cd mynewbox
vagrant init quantal32
vagrant up
vagrant ssh
```
The steps:

1. When we init vagrant in our empty directory Vagrant will create a file called Vagrantfile in there. This file is actually a ruby script and you can edit it to customize your box. Since we gave a basebox name as the argument this file will include an entry ```config.vm.box = "quantal32"```. The file could even include a URL to this basebox so if you had published the basebox somewhere you could actually send this Vagrantfile to some other developer (or commit to SCM).
2. The up command simply brings the box up and running! Tada!
3. And then we can ssh into it easily. For more details see the homepage of Vagrant.

And when we are fed up with the box - just take it down with ```vagrant suspend``` (or halt) or nuke it with ```vagrant destroy```. Just run ```vagrant``` for a list of commands.

So now whenever you need a clean 32 bit Ubuntu for some testing or such - create a directory, run init and up, and there you are. :)

Of course, integrating these commands into Makefiles are quite simple too.
