let last_clicked_input_div_id;

/**This code listens for the DOM to load and then sets a reference for each input-field.
 It then sets an event listener on that input field for the "keydown" and "click" event.*/
document.addEventListener("DOMContentLoaded", function () {
    const multi_answers = document.querySelectorAll('.answer');
    multi_answers.forEach(function (answer) {
        answer.addEventListener("click", function () {
            last_clicked_input_div_id = this.id;
        });
        answer.addEventListener("keydown", keyboard_add_number_div);
    });
});

/** Action for keyboard-input
 The function attached to the event listener checks the pressed key, if it is a number between 0 and 9 and
 the length of the input value is less than 3, it allows the key press to go through. If the pressed key is
 the backspace key, it also allows the key press to go through. In all other cases, it prevents the default
 behavior of the key press.*/
function keyboard_add_number_div(event) {
    if (event.key >= "0" && event.key <= "9" && this.innerText.length < 3) {
    } else if (event.key === "Backspace") {
    } else {
        event.preventDefault();
    }
}

/** Action for number-buttons
 The information about the clicked buttons is stored in stat.
 If no input-field has been clicked, the default-input field "kids_answer_1" will be selected.
 Otherwise, if the user already clicked an input-field the id of that field will be stored in lastclickedinputfield_id.
 If the clicked button id is "p_delete" the input-field is going to be set to ''. If the value of the input-field has
 fewer than 3 digits, the function appends the value of the clicked button (stat) to the target (input-field).*/
function buttons_add_number(stat) {
    if (typeof last_clicked_input_div_id === "undefined") {
        last_clicked_input_div_id = "kids_answer_1"
    }

    let target = document.getElementById(last_clicked_input_div_id);

    if (stat.id === 'p_delete') {
        target.value = ''
    } else {
        if (target.innerText.length < 3) {
            target.innerText = target.innerText + stat.value;
        }
    }
}

//
// let lastclickedid;
//
// //add EventListeners for drop, dragover, dragstart and pressed keys
// document.addEventListener("DOMContentLoaded", function () {
//     for (const zielzone of document.querySelectorAll(".zielzone")) {
//         zielzone.addEventListener("drop", drop);
//         // zielzone.addEventListener("dragover", dragover);
//
//     }
//     for (const draggable of document.querySelectorAll("[draggable=true]")) {
//         draggable.addEventListener("dragstart", dragstart);
//     }
//
//     document.addEventListener("keydown", keydown);
//
// });
//
// // set id for last clicked input-field
// function getID(stat) {
//     lastclickedid = stat.id;
// }
//
// // action for input-buttons
// function add_number(stat) {
//     // get lastclickedid as input-field
//     target = document.getElementById(lastclickedid);
//
//     // key: puzzle-tile id; value: number to add
//     const dict = {'p1': 1, 'p2': 2, 'p3': 3, 'p4': 4, 'p5': 5, 'p6': 6, 'p7': 7, 'p8': 8, 'p9': 9, 'p0': 0};
//
//     // reset inner Text to 'Antwort' if otherwise it will be empty
//     if (stat.id === 'p_delete') {
//         target.innerText = ''
//     }
//     // button handling (max. 5 digits allowed)
//     else {
//         if (target.innerText.length < 5) {
//             let number = dict[stat.id];
//             target.innerText += number;
//         }
//     }
// }
//
// function dragstart(event) {
//     event.dataTransfer.setData('text', event.target.id);
// }
//
// //function dragover(event) {event.preventDefault();}
//
// function drop(event) {
//     // overwrite existing method
//     event.preventDefault();
//     const book_id = event.dataTransfer.getData('text');
//     const target = event.currentTarget;
//
//     if (target.innerText !== '') {
//         target.innerText = ''
//     }
//
//     //remove already dropped book
//     if (target.hasChildNodes()) {
//         unsorted_books.appendChild(target.firstChild);
//     }
//
//     // add book
//     target.appendChild(document.getElementById(book_id));
// }
//
// // keyboard usage
// function keydown(event) {
//     // select lastclickedid as target for input
//     target = document.getElementById(lastclickedid);
//
//     // if input field is chosen do writing actions (this way it allows shortcuts)
//     if (target !== null) {
//         event.preventDefault();
//
//         // add pressed key (max. digits 5)
//         // only numbers allowed digits 0-9 with keyCode 48 to 57 and numpad-digits with keyCode 96 to 105
//         if (target.innerText.length < 5 && event.keyCode !== 8 && [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105].includes(event.keyCode)) {
//             target.innerText += event.key;
//         }
//
//         // catch Backspace (keyCode 8)
//         if (event.keyCode === 8) {
//             target.innerText = target.innerText.substring(0, target.innerText.length - 1);
//         }
//     }
// }
