---
layout: post
title: Disaster Recovery across Data Centers
---


In the era of BigData, the data storage becomes so large that recovery from a disaster, such as the power outage of a data center, becomes very difficult. The traditional transaction-oriented data management system relies on a write-ahead commit log to record the system state and the recovery process will work only if the log processing is faster than the incoming change requests. In other words, commit log based approach hardly works for big data system where terabytes of non-transactional daily changes are norms. 

In Turn, we exploit a geographically apart master-slave architecture to support high availability (HA) and disaster recovery (DR) in the large scale Hadoop-based DWS (Data Warehouse System). 

<!--
<img src="http://thinkingscale.com/public/multi-site.png" width=800x/>
-->
The master and the slave are located in the different data centers that are geographically apart. Functionally, the slave is like a mirror of the master. The master or slave is composed of a Hadoop cluster, a relational database, an analytics engine, a cluster monitor, a query dispatcher, a parallel ETL component, and a console. Not all of these components in the slave are active. For instance, the *cluster monitor* in the slave is standing by, whereas its *analytics engine* should be active to accept query jobs. 

Data replication happens from the master to the slave to assure the data consistency between the Hadoop clusters, and database replication reflects any change on the master database to the slave database. The master and slave are connected with a dedicated high-speed WAN  (Wide Area Network).  

The master-slave architecture makes DR and HA possible when one of the data centers fails. Additionally the workload balancing between master and slave optimizes the query throughput[^1]. 

### Failover and Disaster Recovery

Failure is common in the large storage system. It could be due to hardware failure, software bug, human error etc. The master-slave architecture makes the HA and DR possible and simple in the petabyte-scale data warehouse system at Turn. 

#### Network Failure

When the WAN fails completely, a performance degrading can occur as all queries will be dispatched to the master only. The data and database replications also stop. Fortunately nothing special has to be done with the Hadoop cluster when the WAN comes back to normal, because the data replication process will catch up with the missing data of the slave. A sync-up operation is triggered to synchronize the slave database with the master database. 

#### Hadoop Cluster Failure

In case of the Hadoop cluster failure in the slave, the DWS keeps working as the master has everything untouched. It is a little complex when the master loses its Hadoop cluster, as it implicates a master-slave swapping. Particularly, all components of the slave become active and take over the interrupted processes. For instance, *parallel ETL* becomes active first, starting to ingest data.  Importantly during the swapping, the DWS keeps accepting and running the user query submission. 

When the failed Hadoop cluster comes back, the data replication process can help to identify and copy the difference from the current master to the slave. Depending upon the downtime and data loss caused by the failure, it can take up to days to complete the entire recovery. However, certain queries can be executed in the recovering cluster. Furthermore based on the query history in the relational database, the hot-spots of data can be recovered first. 

#### Data Center Failure

It is rare but fatal if one of the data centers fails. At Turn the DWS tolerates a failure of either the master or the slave. When the slave data center is down, the performance is degraded because only one of the Hadoop clusters is available and all workload are moved to the working one. The data recovery is trivial because the replication processes will catch up the difference once the failure is fixed. 

If the master data center fails, the stand-by services in the slave will become active right away. There is a chance that data or query may lose if the failure happens in the middle of the data replication. However, the loss can be mitigated if the replication is scheduled to run more frequently. After all services are active, the slave becomes the master. When the failed data center is recovered, it will run as a slave. The data replication is issued to transfer the difference over. Before the database replication starts, a database sync-up process is required to make the new slave have the same content in its relational database. 


[^1]: Any query job can be executed in either Hadoop cluster, as long as its input is available. Therefore, it is possible to balance the workload between clusters. Specifically given a query submission, *query dispatcher* first checks the input availability on both clusters. If the input is available in both, the *query dispatcher* assigns the query to the cluster which is less busy. In most case, the query result is  small and the cost of reading it back from the slave is negligible.
