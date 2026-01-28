[buymeacoffee]: https://www.buymeacoffee.com/philip2809
[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png

<div align="center">
  <img alt="neato-brainslug Logo" src="./pics/logo.svg" width="250">
  <h1>neato-brainslug</h1>
</div>

<div align="center">

_Control your Neato vacuum locally with an ESPHome brainslug_

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/V7V61PBIY6)
[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

  <h2>
      <a href="https://discord.gg/PAgwhWvyD8">
        Discord
      </a>
      <span> | </span>
      <a href="faq.md">
        FAQ
      </a>
      <span> | </span>
      <a href="demo.md">
        Demo
      </a>
      <span> | </span>
      <a href="#beta">
        Beta
      </a>
      <span> | </span>
      <a href="https://openpetition.org/!wknmd">
        Sign the petition
      </a>
</div>




Repair your Neato Robot Vacuum to be controlled via locally after the shutdown of the Neato servers. The scope of this project is to give your robot at least the same functionallity as when you bought it, however as the project is in a development state. The `main` branch only gets updates on releases, check out the `next` branch for the latest updates!

Since there is a couple of robots from neato and they have different firmware versions, they will need different configurations. I have decided they will be grouped based on their "generation".

- `gen1` - (Generation 1)
    - XV11
    - XV12
    - XV14
    - XV21
    - XV RS/HP
    - XV signature
    - XV signature pro
- `gen2` - (Generation 2)
    - Neato Botvac D70
    - Neato Botvac D75
    - Neato Botvac D80
    - Neato Botvac D85
    - Neato Botvac Connected **(Non DX)** `905-0249`
- `gen3` - (Generation 3)
    - Neato Botvac D3 Connected `905-0321`
    - Neato Botvac D4 Connected `905-0499`
    - Neato Botvac D5 Connected `905-0358`
    - Neato Botvac D6 Connected `905-0496`
    - Neato Botvac D7 Connected `905-0415`
- `gen 4` (Generation 4) - Sadly not yet supported
    - Neato D800 (probably the same as the d8-d10, not confirmed tho)
    - Neato D8 Intelligent `905-09596`
    - Neato D9 Intelligent `905-`
    - Neato D10 Intelligent `905-`


| Feature | `gen1` | `gen2` | `gen3` |
|---|---|---|---|
| Start & Stop | ✅ | ✅ | ✅ |
| Check errors | ✅ | ✅ | ✅ |
| Status | 🟠 | 🟠 | ✅ |
| Edit settings | ❌ | ✅ | ✅ |
| Scheduling on robot (via screen) | ✅ | ✅ | ❌ |
| Scheduling via ESPHome | ✅ | ✅ | ✅ |
| Scheduling via HA Automation | ✅¹ | ✅¹ | ✅¹ |
| Notifications | ✅¹ | ✅¹ | ✅¹ |
| Return to start | ❌ | ✅ | ❌ |
| Return to dock | ❌ | ❌ | ✅ |
| Manual driving | ❌ | ❌ | ✅ |

- ✅ - Supported
- 🟠 - Limited functionality
- ❌ - Not supported
- ¹ - Home Assistant required

The ability to create, view and edit floormaps so the robot can get the same functionallity with nogo-lines and zones is in the making.

### What is supported?

**We would like to support all robots where an debug interface, or other controls, is accessible!**

As far as we know, only the D3, D4, D5, D6 and D7 has the firmware `4.5.3` and currenly the config is based on that so the robots that should work with that firmware is as follows:
- Confirmed working: **D3, D4, D5, D6, D7**
- Should work with some work: **D70-D85, Connected, XV-series [maybe others? please get in touch!]**

The reason this works on all neato robots is because they all have the command interface, even the robots that originally don't have any wifi will still work, since it is no longer wifi robot that is connecting to the wifi, it is the ESP device. This also removes any limitations the robots wifi may have had.

**Trickier robots**
- D8 (probably D9, D10) - These robots use a compleatly different board, chip and firmware, and because the debug interface seams to be behind a password lock, this cannot be controlled directly. If you have one of these and are willing to tinker, please get in touch!

### What do I need?
- You need access to an USB port or the debug pins
    - We will be going through the different options to access these pins
- An ESPHome capable device
    - I would recommend an ESP32
- Cables to connect the robot to the ESP device
- The rest depends on your install!

# Getting started!

To get this up and running you will need to connect to the debug port or usb port on the robot. The XV-series robots have the usb port on the back, the rest has it in the dustbin area, making it inaccicible when using, for these robots we need to connect via the serial debug port, you would also need to do this if you are installing it internally inside the XV-series. So sadly for this repair you will need to get some extra hardware to get it up and running; however we are happy to help you out any step along the way!

First of all we need to get the version of your robot; to do this do the following:

0. You will need to use a Chromium based browser, e.g. Chrome
1. Connect to the USB port of your robot
2. Go to https://www.serialterminal.com/
3. Set the `Buad` to `115200`
4. Click `Connect` and select your vacuum
5. Send the commmand `GetVersion`
6. Look for the line with `Software`, this should be `Software,X,X,X,X,X`

Since we are parsing the data from the serial interface we need to be on the same verion of the robot firmware, this is what has been confirmed working:
| `gen1`  | `gen2`  | `gen3` |
|---|---|---|
| `3.2` | `2.2.0` or `2.2.1` | `4.5.3` or `4.6.0` |

If you have another version then these; please get in touch!

There is two ways of using this repair:

- [**Without Home Assistant**](./install-no-ha.md) 
- [**With Home Assistant**](./install-ha.md)

**If you don't mind to tinker a little bit I really do recommend to check out Home Assistant and do that route.** It is an open source home automation tool that puts local control and privacy first. Read more about them on their [website](https://www.home-assistant.io/) and try their [live demo](https://demo.home-assistant.io) if you want! There is a lot of great guides and information about home hassistant on youtube and their forums! They also have some amazing guides on their [site](https://www.home-assistant.io/installation/) to get an home assistant installation going. If you have any questions or problems, don't hesitate to ask for help here in the [discusstions](https://github.com/Philip2809/neato-connected/discussions) section, on our [discord](https://discord.gg/PAgwhWvyD8) or the home assistant [help](https://www.home-assistant.io/help/) page. 

**From version 2 of this project, when ROS is used for getting a floormap, you will need a separate computer running ROS, and the easiest and prioritized way to set that up will be via Home Assistant.**

## Beta



## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=philip2809/neato-connected&type=date&legend=top-left)](https://www.star-history.com/#philip2809/neato-connected&type=date&legend=top-left)

## Acknowledgements

- @Fabian Ullrich, Jiska Classen, Johannes Eger, Matthias Hollick, Fabian Freyer, crunch from Secure Mobile Networking Lab
    - [Security and Privacy for IoT Ecosystems](https://tuprints.ulb.tu-darmstadt.de/handle/tuda/4937)
    - [Vacuums in the Cloud:
Analyzing Security in a Hardened IoT Ecosystem](https://www.usenix.org/system/files/woot19-paper_ullrich.pdf)
    - And all of their work on these robots!
- [@jeroenterheerdt](https://github.com/jeroenterheerdt) for testing, reviewing, writing the guide for installing internally and the original [neato-serial](https://github.com/jeroenterheerdt/neato-serial)
- [@algaen](https://github.com/algaen) for the info about the D8 (D9, D10?) robots
- [@tomwj](https://github.com/tomwj) for testing and pictures installing it internally in a D7
- [@RobertSundling](https://github.com/RobertSundling) for the [firmware files](https://github.com/RobertSundling/neato-botvac)

