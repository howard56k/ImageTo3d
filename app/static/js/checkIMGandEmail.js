var propFile = false
var propEmail = false
function checkImg(){
   var uploadField = document.getElementById("images");
        uploadField.onchange = function() {
            var fileName = this.files[0].name;
            var fileExt = this.files[0].name.slice((Math.max(0, this.files[0].name.lastIndexOf(".")) || Infinity) + 1);
            propFile = true;
            fileExt = fileExt.toLowerCase();
            var acceptableExtArr = ['jpg', 'jpeg', 'png'];
            if(!acceptableExtArr.includes(fileExt)){;
                alert("Invalid File Extension!");
                this.value = "";
                propFile = false;
            }
            else if(this.files[0].size > 5242880){
                alert("File is too big!");
                this.value = "";
                propFile = false;
            };
            if(propFile){
                $('#imgUploadLabel').text('Image Loaded'); 
            }
            else{
                $('#imgUploadLabel').text("Error! Select image...");
            }
            propEmail = ValidateEmail();
            buttonEnabler(propFile, propEmail);
            
    }; 
}
function ValidateEmail(){            
        $(document).ready(
            function() {
                $('#email').keyup(
                    function() {
                        var mail = document.getElementById('email').value;
                        var mailformat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                        propEmail = mailformat.test(mail);
                        buttonEnabler(propFile,propEmail);
                        
        });
                    
});
}
ValidateEmail();
checkImg();


