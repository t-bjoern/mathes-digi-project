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

    for (const draggable of document.querySelectorAll("[draggable=true]")) {
        draggable.addEventListener("dragstart", dragStart);
    }
    for (const dropzone of document.querySelectorAll(".dropzone")) {
        dropzone.addEventListener("drop", drop);
    }
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

function dragStart(event) {
    // Setzen der Daten, die beim Ablegen des Elements verwendet werden
    const child_id = event.target.id;
    const child_element = document.getElementById(child_id);
    const parent_element = child_element.parentNode;

    // set ids for child and parent
    event.dataTransfer.setData("moved_element_id", child_id);
    event.dataTransfer.setData('parent_id', parent_element.id)

    // TODO entfernen
    // Setzen des Effekts, der beim Ablegen des Elements angezeigt wird
    // event.dataTransfer.dropEffect = "move";
}

function drop(event) {
    event.preventDefault();

    // get ids (child and parent), target and task_pics-element
    const target = event.currentTarget;
    const unsorted_task_pics = document.getElementById('task_pics');
    const moved_element_id = event.dataTransfer.getData("moved_element_id");
    const parent_id = event.dataTransfer.getData('parent_id');

    // reset text-inputs
    if (target.innerText !== '') {
        target.innerText = ''
    }

    if (parent_id === 'task_pics') {
        //remove already dropped element
        if (target.hasChildNodes()) {
            unsorted_task_pics.appendChild(target.firstChild);

        } else {
            // create placeholder Element
            unsorted_task_pics.appendChild(createPlaceholderElement(moved_element_id));
        }
    }

    // TODO Ablauf wenn zwei liegende Bücher aufeinander geschoben werden (Aktuell ist es so, dass dann beide Bücher in einem Feld landen.)
    // add child to target
    target.appendChild(document.getElementById(moved_element_id));

    // TODO entfernen
    // Entfernen Sie das verschobene Element
    // unsorted_task_pics.removeChild(verschobenesElement);0
    // let parentNode = document.getElementById(moved_element_id).parentNode
    // alert(parentNode.id)
    // element.addEventListener("dragstart", dragStart);
}

function createPlaceholderElement(moved_element_id) {
    const verschobenesElement = document.getElementById(moved_element_id);
    const neuesElement = document.createElement("div");
    neuesElement.style.width = verschobenesElement.offsetWidth + "px";
    neuesElement.style.height = verschobenesElement.offsetHeight + "px";
    // TODO entfernen
    // neuesElement.classList.add('empty');
    // TODO color = transparent
    neuesElement.style.backgroundColor = "red";
    return neuesElement
}