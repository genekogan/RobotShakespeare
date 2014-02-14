##[Robot Shakespeare lives here!](http://www.twitter.com/RobotShakespear)

##[More info on the project](http://www.genekogan.com/works/robot-shakespeare.html)

Source code for [Robot Shakespeare](http://www.twitter.com/RobotShakespear), an automated twitter account which spits out some pseudo-Shakespeare every 30 minutes forever. 

It works by using [NLTK](http://nltk.org) to analyze the complete works of one William Shakespeare and generate an [n-gram](http://en.wikipedia.org/wiki/N-gram) model, i.e. a word-to-word transition probability model. It then generates snippets of occasionally beautiful prose by doing a random walk on the text using a [Markov Model](http://en.wikipedia.org/wiki/Markov_model).

### How to make your own twitter bot

This is well documented, but to create a twitter bot, you need to create a twitter account, then setup an application on [Twitter dev](http://dev.twitter.com)with OAuth protocol. [This link](http://www.apcoder.com/2013/10/03/twitter-bot-20-minutes-node-js/) explains it pretty well minus the node.js stuff. Once you have the access token, you can very easily setup a python script which tweets to your new bot using [tweepy](https://github.com/tweepy/tweepy).

Also handy... if you wish to let your script run indefinitely without generating a massive log file, you need to nohup it before you close your ssh session:
	
	nohup python main.py  > /dev/null 2>&1&
