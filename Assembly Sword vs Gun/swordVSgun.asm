;	(swordVSgun.asm)
;	CSE3120 Contest 2
;	Liam Dumbell and Zealand Brennan
;	Notes: If ran on another computer than Liam's Laptop, (Hello reviewer, I hope you like our game) 
;		  make sure to modify all path strings to the location where the .txt files are downloaded on your computer. (lines 23-29)
;		  Make sure to download banner.txt, goScreen.txt, gunScreen.txt, gunWin.txt, SwordScreen.txt, swordWin.txt and tie.txt
;	Last Update: 12/3/2022

INCLUDE irvine/Irvine32.inc

.data
welcome BYTE "Welcome to Sword VS Gun! To start the game, please press Enter.",0 ; welcome line
swordTimeDisplay BYTE "Sword Reaction Time (ms): ",0 ; displays reaction time of sword player
gunTimeDisplay BYTE "Gun Reaction Time (ms): ",0 ; displays reaction time of gun player
earlySword BYTE "Sword slashed too early!",0 ; displays early press of sword player
earlyGun BYTE "Gun aimed too early!",0 ; displays early press of gun player
invalidLine BYTE "Both times are Invalid!",0 ; displays invalid times
stringIn BYTE 80 DUP (?) ; takes in user input
inputBuffer = 100 ; smaller buffer for situational input
bufferSize = 8000 ; normally sized buffer for files
fileHandle HANDLE ? ; stores handle of file

bannerPath BYTE "D:\cyberops\Github Desktop Path\code-portfolio\Assembly Sword vs Gun\banner.txt",0 ; paths to various files used in program
sword1Path BYTE "D:\cyberops\Github Desktop Path\code-portfolio\Assembly Sword vs Gun\swordScreen.txt",0 
swordWinPath BYTE "D:\cyberops\Github Desktop Path\code-portfolio\Assembly Sword vs Gun\swordWin.txt",0
gun1Path BYTE "D:\cyberops\Github Desktop Path\code-portfolio\Assembly Sword vs Gun\gunScreen.txt",0
gunWinPath BYTE "D:\cyberops\Github Desktop Path\code-portfolio\Assembly Sword vs Gun\gunWin.txt",0
goPath BYTE "D:\cyberops\Github Desktop Path\code-portfolio\Assembly Sword vs Gun\goScreen.txt",0
tiePath BYTE "D:\cyberops\Github Desktop Path\code-portfolio\Assembly Sword vs Gun\tie.txt",0

bannerScreen BYTE 8000 DUP(0),0 ; variables that store the different screens in the program, sized accordingly
Swordscreen1 BYTE 7000 DUP(0),0
swordWinScreen BYTE 7000 DUP(0),0
gunWinScreen BYTE 7000 DUP(0),0
gunScreen1 BYTE 7000 DUP(0),0
goScreen BYTE 8000 DUP(0),0
tieScreen BYTE 8000 DUP(0),0


ranNum1 DWORD ? ; stores random waiting time before GO! screen
ranNum2 DWORD ?

startTime DWORD ? ; stores starting time of timer
swordTime DWORD ? ; stores sword player reaction time
gunTime DWORD ? ; stores gun player reaction time

.code
main proc
;Welcome Screen (displays header txt file and waits for user input to continue)
;--------------------------------------------------------------------------------------------------
	mov eax, 16*cyan+black
	call SetTextColor	;text coloring
	
	mov edx,OFFSET bannerPath ;path to file
	call OpenInputFile
	mov fileHandle,eax ; stores path string in fileHandle

	mov edx,OFFSET bannerScreen ; stores txt file data in bannerScreen
	mov ecx,bufferSize
	call ReadFromFile
	call Crlf
	
	mov edx, OFFSET bannerScreen ; prints txt file
	mov ecx,bufferSize
	call WriteString
	call Crlf
	
	mov edx, OFFSET welcome	;welcome statement
	call WriteString
	call Crlf ; line return call

	mov eax, 16*black+white
	call SetTextColor

	mov edx, OFFSET stringIn	;waits for user input to begin game
	mov ecx, bufferSize
	call ReadString
	call Clrscr ; clear screen call
;--------------------------------------------------------------------------------------------------

;Sword 1 (displays sword 1 screen as well as instructions for player 1)
;--------------------------------------------------------------------------------------------------
	mov eax, 16*black+red
	call SetTextColor
	
	mov edx,OFFSET sword1Path	;stores path
	call OpenInputFile
	mov fileHandle,eax

	mov edx,OFFSET Swordscreen1	;stores data in Swordscreen1
	mov ecx,bufferSize
	call ReadFromFile
	call Crlf
	
	mov edx, OFFSET Swordscreen1	;prints Swordscreen1
	mov ecx,bufferSize
	call WriteString
	call Crlf

	mov eax, 16*black+white
	call SetTextColor

	mov edx, OFFSET stringIn ; waits for user input to continue
	mov ecx, bufferSize
	call ReadString
;--------------------------------------------------------------------------------------------------

;RNG (Generates random time (1-10 seconds) )
;--------------------------------------------------------------------------------------------------
	mov  eax,10
	call Randomize ;re-seed generator
     call RandomRange ;get random 0 to 9
     inc  eax         ;make range 1 to 10

	cdq
	mov ebx, 1000 ; multiple -> eax
	imul ebx	;multiply random number by 1000 for Wait Time = 1 seconds * random number
	mov  ranNum1,eax  ;save random number

	call Crlf

;Timer to wait for Sword Go screen to show
;--------------------------------------------------------------------------------------------------
	call GetMSeconds	;moves time elapsed since midnight -> eax
	mov startTime,eax	;Save the starting time.

	mov ecx, 1
	L1: ; loop that compares times until the allocated time is exceeded
	call GetMSeconds
	sub eax,startTime
	cmp ranNum1,eax ; compares allocated waiting time to time elapsed
	jl next

	add ecx, 1
	LOOP L1
	next:
;--------------------------------------------------------------------------------------------------

;Sword GoScreen (prints GO! txt file)
;--------------------------------------------------------------------------------------------------
	mov eax, 16*green+black
	call SetTextColor
	
	mov edx,OFFSET goPath	;assigns path
	call OpenInputFile
	mov fileHandle,eax

	mov edx,OFFSET goScreen	;moves data into goScreen
	mov ecx,bufferSize
	call ReadFromFile
	call Crlf
	
	mov edx, OFFSET goScreen	;prints goScreen txt file
	mov ecx,bufferSize
	call WriteString
	call Crlf

	call GetMSeconds ; starts timer
	mov startTime,eax	

	mov edx, OFFSET stringIn ; reads user input
	mov ecx, bufferSize
	call ReadString

	call GetMSeconds ; stops timer
	sub eax,startTime
	mov swordTime, eax

	mov eax, 16*black+white
	call SetTextColor

	call Crlf
	call Clrscr
;--------------------------------------------------------------------------------------------------

;Gun 1 (same functionality as Sword 1 but for Player 2)
;--------------------------------------------------------------------------------------------------
	mov eax, 16*black+blue
	call SetTextColor
	
	mov edx,OFFSET gun1Path	;stores path
	call OpenInputFile
	mov fileHandle,eax

	mov edx,OFFSET gunScreen1	;stores data in gunScreen1
	mov ecx,bufferSize
	call ReadFromFile
	call Crlf
	
	mov edx, OFFSET gunScreen1	;prints gunScreen1
	mov ecx,bufferSize
	call WriteString
	call Crlf

	mov eax, 16*black+white
	call SetTextColor

	mov edx, OFFSET stringIn ; waits for user input to continue
	mov ecx, bufferSize
	call ReadString
;--------------------------------------------------------------------------------------------------

;RNG 2 (same functionality of RNG 1 but for Player 2)
;--------------------------------------------------------------------------------------------------
	mov  eax,10     
	call Randomize ;re-seed generator
     call RandomRange ;get random 0 to 10
     inc  eax         ;make range 1 to 100

	cdq
	mov ebx, 1000
	imul ebx	;multiply random number by 100 for Wait Time = 1 seconds * random number
	mov  ranNum2,eax  ;save random number

	call Crlf
;--------------------------------------------------------------------------------------------------

;Timer to wait for Gun Go screen to show (same as Sword GO! wait section) 
;--------------------------------------------------------------------------------------------------	
	call GetMSeconds	;moves time elapsed since midnight -> eax
	mov startTime,eax	;Save the starting time.

	mov ecx, 1
	L2:
	call GetMSeconds
	sub eax,startTime
	cmp ranNum2,eax
	jl next2
	add ecx, 1
	LOOP L2
	next2:
;--------------------------------------------------------------------------------------------------

;Gun GoScreen (same as Sword GO! Screen)
;--------------------------------------------------------------------------------------------------
	mov eax, 16*green+black
	call SetTextColor
	
	mov edx,OFFSET goPath	;opens file
	call OpenInputFile
	mov fileHandle,eax

	mov edx,OFFSET goScreen	;header text
	mov ecx,bufferSize
	call ReadFromFile
	call Crlf
	
	mov edx, OFFSET goScreen	;prints header
	mov ecx,bufferSize
	call WriteString
	call Crlf

	call GetMSeconds
	mov startTime,eax	

	mov edx, OFFSET stringIn
	mov ecx, bufferSize
	call ReadString

	call GetMSeconds
	sub eax,startTime
	mov gunTime, eax

	mov eax, 16*black+white
	call SetTextColor

	call Crlf
	call Clrscr
;--------------------------------------------------------------------------------------------------

;Winner Screen + statistics (prints different screen based on reaction time comparisons)
;--------------------------------------------------------------------------------------------------
	mov eax, 3 ; determines if Sword player pressed Enter before Go screen, making the time invalid
	cmp swordTime, eax
	jl swordEarly

	mov eax, 3 ; determines if Gun player pressed Enter before Go screen, making the time invalid
	cmp gunTime, eax
	jl gunEarly

	jmp validTimes ; times are determined to be valid at this point

	swordEarly: ; prints sword early text, player 2 wins
		mov eax, 3
		cmp gunTime, eax
		jl tie
		
		mov edx, OFFSET earlySword
		mov ecx, bufferSize
		call WriteString
		call Crlf
		jmp gunWin

	gunEarly: ; prints gun early text, player 1 wins
		mov edx, OFFSET earlyGun
		mov ecx, bufferSize
		call WriteString
		call Crlf
		jmp swordWin

	tie: ; prints tie text, checks if times are both invalid, players 1 and 2 tie
		mov eax, 3 ; checks if player 1 time is valid
		cmp swordTime, eax
		jl askip
		jmp next1

		askip:
		mov eax, 3 ; checks if player 1 time is valid
		cmp swordTime, eax
		jl bskip
		jmp next1

		bskip:
		mov eax, 3 ; checks if player 2 time is valid
		cmp gunTime, eax
		jl invalid
		jmp next1

		invalid:
		mov edx, OFFSET invalidLine ; times are both invalid
		mov ecx, bufferSize
		call WriteString
		call Crlf

		next1:

		mov edx, OFFSET tiePath ; stores path
		call OpenInputFile
		mov fileHandle,eax

		mov edx, OFFSET tieScreen ; stores txt file data in tieScreen
		mov ecx,bufferSize
		call ReadFromFile
		call Crlf
	
		mov edx, OFFSET tieScreen ; prints tieScreen
		mov ecx,bufferSize
		call WriteString
		call Crlf
		jmp skip	
	
	validTimes:

	mov eax, gunTime ; determines which player's reaction time is faster (smaller time)
	cmp swordTime, eax
	jl swordWin ; player 1 has faster time
	je tie

	jmp gunWin ; player 2 has faster time


	gunWin:
		mov eax, 16*black+blue
		call SetTextColor
		
		mov edx,OFFSET gunWinPath	;stores path
		call OpenInputFile
		mov fileHandle,eax

		mov edx,OFFSET gunWinScreen	;stores txt file data in gunWinScreen
		mov ecx,bufferSize
		call ReadFromFile
		call Crlf
	
		mov edx, OFFSET gunWinScreen	;prints gunWinScreen
		mov ecx,bufferSize
		call WriteString
		call Crlf
		jmp skip

	swordWin:
		mov eax, 16*black+red
		call SetTextColor
		
		mov edx,OFFSET swordWinPath	;stores path
		call OpenInputFile
		mov fileHandle,eax

		mov edx,OFFSET swordWinScreen	;stores txt file data in swordWinScreen
		mov ecx,bufferSize
		call ReadFromFile
		call Crlf
	
		mov edx, OFFSET swordWinScreen	;prints swordWinScreen
		mov ecx,bufferSize
		call WriteString
		call Crlf
		jmp skip

	skip:
	call Crlf

	mov eax, 16*black+red
	call SetTextColor

	mov edx, OFFSET swordTimeDisplay ; prints sword time info text
	mov ecx,bufferSize
	call WriteString

	mov eax, 16*red+black
	call SetTextColor

	mov eax, swordTime ; prints player 1 reaction time
	call WriteDec
	call Crlf

	mov eax, 16*black+blue
	call SetTextColor

	mov eax, gunTime ; prints gun time info text
	mov edx, OFFSET gunTimeDisplay
	mov ecx,bufferSize
	call WriteString

	mov eax, 16*blue+black
	call SetTextColor

	mov eax, gunTime ; prints player 2 reaction time
	call WriteDec
	call Crlf
		
	mov eax, 16*black+white
	call SetTextColor
;--------------------------------------------------------------------------------------------------

exit
main ENDP
END main