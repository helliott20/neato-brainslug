C:\Users\algra>nmap -p0- -v -A -T4 XX.XX.50.100  
Starting Nmap 7.80 ( https://nmap.org ) at 2025-11-30 10:58 Mountain Standard Time  
NSE: Loaded 151 scripts for scanning.  
NSE: Script Pre-scanning.  
Initiating NSE at 10:58  
Completed NSE at 10:58, 0.00s elapsed  
Initiating NSE at 10:58  
Completed NSE at 10:58, 0.00s elapsed  
Initiating NSE at 10:58  
Completed NSE at 10:58, 0.00s elapsed  
Initiating Ping Scan at 10:58  
Scanning XX.XX.50.100 [4 ports]  
Completed Ping Scan at 10:58, 0.47s elapsed (1 total hosts)  
Initiating Parallel DNS resolution of 1 host. at 10:58  
Completed Parallel DNS resolution of 1 host. at 10:58, 0.00s elapsed  
Initiating SYN Stealth Scan at 10:58  
Scanning Neato-Robot.abcd.ca (XX.XX.50.100) [65536 ports]  
Discovered open port 53/tcp on XX.XX.50.100  
SYN Stealth Scan Timing: About 3.83% done; ETC: 11:11 (0:12:59 remaining)  
SYN Stealth Scan Timing: About 9.78% done; ETC: 11:08 (0:09:23 remaining)  
SYN Stealth Scan Timing: About 10.51% done; ETC: 11:12 (0:12:55 remaining)  
SYN Stealth Scan Timing: About 16.70% done; ETC: 11:10 (0:10:04 remaining)  
Increasing send delay for XX.XX.50.100 from 0 to 5 due to max_successful_tryno increase to 5  
SYN Stealth Scan Timing: About 18.52% done; ETC: 11:12 (0:11:04 remaining)  
SYN Stealth Scan Timing: About 18.73% done; ETC: 11:14 (0:13:05 remaining)  
SYN Stealth Scan Timing: About 19.52% done; ETC: 11:16 (0:14:30 remaining)  
SYN Stealth Scan Timing: About 21.06% done; ETC: 11:18 (0:15:26 remaining)  
SYN Stealth Scan Timing: About 24.29% done; ETC: 11:20 (0:16:25 remaining)  
Increasing send delay for XX.XX.50.100 from 5 to 10 due to max_successful_tryno increase to 6  
Warning: XX.XX.50.100 giving up on port because retransmission cap hit (6).  
SYN Stealth Scan Timing: About 43.75% done; ETC: 11:25 (0:15:19 remaining)  
SYN Stealth Scan Timing: About 52.10% done; ETC: 11:27 (0:13:57 remaining)  
SYN Stealth Scan Timing: About 58.04% done; ETC: 11:28 (0:12:29 remaining)  
SYN Stealth Scan Timing: About 64.08% done; ETC: 11:29 (0:10:58 remaining)  
SYN Stealth Scan Timing: About 69.85% done; ETC: 11:29 (0:09:26 remaining)  
SYN Stealth Scan Timing: About 75.86% done; ETC: 11:31 (0:07:51 remaining)  
SYN Stealth Scan Timing: About 81.62% done; ETC: 11:32 (0:06:11 remaining)  
SYN Stealth Scan Timing: About 87.08% done; ETC: 11:33 (0:04:28 remaining)  
SYN Stealth Scan Timing: About 92.36% done; ETC: 11:33 (0:02:42 remaining)  
SYN Stealth Scan Timing: About 97.54% done; ETC: 11:34 (0:00:53 remaining)  
Completed SYN Stealth Scan at 11:34, 2174.49s elapsed (65536 total ports)  
Initiating Service scan at 11:34  
Scanning 1 service on Neato-Robot.abcd.ca (XX.XX.50.100)  
Completed Service scan at 11:34, 0.22s elapsed (1 service on 1 host)  
Initiating OS detection (try #1) against Neato-Robot.abcd.ca (XX.XX.50.100)  
Retrying OS detection (try #2) against Neato-Robot.abcd.ca (XX.XX.50.100)  
Retrying OS detection (try #3) against Neato-Robot.abcd.ca (XX.XX.50.100)  
Retrying OS detection (try #4) against Neato-Robot.abcd.ca (XX.XX.50.100)  
Retrying OS detection (try #5) against Neato-Robot.abcd.ca (XX.XX.50.100)  
Initiating Traceroute at 11:34  
Completed Traceroute at 11:34, 0.03s elapsed  
Initiating Parallel DNS resolution of 2 hosts. at 11:34  
Completed Parallel DNS resolution of 2 hosts. at 11:34, 0.00s elapsed  
NSE: Script scanning XX.XX.50.100.  
Initiating NSE at 11:34  
Completed NSE at 11:35, 7.13s elapsed  
Initiating NSE at 11:35  
Completed NSE at 11:35, 0.00s elapsed  
Initiating NSE at 11:35  
Completed NSE at 11:35, 0.00s elapsed  
Nmap scan report for Neato-Robot.abcd.ca (XX.XX.50.100)  
Host is up (0.039s latency).  
Not shown: 53770 closed ports, 11765 filtered ports  
PORT   STATE SERVICE    VERSION  
53/tcp open  tcpwrapped  
| dns-nsid:  
|   id.server: marge.abcd.ca  
|_  bind.version: unbound 1.24.0  
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).  
TCP/IP fingerprint:  
OS:SCAN(V=7.80%E=4%D=11/30%OT=53%CT=21%CU=40519%PV=Y%DS=2%DC=T%G=Y%TM=692C8  
OS:E59%P=i686-pc-windows-windows)SEQ(SP=FE%GCD=1%ISR=10E%TI=Z%II=I%TS=21)SE  
OS:Q(II=I)OPS(O1=M5B4NW7ST11%O2=M5B4NW7ST11%O3=M5B4NW7NNT11%O4=M5B4NW7ST11%  
OS:O5=M5B4NW7ST11%O6=M5B4ST11)WIN(W1=FECC%W2=FECC%W3=FECC%W4=FECC%W5=FECC%W  
OS:6=FECC)ECN(R=Y%DF=Y%T=41%W=FECC%O=M5B4NW7SLL%CC=Y%Q=)ECN(R=N)T1(R=Y%DF=Y  
OS:%T=41%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=N)T5(R=Y%DF=Y%T=40%W=0%S=  
OS:Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=N)T7(R=N)U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=  
OS:G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD=S)  
  
Network Distance: 2 hops  
  
TRACEROUTE (using port 80/tcp)  
HOP RTT      ADDRESS  
1   0.00 ms  XX.XX.20.1  
2   26.00 ms Neato-Robot.abcd.ca (XX.XX.50.100)  
  
NSE: Script Post-scanning.  
Initiating NSE at 11:35  
Completed NSE at 11:35, 0.00s elapsed  
Initiating NSE at 11:35  
Completed NSE at 11:35, 0.00s elapsed  
Initiating NSE at 11:35  
Completed NSE at 11:35, 0.00s elapsed  
Read data files from: C:\Program Files (x86)\Nmap  
OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .  
Nmap done: 1 IP address (1 host up) scanned in 2201.85 seconds  
           Raw packets sent: 138770 (6.111MB) | Rcvd: 56142 (2.250MB)  

C:\Users\algra>