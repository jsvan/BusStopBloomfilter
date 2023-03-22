# BusStopBloomfilter
Proof of Concept:

Navigating arbitrarily complex bus systems can be tricky, especially as bus listings and routes are listed in O(N) style wall-posters. Can we use bloom filters to make routing decisions O(1) for the passenger? 

Here is a short look on two problems: 
1) how can we visualize a bit array?
2) how few bits can we get away with to avoid *too many* false positives? 

My technique can visualize 192 bits, and achieve a < 0.5% false positive rate on my Deutsche Bahn system simulation. 

Following is a video presentation of this idea which is the same information that is here just in video format, honestly you shouldn't even watch it unless you really like sitting through presentations:

https://www.youtube.com/watch?v=rGu2NkZPEzo

Population will expand and public transportation will become more complex. How can we rethink how we do public transportation signage to keep finding your bus (and/or your bus stop) independent of how many buses are arriving or how complex their routes are? 




Example:

**You will need to know the "fingerprint" of your destination. This is the fingerprint for Stendal Hbf (three bits of information).** 
> ![image](https://user-images.githubusercontent.com/9337973/182030849-b8a04c14-814e-4075-ae7a-ba321cb38768.png) 




**Every bus stop's destination placard will show the accumulated fingerprints of all the buses coming through. This is the fingerprint of a matching stop. There is at least one bus passing through this stop which will also go to your destination. 
Notice the 'e', 'G', and 'g' all have their symbols present.** 
> ![image](https://user-images.githubusercontent.com/9337973/182030864-cec24c37-6703-48cf-8b2a-f1063a3fd06d.png) 



**Here we have a bus/train coming. This is its fingerprint. Your destination fingerprint does not match, so you do not get on.** 
> ![image](https://user-images.githubusercontent.com/9337973/182030880-0c80d261-aad8-44a1-8eef-9039ab5cf026.png) 



**This bus coming is correct, your fingerprint matches. Get on!** 
> ![image](https://user-images.githubusercontent.com/9337973/182030893-d9b97e27-671d-45c2-b200-73b69e2123de.png) 



Benefits are that 
* scaling your bus system does not lead to more complicated fingerprints
* riders must not read signage in a given language or alphabet
* very quick to see where you need to be and which bus you should board


Other visualization techiniques I've thought of were using a 2d array of emojis. If we could get 15x15 emojis, we could subdivide that into nine 5x5 square tiles like a tic-tac-toe board, give each square a unique background colour, and tell people, if you have a crocodile in the upper left blue tiles and... etc. Emojis may look tacky, but they are distinct images, compact in size, free, prevalent, and people are already largely familiar with that particular set of pictures, so it would be more intuitive. 


<!---
<table>
  <tr>
    <td style="background:lightblue; border: 1px solid #333;">
      ⛺️ 💚 👀 🖊 ☝️<br>
      🗳 🏃 🔵 🙆 ☀️<br>
      🏫 📙 💯 ✏️ 🍺<br>
      🍂 〽️ 🚎 🌽 🔱<br>
      🔼 🕓 😼 💳 🐏
    </td>
    <td style="background:lightgreen; border: 1px solid #333;">  
      🐮 🐬 🚹 ⏏ 🌁<br>
      😴 🚧 🏑 ♨️ 🎪<br>
      😸 🅰️ 🙋 ♿️ ✊<br>
      🐊 🕟 🐨 🏚 🚬<br>
      ™️ 💰 😰 🏡 🍿
    </td>
    <td style="background:yellow;  border: 1px solid #333;">
      💜 ☮ 🛣 ☢ 🐙<br>
      💉 ⛈ 🎞 🎍 🕊<br>
      🍭 🙁 👻 👎 📌<br>
      🚀 📘 🐛 🌖 🍖<br>
      🔥 ✡ 💗 🔯 ➿
    </td>
  </tr>
  <tr>
    <td style="background:lightpink;  border: 1px solid #333;">
      🦄 👷 👵 🌵 😌<br>
      😖 🏐 ✴️ 🔙 🗃<br>
      🚅 🏟 🃏 🐜 ✍<br>
      🎑 👰 🎻 👐 🎵<br>
      🤔 🔒 🌧 🚺 💈
    </td>
    <td style=" border: 1px solid #333;">  
      🍐 🌪 😄 🎓 🌃<br>
      ⏳ 🔨 🚊 ◽️ ↖️<br>
      ⚙ 😡 🔊 🎙 ➰<br>
      🔋 ♈️ 😚 ⚔ ⏪<br>
      🕒 ☺️ 🍳 #️⃣ 🗼
    </td>
    <td style="background:lightgray;  border: 1px solid #333;">
      🎫 🕉 ☹ 🔏 💹<br>
      📕 🎿 🌾 🐻 🏞<br>
      ❎ 💣 🐩 🔝 🚞<br>
      👚 🍎 🚖 😽 ☑️<br>
      🗿 🌛 🈹 📞 🏓
    </td>
  </tr>
  <tr>
    <td style="background:orange; border: 1px solid #333;">
      🐰 🎮 🚲 🚛 😹<br>
      🎚 🚣 🍨 🚂 🍋<br>
      🚭 ⛑ 📝 🚋 🗝<br>
      🙅 🕵 🗯 🕡 🛁<br>
      🌇 👶 🏖 ❣ 🐿
    </td>
    <td style="background:violet; border: 1px solid #333;">  
      🕞 🍊 🈸 9️⃣ 😁<br>
      😝 🏤 ⬇️ 🏕 ⏸<br>
      😲 🎹 🍵 🚁 🌠<br>
      🤒 🔂 🌶 ✂️ 🐃<br>
      🐦 ♐️ 🦂 🐇 2️⃣
    </td>
    <td style="background:black;  border: 1px solid #333;">
      ⚓️ 🍝 💬 🍜 👑<br>
      😤 🎄 🚒 👧 🌕<br>
      🌈 🏀 💦 👄 🏰<br>
      🚉 💐 🍁 👳 🙂<br>
      🔎 ⭐️ 🚢 👪 😪
    </td>
  </tr>
  </table>
-->

The full emoji table could look like:

![image](https://user-images.githubusercontent.com/9337973/227025986-f332118c-8043-4f30-9855-298d28b5f93f.png)

but in practice it would more resemble:

![image](https://user-images.githubusercontent.com/9337973/227028035-7e947ca1-7555-4362-b72d-e0107bf3afa6.png)


With a fingerprint looking like:

![image](https://user-images.githubusercontent.com/9337973/227028595-7bd83d05-4c4a-49a1-964c-dda2080d7243.png)

