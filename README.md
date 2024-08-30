<h2 align="center"> NB-IoT Hbyrid Blockchain using ESHA-256 Algorithm </h2>

<p align="center">
  <a href="#Unique-ID-Generation"> Unique ID Generation </a> •
  <a href="#Device-Join-Procedure"> Device Join Procedure </a> •
  <a href="#Device-Transactions"> Device Transactions </a>
</p>

# Motivation
The goal of this study is to further save energy consumption by NB-IoT Framework in "Enabling secure lightweight mobile Narrowband Internet of Things (NB-IoT) applications using blockchain" by using the Energy Efficient SHA-256 (ESHA-256) algorithm.   

# ESHA-256
<p align="center"><img src="./Figures/Hash.png" width="750" title="ESHA-256">
</p>

ESHA-256 algorithm reduces the computational power required for running the SHA-256 algorithm by access message data from memory banks in parallel rather than sequentially, as shown in the above figure. 

<!--
<p>This section provides the statistical summary of the energy measurements of ESHA-256 Sequential/Parallel using pyRAPL (Python Running Average Power Limit).</p>

| Block Size | Bytes     | Sequential | Parallel  | Energy Savings |
|-------------|-----------|------------|-----------|----------------|
| 8           | 56        | 47,058     | 23,010    | -51%           |
| 800         | 5,600     | 41,260     | 25,696    | -38%           |
| 8,000       | 56,000    | 51,452     | 42,358    | -18%           |
| 80,000      | 560,000   | 134,339    | 115,478   | -14%           |
| 800,000     | 5,600,000 | 916,318    | 911,619   | -1%            |
| 8,000,000   | 56,000,000| 9,084,755  | 9,060,463 | 0%             |
-->
#
# ESHA-NB-IOT Framework
<p align="center">	  
  <img src="./Figures/Fig1.png" width="500" title="NB-IoT Framework">.....<img src="./Figures/Fig7.png" width="300" title="NB-IoT Framework">
</p>

* NB-IOT: devices are resource constrained with less computational power, low memory, storage and bandwidth. Therefore, devices only store hash of transactions initiated by them in an array as linear hash chain. By design, NB-IoT devices will have device address and reputation (default 4).
* BASE STATIONS: Transactions initiated by NB-IoT devices can only be authorized by base station using non-interactive ZKP and then added to blockchain. The base station dynamically partitions its memory to store device transactions in a merkle tree and allocate the rest to store individual device transactions in a linear hash chain for faster access.
* ETHEREUM BLOCKCHAIN: NB-IoT Devices and base stations are connected through ethereum blockchain using Remix IDE Smart Contracts. Non-interactive ZKP (HMAC) is used as consensus algorithm for block approval.
* AUTHENTICATION SERVER: The only responsibility of the authentication server is to authenticate NB-IoT devices using unique ID allocated to the device.
* DATA SERVER: is responsible for issuing Unique ID to NB-IoT devices.
* IPFS (Inter Planetary File System): connects base stations to provide decentralised data storage and sharing.

```bash
Non-Interactive Zero-Knowledge Proof: The prover verifies that it knows secret information without revealing what that information is. In digital signatures, prover can demonstrate knowledge of private key associated with public key, without revealing the private key itself.
```
<br/>

## Unique ID Generation 

* For anonymity, when NB-IoT device joins a new cell, the data server issues a 'New Unique ID' and 'Encryption Secret' to the device after authentication.
* The Unique ID is used as identifier in blockchain.
* IoT Devices are assigned ‘Device Address’ as permanent ID by the Data Server when they join blockchain for the first time. 
  
<p align="center">Seed = Old Unique ID | Encryption Secret | Nonce  <br/>Unique ID = UUID(random.getrandbits(Seed)</p>
<br/>
<p align="center">	  
  <img src="./Figures/Fig2.png" width="550" title="NB-IoT Framework">
</p>

# 
> **IoT Client**
```bash
$ python IoTClient.py
```
> Terminal Output
```bash
Sent tuple to Authentication Server (A): ('127.0.0.1', 1001) - ('NReq', '0x000000000000000a', '6148bf32701b7ddd20a1e7c4b4c052f3', '1721519301')

Received tuple from Authentication Server (A): ('127.0.0.1', 1001) - ('c718faeefcd166b2c1e90f0e08888c6d', '1721519280', '68AFF4353B8317BE24CA6096F19EA95D80DD992BA5F1E0C3F60C296EEE304BB3', '0BD471F807062F5CDA968C3CE14A00368AFE6939B63C985ABDE8A20E5CC93114')

Sent tuple to Data Server (B): ('127.0.0.2', 2002) - ('IDReq', '6', '0x000000000000000a', 'D1CDFB53D3FBD31372A5708DB39B7525AA8D8E0277C1A0BBAEF4589AF237A3D6', '6148bf32701b7ddd20a1e7c4b4c052f3', '1721519280', 'c718faeefcd166b2c1e90f0e08888c6d', '0BD471F807062F5CDA968C3CE14A00368AFE6939B63C985ABDE8A20E5CC93114')

Received tuple from Data Server (B): ('127.0.0.2', 2002) - ('0x00000000000000aa', '7a8253502d40e501662c91eb6c7e162b', '1721519264')

New Unique ID received from Data Server = 0x00000000000000aa

```
# 
> **Authentication Server**
```bash
$ python AuthenticationServer.py
```
> Terminal Output
```bash
Received tuple from IoT (C): ('127.0.0.1', 54044): ('NReq', '0x000000000000000a', '6148bf32701b7ddd20a1e7c4b4c052f3', '1721519301')

Sent tuple to IoT (C): ('127.0.0.1', 54044) - ('c718faeefcd166b2c1e90f0e08888c6d', '1721519280', '68AFF4353B8317BE24CA6096F19EA95D80DD992BA5F1E0C3F60C296EEE304BB3', '0BD471F807062F5CDA968C3CE14A00368AFE6939B63C985ABDE8A20E5CC93114')

Sent tuple to Data Server (B): ('127.0.0.2', 2002) - ('0x000000000000000a', 'c718faeefcd166b2c1e90f0e08888c6d', '1721519301', '1721519280', '0BD471F807062F5CDA968C3CE14A00368AFE6939B63C985ABDE8A20E5CC93114')

```
# 
> **Data Server**
```bash
$ python Dataserver.py
```
> Terminal Output
```bash
Received tuple from Authentication Server (A): ('127.0.0.1', 1001): ('0x000000000000000a', 'c718faeefcd166b2c1e90f0e08888c6d', '1721519301', '1721519280', '0BD471F807062F5CDA968C3CE14A00368AFE6939B63C985ABDE8A20E5CC93114')

Received tuple from IoT (C): ('127.0.0.1', 54044): ('IDReq', '6', '0x000000000000000a', 'D1CDFB53D3FBD31372A5708DB39B7525AA8D8E0277C1A0BBAEF4589AF237A3D6', '6148bf32701b7ddd20a1e7c4b4c052f3', '1721519280', 'c718faeefcd166b2c1e90f0e08888c6d', '0BD471F807062F5CDA968C3CE14A00368AFE6939B63C985ABDE8A20E5CC93114')

Sent tuple to IoT (C): ('127.0.0.1', 54044) - ('0x00000000000000aa', '7a8253502d40e501662c91eb6c7e162b', '1721519264')

```




---
<h3>Unique ID Generation - Statistical Summary (SHA-256 Sequential vs Parallel)</h3>

This section provides the statistical summary of the energy measurements and duration using pyRAPL (Python Running Average Power Limit).
#
> **IOT CLIENT**

| SEQUENTIAL | CPU  | DRAM  | Duration  |
|-----------|----------|----------|-------------|
| MEAN      | 135051 | 12523| 23940 |
| MEDIAN    | 130462      | 7386   | 11310     |

| PARALLEL | CPU  | DRAM  | Duration |
|-----------|----------|----------|-------------|
| MEAN      | 125495 | 9650 | 17977 |
| MEDIAN    | 122620   | 6287      | 10769     |


| PERCENTAGE %      | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | -7      | -23     | -25     |
| MEDIAN    | -6      | -15     | -5      |


For raw data, refer to the
- [SHA-256 Sequential Access Measurement Details](./Device%20ID/IoT%20Client.csv)
- [SHA-256 Parallel Access Measurement Details](./Device%20ID/E-IoT%20Client.csv)
#
> **AUTHENTICATION SERVER**

| SEQUENTIAL       | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 134875  | 12529   | 23959   |
| MEDIAN    | 128540  | 7538    | 11372   |

| PARALLEL    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 126108  | 9685    | 18076   |
| MEDIAN    | 122680  | 6531    | 10914   |

| PERCENTAGE  %    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | -7      | -23     | -25     |
| MEDIAN    | -5      | -13     | -4      |


For raw data, refer to the
- [SHA-256 Sequential Access Measurement Details](./Device%20ID/Authentication%20Server.csv)
- [SHA-256 Parallel Access Measurement Details](./Device%20ID/E-Authentication%20Server.csv)

#
> **DATA SERVER**

| SEQUENTIAL       | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 135259  | 12539   | 23943   |
| MEDIAN    | 130737  | 7447    | 11294   |

| PARALLEL    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 125630  | 9660    | 17959   |
| MEDIAN    | 122192  | 6165    | 10798   |

| PERCENTAGE  %    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | -7      | -23     | -25     |
| MEDIAN    | -7      | -17     | -4      |


For raw data, refer to the
- [SHA-256 Sequential Access Measurement Details](./Device%20ID/Data%20Server.csv)
- [SHA-256 Parallel Access Measurement Details](./Device%20ID/E-Data%20Server.csv)

  
Measurement Units
- Energy Units (CPU, DRAM) = Microjoules
- Duration = Microseconds
---


<br/>

## Device Join Procedure

* (1-2) Authentication Server authenticates the NB-IoT device using its existing Unique ID.
* (3) After authentication, NB-IoT device sends 'Leave Request' to Home Base Station along with address of Visiting Base Station.
* (4-6) Home Base Station 'Approve' the request. Then, Base Station 'Saves' deployed Smart Contract along with transactions recorded in JSON format in Remix IDE. The file is then uploaded to Inter Planetary File System (IPFS) and resulting File Hash is shared with Visiting Base Station.
* (7-10) NB-IoT sends 'Join Request' to Visiting Base Station. Visiting Base Station downloads JSON file from IPFS, verifies IoT device using Unique ID and then sends 'New Unique ID' and 'Encryption Secret' to NB-IoT device. The New Unique ID and Encryption Secret is then used by Non-Interactive ZKP for block approval.

<p align="center">	  
  <img src="./Figures/Fig3.png" width="750" title="NB-IoT Framework">
</p>

# 
> **IoT Client**
```bash
$ python IoTClient.py
```
> Terminal Output
```bash
Sent tuple to Authentication Server (A) ('127.0.0.1', 1001) - ('NReq', '0x000000000000000a', '8e6e0aa746ccc38b3016f5b61bc5d48e', '1721520743', 'F2A2C96B931407AD2E6CC2D0348D76B8F98B6811D6F34A28BF664A17A8B2EAF5')

Received tuple from Authentication Server (A) ('127.0.0.1', 1001) - ('be8064004b62b6310e55f85600e4787e', '1721520729', '36F738E997A320DD386EBB8641E837C9250754848B4A6498193DBCBB5F325CC7')

Sent tuple to Home Base Station (D) ('127.0.0.3', 3003) - ('LReq', '8e6e0aa746ccc38b3016f5b61bc5d48e', '1721520743', '0x000000000000000a', '0x00000000000000bb')

Received tuple from Home Base Station (D) ('127.0.0.3', 3003) - ('RApp', 'eead184328e6c99f48b5115dc6ec3d21', '122F3DADE9419B3779DFE10A58C822664BEAF50A34117BED138B8DA60AB4637B')

Sent tuple to Visiting Base Station (B) ('127.0.0.2', 2002) - ('JReq', '6', '0x000000000000000a', 'F2A2C96B931407AD2E6CC2D0348D76B8F98B6811D6F34A28BF664A17A8B2EAF5', '8e6e0aa746ccc38b3016f5b61bc5d48e', '1721520743', '1721520729', 'F3C3732DCAF39CE4D5324A6180976D644C9158885E44FE6B685918B9D2F430DF')

Received tuple from Visiting Base Station (B) ('127.0.0.2', 2002) - ('RApp', '0x00000000000000aa', '0x0000000000000011', 'f0f9df22c2ac17ccb62abfb4d82a039c', '1721520697')

New Unique ID received from Visiting Base Station (B) = 0x00000000000000aa

```
# 
> **Authentication Server**
```bash
$ python Authentication.py
```
> Terminal Output
```bash
Received tuple from IoT (C): ('127.0.0.1', 50335): ('NReq', '0x000000000000000a', '8e6e0aa746ccc38b3016f5b61bc5d48e', '1721520743', 'F2A2C96B931407AD2E6CC2D0348D76B8F98B6811D6F34A28BF664A17A8B2EAF5')

Sent tuple to IoT (C): ('127.0.0.1', 50335) - ('be8064004b62b6310e55f85600e4787e', '1721520729', '36F738E997A320DD386EBB8641E837C9250754848B4A6498193DBCBB5F325CC7')

Sent tuple to Visiting Base Station Server (B): ('127.0.0.2', 2002) - ('LReq', 'A0E872F7AAF4D52155AF4AA6715F04B5B74A810710DA8F21CF378DAB20EF62D2', '0x000000000000000a', 'be8064004b62b6310e55f85600e4787e', '8e6e0aa746ccc38b3016f5b61bc5d48e')

```
# 
> **Home Base Station**
```bash
$ python HomeBS.py
```
> Terminal Output
```bash
Received tuple from IoT (C): ('127.0.0.1', 50335): ('LReq', '8e6e0aa746ccc38b3016f5b61bc5d48e', '1721520743', '0x000000000000000a', '0x00000000000000bb')

Sent tuple to IoT (C): ('127.0.0.1', 50335) - ('RApp', 'eead184328e6c99f48b5115dc6ec3d21', '122F3DADE9419B3779DFE10A58C822664BEAF50A34117BED138B8DA60AB4637B')

```
# 
> **Visiting Base Station**
```bash
$ python VisitingBS.py
```
> Terminal Output
```bash
Received tuple from Authentication Server (A): ('127.0.0.1', 1001): ('LReq', 'A0E872F7AAF4D52155AF4AA6715F04B5B74A810710DA8F21CF378DAB20EF62D2', '0x000000000000000a', 'be8064004b62b6310e55f85600e4787e', '8e6e0aa746ccc38b3016f5b61bc5d48e')

Received tuple from IoT (C): ('127.0.0.1', 50335): ('JReq', '6', '0x000000000000000a', 'F2A2C96B931407AD2E6CC2D0348D76B8F98B6811D6F34A28BF664A17A8B2EAF5', '8e6e0aa746ccc38b3016f5b61bc5d48e', '1721520743', '1721520729', 'F3C3732DCAF39CE4D5324A6180976D644C9158885E44FE6B685918B9D2F430DF')

Sent tuple to IoT (C): ('127.0.0.1', 50335) - ('RApp', '0x00000000000000aa', '0x0000000000000011', 'f0f9df22c2ac17ccb62abfb4d82a039c', '1721520697')

```



---
<h3>Device Join Procedure - Statistical Summary (SHA-256 Sequential vs Parallel)</h3>

This section provides the statistical summary of the energy measurements and duration using pyRAPL (Python Running Average Power Limit).
#
> **IOT CLIENT**

| SEQUENTIAL | CPU  | DRAM  | Duration  |
|-----------|----------|----------|-------------|
| MEAN      | 190546  | 19709   | 34353   |
| MEDIAN    | 178864  | 12268   | 15825   |

| PARALLEL | CPU  | DRAM  | Duration |
|-----------|----------|----------|-------------|
| MEAN      | 192874  | 16038   | 26915   |
| MEDIAN    | 181641  | 11352   | 14965   |

| PERCENTAGE %      | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 1       | -19     | -22     |
| MEDIAN    | 2       | -7      | -5      |

For raw data, refer to the
- [SHA-256 Sequential Access Measurement Details](./Device%20Join/IoT%20Client.csv)
- [SHA-256 Parallel Access Measurement Details](./Device%20Join/E-IoT%20Client.csv)
#
> **AUTHENTICATION SERVER**

| SEQUENTIAL       | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 190106  | 19695   | 34422   |
| MEDIAN    | 177704  | 12268   | 16004   |

| PARALLEL    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 192218  | 16009   | 26940   |
| MEDIAN    | 181335  | 11109   | 15020   |

| PERCENTAGE  %    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 1       | -19     | -22     |
| MEDIAN    | 2       | -9      | -6      |

For raw data, refer to the
- [SHA-256 Sequential Access Measurement Details](./Device%20Join/Authentication%20Server.csv)
- [SHA-256 Parallel Access Measurement Details](./Device%20Join/E-Authentication%20Server.csv)

#
> **HOME BASE STATION**

| SEQUENTIAL       | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 190375  | 19706   | 34392   |
| MEDIAN    | 177123  | 12146   | 15813   |

| PARALLEL    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 192592  | 16016   | 26934   |
| MEDIAN    | 181885  | 10925   | 14977   |

| PERCENTAGE  %    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 1       | -19     | -22     |
| MEDIAN    | 3       | -10     | -5      |

For raw data, refer to the
- [SHA-256 Sequential Access Measurement Details](./Device%20Join/Home%20Base%20Station.csv)
- [SHA-256 Parallel Access Measurement Details](./Device%20Join/E-Home%20Base%20Station.csv)

#
> **VISITING BASE STATION**

| SEQUENTIAL       | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 190384  | 19704   | 34355   |
| MEDIAN    | 178039  | 12268   | 15867   |

| PARALLEL    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 192296  | 16007   | 26874   |
| MEDIAN    | 181213  | 11261   | 14922   |

| PERCENTAGE  %    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 1       | -19     | -22     |
| MEDIAN    | 2       | -8      | -6      |

For raw data, refer to the
- [SHA-256 Sequential Access Measurement Details](./Device%20Join/Visiting%20Base%20Station.csv)
- [SHA-256 Parallel Access Measurement Details](./Device%20Join/E-Visiting%20Base%20Station.csv)
  
Measurement Units
- Energy Units (CPU, DRAM) = Microjoules
- Duration = Microseconds
---















<br/>

## Device Transactions

* Devices generate SHA256 hash using Timestamp, nonce, unique ID, reputation, message and Encryption Secret.
* Resulting hash is sent to Base Station along with Timestamp, nonce, unique ID, reputation, message.
* Base station will generate and compare its hash with received hash and on verification will append the transaction to its merkle tree and linear hash chain.

<p align="center">	  
  <img src="./Figures/Fig6.png" width="550" title="NB-IoT Framework">
</p>

# 
> **IoT Client**
```bash
$ python IoTClient.py
```
> Terminal Output
```bash
Sent tuple to Home Base Station (D) ('127.0.0.3', 3003) - ('AReq', '0x00000000000000aa', 4, 'IoT Data', 'FCC7B19574CD8A483CF4CB64705C6971530A3BE70CE8229469DE92AD08E92D0C', '063913a9bcd99ec0815b9434e99e7722', '1721523291')

Transaction 1 Approved, Device reputation incremented: 5, transaction hash from Base Station (D): ('127.0.0.3', 3003) - 0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419

Sent tuple to Home Base Station (D) ('127.0.0.3', 3003) - ('AReq', '0x00000000000000aa', 5, 'IoT Data', '37A9954F77FC7F026BDC1857A4B1B87F211274EFB6F2082EF5CDC60DC0B63E04', '063913a9bcd99ec0815b9434e99e7722', '1721523291')

Transaction 2 Approved, Device reputation incremented: 6, transaction hash from Base Station (D): ('127.0.0.3', 3003) - 0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419

Sent tuple to Home Base Station (D) ('127.0.0.3', 3003) - ('AReq', '0x00000000000000aa', 6, 'IoT Data', '12BEF72552682A93013650E5406D3D6A1E044424EB3FC9D38DDAFAC747870462', '063913a9bcd99ec0815b9434e99e7722', '1721523291')

Transaction 3 Approved, Device reputation incremented: 7, transaction hash from Base Station (D): ('127.0.0.3', 3003) - 0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419

Sent tuple to Home Base Station (D) ('127.0.0.3', 3003) - ('AReq', '0x00000000000000aa', 7, 'IoT Data', '449DED05D72BB5D9BDA013A7CB2433F6CB2E0BC1512DE696F0F781EAAF4BFD71', '063913a9bcd99ec0815b9434e99e7722', '1721523291')

Transaction 4 Approved, Device reputation incremented: 8, transaction hash from Base Station (D): ('127.0.0.3', 3003) - 0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419

Approved Transactions in Linear Hash Chain: ['0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419', '0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419', '0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419', '0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419']

```
# 
> **Base Station**
```bash
$ python BS.py
```
> Terminal Output
```bash
Received tuple from IoT (C): ('127.0.0.1', 59655): ('AReq', '0x00000000000000aa', 4, 'IoT Data', 'FCC7B19574CD8A483CF4CB64705C6971530A3BE70CE8229469DE92AD08E92D0C', '063913a9bcd99ec0815b9434e99e7722', '1721523291')

Sent tuple to IoT (C): ('127.0.0.1', 59655) - ('0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419', 5)

Received tuple from IoT (C): ('127.0.0.1', 59655): ('AReq', '0x00000000000000aa', 5, 'IoT Data', '37A9954F77FC7F026BDC1857A4B1B87F211274EFB6F2082EF5CDC60DC0B63E04', '063913a9bcd99ec0815b9434e99e7722', '1721523291')

Sent tuple to IoT (C): ('127.0.0.1', 59655) - ('0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419', 6)

Received tuple from IoT (C): ('127.0.0.1', 59655): ('AReq', '0x00000000000000aa', 6, 'IoT Data', '12BEF72552682A93013650E5406D3D6A1E044424EB3FC9D38DDAFAC747870462', '063913a9bcd99ec0815b9434e99e7722', '1721523291')

Sent tuple to IoT (C): ('127.0.0.1', 59655) - ('0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419', 7)

Received tuple from IoT (C): ('127.0.0.1', 59655): ('AReq', '0x00000000000000aa', 7, 'IoT Data', '449DED05D72BB5D9BDA013A7CB2433F6CB2E0BC1512DE696F0F781EAAF4BFD71', '063913a9bcd99ec0815b9434e99e7722', '1721523291')

Sent tuple to IoT (C): ('127.0.0.1', 59655) - ('0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419', 8)

```
---
<h3>Device Transactions - Statistical Summary (SHA-256 Sequential vs Parallel)</h3>

This section provides the statistical summary of the energy measurements and duration using pyRAPL (Python Running Average Power Limit).
#
> **IOT CLIENT**

| SEQUENTIAL | CPU  | DRAM  | Duration  |
|-----------|----------|----------|-------------|
| MEAN      | 53465   | 9356    | 21963   |
| MEDIAN    | 18005   | 1465    | 785     |

| PARALLEL | CPU  | DRAM  | Duration |
|-----------|----------|----------|-------------|
| MEAN      | 25083   | 3944    | 8038    |
| MEDIAN    | 13550   | 1343    | 817     |

| PERCENTAGE %      | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | -53     | -58     | -63     |
| MEDIAN    | -25     | -8      | 4       |


For raw data, refer to the
- [SHA-256 Sequential Access Measurement Details](./Device%20Transactions/IoT.csv)
- [SHA-256 Parallel Access Measurement Details](./Device%20Transactions/E-IoT.csv)
#
> **BASE STATION**

| SEQUENTIAL       | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 53509   | 9356    | 21981   |
| MEDIAN    | 18005   | 1465    | 799     |

| PARALLEL    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | 25075   | 3950    | 8042    |
| MEDIAN    | 13550   | 1343    | 826     |

| PERCENTAGE  %    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| MEAN      | -53     | -58     | -63     |
| MEDIAN    | -25     | -8      | 3       |


For raw data, refer to the
- [SHA-256 Sequential Access Measurement Details](./Device%20Transactions/BaseStation.csv)
- [SHA-256 Parallel Access Measurement Details](./Device%20Transactions/E-BaseStation.csv)
  
Measurement Units
- Energy Units (CPU, DRAM) = Microjoules
- Duration = Microseconds
---

<h4>Device ID Procedure</h4>

| PERCENTAGE  %    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| IoT Client            | -7.1     | -22.9    | -24.9    |
| Authentication Server | -6.5     | -22.7    | -24.6    |
| Data Server           | -7.1     | -23.0    | -25.0    |
| **Average %**         | **-6.9** | **-22.9**| **-24.8**|

<h4>Device Join Procedure</h4>

| PERCENTAGE  %    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| IoT Client               | 1.22     | -18.62   | -21.65   |
| Authentication Server    | 1.11     | -18.72   | -21.74   |
| Home Base Station        | 1.16     | -18.73   | -21.69   |
| Visiting Base Station    | 1.00     | -18.76   | -21.78   |
| **Average %**            | **1.13** | **-18.71**| **-21.71**|

<h4>Device Transactions Procedure</h4>

| PERCENTAGE  %    | CPU   | DRAM  | Duration |
|--------------------|---------|---------|----------|
| Base Station| -53.14   | -57.78   | -63.41   |
| IoT Client  | -53.09   | -57.85   | -63.40   |
| **Average %** | **-53.11** | **-57.81** | **-63.41** |
---


<h4 align="center"> NB-IoT Hbyrid Blockchain using ESHA-256 Algorithm </h4>

<p align="center">
  <a href="#Unique-ID-Generation"> Unique ID Generation </a> •
  <a href="#Device-Join-Procedure"> Device Join Procedure </a> •
  <a href="#Device-Transactions"> Device Transactions </a>
</p>
