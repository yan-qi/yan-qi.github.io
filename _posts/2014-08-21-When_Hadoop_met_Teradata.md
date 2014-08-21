---
layout: post
title: When Hadoop met Teradata
---


In 2009, I got my first full-time job with [Teradata](http://www.teradata.com). It was a R&D position. Since then, I have migrated my focus to the parallel DBMS and the distributed computation. 

[Hadoop](http://hadoop.apache.org/) was rising as a super-star in the big data movement. Comparing with proprietary software, Hadoop is open source (i.e., *FREE*) and has an very active community, getting favors from small or middle business. 
However, Teradata sells its product and service, in most cases, very expensively. Most of its clients are big companies.
As one of the important players in the field, Teradata does not want to be left behind in the race, even though it does actually lead in many aspects. One big move occurred in 2011, when Teradata acquired [Aster Data Systems](http://en.wikipedia.org/wiki/Aster_Data_Systems), to address the challenge.
 
The common strategy shared by both Hadoop and Teradata EDW (Enterprise Data Warehouse) is that data are partitioned across multiple nodes thus the computation can be done in parallel. Therefore one of my work then was to explore the collaboration opportunities between them. 

* One application was to load data from the HDFS into the Teradata data warehouse[^1]. It enables a Hadoop-Teradata EDW co-existing environment: Teradata EDW is the first tier as the data storage and for the main data analytics, whereas Hadoop is the second tier as the intermediate data storage and processing. Here Hadoop is mainly used as part of an ETL process, instead of serving for data analytics.

* On the other hand, it is possible to run the Hadoop MapReduce job on data stored in the Teradata EDW, through the customized input format classes[^2]. Thus Hadoop provides a more flexible but maybe less efficient solution to the complex data analytics, comparing with the UDF (User Defined Function).

* One interesting technique we developed is to optimize the data assignment from the HDFS (Hadoop File System) to the Teradata EDW[^3], when the Hadoop and Teradata EDW are located in the same hardware cluster. It was exciting to see the problem can reduce to [min-cost flow](http://en.wikipedia.org/wiki/Minimum-cost_flow_problem) in the bipartite network. 

<!-- 

My work experience in Teradata has a long-lasting impact to my career in the following years. It leads me to 

-->

[^1]: [A Hadoop based distributed loading approach to parallel data warehouses](http://dl.acm.org/citation.cfm?id=1989323.1989440&coll=DL&dl=GUIDE&CFID=537999572&CFTOKEN=72178896)

[^2]: [Hadoop MapReduce Connector to Teradata EDW](http://developer.teradata.com/extensibility/articles/hadoop-mapreduce-connector-to-teradata-edw)

[^3]: [Techniques for data assignment from an external distributed file system to a database management system](http://www.google.com/patents/US20130173666)
