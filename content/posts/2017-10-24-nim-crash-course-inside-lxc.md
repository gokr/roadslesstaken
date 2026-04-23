---
title: Nim crash course in LXC
date: '2017-10-24'
slug: nim-crash-course-inside-lxc
categories:
- Nim
- LXC
- Languages
- Programming
---
[Nim](http://nim-lang.org) is an awesome programming language and this article is a **whirlwind-copy-paste-into-your-terminal-as-you-read-thing** to show how you install Nim, write a small program, compile it and package it in a very short time.

To spice it up, for **no specific reason at all**, we are doing it all inside a [Linux Container](http://linuxcontainers.org) - a fast virtual environment to work in. It's just a nice way to have a clean environment and to ensure that you as a reader see the same results as I do.

<!--more-->

You can of course just [skip the part on LXC and go directly to Nim fun](#skipit). :)

## Get going with LXC
**NOTE: The following presumes you are on a Ubuntu box, virtual should work fine.**

[Linux Containers](http://linuxcontainers.org) let's us run an isolated full Linux system inside a Linux host, kinda like KVM/Virtualbox but much more lightweight, similar to Docker. Contrary to Docker though, **LXC is not constrained to a single process**. Instead it behaves like a full VM which is much more what I want!

[LXD](https://linuxcontainers.org/lxd) is then a REST based daemon sitting on top of LXC that also gives us nice CLI tools operating against the daemon. See this [nice blog article series on LXD version 2.0](http://insights.ubuntu.com/2016/03/14/the-lxd-2-0-story-prologue/). Let's install LXD and get us a clean spanking new Ubuntu 17.04 environment!

NOTE: More detailed steps are [found here](https://linuxcontainers.org/lxd/getting-started-cli/) and a [cheat sheet](http://bartsimons.me/lxd-cheat-sheet-for-beginners/)

    sudo apt install lxd lxd-client zfsutils-linux
    newgrp lxd

Then step through a bunch of questions, just using defaults work fine:

    sudo lxd init

So that dance felt long, but... it was worth it!

## Fire up a fresh Ubuntu 17.04
Now we can fire up a fresh Ubuntu, say version 17.04, and call it `nim`:

    lxc launch ubuntu:17.04 nim

We can now see it's running:

    lxc list

And we can get a root shell inside it:

    lxc exec nim -- bash

But better to login properly as the `ubuntu` user:

    lxc exec nim -- su --login ubuntu

## <a name="skipit"></a>Install Nim
Today the preferred way to install Nim on Linux is to use [choosenim](https://github.com/dom96/choosenim), a neat toolchain multiplexer which makes it easy to switch between different versions of the Nim compiler. First we install GCC though, needed by choosenim:

    sudo apt install gcc

Then we can do the dance to install choosenim and nim:

    curl https://nim-lang.org/choosenim/init.sh -sSf | sh
    echo "export PATH=~/.nimble/bin:\$PATH" >> ~/.bashrc
    export PATH=~/.nimble/bin:$PATH

And we should have the Nim compiler in our path:

    ubuntu@nim:~$ nim --version
    Nim Compiler Version 0.17.2 (2017-09-07) [Linux: amd64]
    Copyright (c) 2006-2017 by Andreas Rumpf

    git hash: 811fbdafd958443ddac98ad58c77245860b38620
    active boot switches: -d:release


# Create a Nim program
Allright! Time to make a small Nim program called "moni" - don't ask why. First create a directory to work in, obviously we should use git etc, but I leave that to you. We also run `nimble init` to get a skeleton of a so called `.nimble` file. Nimble is the "npm" of the Nim ecosystem. And a nimble file is similar to `packages.json` for npm.

    mkdir moni && cd moni
    nimble init

Now, let's add some more lines to `moni.nimble`, starting with these three in the top section:

    binDir        = "bin"
    bin           = @["moni"]
    skipExt       = @["nim"]
 
This tells nimble that this package produces binaries and will put them in the directory `bin` when building. We also tell it that we have a list of binaries, the syntax for a `seq` in Nim, which is a dynamic array, looks like `@[ a, b, ... c ]`. So we add `"moni"` to that list, the executable's name.

Finally we also tell Nimble that when this package later is installed, skip installing all `.nim` files, since we are not making a Nim library, we only want the **compiled executable** to be installed.

Let's also add a dependency called `docopt` which is a [really nice Nim library](https://github.com/docopt/docopt.nim) for parsing command line arguments, to the bottom list of dependencies:

    requires "docopt"

The full file should now look like this:

```nimrod
# Package

version       = "0.1.0"
author        = "Göran Krampe"
description   = "A simple MQTT publisher tool."
license       = "MIT"
binDir        = "bin"
bin           = @["moni"]
skipExt       = @["nim"]

# Dependencies

requires "nim >= 0.17.2"
requires "docopt"
```

Ok, and finally, let's write some code. To begin with the program will just parse out arguments, and can show help, save this as `moni.nim`:
```nimrod
import docopt

let help = """
  moni - A simple MQTT publisher tool.
  
  Usage:
    moni [-u username] [-p password] [-s mqtturl] <topic> <payload>
    moni (-h | --help)
    moni (-v | --version)

  Options:
    -u username       Set username [default: test].
    -p password       Set password [default: test].
    -s mqtturl        Set URL for the MQTT server [default: tcp://localhost:1883]
    -h --help         Show this screen.
    -v --version      Show version.
  """

var args = docopt(help, version = "0.1.0")

# Get parameters
let username = $args["-u"]
let password = $args["-p"]
let mqtturl = $args["-s"]
let topic = $args["<topic>"]
let payload = $args["<payload>"]

echo "Username: " & $username
echo "Password: " & $password
echo "Server: " & $mqtturl
echo "Topic: " & $topic
echo "Payload: " & $payload

quit
```
Time to compile it!

If we want nimble to suck down dependencies automatically for us, then we build using nimble, it will use the `moni.nimble` to figure out what to do:

    nimble build

And we can then run the binary:

    ./bin/moni

If we supply a topic and payload we can see default values for options:

    ./bin/moni topic payload

We can also compile the `moni.nim` file directly, simply using the nim compiler - but that would have failed initially since we didn't have the `docopt` dependency installed. But do try it now:

    nim c moni.nim

The nim compiler will however put the binary in your current directory, not in `bin`.

Ok, let's get serious and add some real MQTT code into this. First add a dependency in `moni.nimble` to the Nim wrapper of the PAHO MQTT C library, by adding the following line at the bottom of `moni.nimble`:

    requires "https://github.com/barnybug/nim-mqtt"

So with nimble we can require using **direct URLs to git or mercurial repositories as well**, we are not limited to the pulished known packages in the Nimble catalog. Then make the code look like this instead:

```nimrod
import docopt, mqtt, MQTTClient

let help = """
  moni - A simple MQTT publisher tool.
  
  Usage:
    moni [-u username] [-p password] [-s mqtturl] <topic> <payload>
    moni (-h | --help)
    moni (-v | --version)

  Options:
    -u username       Set username [default: test].
    -p password       Set password [default: test].
    -s mqtturl        Set URL for the MQTT server [default: tcp://localhost:1883]
    -h --help         Show this screen.
    -v --version      Show version.
  """

var args = docopt(help, version = "0.1.0")

# Get parameters
let username = $args["-u"]
let password = $args["-p"]
let mqtturl = $args["-s"]
let topic = $args["<topic>"]
let payload = $args["<payload>"]

# Print them
echo "Username: " & $username
echo "Password: " & $password
echo "Server: " & $mqtturl
echo "Topic: " & $topic
echo "Payload: " & $payload

const ClientId = "nim-mqtt-pub"

proc connect(username, password, mqtturl: string): MQTTClient =
  ## Connect to MQTT server
  result = newClient(mqtturl, ClientId, MQTTPersistenceType.None)
  var connectOptions = newConnectOptions()
  connectOptions.username = username
  connectOptions.password = password
  result.connect(connectOptions)

proc disconnect(client: MQTTClient) =
  ## Disconnect the client
  client.disconnect(1000)
  client.destroy()

proc publish(client: MQTTClient, topic, payload: string) =
  ## Publish a payload on a topic
  discard client.publish(topic, payload, QOS.AtMostOnce, false)

try:
  var client = connect(username, password, mqtturl)
  client.publish(topic, payload)
  client.disconnect()
  echo "Payload sent"
except MQTTError:
  quit("MQTT exception: " & getCurrentExceptionMsg(), QuitFailure)

quit(QuitSuccess)
```

A few quick remarks about the code:

* When you see `$something`, that's Nim's way of saying `something.toString()`
* When you see `&` that's string concatenation.
* You also see three [procs](https://nim-lang.org/docs/tut1.html#procedures) that we later call inside the [try:](https://nim-lang.org/docs/tut2.html#exceptions-try-statement) block. A proc is just another name for function.
* In the `connect` proc there is a variable called `result`. It's an implicit variable available in all procs that have a return value and represents the thing that will be returned.
* In the `publish` proc we see the `discard` statement, it's used to "throw away" return values that we ignore, it has to be done explicitly in Nim or the compiler will complain.
* If all goes well we [quit](https://nim-lang.org/docs/system.html#quit,int) with success, otherwise [with the exception message and failure](https://nim-lang.org/docs/system.html#quit,string).

Then we build again:

    nimble build

And let's try running it aginst a public demo broker:

    ./bin/moni -s tcp://broker.hivemq.com:1883 sensor/99 '{"temp": 25.4, "flow": 0.7}'
    could not load: libpaho-mqtt3c.so
    compile with -d:nimDebugDlOpen for more information

Oops! Ok, so the MQTT wrapper library needs the C library of course! And it's not available as a deb, so let's get our hands dirty:

    sudo apt install libssl-dev make

Then we can build and install Paho C from source:

```bash
cd ~
git clone https://github.com/eclipse/paho.mqtt.c.git
cd paho.mqtt.c
make
sudo make install
sudo ldconfig
```

Let's try building again:

```bash
cd ~/moni
nimble build
```

And finally we can hopefully publish via MQTT, let's try it once more:

```bash
./bin/moni -s tcp://broker.hivemq.com:1883 cucumber/99 '{"temp": 25.4, "flow": 0.7}'
```

If it ends with "Payload sent" we are all good! We just sent a JSON payload to the cucumber/99 topic.

HiveMQ accepts anonymous connections on the test broker so we don't need to specify username/password. In order to verify that the above actually worked, you can point your browser to [http://www.hivemq.com/demos/websocket-client/](http://www.hivemq.com/demos/websocket-client/) and connect on port **8000** to **broker.hivemq.com**, then add topic subscription to "cucumber/#" and run the above command once more. If all works you should see the message appear!

Now, to round things off we can install this little program too, locally for your user inside the LXC container that is. :) You just run `nimble install` and then we have it in our path.

Ok, that's all folks - **you are now a Nim hacker!**

