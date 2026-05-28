const board = document.getElementById("board");

const statusText =
    document.getElementById("status");

const whiteTimerText =
    document.getElementById("white-timer");

const blackTimerText =
    document.getElementById("black-timer");

let selected = null;

let playerTurn = true;

// ========================================
// TIMER
// ========================================

let whiteTime = 600;
let blackTime = 600;

// ========================================
// BOARD
// ========================================

let pieces = [

"♜","♞","♝","♛","♚","♝","♞","♜",
"♟","♟","♟","♟","♟","♟","♟","♟",
"","","","","","","","",
"","","","","","","","",
"","","","","","","","",
"","","","","","","","",
"♙","♙","♙","♙","♙","♙","♙","♙",
"♖","♘","♗","♕","♔","♗","♘","♖"

];

// ========================================
// FORMAT TIMER
// ========================================

function formatTime(seconds){

    let min =
        Math.floor(seconds / 60);

    let sec =
        seconds % 60;

    if(sec < 10){

        sec = "0" + sec;
    }

    return min + ":" + sec;
}

// ========================================
// UPDATE TIMER
// ========================================

function updateTimer(){

    whiteTimerText.innerText =
        "PLAYER : " +
        formatTime(whiteTime);

    blackTimerText.innerText =
        "AI : " +
        formatTime(blackTime);
}

// ========================================
// TIMER LOOP
// ========================================

setInterval(()=>{

    if(playerTurn){

        whiteTime--;

    }else{

        blackTime--;
    }

    updateTimer();

    // PLAYER LOSE

    if(whiteTime <= 0){

        alert("TIME OUT! AI MENANG!");

        location.reload();
    }

    // AI LOSE

    if(blackTime <= 0){

        alert("AI KEHABISAN WAKTU!");

        location.reload();
    }

},1000);

// ========================================
// CHECK PIECES
// ========================================

function isWhitePiece(piece){

    return "♙♖♘♗♕♔".includes(piece);
}

function isBlackPiece(piece){

    return "♟♜♞♝♛♚".includes(piece);
}

// ========================================
// INDEX -> CHESS
// ========================================

function indexToSquare(index){

    const files = "abcdefgh";

    let row = Math.floor(index / 8);

    let col = index % 8;

    return files[col] + (8 - row);
}

// ========================================
// CHESS -> INDEX
// ========================================

function squareToIndex(square){

    const files = "abcdefgh";

    let col = files.indexOf(square[0]);

    let row = 8 - parseInt(square[1]);

    return row * 8 + col;
}

// ========================================
// DRAW BOARD
// ========================================

function drawBoard(){

    board.innerHTML = "";

    for(let i=0;i<64;i++){

        const square =
            document.createElement("div");

        square.classList.add("square");

        let row = Math.floor(i/8);

        let col = i%8;

        // warna papan

        if((row+col)%2==0){

            square.classList.add("white");

        }else{

            square.classList.add("black");
        }

        // isi bidak

        square.innerHTML = pieces[i];

        // warna putih

        if(isWhitePiece(pieces[i])){

            square.style.color = "white";

            square.style.textShadow =
                "0 0 2px black";
        }

        // warna hitam

        if(isBlackPiece(pieces[i])){

            square.style.color = "black";
        }

        // highlight

        if(selected===i){

            square.style.outline =
                "4px solid yellow";
        }

        square.addEventListener(

            "click",

            ()=>movePiece(i)
        );

        board.appendChild(square);
    }
}

// ========================================
// MOVE
// ========================================

async function movePiece(index){

    if(!playerTurn){

        return;
    }

    // pilih bidak

    if(selected===null){

        if(isWhitePiece(pieces[index])){

            selected=index;

            drawBoard();
        }

        return;
    }

    const from =
        indexToSquare(selected);

    const to =
        indexToSquare(index);

    playerTurn=false;

    statusText.innerText =
        "AI THINKING...";

    try{

        const response = await fetch(

            "/move",

            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    from:from,
                    to:to,

                    depth:document.getElementById(
                        "difficulty"
                    ).value
                })
            }
        );

        const result =
            await response.json();

        // legal move

        if(result.success){

            // jalan pemain

            pieces[index] =
                pieces[selected];

            pieces[selected] = "";
            // ====================================
            // CASTLING WHITE
            // ====================================

            // rokade kanan putih

            if(

                pieces[index] === "♔" &&

                selected === 60 &&

                index === 62

            ){

                pieces[61] = "♖";

                pieces[63] = "";
            }

            // rokade kiri putih

            if(

                pieces[index] ==="♔" &&

                selected === 60 &&

                index === 58

            ){

                pieces[59] = "♖";

                pieces[56] = "";
            }    

            drawBoard();

            // delay AI

            await new Promise(

                r=>setTimeout(r,1000)
            );

            // jalan AI

            if(result.ai_from){

                const aiFrom =
                    squareToIndex(
                        result.ai_from
                    );

                const aiTo =
                    squareToIndex(
                        result.ai_to
                    );

                pieces[aiTo] =
                    pieces[aiFrom];

                pieces[aiFrom] = "";
                // ====================================
                // CASTLING BLACK
                // ====================================

                // rokade kanan hitam

                if(

                    pieces[aiTo] === "♚" &&

                    aiFrom === 4 &&

                    aiTo === 6

                ){

                    pieces[5] = "♜";

                    pieces[7] = "";
                }

                // rokade kiri hitam

                if(

                    pieces[aiTo] === "♚" &&

                    aiFrom === 4 &&

                    aiTo === 2

                ){

                    pieces[3] = "♜";

                    pieces[0] = "";
                }


                drawBoard();
            }

          
        }

        if(result.game_over){

            if(result.winner==="PLAYER"){

                alert("CHECKMATE! PLAYER MENANG!");

            }else{

                alert("CHECKMATE! AI MENANG!");
            }

            location.reload();

            return;
        }

    }catch(error){

        console.log(error);
    }

    selected=null;

    playerTurn=true;

    statusText.innerText =
        "YOUR TURN";

    drawBoard();
}

// ========================================
// RESTART
// ========================================

function restartGame(){

    location.reload();
}

// ========================================

updateTimer();

drawBoard();
// ========================================
// START GAME
// ========================================

function startGame(){

    const input =
        document.getElementById("name-input");

    let playerName = input.value;

    if(playerName.trim()===""){

        playerName="PLAYER";
    }

    document.getElementById(
        "player-name"
    ).innerText = playerName;

    document.getElementById(
        "name-popup"
    ).style.display = "none";
}