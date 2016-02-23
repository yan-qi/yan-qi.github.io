---
layout: post
title: RecordBuffer - A Data Serialization Approach in DataMine
---

Data serialization is a basic problem that every data system has to deal with. To provide an efficient solution, a data serialization approach should be able to arrange the data into a compact binary format which is independent of any particular application. Nowadays there are some open-source projects on the data serialization system, such as [Avro](http://avro.apache.org/), [Protocol Buffer](https://developers.google.com/protocol-buffers/) and [Thrift](https://thrift.apache.org/). These projects have reasonable large communities and are rather successful in different application scenarios. They are generally applicable in different applications, more or less following the similar ideas when serializing the data and providing APIs for message exchanges. These approaches are for general purpose and usually working well. Additionally it is also possible for them to work with other data formats such as [Parquet](https://parquet.apache.org/) to provide variety of options. 

However, they could do better when applied to the data with nested structure. For example, the in-memory record representation may consume the similar memory even though only a few of columns have meaningful values. On the other hand, it is possible to improve the deserialization performance with the help of index. 

[DataMine](http://www.turn.com/digital-hub/product-suites#analytics), the data warehouse of Turn, exploits a flexible, efficient and automated mechanism to manage the data storage and access. It describes the data structure in [DataMine IDL](https://github.com/turn/DataMine/blob/master/doc/DataMine_IDL.md), follows a code generation approach to define the APIs for data access and schema reading. A data encoding scheme, [RecordBuffer](https://github.com/turn/DataMine/tree/master/recordbuffers) is applied to the data serialization/de-serialization. RecordBuffer depicts the content of a table record as a byte array. Particularly RecordBuffer has the following structure. 


<img src="https://github.com/turn/DataMine/raw/master/recordbuffers/doc/res/record_buf.png" width=1100x/>


- *Version No.* specifies what version of schema this record uses; it is required and takes 2 bytes.
- The number of attributes in the table schema is required and takes 2 bytes.
- *Reference section length* is the number of bytes used for the reference section; it is required and takes 2 bytes.
- *Sort-key reference* stores the offset of the sort key column if exists; it is optional and takes 4 bytes if exists.
- The number of collection-type attributes uses 1 byte for the number of collections in the table, and it is required.
- *Collection-type field references* store the offsets of the collections in the table sequentially; note that the offset of an empty collection is -1.
- The number of non-collection-type field reference uses 1 byte for the number of non-collection-type columns which have hasRef annotation.
- *Non-collection-type field references* sequentially store the ID and offset pair of columns with hasRef annotation if exist.
- *Bit mask of attributes* is a series of bytes to indicate the availability of any attributes in the table.
- *Attribute values* store the values of available attributes in sequence; note that the sequence should be the same as that defined in the schema.


Different from other encoding schemes, RecordBuffer has a reference section which allows index or any record-specific information. Having index in the reference section can locate the field (like sort-key) directly, simplifying data de-serialization significantly. On the other hand, the frequently-accessed derived values can be stored in the reference section to speed up data analytics. This is quite useful when nested data are allowed. For example, a summary on the nested attribute values can be derived and stored in the reference section, such that the deserialization of the nested table (usually very costly) can be avoid when applying aggregation to the attribute. 