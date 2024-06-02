#  __DVB-S2 Stream Analysis and Processing Application__
##  __Overview__
This project is dedicated to the development of a software application for the analysis and processing of DVB-S2 receiver output streams, including raw BB Frames, GSE, and TS in near real-time. The software is capable of classifying and identifying various types of data and protocols, detecting encryption or scrambling, and extracting useful content such as VoIP calls, audio/video programs, files, emails, and web pages.
## __Features__
1. __Classification & Identification__
   Audio, video, data, and protocols such as MPE, ULE, SIP, RTP, FTP, SFTP, HTTP, HTTPS, SNMP, POP, SMTP, SSH, etc.
   
   __What Exactly Happens:Classification Function (classify_protocols)__

      The classify_protocols function is responsible for categorizing packets into different protocols. It examines each packet and identifies the protocol based on the following criteria:

      Port Numbers: Certain protocols are associated with specific destination port numbers. For example, SIP typically uses port 5060, HTTP uses port 80, and HTTPS uses port 443.

      Payload Patterns: Some protocols have distinct patterns in their payload. For instance, MPEG-TS streams contain packets with a specific marker pattern (hexadecimal value 0x47).

      Header Values: Scrambled MPEG-TS streams are identified by examining the Transport Scrambling Control (TSC) value in the packet header.

      Processing Folder Function (process_folder)

      The process_folder function scans a specified folder for PCAP files. It iterates through each file, reads it as a PCAP file, and applies the classify_protocols function to categorize the packets within. 
   
3. __Encryption/Scrambling Detection:__
   Identify encryption or scrambling techniques through headers and SI tables.
4. __Content Extraction:__
   Extract VoIP calls, audio and video programs, files, emails, web pages, etc., into separate files.
5. __Content Decoding and Playback:__
Decode and play selected audio/video content.
