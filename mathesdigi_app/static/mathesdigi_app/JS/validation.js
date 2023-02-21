function validateForm_singleAnswer() {
    var x = document.getElementById("kids_answer_1").value;
    if (x.trim() === "") {
        document.getElementById("kids_answer_1").classList.add("input_field_shake");
        setTimeout(function () {
            document.getElementById("kids_answer_1").classList.remove("input_field_shake");
        }, 1000);
        return false;
    } else {
        document.getElementById("kids_answer_1").classList.remove("input_field_shake");
        return true;
    }
}