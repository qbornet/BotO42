# Installation

## Requierement

First you will need python 3.8.13 or above, lesser version might work. I only tested for 3.8.10 so please refer to the version that i indicate, so you dont have trouble while runing the bot.

To check your python version: `python3 -V`

### Important
**You will do this part only if you want to have the bot running locally or if you are running on a different hosting plateform then heroku !**

`pip3 install -r requirements.txt`

## Begining

First we will get the 42 api key for **OAuth2.** This will allow us to communicate with the api and receive the information that we need.

**So how do we get the 42 api key ?**

We need to register a new app dont worry it's not that big of deal, click on **Settings** on your intra profile.

[![settings](https://i.postimg.cc/qRZQGQ4b/Screenshot-1.png)](https://postimg.cc/MMVy67cV)

**From here go to API**, Now click on **REGISTER NEW APP**
[![api](https://i.postimg.cc/Vv282jB4/Screenshot-3.png)](https://postimg.cc/dZRpyZfT)

This will prompt to you this
[![apimenu](https://i.postimg.cc/WpZqbSx2/Screenshot-4.png)](https://postimg.cc/mhbgm3bq)

So from here you will put a name **BotO42_yourlogin**.

For URI part, put this `file://localhost/dev/null` we dont need a uri because it's not a web application work flow.

In scopes check **manage user data**.

Other part are **optional** do whatever you want it doesn't matters.

You will end up with **2 keys** like this. **Important** don't share does key they should stay private
[![keys](https://i.postimg.cc/br22b96j/Screenshot-6.png)](https://postimg.cc/vxbBwfFP)

### Important
**If you are a student from a different campus then 42 Paris**, you will have to do the next step to find out what id your campus have on the api,

Also the api of other campus **might work in different way** and also have different endpoint if it's the only thing that you have to change this is not really hard,

you will have to change the url and endpoint probably. (E.g. https://api.intra.42.fr/oauth/token) The one that the bot use.

**If the api of your campus doesn't use OAuth just leave the installation part and try to redo the whole bot through requests module**

```
git clone https://github.com/qbornet/BotO42.git
cd BotO42
export UID_42="your_token"
export SECRET_42="your_token"
python3 test.py
```

The output would be like this **[index]: campus_id campus_name / campus_website** find your campus and remember your campus id and it's done now we will have to get the api key of Discord. 

## Discord

From here go through the developer portal of discord
- [Discord developers](https://discord.com/developers/applications)

Then create a new application chose a name.
[![NEWAPP](https://i.postimg.cc/mkKVHG9Z/Screenshot-5.png)](https://postimg.cc/bSH17WL4)

After that go in **Bot** click on Add Bot this will create a new bot,
[![addbot](https://i.postimg.cc/7YMmLj64/Screenshot-7.png)](https://postimg.cc/SJRWTTC1)

you will see a key looking like this: OTYyNzgxNjgzNDAzMzUwMDY2.YlMiUA._Crn_U2O2wI-RJAmWya-5e8HudQ. If you dont see a key click on Reset Token

Copy this and save it you will need that key to interact with the discord api, Remember this key should stay private if you leak this key you can reset it

For example the key above was a real key generated, now you cannot use this key because i reseted the key

[![token](https://i.postimg.cc/KcVyNkrj/Screenshot-8.png)](https://postimg.cc/PNmcfq7n)

Then **click OAuth2 > URL Generator** Check **bot** and scroll down copy the link given should look like this: 
- https://discord.com/api/oauth2/authorize?client_id=XXXXXXXXXXXXXXXXX&permissions=0&scope=bot

Modifiy the **permissions=0 to permissions=3072** and copy the full link on your browser (your link should like this now):
- https://discord.com/api/oauth2/authorize?client_id=XXXXXXXXXXXXXXXXX&permissions=3072&scope=bot


[![permandfinished](https://i.postimg.cc/L6H0jmG5/Screenshot-9.png)](https://postimg.cc/V5VR8PfP)

The last part is now to **add the bot to your server** or **a server where you have admin right** chose the right one and then we will test the bot on your machine

## Testing

Remember we have 3 key now. 2 from 42 api and 1 from discord api.

We have to export those as environment variable, it's safer if you have to modify the code and you want to push that through github.

**Those key must not appear as plain text inside your source code !**

### Important
If you already installed the requierements skip to **Usage**

WSL:
```
sudo apt-get update
sudo apt-get install libpython3-dev
sudo apt-get install python3-venv
```

Debian/Ubuntu:
```
sudo apt install python3.8-venv (try to find your equivalent for your system)
```

So for the testing we will use python3 virtual environment, which is cool because we can install multiple dependencies without adding that to our main environment

Testing:
```
cd BotO42
python3 -m venv env
source env/bin/activate
```

Now if you **check your python3 path** with:
`which python3` it should output `PATH_OF_THE_PROJECT/env/bin/python3`

Now we can install all the dependencies:
`python3 -m pip install -r requirements.txt`

## Usage

### Important
Now we have to export multiple variable respect the name of those variable it's important if you changed the name the bot will not work.

```
export CHAN_NAME="name of the channel where the bot will write"
export DISCORD_GUILD="name of the discord server (it's call guild yeah yeah)"
export DISCORD_TOKEN="your key to your discord api"
export UID_42=your uid key for 42 api (without the double quote sometimes it makes your key not register well)
export SECRET_42=your secret key for 42 api
```

### Warning
Be careful if you run the script and it doesn't work this is probably because you missed something in all of the step.

Also **if you are not at 42 Paris** you should change one line in the python script line 108 you should change the campus_id with yours, this line:
- [![line2change](https://i.postimg.cc/1RMkzW3L/Screenshot-10.png)](https://postimg.cc/dDkHHjdB)

Remember change any other stuff needed (link, endpoint, ...) if the behavior of the api is different depending on your campus

Once this is done you can run the bot:
`python3 boto.py`


Now everything should work we have 3 command !help, !add, !del just check !help for further information,

Next step is the hosting so you don't have to run the script on your PC if you have a different way of hosting or you think it's fine that the script 24/7 on your pc

The Installation Guide is finish for you for the other, we will setup heroku (without paying anything we will be able to run the bot)

Before going to the next part type `deactivate` this will quit venv

## Hosting

Now this is the fun part, here we gonna setup heroku first of all we need a heroku account create one, then install the cli:

- [Heroku-cli install](https://devcenter.heroku.com/articles/heroku-cli)


From here i lay down everything for you so you will have to setup nothing just use your account with the remote that heroku will create for you

Go on heroku dashboard and create a new app:

- [heroku-dashboard](https://dashboard.heroku.com/apps)

Now do both blue command (don't do the one on my screenshot do the one on your account):
[![bluecommand](https://i.postimg.cc/6Q0kGzh2/Screenshot-11.png)](https://postimg.cc/sBM6kYqs)

Once this is done we will go to the **Settings** > **Config Vars** all the variables that we need so the bot will run

| KEY | VALUE |
|-----| ------|
| DISCORD_TOKEN | Api key of discord |
| DISCORD_GUILD | Name of the server discord |
| CHAN_NAME | Name of the chan where the bot will write |
| UID_42 | UID key of 42 api |
| SECRET_42 | SECRET key of 42 api |

Once this is done you just have to go **Resources** and click on the button:
[![resoucre](https://i.postimg.cc/9F0gxCYf/Screenshot-12.png)](https://postimg.cc/rK69s6b6)

### The End
