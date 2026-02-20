# Install ESPHome device

Now its time to install the ESPHome device in a more permanent way, there is two main ways to do this, and both of these methods use the following item:
| |  | | |
:-:|:-:|:-:|:-:
**JST-XH to DuPont** | ![JST-XH to dupont](pics/installs/0_jst-xh.jpg) | Either buy or make this type of cable, it will be used to connect the ESP device to the debug port. You could also use dupont female-female connectors, but you will need the make the hole larger and add some protection for the cables because they would be too stiff and could break when the robot bumps into things. | https://www.aliexpress.com/item/1005006251847933.html


[Externally; by drilling a hole in the bumper](#externally) | [Internally; by connecting to the debug port using an JST-XH connector (recommended)](#internally)
:-------------------------:|:-------------------------:
![cables-via-bumper](./pics/installs/8_cables-via-bumper.jpg) ![d3-install-outside](./pics/installs/external.jpg) | ![jay-jst-xh](./pics/installs/jay/2-install-JST-XH.jpg) ![jay-installed](./pics/installs/jay/4-installed-and-taped.jpg)


## Internally

**Warning: before opening up the robot, make sure to open the battery compartment and remove the battery. We will include this again step in the step-by-step procedure.**

The pictures here are from a D5 but should be similar for others. Please read the guide fully before doing it yourself!

### What you need
- protective cover for your work surface
- Long T10 Torx bit + bit holder
- Philips screwdriver
- The ESP you flashed
- [One male JST-XH cable](https://www.amazon.com/dp/B0D9R3MP4G?ref=cm_sw_r_cso_cp_apan_dp_N8757APDHEV6D087T3VR&ref_=cm_sw_r_cso_cp_apan_dp_N8757APDHEV6D087T3VR&social_share=cm_sw_r_cso_cp_apan_dp_N8757APDHEV6D087T3VR&titleSource=true)
- A soldering iron
- 4 pieces of about 10 cm of wire
- 4 pieces of heath shrink tubing
- [4x Dupont connector and crimping tool](https://a.co/d/8DN4Z0P)
- Electrical tape (preferably black)
- Electrical masking tape / Kapton tape to prevent shorts
- (optional) Hot glue
- Ability to follow written instructions and basic soldering
- About 15 minutes of time

### Step-by-step
1. Solder the 4 pieces of wire to one female JST-XH cable (the one that does not have pins sticking out). Make sure to protect the soldering with heat shrink tubing so it cannot short anything.

2. Put a protective cover over your work surface as there will be some dust coming out of your robot and you don't want that on your kitchen table. A piece of cardboard, plastic or tablecloth will do.

3. Remove the dustbin from the robot.

4. Turn the robot over, so you can see the bottom side of the robot, where the wheels are.

5. Remove the main brush cover by pulling upwards. If you have a side brush, you will need to pull that off too.

6. Remove the main brush.

7. Remove the bumper by pulling it off.

8. Remove the 2 Philips screws marked yellow in the image below and open the battery compartment. Remove the battery and leave it unplugged into told to plug it back in.

9. Remove the 6 Torx screws red marked in the image below. You will need a long T10 Torx bit for that.
![Neato robot on its back. Screws to remove are marked](pics/installs/jay/1-removing-screws.jpg "Remove these screws")

10. Turn the robot back over so you can see space where the dust bin normally sits.

11. Remove two more torx screws as indicated in the image below.

![Neato robot normals ide up. Screws to remove are marked](pics/installs/jay/1a-removing-two-more-screws.jpg "Remove two more screws")

12. Pull of the top cover by pushing the two tabs at the front out of the way.

13. Double check again that you've removed the battery before continuing. There should be no LEDs on at this point.

14. Install the JST-XH cable on the connector on the front-left of the board and then run the wire up tightly across the board, under some other wires, to the right of the board.
![Close-up of Neato board with JST-XH connector and wire installed](pics/installs/jay/2-install-JST-XH.jpg "Installing the JST-XH cable")

15. Find a place for your ESP. It normally fits in the space to the right of the main board.

16. Run the wires up/under existing wires as needed so they don't stick out. It's ok to cut extra wire.

17. Add Dupont connectors to the four wires.

18. Connect the wires to the ESP, making sure you make the right connections. From left to right looking at the front of the board the wires need to be connected this way:

    | Robot | ESP |
    |---|---|
    |RX|TX|
    |3.3V|VCC / 3.3V|
    |TX|RX|
    |GND|GND|

    *Note that depending on your exact board type you might have more or less choice in which connections you use for TX/RX. One confirmed set of connections is GPIO22 for TX and GPIO21 for RX on a ESP32 D1 Mini.*

    ![Neato board with serial connections indicated](pics/installs/jay/3-connections.jpg "Making the connections to the ESP")

19. Wrap your ESP in masking tape / Kapton tape to prevent shorts. Also make sure to secure the connections to the ESP as there will be a lot of vibration. Either include them in the tape wrap or use some hot glue.
![ESP installed and taped](pics/installs/jay/4-installed-and-taped.jpg "Installing and taping the ESP")

20. Use some electrical tape on the Neato enclosure across the JST-XH cable wires to secure them.
![Closeup of JST-XH cable with electrical tape on plastic enclosure](pics/installs/jay/5-electrical-tape-1.jpg "Securing JST-XH cable")

21. Put back the top cover. Don't turn Neato over just yet.

22. Add another round of electrical tape to further secure the JST-XH cable.
![Closeup of Neato with electrical tape on plastic enclosure](pics/installs/jay/6-electrical-tape-2.jpg "Securing JST-XH cable once more")

23. Put back the two screws you removed earlier.

24. Now, turn Neato back over and put back the 6 Torx screws your removed from the bottom.

25. Reconnect battery and close battery compartment.

26. Turn Neato on and enjoy!


### Bending pins (not recommended)
You could, instead of using an JST-XH connector bend the debug pins to allow for dupont connectors to connect.

![bent-pins-dupont](./pics/installs/tom/bend-pins.png)

Bending the pins you risk breaking the board, so this method should be avoided.


## Externally

My initial external install was with the ESP on the back of robot, however after running a couple of cleanings, it became clear this was not a good way. I have since then found a new way that I will detail here; it works a lot better, however the first steps are the same.

### Prerequisites



### Step-by-step
### 0. Make sure your ESP device fits in the handle area of the robot!

### 1. Turn the robot over, so you can see the bottom side of the robot, where the wheels are.

### 2. Remove the main brush cover by pulling upwards. If you have a side brush, you will need to pull that off too.

### 3. Remove the main brush.

### 4. Remove the bumper by pulling it off.

### 5. Drill a hole in the bumper

Bumber front | Bumber back
:-------------------------:|:-------------------------:
![bumper-front](./pics/d3/bumper-front.jpg) | ![bumper-back](./pics/d3/bumper-back.jpg)


Debug port | Debug port with bumber 
:-------------------------:|:-------------------------:
![debug-port](./pics/d3/debug-port.jpg) |  ![bumper-with-hole](./pics/d3/bumper-with-hole.jpg)


### 6. Route the JST-XH thour the hole and connect them to the debug port
![Route the JST-XH throuhg bumper](pics/installs/6_cable-in-bumper.jpg)


### 7. Plug the JST-XH connector into the debug port
![Plug the JST-XH connector into the debug port](pics/installs/7_plug-cable-in.jpg)

Now you will need to make sure the cable is pushed as far in as possible, the connector might get stuck on the plastic of the body, you will need to "wiggle" and push on each side of the connector

When you plug it in it might feel like it stops after a little while, but the top part catches the connector, keep pushing | It should be pushed this far back, make sure to be careful, you don't want to break anything!
:-------------------------:|:-------------------------:
![not connected to debug port](pics/installs/7_not-connected.jpg) | ![connected to debug port](pics/installs/7_connected.jpg)

As written before, this type of connector just fits, I needed to press on each side of the connector a little bit at a time, that way it went in correctly, it should be about as deep as shown here | How far back the connector should be pushed with a ruler in **cm**
:-------------------------:|:-------------------------:
![not connected to debug port](pics/installs/7_how-far-to-push.jpg) | ![connected to debug port](pics/installs/7_connector-with-ruler.jpg)


### 8. Put the bumper back on and make sure the cable is out

Make sure the cables come out like this | The cables should reach the handle like this
:-------------------------:|:-------------------------:
![not connected to debug port](pics/installs/8_cables-via-bumper.jpg) | ![connected to debug port](pics/installs/8_cables-to-handle.jpg)

### 9. Connect (and bend the pins) the ESP device to the robot
Depedning on how your ESP device looks like, you may need, like me, to bend the pins to fit it in a better way, it is to make sure the cables don't interfere with the lidar.

Place your ESP device down | Connect dupont cables to the pins you want to bend | Bend the pins out towards the side like this, don't use too much force!
:-------------------------:|:-------------------------:|:-------------------------:
![bend step 1](pics/installs/9_bend-1.jpg) | ![bend step 2](pics/installs/9_bend-2.jpg) | ![bend step 3](pics/installs/9_bend-3.jpg)

Now you need to connect the cables from the debug port to the ESP device

Based on above, on my ESP device with this adapter cable, I needed to connect like this | Put some hot glue on the connections to make sure they are not going anywhere
:-------------------------:|:-------------------------:
![bend step 1](pics/installs/9_connected.jpg)  | ![bend step 1](pics/installs/9_connected-hot-glue.jpg)


### 10. Secure the ESP in the handle area
You should now have your ESP device connected to the robot like this | Place the ESP device like this; MAKE SURE YOU CAN CLOSE THE DUST BIN!!
:-------------------------:|:-------------------------:
![secure step 1](pics/installs/10_step-1.jpg)  | ![secure step 2](pics/installs/10_step-2.jpg)  

Put some tape on the cables, hole and ESP device to keep them in place| Put more tape over the ESP device to secure it and avoid shorts. You can also like me put a dot of hot glue
:-------------------------:|:-------------------------:
![secure step 3](pics/installs/10_step-3.jpg)  | ![secure step 4](pics/installs/10_step-4.jpg)  

Cover all cable but a little piece (needed for the bumper action to work) with tape to avoid it getting cought on anything.

![Installed externally](./pics/installs/external.jpg)

### 11. You have now installed the ESP device on your robot!