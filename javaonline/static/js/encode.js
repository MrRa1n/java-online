let createChallengeButton = document.getElementById('create_challenge');

if (createChallengeButton) {
    createChallengeButton.addEventListener('click', function() {
        console.log(editor.getValue());
        encodeCodeData();
        encodeTestData();
    });
}

window.onload = function() {
    let encodedCode = document.getElementById('code_hidden').value;
    let encodedTests = document.getElementById('tests_hidden').value;

    console.log('hit')

    editor.setValue(decodeBase64(encodedCode));
    editor2.setValue(decodeBase64(encodedTests));

    editor.clearSelection();
    editor.gotoLine(2,4,false);

    editor2.clearSelection();
    editor2.gotoLine(5,4,false);

}

function encodeBase64(data) {
    console.log(btoa(data))
    return btoa(data);
}

function decodeBase64(data) {
    console.log(atob(data))
    return atob(data);
}

function encodeCodeData() {
    let encodedCode = encodeBase64(editor.getValue());
    document.getElementById('code_hidden').value = encodedCode;
}

function encodeTestData() {
    let encodedTests = encodeBase64(editor2.getValue());
    document.getElementById('tests_hidden').value = encodedTests;
}

$(document).ready(function(){
    $('input').click(function() {
        console.log('button click');
        let challengeId = document.getElementById('challenge_id').value;
        $.post(`/challenges/${challengeId}`, {
            code: encodeBase64(editor.getValue())
        },
        function(data, status) {
            output.setValue(data);
        });
    });
});