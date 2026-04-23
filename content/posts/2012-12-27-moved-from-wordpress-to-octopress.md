---
title: Moved from Wordpress to Octopress
date: '2012-12-27'
categories:
- Octopress
---
So… I kinda got tired of Wordpress. A bit too much for me, I want something more lightweight that “just works”. I also stumbled over some blog that had just moved over to Octopress and made it sound like “da shit” for coders. So be it! And so far so good.

In short I did an XML export from inside Wordpress admin, created an account on Disqus, added the disqus plugin for Wordpress, exported over all comments, then “git cloned” Octopress onto my laptop, used exitwp (from github) to migrate my XML file from Wordpress, used rsync deploy over to my server and adjusted config in Octopress to use disqus (and thus pick up all old comments).

Yeah, that’s about it. :)
