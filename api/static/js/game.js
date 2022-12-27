var boardSize = 4; // board size
var cardIds = [];  // holds the IDs (0..n*n/2) for each card; IDs indicate which pairs of cards match


/* ------- Stopwatch declaration ------- */
// simplified from this version:  https://jsfiddle.net/Daniel_Hug/pvk6p/
var minutes = 0;
var seconds = 0;
var t;

function add() {
    seconds++;
    if (seconds >= 60) {
        seconds = 0;
        minutes++;
    }

    $("#time").text(String((minutes ? (minutes > 9 ? minutes : "0" + minutes) : "00") + ":" + (seconds > 9 ? seconds : "0" + seconds)));
    timer();
}
function timer() {
    t = setTimeout(add, 1000);
}
/* ------- OK stopwatch declaration ------- */

/* ------- Game board and logic ------- */

/* --- Auxiliary function --- */
function underline_player(player) {
    if (player == 1) {
        $("#player2 span:nth-child(1)").removeClass("current-player");
        $("#player1 span:nth-child(1)").addClass("current-player");
    }
    else {
        $("#player1 span:nth-child(1)").removeClass("current-player");
        $("#player2 span:nth-child(1)").addClass("current-player");
    }
}

/*  --- Init deck  --- */
function initDeck() {
    // assign IDs to pairs of cards
    cardIds = [];
    for (var i = 0; i < boardSize * boardSize / 2; i++) {
        cardIds.push(i);
        cardIds.push(i);
    }
}

/*  --- Shuffle an array  --- */
function shuffle(array) {
    var counter = array.length;

    while (counter > 0) {
        // pick a random index
        var index = Math.floor(Math.random() * counter);
        counter--;
        // swap the last element with it
        var temp = array[counter];
        array[counter] = array[index];
        array[index] = temp;
    }

    return array;
}

/*  -------  Game cards ------- */
$(document).ready(function () {

    /* effect when hovering over start button */
    $("#startbutton").hover(function () {
        $(this).animate({ width: "150px" });
    }, function () {
        $(this).animate({ width: "100px" });
    });

    /* start game */
    $("#startbutton").click(function () {
        $(this).hide();   // hide start button

        $("#cardboard").empty().show();  // empty and show cardboard div
        $("#gamestat").show();

        // init and shuffle pairs of cards (IDs)
        initDeck();
        shuffle(cardIds);
        console.log(cardIds.join(","));

        timer(); // start timer

        // create cards
        var card;
        for (var row = 0; row < boardSize; row++) {
            for (var col = 0; col < boardSize; col++) {
                card = $("<div></div>").addClass("card");
                if (col == 0) {  // break card to new row
                    card.addClass("clearleft");
                }
                // card index (0..boardSize*boardSize-1)
                var idx = row * boardSize + col;

                // add front and back sides to the card; initially, backside is up
                var front = $("<div></div>").addClass("front");
                // front side includes an image
                var img = $("<img />").attr("src", "/static/images/game/" + cardIds[idx] + ".png");
                front.append(img);
                card.append(front);
                var back = $("<div></div>").addClass("back");
                card.append(back);

                $("#cardboard").append(card);

            }
        }

        // set the width of the cardboard
        var cardWidth = card.outerWidth(true);
        $("#cardboard").width(boardSize * cardWidth);
    });

    /* ----- Variables for the game logic ----- */
    var currentPlayer = 1;
    var player = $("<span></span>").text("Current player: " + String(currentPlayer));
    $("#player").append(player);
    underline_player(currentPlayer);

    var scorePlayer1 = 0;
    var scorePlayer2 = 0;

    var currentPlayerClicks = 0;  // Say, after 2 clicks without being able to match a pair, player must change
    var clicks = $("<span></span>").text("with " + String(2 - currentPlayerClicks) + " clicks left");
    $("#clicks").append(clicks);

    var totalCardsToRemove = boardSize * boardSize;  // so that when it becomes 0 we show some alert

    /* --- Clicking on a card --- */
    $("#cardboard").on("click", ".card", function () {
        // card is "removed from board" but still it's a clickable div. Those clicks are ignored
        if ($(this).hasClass("non-clickable")) {
            return;
        }
        if ($(this).hasClass("flipped")) {  // clicks on a card in front side are ignored
            return;
        }

        currentPlayerClicks++;
        clicks.text("with " + String(2 - currentPlayerClicks) + " clicks left");

        // set total number of flips
        currentFlips = parseInt($("#flips").text().split(" ")[0]);
        $("#flips").text(String(currentFlips + 1) + " flips");

        $(this).toggleClass("flipped");  // if it has flipped class, it is removed; o.w., is added

        if ($(this).hasClass("flipped")) {
            $(this).css('transform', 'rotateY(180deg)');

            $(this).children(".front").css("z-index", 3);  // show front side

            /* Check whether there is a match */

            // get Id for current clicked+flipped card...
            var cardId = $(this).children(".front").children("img").attr("src").split("/")[4].split(".png")[0];
            
            // ...and compare it vs all the flipped ones	        
            var flipped = $(".flipped")
            foundPair = false;  // to be used to decide whether to change player
            for (var i = 0; i < flipped.length; i++) {
                var c = flipped[i]  // a flipped card
                if (c === this) {
                    // skip the same card when looking for its pair
                    continue;
                }
                // ...but in the following, as usual, c requires to be evaluated like $(c)
                var cId = $(c).children(".front").children("img").attr("src").split("/")[4].split(".png")[0];
                if (cardId === cId) {  // there is a match
                    foundPair = true;

                    // c is the pair card of this:
                    $(this).toggleClass("flipped");  // remove flipped class from this
                    $(this).addClass("non-clickable");  // and ensure any click will be ignored for this from now on
                    $(this).children(".front").fadeTo(2000, 0);  // remove this clicked+flipped card from screen
                    $(c).toggleClass("flipped");  // remove flipped class from c
                    $(c).addClass("non-clickable");  // and ensure any click will be ignored for c from now on
                    $(c).children(".front").fadeTo(2000, 0);  // remove the clicked+flipped c card from screen
                    totalCardsToRemove = totalCardsToRemove - 2;  // update remaining cards counter

                    // increment score for the current player, and indicate who is the current player	    		    
                    playerDivSpanStr = "#player1 span:nth-child(2)";  // init as 1...
                    if (currentPlayer == 1) {
                        scorePlayer1++;
                    }
                    else {
                        playerDivSpanStr = "#player2 span:nth-child(2)";  // ...and possibly change it to 2
                        scorePlayer2++;
                    }
                    underline_player(currentPlayer);

                    var playerDivSpan = $(playerDivSpanStr)
                    var currentScore = parseInt($(playerDivSpan).text())
                    $(playerDivSpan).text(String(currentScore + 1))

                    currentPlayerClicks = 0;  // reset to 0 the counter of clicks, so current player can continue with 2 chances
                    clicks.text("with " + String(2 - currentPlayerClicks) + " clicks left");
                }
            }
        }
        else {  // i.e., if this card has NOT flipped class
            $(this).children(".front").css("z-index", 1);  // show back side
        }

        /* Check whether player must change  */

        // this condition must be verified outside the "if flipped" block
        // Otherwise, this can happen:
        //  - A player click two consecutive times on the same card, so it's seen and then back to unseen;...
        // ...it's without flipped class, so it doesn't enter in "if flipped" block 
        if (!foundPair && (currentPlayerClicks > 1)) {
            // player must change
            // if player ids were 0 and 1, I could use sum modulo 2 to change from one to another
            // Here I just did it naively
            currentPlayer = (currentPlayer === 1) ? 2 : 1;
            underline_player(currentPlayer);

            currentPlayerClicks = 0;  // reset to 0 the counter of clicks, so new player starts with 2 chances

            // We flip back all the flipped ones, so it's a memory game ;)
            // Let's wait some milliseconds after the click, but ONLY for flipping back: NOT for toggling class;
            // otherwise, there can be some inconsistencies if: there is a click of the new player anywhere, between 
            // the previous click and the back flipping, and that other card matches with one of the ones waiting to flip
            var toFlipBack = []
            for (var i = 0; i < flipped.length; i++) {
                var aFlippedCard = flipped[i];
                $(aFlippedCard).toggleClass("flipped");  // remove flipped class
                toFlipBack.push(aFlippedCard);
            }
            setTimeout(function () {
                for (var i = 0; i < toFlipBack.length; i++) {
                    var aFlippedCard = toFlipBack[i];
                    $(aFlippedCard).children(".front").css("z-index", 1);  // turn the card back
                    $(aFlippedCard).css('transform', 'rotateY(0deg)');  // rotating it
                }
            }, 1000);

            player.text("Current player: " + String(currentPlayer))
            clicks.text("with " + String(2 - currentPlayerClicks) + " clicks left");

        }

        /* Check for showing an alert at the end */
        if (totalCardsToRemove == 0) {
            clearTimeout(t);  // stop the watch

            $("#playerWrapper").html("");  // remove info about current player

            winner = currentPlayer;
            if (scorePlayer1 > scorePlayer2) {
                winner = 1;
            }
            else if (scorePlayer2 > scorePlayer1) {
                winner = 2;
            }
            else {
                winner = 0;  // a tie
            }

            time_taken = $("#time").text();
            var status = "... it was a tie :P";  // init alert message
            if (winner !== 0) {
                status = "... congratulations, Player " + String(winner) + ", you won!";
            }

            setTimeout(function () {  // I realized that alert appears before last card ends to flip ;P ...


                var answer = confirm("After " + time_taken + status + " Do you want to play again?");

                
                if (answer) {

                    // Clean everything from before:
                    $("#time").text(String("00:00"));  // clock....
                    seconds = 0; minutes = 0;
                    currentFlips = parseInt($("#flips").text().split(" ")[0])  // ...flips, ...
                    $("#flips").text(String(0) + " flips")

                    // ...and scores.
                    scorePlayer1 = 0;
                    scorePlayer2 = 0;
                    scores = $(".score")
                    for (var i = 0; i < scores.length; i++) {
                        var score = scores[i];
                        $(score).text(String(0));
                    }

                    // Reset the layout				
                    totalCardsToRemove = boardSize * boardSize;  // so that when it becomes 0 we show some alert

                    $("#cardboard").hide();  // hide previous stuff...
                    $("#gamestat").hide();
                    $("#startbutton").show();  // ...and ask again with start button

                }
            }, 2000);  // ... so 2 seconds is enough delay between the end of the game, and the alert :)	
        }
    });

});
