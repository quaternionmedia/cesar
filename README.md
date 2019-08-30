# Cesar
A unified lighting / sound / video controller for theatrical applications

## About
This project stemmed from a necessity to control a sound board, a lighting board, and multiple video projections simultaneously with realtime cues for a theatrical production of "Cesar and Rubin", by Ed Begley Jr. 


### Architecture

For the show, we used Qlab4 as the master controller, which sends OSC messages (with SLIP encoding) to Cesar, which interprets the command and translates it to the appropriate device, along with all other cues currently running.

Everything is built around an iPython kernel (using magic functions). On startup, the `@line_magic cesar()` function is loaded, which attempts to set up the following:

- ##### QLab
Connect to QLab over OSC, and 
- ##### Sound
Connect to Allen & Heath QU-32 as a USB midi device. 
- ##### Lights
Connect to EOS Element lighting console over OSC protocol
- ##### Video
Create a tkinter GUI, sized to the full resolution of the external monitor
- ##### Control
Create a secondary tkinter GUI window for quick access to controls

After everything is connected, Cesar is ready to accept OSC commands, while the python interpreter remains ready to accept new commands, used to change settings on the fly as needed.


### Commands
All cues sent to Cesar are decoded with the SLIP protocol (RFC 1055) and then translated into its compilable python equivilent. For example, to fade an audio channel, send an OSC message such as: `/mix/cesar v`, which becomes `mix('cesar', v)`, executed in the iPython namepace against the sound module, which is sent to the sound board over USB with the appropriate midi values according to the A&H spec and the patch list.

The advantage here is many disparate effects can fire simultaneously, and still leave the command line free to execute emergency cues in the context of the live show. 
