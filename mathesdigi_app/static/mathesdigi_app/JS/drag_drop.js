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
 The function attached to the event listener checks the pressed key. If the target already contains an
 image the image gets reset to the other task_pics. If it is a number between 0 and 9 and
 the length of the input value is less than 3, it allows the key press to go through. If the pressed key is
 the backspace key, it also allows the key press to go through. In all other cases, it prevents the default
 behavior of the key press.*/
function keyboard_add_number_div(event) {
    if (this.innerHTML.includes('<img')) {
        let imgElement = this.querySelector('img');
        const task_pics = document.getElementById('task_pics');
        task_pics.appendChild(imgElement);
    }
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
 If the target already contains an image the image gets reset to the other task_pics.
 If the clicked button id is "p_delete" the input-field is going to be set to ''. If the value of the input-field has
 fewer than 3 digits, the function appends the value of the clicked button (stat) to the target (input-field).*/
function buttons_add_number(stat) {
    if (typeof last_clicked_input_div_id === "undefined") {
        last_clicked_input_div_id = "kids_answer_1"
    }

    let target = document.getElementById(last_clicked_input_div_id);
    if (target.innerHTML.includes('<img')) {
        let imgElement = target.querySelector('img');
        const task_pics = document.getElementById('task_pics');
        task_pics.appendChild(imgElement);
    }

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
// });
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
