---
layout: post
title: Efficient Distributed Copy across Data Centers
---

> DistCp is a tool used for large inter/intra-cluster data transfer. It uses Map-Reduce to effect its distribution, error handling and recovery, and reporting. [^1]

Currently DistCp is mainly used for transferring data across different HDFSs (HaDoop File Systems). The HDFSs can sit in the same data center where the data flow through LAN (Local Area Network) or in the different data centers connected by WAN (Wide Area Network). Basically, DistCp issues Remote Procedure Calls (RPCs) to the name nodes of both source and destination, to fetch and compare file statuses, to make a list of files to copy. <img style="float: right" src="http://thinkingscale.com/public/hadoop-mirror.png" width="500x"/> The PRC is often very expensive if the name nodes are located in the different data centers, for example, it could be up to 200x slower than the case within the same date center in our experience. DistCp may issue the same RPCs more than once, dragging down the entire performance even further. DistCp doesn't support regular expression as input. If the user wants to filter and copy files from different folders, she has to either calculate a list of file paths beforehand or execute multiple DistCp jobs. Moreover DistCp allows preserving the file attributes during the data transfer. However, it does not preserve time stamp of file, which is quite important in some applications.  


To address these problems with DistCp, we introduced an enhanced version of distributed copy tool, DistCp+[^3]. Particularly DistCp+ makes it easier and faster to transfer a large amount of data across data centers. Comparing with DistCp, DistCp+ introduces improvement in the following aspects:

### Support Regular Expression

<!--More flexibility: the regular expression is allowed as the input, enabling filtering and transferring files from different source folders in one job;-->

A regular expression is a sequence of characters that forms a search pattern. It has been wildly used in the text processing utilities, for example the command *grep* in Unix. The regular expression used by DistCp+ is based on the syntax of regular expression in Java [^2] with minor changes. To use the regular expression option with DistCp+ you must specify 2 parameters: a root URI and a path filter. The path filter follows normal regular expression rules but treats all ‘/’ tokens in a special way. The ‘/’ token is used as a delimiter and the regular expression provided is split into multiple sub-expressions around this token. Each sub-expression is used as a separate path filter for a specific depth relative to the URI with the leftmost sub-expression being used first.
 
> For example, assuming you specify “/logs/” as the root URI and provide a regular expression of “server1\|server2/today\|yesterday”. The regular expression will be split into the 2 sub-expressions “server1\|server2” and “today\|yesterday”. Then DistCp+ will traverse the file system starting at the root (“/logs/”) and use any file that matches the first sub-expression (“server1\|server2”). Folders are recursively expanded, but at each new depth in the file system the next sub-expression is used as the path filter. Using this example provided, you can match such files as “/logs/server1/yesterday” and “/logs/server2/today”, but it will not match something like “/logs/yesterday”. Also note that if a folder matches the last path filter, the entire folder is used as input instead of being recursively traversed.

### Cache File Status

<!--2. Better scalability: the caching is exploited to minimize the number of RPCs for comparing data between HDFs;-->

When a DistCp job copies a large number of files especially across geographically distant data centers, it usually has a very long setup time as several RPCs are issued to collect the file status from both sides.  However, the cost of RPC is very high especially when it is through WAN. DistCp repetitively issues RPCs to get individual directory or file’s status object. These RPCs either overlap with previous ones or can be combined into fewer RPCs. To reduce the  cost, a cache of file status is created in the early stage, when directory level RPC is used to get all file status under the very directory in one RPC. Then RPC is necessary only if a cache miss occurs in the following stages. For tens of thousands file transferring, we observe a significant improvement on the end-to-end time cost. 

### Keep Time Stamp

<!--3. Preserve the temporal property: the time stamp of file to transfer can be preserved.-->

DistCp supports to preserve the file status, including block size, replication factor, user, group and permission. However, it does not keep the time stamp (or last modified time stamp) of the file, which is important especially when we use "-update" option to skip files without any change. Checking CRC (Cyclic Redundancy Check) of the file is an alternative, but the CRC computation of files is too high to be practical for large data transfer. Comparing the file size may not be accurate as some changes do not change the size of files. Therefore the time stamp is better to decide if an update is necessary. Particularly, the file has its time stamp preserved after copied if necessary. When "-update" option is specified, DistCp+ compares the time stamps of files on different clusters to decide if the file is included.


In [Turn](http://www.turn.com), DistCp+ has been used to transfer data among different data centers regularly. A DistCp+ job can usually copy thousands of files from different folders and the data volume can be terabytes.


[^1]: Hadoop DistCp: [http://hadoop.apache.org/docs/current1/distcp.html](http://hadoop.apache.org/docs/current1/distcp.html)

[^2]: Lesson: Regular Expressions, [http://docs.oracle.com/javase/tutorial/essential/regex/](http://docs.oracle.com/javase/tutorial/essential/regex/) 

[^3]: DistCp+: [https://github.com/turn/DistCPPlus](https://github.com/turn/DistCPPlus)
