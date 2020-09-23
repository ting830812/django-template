$(function() {
    $('#uploaded-file').on('change', function(){
        var fileName = $(this).val().replace(/^.*\\/, "");
        document.getElementById('uploaded-file-path').value = fileName
    })
});