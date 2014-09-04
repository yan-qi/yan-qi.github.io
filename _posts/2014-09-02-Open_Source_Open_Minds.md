---
layout: page
title: Open Source, Open Minds
---

When I was in the graduate school of ASU, I worked with my Ph.D adviser, [Dr. K. Selçuk Candan](http://aria.asu.edu/candan/) on data integration. One goal of my work was to develop efficient algorithms to capture conflicts in the data integration and provide effective schemes to resolve them. In our proposal[^2], we represent the integration result as a loop-less weighted directed graph, thus a set of resolutions can be collected by searching for the top-k shortest paths. 

Clearly finding the top-k shortest paths is a classical graph problem, and [Yen's algorithm](http://en.wikipedia.org/wiki/Yen's_algorithm) provides the commonly-known solution. A recent and elegant discussion is proposed in [^4]. 
However, I needed an implementation of this algorithm in C++ or Java. After searching Google, I could find neither. So I decided to *do it myself*. The initial implementation was in Java, used in our [SIGMOD](http://sigmod07.riit.tsinghua.edu.cn/acceptedPaperForSIGMOD.shtml) demo[^1]. 

Afterwards, I created a Google project[^3] to share my implementation as I believe it is great if anyone can benefit from my work. Later on I added its C++ implementation per people's requests. Actually I was surprised as so many people were interested in the project. Many of them did really apply the code to their work. More importantly, they gave me quite a few good feedbacks. 
<img style="float: right" src="http://thinkingscale.com/public/open_source.jpg" width=110x/>

* My implementation had bugs, which were not captured in my tests. Some feedbacks helped me **identify and fix** most of them. Actually one [bug](https://code.google.com/p/k-shortest-paths/wiki/AlgorithmBug) was so tricky, because it's hidden in the algorithm[^4], that it was almost impossible to dig it out without users' feedbacks.
* Some developers would like to **contribute back**, joining me with bug fixing, code refactoring, and even new implementation. For instance, Vinh Bui added the C# implementation. 
* A small **community** was built up around this project, to help each other and encourage me work harder towards a better software. 

Up to this point, the project became not only my own work, but one involving *many minds*. 
I realized that the core of open source is *sharing*, but it should not be limited to the code only. It is more about *the human minds*, such as the developer experience and the user feedback. 
On the other hand, the *sharing* should be bi-directional, thus the roles of the user and the contributor are interchangeable. 
Additionally *sharing* can draw people together as a *community*, which in turn will definitely lead *sharing* up to a higher level. 
In the sense, the philosophy advocated by open source, I believe, can be summarized as *open minds*. 





[^1]: [Integrating and querying taxonomies with quest in the presence of conflicts. SIGMOD Conference 2007](http://dl.acm.org/citation.cfm?doid=1247480.1247639)

[^2]: [FICSR: feedback-based inconsistency resolution and query processing on misaligned data sources. SIGMOD Conference 2007](http://dl.acm.org/citation.cfm?doid=1247480.1247499)

[^3]: [Google Code Project: An implementation of K-Shortest Path Algorithm](https://code.google.com/p/k-shortest-paths/)

[^4]: [A new implementation of Yen’s ranking loopless paths algorithm](http://link.springer.com/article/10.1007%2Fs10288-002-0010-2)