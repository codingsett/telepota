<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]




<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/codingsett/telepota">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Telepota - an actively maintained python3 wrapper for the telegram BOT API.</h3>

  <p align="center">
    This project aims to simplify telegram bot development using higher level classes and functions which are easy to 
    understand and implement. I took over development and maintenance from <a href="https://github.com/nickoala">
    <strong>nickoala</strong></a> who was the author of this beautiful project.
    <br />
    <br />
    <a href="https://github.com/codingsett/telepota"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://t.me/telepota_dev">Ask Questions</a>
    ·
    <a href="https://github.com/codingsett/telepota/issues">Report  Bug</a>
    ·
    <a href="https://github.com/codingsett/telepota/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents


* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgements](#acknowledgements)





<!-- GETTING STARTED -->
## Getting Started

This project only supports python 3+, but for asyncio you are required to have python 3.5+

<p><strong>If you are previous telepot library user please uninstall it in your system before installing telepota. This is to prevent conflicts from happening while using this library.</strong></p>

### Installation

1. You can install this library using pip
```sh
pip install telepota --upgrade
```
1. You can install this library using easy install
```sh
easy_install telepota --upgrade
```
2. or you can install it from this repository
```sh
git clone https://github.com/codingsett/telepota
cd telepot
python setup.py install
```




<!-- USAGE EXAMPLES -->
## Usage

Lets dive into the code so that you can get a feel of what to expect.

``````python
import sys
import time
import telepot
from telepot.loop import MessageLoop

#Namedtuple module contains different helper classes that help you pass the correct data required
#by telegram bot api
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

#this function catches all 'normal' messages from the bot. There are other helper functions such 
#on_poll_data that catches all reponses from actions performed on a poll
def on_chat_message(msg):
    #telepot glance method extracts some useful data that you may require in different sections.
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    #keyboard made easily from a constructor class that we imported earlier.
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Press me', callback_data='press')],
               ])
    #This is how we send messages
    bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

#catches all inline_queries from the bot. Go to the documentation to read more.
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')

TOKEN = sys.argv[1]  # get token from command-line

#we pass the token from botfather to the bot instance.
bot = telepot.Bot(TOKEN)

#Messageloop initiates polling for the bot.
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

#make sure the bot runs forever.
while 1:
    time.sleep(10)
``````


_For more examples, please refer to the [Examples Folder](https://github.com/codingsett/telepota/tree/master/examples)_


<!-- ROADMAP -->
## Roadmap

- [ ] Modify and improve test coverage.
- [ ] Include github actions in the workflow.
- [ ] Replace urllib with requests maybe.
- [x] Update telepot to latest BOT API version.

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
I would like to thank the original author <a href="https://github.com/nickoala">
<strong>nickoala</strong></a> for making this framework. I have been using it for 3yrs+ without any changes.





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/codingsett/telepota.svg?style=flat-square
[contributors-url]: https://github.com/codingsett/telepota/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/codingsett/telepota.svg?style=flat-square
[forks-url]: https://github.com/codingsett/telepota/network/members
[stars-shield]: https://img.shields.io/github/stars/codingsett/telepota.svg?style=flat-square
[stars-url]: https://github.com/codingsett/telepota/stargazers
[issues-shield]: https://img.shields.io/github/issues/codingsett/telepota.svg?style=flat-square
[issues-url]: https://github.com/codingsett/telepota/issues
[license-shield]: https://img.shields.io/github/license/codingsett/telepota.svg?style=flat-square
[license-url]: https://github.com/codingsett/telepota/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
