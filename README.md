# python-class-2019-spring
下學期的程式課程

## REVERSI
* 這是一款黑白棋遊戲，總共有三個模式，單人（難/易）與雙人pk模式。
* 我們用的是網路上已經寫好的reversi，並加以更改，原本的版本有簡單的單人模式，而我們擴增到雙人模式與較難的電腦模式。 

## PYGAME
* 我們使用的是pygame這個開發環境，並運用它裡面的函數來寫出遊戲的介面。

## ALPHA-BETA PRUNING
* 這是我們為了寫較難的電腦模式而寫的。主要是透過 *alpha-beta pruning* 來預判對方下在哪邊與自己要怎麼下。我們總共做了5層樹，因為若再往下搜尋會有matrix overloading的問題，所以我們只做了五層，這樣還是有一定的機率可以打贏電腦的，增加遊戲樂趣。

## TRY.PY
* 遊戲主程式
* 還不太會將程式分成很多小部分來打，所以所有class 與 struct 還有函數都寫在同一個檔案之中
