---
layout: post
title: Met the Neural Network
---

When I was in [college](http://en.cs.ustc.edu.cn/), I had a chance of working with a post-doc in our
department on the contented-based image retrieval (CBIR)[^1]. Clearly it was a
hard problem. For example, not like text, it is challenging to capture the user 
real intention. Moreover the image object recognition has been always an open problem.
Therefore, we proposed a different approach from the traditional submit-question-return-answer
search strategy. It is an interactive retrieval. In other words, it might not be able to return the
satisfactory result first, instead it invites the user to give its
feedback if the result is not perfect. An improved result will be given
in the following taking the user feedback into account, until the user
gets the right image, conceptually. 
The tools serving our purpose included [the BP neural network](http://en.wikipedia.org/wiki/Backpropagation) and the interactive genetic algorithm
([IGA](http://en.wikipedia.org/wiki/Interactive_evolutionary_computation#IGA))[^2].

Then [ImageNet](http://www.image-net.org/) didn't exist in those years, so in our experiments, we had to crawl
many images from the Internet. Whereas the variety was a problem as most
of the images we got were landscape photos. You can image that the
quality of our work was kind of limited. 
However, working on this project was really an inspiring experience to me, as it opened a door to an unknown world where I had never been. 

![Alt text](../public/tongling_bridge.jpg "bridge@tongling") 

Another interesting project that I got involved in my graduate school in the [USTC](http://en.ustc.edu.cn/) was to create a bridge health monitor system. My advisor, Professor [Lu](http://dsxt.ustc.edu.cn/zj_ywjs.asp?zzid=322) led the effort to the software development.
Tentatively I created a BP neural network to predict the bridge health [^3]. However, the performance was not good enough for the real-life application. On one hand, if the training data were not chosen properly, the result would not be right. In my experiment, there were often no enough data for the training. On the other hand, the training process was always time consuming, and not very effective.  

I started realizing that the neural network might not be as effective or efficient as it does sound. It tries to simulate the way people think, but clearly there is still a long way to go before it can act like a man.


[^1]: [Content-based Interactive Emotional Image Retrieval](http://www.cqvip.com/Read/Read.aspx?id=5868569)

[^2]: [The Application of the IGA in the CBIR](http://www.cqvip.com/qk/90287x/200401/9625006.html)

[^3]: [The Application of ANN to the Bridge Survey](http://wenku.baidu.com/link?url=neJaqED7eN9S7jK37wbvWv53bj_ZI5JFMWPStqPCCJt1nqZVoVjzoJ3SXg34Kh_9eNpj80EBccVdCa-Ivpdrmobt5W-MHNj9H7vryy4KDEa)