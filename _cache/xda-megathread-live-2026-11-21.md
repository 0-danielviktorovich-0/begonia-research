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
[GUIDE][INFO][PSA] Redmi Note 8 Pro - Megathread + CFW
 
Thread starter
Agent_fabulous  
Start date
Feb 24, 2020
Forums
Xiaomi
Redmi Note 8 Pro
Redmi Note 8 Pro Guides, News, & Discussion
1
	
2
	
3
	
…
	
39
Next
Agent_fabulous
Retired Recognized Developer
Apr 24, 2014
496
5,203
Bangalore
Feb 24, 2020
#1
Redmi Note 8 Pro - The Megathread​

Background
Xiaomi sent many of us the Redmi Note 8 Pro (Indian variant - begoniain) back in November 2019. Development started out great, but came to an abrupt halt, when at one point all of us were bricked. A little bit of caution and a bit more of tinkering, and we're back!
Long story short, yes this device does brick, and yes there IS a method to avoid it! I request you to take out some time and read the entire post, before you proceed. Following instructions is crucial, if you want to save yourself trips to the service center.

begonia? begoniain? what's happening?
There are 2 variants of the Redmi Note 8 Pro. "begonia" is the global variant whereas "begoniain" is the Indian variant. The only difference between the 2 is NFC. The Indian Variant has no NFC. And no, it's not as if it's disabled, the hardware is just not present. The TWRP and ROM builds target both, so you do not have to worry about a thing. Irrespective of where you bought the phone, all custom software is the same, and will run on both variants.

Unlocking the bootloader and gaining root
This has been covered by other threads in the past, so I won't dive into too much detail here. You need to unlock your device using the Unlock Tool that Xiaomi provides and wait for almost a week (168 hours) to gain unlock permissions. There's no way to get around this. Please follow any other guides for installing a recovery, flashing Magisk, disabling AVB and booting up.

Custom ROMs and bricking
Regarding bricks, yes this device will get bricked if you do stupid things or don't follow instructions. Feel free to ask if you ever have a doubt. Do NOT spam on ROM threads. Ask here, and use search before you do. Chances are, someone has asked the same thing in the past.

Now, doing things like:
- Tripping AVB
- Flashing an incompatible boot and dtbo
- Flashing a weird boot image
- ???
will result in a brick. You won't have fastboot, you won't have anything in such cases. Only Boot ROM download mode, which requires a Mi Authorized Account. In such cases, you will need to visit a service center.

PLEASE NOTE: I do NOT recommend online services that promise to unbrick your device. Not only are they highly overpriced, but could result in you getting scammed, or have your data stolen. If you have a Mi Authorized Account and are willing to help us out, feel free to PM me. Any online service ads for the same will NOT be entertained.

Now, there is a way to prevent bricks entirely. However, it does not work with the MIUI 11 Android 10 China build that surfaced a few months ago. The factory firmware for begonia was leaked, @Xakep1993 discovered that the factory had a lot of security checks disabled, and compiled in engineering mode.

Before we go any further, know that there is no way for you to unbrick a phone that's already bricked and is running the MIUI preloader. (Visit a Service Center in such a case) The following applies only to devices that are in a good, working state and will prevent bricks.

Okay so how does that help?
Glad you asked. Every MediaTek device has 2 download connections. Boot ROM (aka BROM) and Preloader. Boot ROM is burnt onto the SoC and is the first program to run. Preloader is loaded after. Boot ROM implements security measures against attacks, which includes flashing improper or malicious firmwares. This is "SLA" and "DAA", that is "Serial Link Authentication" or "Download Agent Authentication". This happens server side and requires the Mi Authorized Account, that only service centers have.

What's so different with this firmware?
Preloader runs after BROM, and does not require any security verification to write partitions. MIUI's preloader has download disabled. When you brick, you have Preloader starting and rebooting constantly. (And holding volume up gets you to BROM download). There's no way to talk to the MIUI Preloader. The Factory Preloader on the other hand, has download enabled. So, if something goes wrong, as long as the Factory Preloader is present you CAN unbrick!

How to install it?
If you are on MIUI 11 - Android 10, you WILL need to downgrade to Android 9! This method will not work if you're on Android 10. Use MiFlashPro or fastboot to flash all partitions to a compatible MIUI 10 or 11 Android 9 build.
I will add a zip that can be flashed from TWRP, soon. Until then, you can flash it via Fastboot.
1. Download preloader_begonia.bin and lk.img from attachments
2. Execute

Code:
fastboot flash preloader preloader_begonia.bin
fastboot flash lk lk.img
fastboot flash lk2 lk.img
(LK = Little Kernel = Bootloader)
You can now use SP Flash Tools to restore your "bricked" phone!
This will also make the bootloader append certain debug flags to the kernel cmdline. So you may see some interesting behavior while Android is running! 
You can find the full factory build here. This is a barebones MTK-Android build. We don't recommend using it xD

Where are my Custom ROMs? ETA PL0Z BRO!!!
They're almost ready now, you should see threads popping up in a few more days.

Okay, thanks for the "anti-brick" factory preloader! I'm gonna flash another MIUI build!
Hol' up, fam. You need to check whether the MIUI OTA you're installing contains Preloader and LK or not. If it does, remove it manually. Another method could be to install the OTA and then flash the factory Preloader and LK image again via fastboot.

Flashing ROMs
Once ROMs are out, the install process is very simple and much like any other device:
- Download ZIP
- Push ZIP to device
- Flash using TWRP
- Install GApps (optional)
- Reboot
- Profit!

Unbricking
Assuming you have the factory preloader installed,
- Disconnect device from PC if connected
- Load SP Flash tool
- Load firmware of choice
- Press download, SP Flash tool will now wait for the device
- Connect device and don't hold any keys
- If the device doesn't detect, hold power for a 8-10 seconds
- It should start flashing right away without any authorization prompt!

Building ROMs (Developers only)
Things are still under development. Things may be broken, may or may not boot at all. Current code can be found below:
Device Tree - branch android-10
Vendor Tree - branch android-10
Kernel - branch master
DTBO Patch
Info about the patch: many partitions of the device (including DTBO) are signed using private keys. We don't have access to these keys, and thus our generated dtbo images don't boot. I managed to strip out the certs, write a simple Python script and write custom dtbo generation rules that append the required certs.

Things may be missing here, more information will be added as necessary 

XDA:DevDB Information
The go-to modding guide for the Redmi Note 8 Pro (begonia/begoniain), ROM for the Redmi Note 8 Pro

Contributors
Agent_fabulous
ROM OS Version: Android 10
ROM Kernel: Linux 4.x

Version Information
Status: Testing

Created 2020-02-24
Last Updated 2020-10-26
 
Attachments
photo_2020-02-23_16-20-30.jpg
159.6 KB · Views: 24,372
preloader_begonia.bin
318.6 KB · Views: 3,749
lk.img
1.4 MB · Views: 3,338
Last edited: Dec 23, 2020
 
Reactions:
morfikov, shayanjojo123, ttrublu and 121 others
Agent_fabulous
Retired Recognized Developer
Apr 24, 2014
496
5,203
Bangalore
Feb 24, 2020
#2
CFW and CFW builds and recoveries


CFW​
[SIZE="+1"]What is a CFW?[/SIZE]
The A10 Custom Firmware, or CFW for short, is a combination of multiple Xiaomi firmware packages.

[SIZE="+1"]Why do I need it?[/SIZE]
You are probably aware of the leaked factory firmware for the Redmi Note 8 Pro. This firmware contains a preloader which was compiled with the download code.
Since the preloader does not need to setup platform security it allows us to unbrick without an authorized account.
Unfortunately, the MIUI bootloader do not run on the factory preloader - only the factory bootloader does, which works just fine with A9 kernels.
Furthermore, the A10 kernel source released by Xiaomi does not work with the factory bootloader/preloader, which was the reason I worked on a new kernel source based on Android 9 (A9) with several Android 10 (A10) drivers to work nicely with the A10 blobs.
In short, the CFW enables you to use the new builds without worrying about bricks while running newer proprietary vendor software.

[SIZE="+1"]What's special about the new builds?[/SIZE]
New builds, tagged "[CFW]", come with their own vendor images. These builds are unified for all variants of the Redmi Note 8 Pro and have pretty much all issues fixed at this point. They ship with the new modified A10 kernel I mentioned earlier.
NOTE: While the builds are unified, the CFW is not. Please flash the correct version of CFW, for your variant
While flashing the wrong CFW is not catastrophic, it may lead to issues such as poor reception.

[SIZE="+1"]What really is inside this CFW?[/SIZE]
The CFW contains firmware files from the latest A9 and latest A10 firmware image. Along with this, the CFW also installs the factory preloader and bootloader (LK) to make sure you're safe when modifying your device.

[SIZE="+1"]How do I install the CFW and builds?[/SIZE]
CFW is a recovery-flashable package. You WILL HAVE TO downgrade to MIUI A9 to flash this since there are no recoveries which work nicely with MIUI A10.
Even though the CFW does install factory preloader and LK, I do highly recommend flashing preloader and LK from fastboot first and then the CFW.
Once you are sure you are running the CFW, simply flash a CFW compatible build. You may also need to update your recovery after installing CFW. See next post for full step-by-step instructions.

[SIZE="+1"]Recoveries? How do those work with CFW?[/SIZE]
Since recovery images also contain their own kernel, there are also CFW compatible recovery images. After installing a CFW, reboot to fastboot and flash any CFW enabled recovery image.
Trying to run a non-CFW recovery on CFW will make it reboot to system or recovery itself after a few seconds of entering recovery. Should you find yourself in a situation like this: as soon as recovery loads, hit [reboot] > [bootloader]. If you cannot do this, flash the new recovery image from SP Flash tools (or wait for your device to drain it's battery out )
See next post for full step-by-step instructions.

[SIZE="+1"]Do I need to flash the CFW everytime?[/SIZE]
Nope. If you flashed CFW once, you're good. Just make sure the ROM you're flashing does not install any firmware images. Ask your ROM developer before installing a zip.
ALL MIUI ZIPS CONTAIN FIRMWARE IMAGES. DO NOT FLASH ON TOP OF CFW

[SIZE="+1"]I'm on CFW and rocking a custom ROM. How do I go back to MIUI?[/SIZE]
Flash a full MIUI Fastboot ROM, or use SP Flash tools to install the flash all MIUI partitions. Again, do not flash a recovery package for switching to MIUI.
See next post for full step-by-step instructions.

[SIZE="+1"]What would happen if I install a non-CFW build on CFW?[/SIZE]
Again, nothing catastrophic. It'll make the device reboot itself a few seconds into the bootanimation. All current non-CFW builds run the A9 kernel code. The new kernel is based on the A9 kernel code as well; some drivers just don't like the new firmware images included in the CFW So, save yourself the trouble and check what you're installing. CFW supported builds are listed in the next post.

[SIZE="+1"]Where can I download the CFW?[/SIZE]
Please see the next post, below.

While the whole CFW thing may seem a bit overwhelming to some, remember, it's something to protect your device in the long run! Take out a few minutes and please read through this post properly.
 
Last edited: Jun 5, 2020
 
Reactions:
verdugon, ttrublu, Dainslef.Tei and 34 others
Agent_fabulous
Retired Recognized Developer
Apr 24, 2014
496
5,203
Bangalore
Feb 24, 2020
#3
Reserved

CFW Migration Steps

Coming from MIUI
Method 1
- Downgrade to MIUI Android 9 if not already, or try using Method 2
- Flash preloader and lk as mentioned in first post
- Flash any non-CFW Android 9 recovery
- Boot into recovery
- Wipe system, cache, dalvik
- Flash CFW, CFW compatible ROM (flash GApps mods later!  )
- Format data (not wipe, select "Format Data", you'll lose all userdata)
- Reboot to bootloader
- Flash CFW recovery
- Reboot! You're now on CFW!

Method 2 Try at own risk!*
- Flash a non-CFW A10 recovery from fastboot (such as LR TWRP for MIUI A10)
- Boot directly into recovery by holding [Volume +] after flashing and rebooting
- (Optional) For safety sake, select Advanced option "Close AVB 2.0"
- Take a full nandroid backup (IMPORTANT! Will be helpful if lost IMEI)
- Turn off "Reboot after installing ROM" from TWRP settings
- Wipe system, dalvik and cache
- Flash CFW and a CFW compatible ROM (flash GApps and mods later!  )
- Format data (not wipe, select "Format Data", you'll lose all userdata)
- Reboot to bootloader from the Reboot menu
- Flash CFW recovery
- Reboot! You're now on CFW!
*NOTE: This method has worked for each everyone who has tried it and followed correctly, so far. The idea for this method was mine, but I personally have not tried it myself. It will particularly be useful if you're using MIUI A10 and are on a limited data plan 

Coming from non-CFW Custom ROMs
- Make sure preloader and LK are installed (see first post)
- Boot into recovery
- Wipe system, cache, dalvik
- Flash CFW, CFW compatible ROM (flash GApps here if necessary, flash any extra mods later!  )
- Format data (not wipe, select "Format Data", you'll lose all userdata)
- Reboot to bootloader
- Flash CFW recovery

Updating CFW-enabled builds on CFW
Since you're already on CFW, just install the update and reboot like any other device:
- Remove lockscreen if any
- Reboot to recovery
- Wipe data, system, cache, dalvik
- Flash ROM (+ GApps if necessary)
- Reboot!

Going back to MIUI from CFW
- Flash full MIUI firmware from SP Flash Tools or fastboot 

Android 11
Changes
- Update to MIUI 12 blobs and fw images
- Prebuilt vendor image for A11
- Fully enforced and vendor isolation enabled

Coming from A10 CFW
- Flash "CFWv3+vendor" package followed by the ROM.
Note: You don't need to flash the "CFWv3+vendor" package more than once when switching to other A11 ROMs, unless you have gone back to A10.

Coming from MIUI
- Follow instructions above to CFW, just use A11 CFW and A11 ROM instead

Going back to A10 CFW
- Flash CFWv2 along with your A10 ROM.

Going back to MIUI
- Fastboot flash full MIUI ROM

Note 1: Do not wipe vendor on A11. If you do, you'll have to reflash the "CFWv3+vendor" package to have a functional device.

Note 2: On VNDK30 A11 builds, you may wipe vendor, since the builds ship with a vendor image. 

CFW Downloads
Android 11 (CFWv4) For VNDK-30 builds only! (is the same as CFWv2.1, but version changed to avoid confusion )
- begoniain: https://sourceforge.net/projects/begonia-oss/files/CFW/begoniain-A11-CFW_20210105.zip/download
- begonia: https://sourceforge.net/projects/begonia-oss/files/CFW/begonia-A11-CFW_20210105.zip/download
Android 11 (CFWv3+vendor)
- begoniain: https://sourceforge.net/projects/be...egoniain-A11-CFW-vendor-20201026.zip/download
- begonia: https://sourceforge.net/projects/begonia-oss/files/CFW/begonia-A11-CFW-vendor-20201026.zip/download
Android 10 (CFWv2)
- begoniain: https://sourceforge.net/projects/begonia-oss/files/CFW/begoniain-A10-CFW_20200823.zip/download
- begonia: https://sourceforge.net/projects/begonia-oss/files/CFW/begonia-A10-CFW_20200823.zip/download

CFW Supported Recoveries
- Unofficial TWRP
- Anything else marked with "[CFW]"

CFW Supported ROMs and kernels
- Pretty much everything active, at this point lol

The latest non-CFW Unofficial TWRP can be found on AFH, on my thread (see last line on post) and in the Telegram group as note "#twrp-non-cfw-for-roms"

Troubleshooting
IMEI lost (requires full TWRP backup of MIUI when IMEI was present!):
From a full TWRP backup, restore the following partitions:
- nvcfg
- nvdata
- nvram
- persist
- protect_f
- protect_s
Reboot and check! IMEI should be back :highfive:

ROM Reboots to recovery after boot logo (no bootanimation):
Usually, this indicates that the device isn't able to setup encryption. You'll also see randomly named files and folders in TWRP. In this case, just Format Data (not wipe), and reboot.

Rescuing the device:
Since CFW is always running factory preloader and bootloader (LK), you can use SP Flash in case something should go wrong.
Assuming you're stuck in some sort of loop/brick while on factory preloader/CFW, here are the EDL modes:
There are 2 modes of "EDL":
- Preloader: Factory preloader will always advertise a download mode when the device is starting, right before the Redmi logo (You may not get a logo if you're bricked, only a blinking LED). You do not need to hold ANY buttons. Just plug in the device and it'll show up on your computer periodically. Load any Android 9 firmware in SP Flash, uncheck preloader, lk and lk2, connect your device and hit Download in SP Flash.
- BootROM: If you don't have factory preloader, you will have to flash via BootROM. This requires an authorized account. Unless you have one yourself, you will need to head to a service center to get your device fixed. If you do need to load BootROM download, hit download in SP Flash with the Authorized Account logged in, hold volume up and plug in the device while holding the key. Release the key as soon as your computer recognizes it. SP Flash will start the download.
If you are able to enter this mode yourself, and the service center quotes something like a "motherboard replacement", show them this section of the post and tell them it's a software issue. Given the nature of such a new and unique device, often even the best make mistakes! If you're a XIaoMi Service Center and a customer has showed this to you, PLEASE try this. The phone will enter BootROM if you hold the keys at the correct time. You do not need to take the phone apart to short any pins. Just login and bind to your special account, hit "Download" in SP Flash and hold the keys for 5-15 seconds with the device plugged in. The software will recognize the device and start flashing.
If you as the technician are wondering why you should trust a random person on the internet, here's why: I received the device from XiaoMi India, as part of their developer program and have been reversing things on it for the past 6+ months. I have been through 3 hard-bricks and have helped multiple service centers diagnose the device correctly and having them fix my own device too.


 
Last edited: Jan 5, 2021
 
Reactions:
cevher62, ttrublu, Dainslef.Tei and 32 others
K
kamyk70
Senior Member
Aug 11, 2008
98
14
Feb 24, 2020
#4
Wow!!! Thanks man! Does it work with custom firmware such as xiaomi.eu or miuipro based on China builds?
 
X
Xakep1993
Member
Oct 3, 2016
27
10
33
Rtishevo
4pda.ru
Feb 24, 2020
#5
Nice! 
Remember only ANDROID 9 Rom !!
 
 
Reactions:
Agent_fabulous and polfrank
saurabhcharde
Senior Member
Apr 25, 2015
193
114
Feb 24, 2020
#6
DAMN!

P.S: Snapdragon ftw 
 
djzero86
Senior Member
Oct 26, 2011
286
98
San José
Redmi Note 10
Feb 24, 2020
#7
Oh thanks @Agent_fabulous you are the best
 
D
Deleted member 7257971
Guest
Feb 24, 2020
#8
Great thread
 
N
nwazie
Member
May 6, 2017
29
6
Feb 24, 2020
#9
Great thread. I'm super excited.
 
M
mad20012
Member
Nov 21, 2014
18
1
Feb 24, 2020
#10
I haven't flashed any thing on my phone before, can i flash this preloader??
 
soleali
Senior Member
Jan 19, 2013
183
27
Feb 24, 2020
#11
This thread explains greatly. Thanks!
 
A
ariber14
Senior Member
Feb 7, 2018
144
42
Redmi Note 8 Pro
Feb 24, 2020
#12
Great work!!!
 
 
Reactions:
milowysh
K
kitowsci
Member
Nov 2, 2013
6
0
Feb 24, 2020
#13
Is there a preloader for Xiaomi Redmi 6? It's also on the mediatek, but it has a different processor. Unfortunately, it's hard bricked
 
Danmann
Senior Member
Jan 11, 2015
487
125
pwoss.org
Feb 24, 2020
#14
Thank you for all the info and work!


1. Download preloader_begonia.bin and lk.img from attachments
2. Execute
Code:


Code:
fastboot flash preloader preloader_begonia.bin
fastboot flash lk lk.img
fastboot flash lk2 lk.img
Click to expand...


Just for clearrefining. Do we need to flash TWRP first? Or is it safer to use the factory firmware first?

Thanks
Dan
 
Cao Zihuan
Member
Aug 30, 2014
15
1
shenzhen
Feb 25, 2020
#15
Thank you very much, we are looking forward to more custom ROMs coming!
 
Helhound0
Senior Member
Nov 2, 2012
449
139
New South Wales
LG V60 ThinQ
Samsung Galaxy S26 Ultra / 26+ / 26
Feb 25, 2020
#16
Super excited.. We're going to be busy next week 
 
donkyshot
Senior Member
Dec 19, 2011
449
215
Redmi Note 8 Pro
Feb 25, 2020
#17
Great news. So if we remove lk.img, preloaded.img, preloader_emmc.img, preloader_ufs.img from (original) image / rom, we should be safe to flash without permanent brick right?
Looks like this is the good news we've all been waiting for.
 
Muad.Dib
Senior Member
Sep 3, 2015
251
66
Lenovo Thinkpad Tablet
Lenovo Yoga Tab 3 Plus
Feb 25, 2020
#18
Danmann said:
Just for clearrefining. Do we need to flash TWRP first? Or is it safer to use the factory firmware first?

Thanks
Dan

Greetings @Danmann.

From what I can read in the Original Post, quoted bellow for reference:


Agent_fabulous said:
[...]

Before we go any further, know that there is no way for you to unbrick a phone that's already bricked and is running the MIUI preloader. (Visit a Service Center in such a case) The following applies only to devices that are in a good, working state and will prevent bricks.


This thread/measures are therefore PREVENTIVE and certainly not CURATIVE.
Knowing probably 99% of people who bricked their devices did it trying to flash TWRP, I think it is safe to assume by all means, it is highly recommended to flash this BEFORE you attempt to flash TWRP.
That said I never had issue with the few releases of TWRP either from OP or LR team, but what I would do is probably first getting stock image of your current MIUI (NOTE: ANDROID 9 ONLY AS SAID BY OP) to get the original files you are about to replace just in case.
You still have to unlock your bootloader if not done already.
 
 
Reactions:
Agent_fabulous and polfrank
J
jumper047
Member
Feb 4, 2020
14
8
Feb 25, 2020
#19
First of all, hurray Agent and Xakep1993!!
Second. Feeling stupid, but I don't see any atachments to post:/.

Agent_fabulous said:
1. Download preloader_begonia.bin and lk.img from attachments
 
Muad.Dib
Senior Member
Sep 3, 2015
251
66
Lenovo Thinkpad Tablet
Lenovo Yoga Tab 3 Plus
Feb 25, 2020
#20
jumper047 said:
First of all, hurray Agent and Xakep1993!!
Second. Feeling stupid, but I don't see any atachments to post:/.

Just bellow the thread Tittle, you have a black bar with tabs you can click on. One of them being Download 

Don't feel stupid I was also feeling dumb yesterday before I found that bar lol 

Hope this helps.

Regards,
 
 
Reactions:
$Ayush$ and jumper047
1
	
2
	
3
	
…
	
39
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
	
Redmi Note 8 Pro Guide [Firmwares | ROOT CN/GLOBAL | TWRP Recovery]
madsponge26 Oct 20, 2019 13 14 15
	
Replies 285
Views 188K
	
	Jan 18, 2026
Ritesh123456
F
	
[RECOVERY][begonia][UNOFFICIAL] TWRP recovery for Redmi Note 8 Pro
fi4tch Sep 25, 2019 7 8 9
	
Replies 167
Views 96K
	
P
	Dec 23, 2025
polaknabat
	
[GUIDE] [begonia/begoniain] How to UNBRICK when stuck on preloader mode
polfrank Nov 9, 2019 16 17 18
	
Replies 359
Views 168K
	
	Jul 24, 2024
Kirasu2080
	
Full Guide on how to Unlock, Root, and flash GSI to Redmi Note 8 Pro
yayimathrowaway Jan 19, 2020 3 4 5
	
Replies 80
Views 55K
	
J
	Aug 18, 2021
Jeson Edward
	
[GUIDE][BEGONIA]Unlock Bootloader, Flash TWRP and Root[PROPER]
pritish1998 Nov 2, 2019 14 15 16
	
Replies 315
Views 135K
	
	Jul 18, 2024
GL1TCH2928
Forums
Xiaomi
Redmi Note 8 Pro
Redmi Note 8 Pro Guides, News, & Discussion
TOP LIKED POSTS
24 Hours All time
124
Agent_fabulous
Redmi Note 8 Pro - The Megathread​

Background
Xiaomi sent many of us the Redmi Note 8 Pro (Indian variant - begoniain) back in November 2019. Development started out great, but came to an abrupt halt, when at one point all of us were bricked. A little bit of caution and a bit more of tinkering, and we're back!
Long story short, yes this device does brick, and yes there IS a method to avoid it! I request you to take out some time and read the entire post, before you proceed. Following instructions is crucial, if you want to save yourself trips to the service center.

begonia? begoniain? what's happening?
There are 2 variants of the Redmi Note 8 Pro. "begonia" is the global variant whereas "begoniain" is the Indian variant. The only difference between the 2 is NFC. The Indian Variant has no NFC. And no, it's not as if it's disabled, the hardware is just not present. The TWRP and ROM builds target both, so you do not have to worry about a thing. Irrespective of where you bought the phone, all custom software is the same, and will run on both variants.

Unlocking the bootloader and gaining root
This has been covered by other threads in the past, so I won't dive into too much detail here. You need to unlock your device using the Unlock Tool that Xiaomi provides and wait for almost a week (168 hours) to gain unlock permissions. There's no way to get around this. Please follow any other guides for installing a recovery, flashing Magisk, disabling AVB and booting up.

Custom ROMs and bricking
Regarding bricks, yes this device will get bricked if you do stupid things or don't follow instructions. Feel free to ask if you ever have a doubt. Do NOT spam on ROM threads. Ask here, and use search before you do. Chances are, someone has asked the same thing in the past.

Now, doing things like:
- Tripping AVB
- Flashing an incompatible boot and dtbo
- Flashing a weird boot image
- ???
will result in a brick. You won't have fastboot, you won't have anything in such cases. Only Boot ROM download mode, which requires a Mi Authorized Account. In such cases, you will need to visit a service center.

PLEASE NOTE: I do NOT recommend online services that promise to unbrick your device. Not only are they highly overpriced, but could result in you getting scammed, or have your data stolen. If you have a Mi Authorized Account and are willing to help us out, feel free to PM me. Any online service ads for the same will NOT be entertained.

Now, there is a way to prevent bricks entirely. However, it does not work with the MIUI 11 Android 10 China build that surfaced a few months ago. The factory firmware for begonia was leaked, @Xakep1993 discovered that the factory had a lot of security checks disabled, and compiled in engineering mode.

Before we go any further, know that there is no way for you to unbrick a phone that's already bricked and is running the MIUI preloader. (Visit a Service Center in such a case) The following applies only to devices that are in a good, working state and will prevent bricks.

Okay so how does that help?
Glad you asked. Every MediaTek device has 2 download connections. Boot ROM (aka BROM) and Preloader. Boot ROM is burnt onto the SoC and is the first program to run. Preloader is loaded after. Boot ROM implements security measures against attacks, which includes flashing improper or malicious firmwares. This is "SLA" and "DAA", that is "Serial Link Authentication" or "Download Agent Authentication". This happens server side and requires the Mi Authorized Account, that only service centers have.

What's so different with this firmware?
Preloader runs after BROM, and does not require any security verification to write partitions. MIUI's preloader has download disabled. When you brick, you have Preloader starting and rebooting constantly. (And holding volume up gets you to BROM download). There's no way to talk to the MIUI Preloader. The Factory Preloader on the other hand, has download enabled. So, if something goes wrong, as long as the Factory Preloader is present you CAN unbrick!

How to install it?
If you are on MIUI 11 - Android 10, you WILL need to downgrade to Android 9! This method will not work if you're on Android 10. Use MiFlashPro or fastboot to flash all partitions to a compatible MIUI 10 or 11 Android 9 build.
I will add a zip that can be flashed from TWRP, soon. Until then, you can flash it via Fastboot.
1. Download preloader_begonia.bin and lk.img from attachments
2. Execute

Code:
fastboot flash preloader preloader_begonia.bin
fastboot flash lk lk.img
fastboot flash lk2 lk.img
(LK = Little Kernel = Bootloader)
You can now use SP Flash Tools to restore your "bricked" phone!
This will also make the bootloader append certain debug flags to the kernel cmdline. So you may see some interesting behavior while Android is running! 
You can find the full factory build here. This is a barebones MTK-Android build. We don't recommend using it xD

Where are my Custom ROMs? ETA PL0Z BRO!!!
They're almost ready now, you should see threads popping up in a few more days.

Okay, thanks for the "anti-brick" factory preloader! I'm gonna flash another MIUI build!
Hol' up, fam. You need to check whether the MIUI OTA you're installing contains Preloader and LK or not. If it does, remove it manually. Another method could be to install the OTA and then flash the factory Preloader and LK image again via fastboot.

Flashing ROMs
Once ROMs are out, the install process is very simple and much like any other device:
- Download ZIP
- Push ZIP to device
- Flash using TWRP
- Install GApps (optional)
- Reboot
- Profit!

Unbricking
Assuming you have the factory preloader installed,
- Disconnect device from PC if connected
- Load SP Flash tool
- Load firmware of choice
- Press download, SP Flash tool will now wait for the device
- Connect device and don't hold any keys
- If the device doesn't detect, hold power for a 8-10 seconds
- It should start flashing right away without any authorization prompt!

Building ROMs (Developers only)
Things are still under development. Things may be broken, may or may not boot at all. Current code can be found below:
Device Tree - branch android-10
Vendor Tree - branch android-10
Kernel - branch master
DTBO Patch
Info about the patch: many partitions of the device (including DTBO) are signed using private keys. We don't have access to these keys, and thus our generated dtbo images don't boot. I managed to strip out the certs, write a simple Python script and write custom dtbo generation rules that append the required certs.

Things may be missing here, more information will be added as necessary 

XDA:DevDB Information
The go-to modding guide for the Redmi Note 8 Pro (begonia/begoniain), ROM for the Redmi Note 8 Pro

Contributors
Agent_fabulous
ROM OS Version: Android 10
ROM Kernel: Linux 4.x

Version Information
Status: Testing

Created 2020-02-24
Last Updated 2020-10-26
Feb 24, 2020
View
37
Agent_fabulous
CFW and CFW builds and recoveries


CFW​
[SIZE="+1"]What is a CFW?[/SIZE]
The A10 Custom Firmware, or CFW for short, is a combination of multiple Xiaomi firmware packages.

[SIZE="+1"]Why do I need it?[/SIZE]
You are probably aware of the leaked factory firmware for the Redmi Note 8 Pro. This firmware contains a preloader which was compiled with the download code.
Since the preloader does not need to setup platform security it allows us to unbrick without an authorized account.
Unfortunately, the MIUI bootloader do not run on the factory preloader - only the factory bootloader does, which works just fine with A9 kernels.
Furthermore, the A10 kernel source released by Xiaomi does not work with the factory bootloader/preloader, which was the reason I worked on a new kernel source based on Android 9 (A9) with several Android 10 (A10) drivers to work nicely with the A10 blobs.
In short, the CFW enables you to use the new builds without worrying about bricks while running newer proprietary vendor software.

[SIZE="+1"]What's special about the new builds?[/SIZE]
New builds, tagged "[CFW]", come with their own vendor images. These builds are unified for all variants of the Redmi Note 8 Pro and have pretty much all issues fixed at this point. They ship with the new modified A10 kernel I mentioned earlier.
NOTE: While the builds are unified, the CFW is not. Please flash the correct version of CFW, for your variant
While flashing the wrong CFW is not catastrophic, it may lead to issues such as poor reception.

[SIZE="+1"]What really is inside this CFW?[/SIZE]
The CFW contains firmware files from the latest A9 and latest A10 firmware image. Along with this, the CFW also installs the factory preloader and bootloader (LK) to make sure you're safe when modifying your device.

[SIZE="+1"]How do I install the CFW and builds?[/SIZE]
CFW is a recovery-flashable package. You WILL HAVE TO downgrade to MIUI A9 to flash this since there are no recoveries which work nicely with MIUI A10.
Even though the CFW does install factory preloader and LK, I do highly recommend flashing preloader and LK from fastboot first and then the CFW.
Once you are sure you are running the CFW, simply flash a CFW compatible build. You may also need to update your recovery after installing CFW. See next post for full step-by-step instructions.

[SIZE="+1"]Recoveries? How do those work with CFW?[/SIZE]
Since recovery images also contain their own kernel, there are also CFW compatible recovery images. After installing a CFW, reboot to fastboot and flash any CFW enabled recovery image.
Trying to run a non-CFW recovery on CFW will make it reboot to system or recovery itself after a few seconds of entering recovery. Should you find yourself in a situation like this: as soon as recovery loads, hit [reboot] > [bootloader]. If you cannot do this, flash the new recovery image from SP Flash tools (or wait for your device to drain it's battery out )
See next post for full step-by-step instructions.

[SIZE="+1"]Do I need to flash the CFW everytime?[/SIZE]
Nope. If you flashed CFW once, you're good. Just make sure the ROM you're flashing does not install any firmware images. Ask your ROM developer before installing a zip.
ALL MIUI ZIPS CONTAIN FIRMWARE IMAGES. DO NOT FLASH ON TOP OF CFW

[SIZE="+1"]I'm on CFW and rocking a custom ROM. How do I go back to MIUI?[/SIZE]
Flash a full MIUI Fastboot ROM, or use SP Flash tools to install the flash all MIUI partitions. Again, do not flash a recovery package for switching to MIUI.
See next post for full step-by-step instructions.

[SIZE="+1"]What would happen if I install a non-CFW build on CFW?[/SIZE]
Again, nothing catastrophic. It'll make the device reboot itself a few seconds into the bootanimation. All current non-CFW builds run the A9 kernel code. The new kernel is based on the A9 kernel code as well; some drivers just don't like the new firmware images included in the CFW So, save yourself the trouble and check what you're installing. CFW supported builds are listed in the next post.

[SIZE="+1"]Where can I download the CFW?[/SIZE]
Please see the next post, below.

While the whole CFW thing may seem a bit overwhelming to some, remember, it's something to protect your device in the long run! Take out a few minutes and please read through this post properly.
Feb 24, 2020
View
35
Agent_fabulous
Reserved

CFW Migration Steps

Coming from MIUI
Method 1
- Downgrade to MIUI Android 9 if not already, or try using Method 2
- Flash preloader and lk as mentioned in first post
- Flash any non-CFW Android 9 recovery
- Boot into recovery
- Wipe system, cache, dalvik
- Flash CFW, CFW compatible ROM (flash GApps mods later!  )
- Format data (not wipe, select "Format Data", you'll lose all userdata)
- Reboot to bootloader
- Flash CFW recovery
- Reboot! You're now on CFW!

Method 2 Try at own risk!*
- Flash a non-CFW A10 recovery from fastboot (such as LR TWRP for MIUI A10)
- Boot directly into recovery by holding [Volume +] after flashing and rebooting
- (Optional) For safety sake, select Advanced option "Close AVB 2.0"
- Take a full nandroid backup (IMPORTANT! Will be helpful if lost IMEI)
- Turn off "Reboot after installing ROM" from TWRP settings
- Wipe system, dalvik and cache
- Flash CFW and a CFW compatible ROM (flash GApps and mods later!  )
- Format data (not wipe, select "Format Data", you'll lose all userdata)
- Reboot to bootloader from the Reboot menu
- Flash CFW recovery
- Reboot! You're now on CFW!
*NOTE: This method has worked for each everyone who has tried it and followed correctly, so far. The idea for this method was mine, but I personally have not tried it myself. It will particularly be useful if you're using MIUI A10 and are on a limited data plan 

Coming from non-CFW Custom ROMs
- Make sure preloader and LK are installed (see first post)
- Boot into recovery
- Wipe system, cache, dalvik
- Flash CFW, CFW compatible ROM (flash GApps here if necessary, flash any extra mods later!  )
- Format data (not wipe, select "Format Data", you'll lose all userdata)
- Reboot to bootloader
- Flash CFW recovery

Updating CFW-enabled builds on CFW
Since you're already on CFW, just install the update and reboot like any other device:
- Remove lockscreen if any
- Reboot to recovery
- Wipe data, system, cache, dalvik
- Flash ROM (+ GApps if necessary)
- Reboot!

Going back to MIUI from CFW
- Flash full MIUI firmware from SP Flash Tools or fastboot 

Android 11
Changes
- Update to MIUI 12 blobs and fw images
- Prebuilt vendor image for A11
- Fully enforced and vendor isolation enabled

Coming from A10 CFW
- Flash "CFWv3+vendor" package followed by the ROM.
Note: You don't need to flash the "CFWv3+vendor" package more than once when switching to other A11 ROMs, unless you have gone back to A10.

Coming from MIUI
- Follow instructions above to CFW, just use A11 CFW and A11 ROM instead

Going back to A10 CFW
- Flash CFWv2 along with your A10 ROM.

Going back to MIUI
- Fastboot flash full MIUI ROM

Note 1: Do not wipe vendor on A11. If you do, you'll have to reflash the "CFWv3+vendor" package to have a functional device.

Note 2: On VNDK30 A11 builds, you may wipe vendor, since the builds ship with a vendor image. 

CFW Downloads
Android 11 (CFWv4) For VNDK-30 builds only! (is the same as CFWv2.1, but version changed to avoid confusion )
- begoniain: https://sourceforge.net/projects/begonia-oss/files/CFW/begoniain-A11-CFW_20210105.zip/download
- begonia: https://sourceforge.net/projects/begonia-oss/files/CFW/begonia-A11-CFW_20210105.zip/download
Android 11 (CFWv3+vendor)
- begoniain: https://sourceforge.net/projects/be...egoniain-A11-CFW-vendor-20201026.zip/download
- begonia: https://sourceforge.net/projects/begonia-oss/files/CFW/begonia-A11-CFW-vendor-20201026.zip/download
Android 10 (CFWv2)
- begoniain: https://sourceforge.net/projects/begonia-oss/files/CFW/begoniain-A10-CFW_20200823.zip/download
- begonia: https://sourceforge.net/projects/begonia-oss/files/CFW/begonia-A10-CFW_20200823.zip/download

CFW Supported Recoveries
- Unofficial TWRP
- Anything else marked with "[CFW]"

CFW Supported ROMs and kernels
- Pretty much everything active, at this point lol

The latest non-CFW Unofficial TWRP can be found on AFH, on my thread (see last line on post) and in the Telegram group as note "#twrp-non-cfw-for-roms"

Troubleshooting
IMEI lost (requires full TWRP backup of MIUI when IMEI was present!):
From a full TWRP backup, restore the following partitions:
- nvcfg
- nvdata
- nvram
- persist
- protect_f
- protect_s
Reboot and check! IMEI should be back :highfive:

ROM Reboots to recovery after boot logo (no bootanimation):
Usually, this indicates that the device isn't able to setup encryption. You'll also see randomly named files and folders in TWRP. In this case, just Format Data (not wipe), and reboot.

Rescuing the device:
Since CFW is always running factory preloader and bootloader (LK), you can use SP Flash in case something should go wrong.
Assuming you're stuck in some sort of loop/brick while on factory preloader/CFW, here are the EDL modes:
There are 2 modes of "EDL":
- Preloader: Factory preloader will always advertise a download mode when the device is starting, right before the Redmi logo (You may not get a logo if you're bricked, only a blinking LED). You do not need to hold ANY buttons. Just plug in the device and it'll show up on your computer periodically. Load any Android 9 firmware in SP Flash, uncheck preloader, lk and lk2, connect your device and hit Download in SP Flash.
- BootROM: If you don't have factory preloader, you will have to flash via BootROM. This requires an authorized account. Unless you have one yourself, you will need to head to a service center to get your device fixed. If you do need to load BootROM download, hit download in SP Flash with the Authorized Account logged in, hold volume up and plug in the device while holding the key. Release the key as soon as your computer recognizes it. SP Flash will start the download.
If you are able to enter this mode yourself, and the service center quotes something like a "motherboard replacement", show them this section of the post and tell them it's a software issue. Given the nature of such a new and unique device, often even the best make mistakes! If you're a XIaoMi Service Center and a customer has showed this to you, PLEASE try this. The phone will enter BootROM if you hold the keys at the correct time. You do not need to take the phone apart to short any pins. Just login and bind to your special account, hit "Download" in SP Flash and hold the keys for 5-15 seconds with the device plugged in. The software will recognize the device and start flashing.
If you as the technician are wondering why you should trust a random person on the internet, here's why: I received the device from XiaoMi India, as part of their developer program and have been reversing things on it for the past 6+ months. I have been through 3 hard-bricks and have helped multiple service centers diagnose the device correctly and having them fix my own device too.


Feb 24, 2020
View
12
Agent_fabulous
class1ok said:
He, OK, now I feel stupid. What does it mean in instruction (first post) -
fastboot flash preloader preloader_begonia.bin
fastboot flash lk lk.img
fastboot flash lk2 lk.img

Flash lk.img twice, or...?


bandos23 said:
hello guys, the lk.img file should be rewritten to lk2.img on the second flash or just flash 2x lk.img? sorry that I ask maybe clear things but I do not want to have a brick next to it thanks for the answer.

I didn't want to go further into detail, but those interested, here it goes:
Even though begonia is A-only, many OEM partitions are A/B. This isn't the traditional A/B other Android devices use. It's purely for redundancy, in case say an OTA update (that also updates bootloader and preloader) fails. Partitions that are A/B:
- sspm
- tee
- lk
- gz
- scp
- preloader
Main loader: sspm_1, tee1, lk, gz1, scp1, preloader_a
Alternate loader: sspm_2, tee2, lk2, gz2, scp2, preloader_b
Let's take an example scenario to understand it's use better - You received a shiny new update and the entire recovery zip is gonna be flashed. Or let's say you're manually sideloading it. Your device managed to start the update with low battery and isn't plugged into the charger. Ignoring the usual Android partitions, first the partitions of Alternate loader are flashed to. Once all of them are written, the script will change active slot to alternate and the script will increment the update_stage status, implying that alternate loader is now usable. Now, the script needs to do the same thing for Main loader. Suppose it starts updating Main loader and your battery runs out. It hasn't set the update_stage and the active slot is Alternate loader. So when you charge up and try to use your phone, your phone will still be functional and can continue the update from the incomplete stage.
For reference on the partitions that are updated, see any full MIUI recovery zip's updater-script.

Danmann said:
Yeah, that's how I understand it, too. But "Unlocking the bootloader and gaining root" came at first. I just wanted to make sure. 

Anyway, I tried it and it worked:
1. Factory Preloader (reboot it)
2. TWRP (as expained)

It worked, but I can't see anything on recovery - black screen bug. Adb is showing me that the recovery is loaded. So, I'll wait for the fix.

I have created a small guide on the PwOSS website in case anyone wants to take a look. Feel free to copy the whole thing and create another thread if needed.

I had the same problem. I looked at the end of the post ;D
Click to expand...
Regarding black screen in recovery, try my last unofficial TWRP build. I'll post one more final update ig, for completeness sake. TWRP needs to merge the new blanking code for brightness to work consistently for everyone.
Feb 27, 2020
View
12
Agent_fabulous
CFW Updated (v2; 2020/08/23)

Changelog:
- Update bootloader from latest A9 builds
- Fix Offline Charging (needs changes in ROM too  )
- Revert to MIUI-like recovery and fastboot menus (volume + loads recovery, volume - loads fastboot)
- Disable MRDUMP on force reboot
- Fix Netflix 1080p panics

CFW Downloads
- begoniain: https://sourceforge.net/projects/begonia-oss/files/CFW/begoniain-A10-CFW_20200823.zip/download
- begonia: https://sourceforge.net/projects/begonia-oss/files/CFW/begonia-A10-CFW_20200823.zip/download
Aug 23, 2020
View
NEW POSTS
R
[ROM][UNOFFICIAL][11][onyx] LineageOS 18.1 for the Amazon Fire HD 8 / HD 8 Plus (10th Gen, 2020)
Latest: ralfbergs 1 minute ago
Fire HD 8 and HD 10 Original Android Development
*** New Device Forum Requests ***
Latest: Ben9543 1 minute ago
About XDA developers
Snapdragon N900x Optimus ROM [4.4.2]
Latest: tsengxun 2 minutes ago
Galaxy Note 3 Android Development
[ROM][16][UNOFFICIAL] AxionOS 2.9 for Galaxy M20
Latest: umutcagand 4 minutes ago
Samsung Galaxy M20 ROMs, Kernels, Recoveries, & Ot
Development [RECOVERY] [OFFICIAL] [Xiaomi Redmi Note 13 Pro 5G/POCO X6 5G] [OrangeFox Recovery Project] [R12.0] [13/14/15/16/17]
Latest: DarthJabba9 9 minutes ago
Xiaomi Redmi Note 13 Pro 5G / Poco X6 5G

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