function ValidateEmail(){            
        $(document).ready(
            function() {
                $('#email').keyup(
                    function() {
                        var mail = document.getElementById('email').value;
                        var mailformat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                        propFile = checkImg();
                        buttonEnabler(propFile,mailformat.test(mail));
                        
        });
                    
});
}
ValidateEmail();