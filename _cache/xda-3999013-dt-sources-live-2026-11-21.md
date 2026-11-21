Home
Forums
Devices
Guides
What's new
Log in
Register
New posts
 
Manufacturers
 
What's new
 
Members
TOPICS
Hot Deals
3D Printing
Android Auto
Android Mods
Android TV
Apps & Games
Themes
Wear OS
Smartwatches
Windows 11
XDA Computing
Terms and rules Privacy 
[RESOURCES] Device tree for redme note 8 pro
 
Thread starter
LehKeda  
Start date
Nov 7, 2019
Forums
Xiaomi
Redmi Note 8 Pro
Redmi Note 8 Pro ROMs, Kernels, Recoveries, & Othe
1
	
2
Next
LehKeda
Senior Member
Jan 26, 2014
768
672
My little cave
Samsung Galaxy Note II
Samsung Galaxy Star
Nov 7, 2019
#1
Hello everyone,
I've made an initial device tree for this device. This tree is highly experimental and the system image resulting from this tree is not guaranteed to boot.

you can find the device tree here ==> https://github.com/Lehkeda/android_device_xiaomi_begonia
you will find a branch for lineage 16 and TWRP version 3.3.1-0
the kernel in this tree is from the global rom V10.4.2.0.PGGMIXM https://bigota.d.miui.com/V10.4.2.0...XM_20191024.0000.00_9.0_global_270117fdb2.tgz

For now, I've managed to build the boot image and TWRP recovery(I need testers for the recovery).
you can find the recovery here ==> https://androidfilehost.com/?fid=4349826312261622208.
flash it at your own risk!!! but before flashing it, make sure you know what you're doing and make sure you know how to restore original recovery if this one doesn't work. to flash it, decompress it then flash it using fastboot.

Any pull requests are more than welcome so feel free to make any pull request or send me your changes!
 
Last edited: Nov 7, 2019
 
Reactions:
Photopuppet, gsser, FrOz3NKu$h and 19 others
F
Foreal_Bruh
Member
May 12, 2019
45
15
Nov 7, 2019
#2
Good job mate
 
M
mub19
Member
Nov 8, 2019
14
0
Nov 8, 2019
#3
keep it up, please
unfortunately I am noob
and can not test 
 
A
Adlon
Member
Jul 3, 2013
16
4
Nov 9, 2019
#4
hi guys,
i need your help please.
have a redmi note 8 pro global, unlocked. after i flashed this recovery i can not turn on my device, only blackscreen and on pc it didnt recornize.
can anyone help please
 
 
Reactions:
danonaba
X
Xakep1993
Member
Oct 3, 2016
27
10
33
Rtishevo
4pda.ru
Nov 9, 2019
#5
https://xdaforums.com/redmi-note-8-pro/how-to/guide-unbrick-stuck-da-mode-authorised-t4000433
 
 
Reactions:
danonaba
F
Fiuva
New member
Nov 9, 2019
1
0
Nov 9, 2019
#6
Can I change my China ROM (MIUI 11.0.1) to global rom?
 
M
mcarden2006
Senior Member
Sep 16, 2011
191
58
Nov 10, 2019
#7
I definitely want to try this but I have this stupid 168 hour wait period for bootloader unlock.
 
 
Reactions:
Nimone and danonaba
M
marc2800
Senior Member
May 26, 2014
81
12
Nov 27, 2019
#8
Is dev still ongoing ?
 
V
Vamsie Somayajula
New member
May 13, 2016
4
0
Samsung Galaxy A50
Nov 30, 2019
#9
I'm familiar to flashing roms and all. So is there a way to test lineage os on redmi note 8 pro right now?
 
Z
Zukian
Member
Aug 29, 2017
33
2
Dec 2, 2019
#10
Vamsie Somayajula said:
I'm familiar to flashing roms and all. So is there a way to test lineage os on redmi note 8 pro right now?

No right now.
 
KonahZave
Senior Member
Sep 1, 2019
64
8
Kokkola
Dec 31, 2019
#11
Adlon said:
hi guys,
i need your help please.
have a redmi note 8 pro global, unlocked. after i flashed this recovery i can not turn on my device, only blackscreen and on pc it didnt recornize.
can anyone help please

You bricked, will need authorized account.
 
A
activatorwmw
New member
Jan 9, 2020
2
0
Jan 9, 2020
#12
efuseMt6785.xml

Hi! Can anybody help me and give efuseMt6785.xml file for SDA tool?
rgds
 
G
girishjangir7
Senior Member
Jun 28, 2017
146
77
Bengaluru
Jan 11, 2020
#13
activatorwmw said:
Hi! Can anybody help me and give efuseMt6785.xml file for SDA tool?
rgds
I hope you know what u doing and succeed:fingers-crossed:
 
D
DarkMode101
Member
Aug 30, 2019
18
2
Jan 14, 2020
#14
Adlon said:
hi guys,
i need your help please.
have a redmi note 8 pro global, unlocked. after i flashed this recovery i can not turn on my device, only blackscreen and on pc it didnt recornize.
can anyone help please

bricked.. you need to flash the factory image or the image that your device has right now and you will need some authorised mi account
 
A
ariber14
Senior Member
Feb 7, 2018
144
42
Redmi Note 8 Pro
Jan 14, 2020
#15
Adlon said:
hi guys,
i need your help please.
have a redmi note 8 pro global, unlocked. after i flashed this recovery i can not turn on my device, only blackscreen and on pc it didnt recornize.
can anyone help please

There are people saying they managed to flash stock rom without authorized account.search online and on telegram at the redminote8pro group. and let us know when you succeed.regards
 
G
gopikrishnanrmg
Senior Member
Jan 17, 2020
70
52
Jan 19, 2020
#16
Adlon said:
hi guys,
i need your help please.
have a redmi note 8 pro global, unlocked. after i flashed this recovery i can not turn on my device, only blackscreen and on pc it didnt recornize.
can anyone help please

Can you boot into recovery at least?
If yes flash the latest zip from below, it may help
Please try

http://c.mi.com/in/miuidownload/detail?device=1900375

---------- Post added at 10:18 AM ---------- Previous post was at 10:16 AM ----------


KonahZave said:
You bricked, will need authorized account.

But how can he unlock the bootloader without authorized account? The account should be authorized... Unless he resorted to some unofficial method....
 
KonahZave
Senior Member
Sep 1, 2019
64
8
Kokkola
Jan 19, 2020
#17
SP Flash


gopikrishnanrmg said:
Can you boot into recovery at least?
If yes flash the latest zip from below, it may help
Please try

http://c.mi.com/in/miuidownload/detail?device=1900375

---------- Post added at 10:18 AM ---------- Previous post was at 10:16 AM ----------



But how can he unlock the bootloader without authorized account? The account should be authorized... Unless he resorted to some unofficial method....
Click to expand...
SP Flash doesnt need bootloader unlocked I guess.
 
L
L1nx99
Member
Apr 28, 2018
36
5
Samsung Galaxy S6 Edge
Feb 5, 2020
#18
What about los
 
V
Varshank Dhiman
Senior Member
Aug 2, 2015
121
224
New Delhi
Feb 13, 2020
#19
when will i get rom

when will i get rom
 
U
ulkika
Senior Member
Apr 15, 2010
399
74
USA
Feb 13, 2020
#20
LahKeda said:
Hello everyone,
I've made an initial device tree for this device. This tree is highly experimental and the system image resulting from this tree is not guaranteed to boot.

you can find the device tree here ==> https://github.com/Lehkeda/android_device_xiaomi_begonia
you will find a branch for lineage 16 and TWRP version 3.3.1-0
the kernel in this tree is from the global rom V10.4.2.0.PGGMIXM https://bigota.d.miui.com/V10.4.2.0...XM_20191024.0000.00_9.0_global_270117fdb2.tgz

For now, I've managed to build the boot image and TWRP recovery(I need testers for the recovery).
you can find the recovery here ==> https://androidfilehost.com/?fid=4349826312261622208.
flash it at your own risk!!! but before flashing it, make sure you know what you're doing and make sure you know how to restore original recovery if this one doesn't work. to flash it, decompress it then flash it using fastboot.

Any pull requests are more than welcome so feel free to make any pull request or send me your changes!
Click to expand...


just to understand also why for me this device is to be discovered,
I would like to understand if the fact that within the folder dedicated to the Note 8 Pro there are only the recovery indicates that the work for the new Roma related to this mobile phone still needs to be done or if you can possibly rely on the work done for the Note 8 normal thing that frankly seems strange to me Considering that however the Note 8 Pro mounts a more different CPU.
In addition, I also wanted to understand something else they told me about a poor camera or at least a poor camera compartment in comparison between the stock and the TR cam in order to install the latter it is necessary to have root permissions or I can install it normally?
Sorry for macaronic english but i'm using the google translator so be patient!
 
1
	
2
Next
You must log in or register to reply here.
Share:
Facebook
Twitter
Reddit
WhatsApp
Email
Link
Similar threads
	
[Firmware] Xiaomi Redmi Note 8 Pro [begonia] [Auto updated daily!]
yshalsager May 8, 2020 6 7 8
	
Replies 145
Views 77K
	
J
	Oct 3, 2022
jhay006
	
[KERNEL] [Begonia] HYDRA KERNEL REDMI NOTE 8 PRO [AOSP] [MIUI]
ishitachakraborty22 Nov 26, 2022 2
	
Replies 30
Views 39K
	
	Jun 19, 2026
Knightisbrave
	
[RECOVERY][CFW][3.3.1-0][begonia]Unofficial TWRP recovery for begonia(in) [05/06]
Agent_fabulous Nov 13, 2019 7 8 9
	
Replies 178
Views 106K
	
J
	Jun 28, 2026
Jilomanking
	
[ROM] [NONCFW] [12.1] [BEGONIA/BEGONIAIN] PixelPlusUI v4.5 | Xiaomi Redmi Note 8 Pro [OFFICIAL] [AOSP]
7Soldier Mar 17, 2022 2 3 4
	
Replies 68
Views 44K
	
	Dec 27, 2022
HLP Mr. Lin Yu
	
[UNOFFICIAL][RECOVERY][UNIFIED][begonia/begoniain] OrangeFox Recovery Project [R11.1]
Sahil_Sonar Nov 16, 2019 8 9 10
	
Replies 190
Views 97K
	
S
	Jul 26, 2024
sebe131313
Forums
Xiaomi
Redmi Note 8 Pro
Redmi Note 8 Pro ROMs, Kernels, Recoveries, & Othe
TOP LIKED POSTS
24 Hours All time
22
LehKeda
Hello everyone,
I've made an initial device tree for this device. This tree is highly experimental and the system image resulting from this tree is not guaranteed to boot.

you can find the device tree here ==> https://github.com/Lehkeda/android_device_xiaomi_begonia
you will find a branch for lineage 16 and TWRP version 3.3.1-0
the kernel in this tree is from the global rom V10.4.2.0.PGGMIXM https://bigota.d.miui.com/V10.4.2.0...XM_20191024.0000.00_9.0_global_270117fdb2.tgz

For now, I've managed to build the boot image and TWRP recovery(I need testers for the recovery).
you can find the recovery here ==> https://androidfilehost.com/?fid=4349826312261622208.
flash it at your own risk!!! but before flashing it, make sure you know what you're doing and make sure you know how to restore original recovery if this one doesn't work. to flash it, decompress it then flash it using fastboot.

Any pull requests are more than welcome so feel free to make any pull request or send me your changes!
Nov 7, 2019
View
2
M
mcarden2006
I definitely want to try this but I have this stupid 168 hour wait period for bootloader unlock.
Nov 10, 2019
View
1
A
Adlon
hi guys,
i need your help please.
have a redmi note 8 pro global, unlocked. after i flashed this recovery i can not turn on my device, only blackscreen and on pc it didnt recornize.
can anyone help please
Nov 9, 2019
View
1
X
Xakep1993
https://xdaforums.com/redmi-note-8-pro/how-to/guide-unbrick-stuck-da-mode-authorised-t4000433
Nov 9, 2019
View
NEW POSTS
K
[ROM][13.0][ LineageOS 20 - Huawei MediaPad M3 8.4 (Beethoven) ][ Update 23/06/2026 ]
Latest: Kosta2k9 A moment ago
Huawei Mediapad M3 ROMs, Kernels, Recoveries, & Ot
[ANDROID 9.0+] How to install LineageOS 17 Treble on SM-J330FN and other Exynos 7570 devices
Latest: fixisunreal A moment ago
Samsung Galaxy J3 (2017) ROMs, Kernels, Recoveries
M
Question What Should Developers Consider When Integrating UAE Pass into Android Apps?
Latest: mrymg 2 minutes ago
General Questions and Answers
[ROM][17][OFFICIAL] LineageOS 24.0 for Amazon Fire Max 11 [sunstone]
Latest: janma8 2 minutes ago
Fire HD 8 and HD 10 Original Android Development
[MODULE] Play Integrity Fork (PIFork)
Latest: zgfg 2 minutes ago
Magisk

XDA Developers was founded by developers, for developers. It is now a valuable resource for people who want to make the most of their mobile devices, from customizing the look and feel to adding new functionality.

Crafted by Audentio
MORE INFO
Contact Us (Forum Issues)
Advertise
Terms and rules
Suggest Content
USEFUL LINKS
Best Phones
Tutorials
Recognized Developer Program
Recognized Themer / Contributor Program
Admin & Moderators
Delete XDA Forums Account
XDA - Dark