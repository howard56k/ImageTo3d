function buttonEnabler(propFile, propEmail){
    if(propFile && propEmail){
        $('#btnSubmit').removeAttr("disabled");
    } else {
        $('#btnSubmit').prop('disabled', true);
    }
}
