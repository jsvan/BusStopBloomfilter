# BusStopBloomfilter
Proof of Concept:

Navigating arbitrarily complex bus systems can be tricky, especially as bus listings and routes are listed in O(N) style wall-posters. Can we use finger printing ie bloom filters to make routing decisions O(1) for the passenger? 

Here is a short look on two problems: 
1) how can we visualize a bit array?
2) how few bits can we get away with to avoid *too many* false positives? 

My technique can visualize 192 bits, and achieve a < 0.5% false positive rate on my Deutsche Bahn system simulation. 

https://www.youtube.com/watch?v=rGu2NkZPEzo

Population will expand and public transportation will become more complex. How can we rethink how we do public transportation signage to keep finding your bus (and/or your bus stop) independent of how many buses are arriving or how complex their routes are?


Example:

You will need to know the "fingerprint" of your destination. This is the fingerprint for Stendal Hbf.
![image](https://user-images.githubusercontent.com/9337973/182030849-b8a04c14-814e-4075-ae7a-ba321cb38768.png)


Every stop will have a fingerprint of all the buses coming through. This is the fingerprint of a matching stop. 
Notice the 'e', 'G', and 'g' all have their symbols present.
![image](https://user-images.githubusercontent.com/9337973/182030864-cec24c37-6703-48cf-8b2a-f1063a3fd06d.png)


Here we have a bus/train coming. This is its fingerprint. Your destination fingerprint does not match, so you do not get on.
![image](https://user-images.githubusercontent.com/9337973/182030880-0c80d261-aad8-44a1-8eef-9039ab5cf026.png)


This bus coming is correct, your fingerprint matches. Get on!
![image](https://user-images.githubusercontent.com/9337973/182030893-d9b97e27-671d-45c2-b200-73b69e2123de.png)


Benefits are that 
> scaling your bus system does not lead to more complicated fingerprints
> riders must not read signage, and no written language or alphabet
> very quick to see where you need to be and which bus you should board
