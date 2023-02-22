let last_clicked_input_div_id;

//TODO remove keyboard-function (Führt zu Seiteneffekten beim drag and drop. In manchen Fällen wird das Bild dann anstelle
// von geschoben kopiert.

/** This code listens for the DOM to load. After that it adds EventListener for clicking, keyboard-inputs
 * and drag & drop. */
document.addEventListener("DOMContentLoaded", function () {
    const multi_answers = document.querySelectorAll('.answer');
    multi_answers.forEach(function (answer) {
        answer.addEventListener("click", function () {
            last_clicked_input_div_id = this.id;
        });
        // answer.addEventListener("keydown", keyboard_add_number_div);
    });

    for (const draggable of document.querySelectorAll("[draggable=true]")) {
        draggable.addEventListener("dragstart", dragStart);
    }
    for (const dropzone of document.querySelectorAll(".dropzone")) {
        dropzone.addEventListener("drop", drop);
        dropzone.addEventListener("dragover", function (event) {
            event.preventDefault()
        });
    }
});

// /** Action for keyboard-input
//  * Only keys 0-9 and Backspace are allowed. Only three digits can be written.
//  * If an image had been set before to the target, the image is set back to the task images.
//  */
// function keyboard_add_number_div(event) {
//     if ((event.key >= "0" && event.key <= "9" && this.innerText.length < 3) || event.key === "Backspace") {
//         if (this.innerHTML.includes('<img')) {
//             const imgElement = this.querySelector('img');
//             const task_pics = document.getElementById('task_pics');
//             task_pics.appendChild(imgElement);
//             task_pics.querySelector('.img_placeholder').remove();
//         }
//     } else {
//         event.preventDefault();
//     }
// }

/** Action for number-buttons
 * The value of the clicked button is appended to the text of the last clicked target. Only three digits are allowed.
 * If no input-field had been clicked it will automatically start writing in the first field.
 * If the user already dragged an image into the target the image ist set back to the task-images.
 *
 * The information about the clicked buttons is stored in stat.*/
function buttons_add_number(stat) {
    if (typeof last_clicked_input_div_id === "undefined") {
        last_clicked_input_div_id = "kids_answer_1"
    }

    let target = document.getElementById(last_clicked_input_div_id);
    if (target.innerHTML.includes('<img')) {
        const imgElement = target.querySelector('img');
        const task_pics = document.getElementById('task_pics');
        task_pics.appendChild(imgElement);
        task_pics.querySelector('.img_placeholder').remove();
    }

    if (stat.id === 'p_delete') {
        target.innerText = ''
    } else {
        if (target.innerText.length < 3) {
            target.innerText = target.innerText + stat.value;
        }
    }
}

/** dragStart is set for each element that is draggable. It saves the id of the element that is moved and its parent-id.
 * This data is used for actions in drop()
 * */
function dragStart(event) {
    // Setzen der Daten, die beim Ablegen des Elements verwendet werden
    const child_id = event.target.id;
    const child_element = document.getElementById(child_id);
    const parent_element = child_element.parentNode;

    // set ids for child and parent
    event.dataTransfer.setData("moved_element_id", child_id);
    event.dataTransfer.setData('parent_id', parent_element.id);

    event.dataTransfer.dropEffect = "move";
}

/** First it gets all information which were set it dragStart.
 * Already set text in the target is removed. Images are dropped in the target and an empty field
 * gets appended to the task-pics (so that the distance between two elements does not change). Two
 * already moved elements will be changed.
 */
function drop(event) {
    event.preventDefault();

    // get ids (child and parent), target and task_pics-element
    const target = event.currentTarget;
    const task_pics = document.getElementById('task_pics');
    const moved_element_id = event.dataTransfer.getData("moved_element_id");
    const parent_id = event.dataTransfer.getData('parent_id');
    const parent_element = document.getElementById(parent_id);


    // reset text-inputs
    if (target.innerText !== '') {
        target.innerText = ''
    }

    if (parent_id === 'task_pics') {
        if (target.id === 'task_pics') {
            return
        } else if (target.hasChildNodes()) {
            parent_element.appendChild(target.firstChild);
        } else {
            // create placeholder Element
            task_pics.appendChild(createPlaceholderElement(moved_element_id));
        }
    } else {
        if (target.id === 'task_pics') {
            task_pics.querySelector('.img_placeholder').remove();
        } else if (target.hasChildNodes()) {
            parent_element.appendChild(target.firstChild);
        }
    }

    target.appendChild(document.getElementById(moved_element_id));
}

/** It creates an HTML-Element, with the same dimensions as the moved-element
 *
 * @param moved_element_id
 * @returns {HTMLDivElement}
 */
function createPlaceholderElement(moved_element_id) {
    const verschobenesElement = document.getElementById(moved_element_id);
    const neuesElement = document.createElement("div");
    neuesElement.style.width = verschobenesElement.offsetWidth + "px";
    neuesElement.style.height = verschobenesElement.offsetHeight + "px";
    neuesElement.classList.add('img_placeholder');
    neuesElement.style.backgroundColor = "transparent";
    return neuesElement
}