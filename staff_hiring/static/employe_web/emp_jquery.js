$(document).ready(function(){

  jQuery.validator.addMethod("noSpace", function(value, element) { 
    if(value.indexOf(" ")==0){
        return false;
    }
    return true;
}, "No space please and don't leave it empty");


$("#loginform").validate({
     rules: {
        email: {
           noSpace:true,
            required: true
        },
    pass:{
         noSpace:true,
           
            maxlength: 10,
            required: true
            
        },
},
})
$("#forgotpassword").validate({
     rules: {
        email: {
            required: true,
           noSpace:true,
            
        },
    
       
},
})

$("#changepass").validate({
     rules: {
        pass: {
            required: true,
           noSpace:true,
            
        },
        newpass:{
            required: true,
           noSpace:true, 
        },cnewpass:{
            required: true,
           noSpace:true, 
        }
    }
}) 
$("#emp-company-information").validate({
   rules: {
        Cname: {
            required: true,
           noSpace:true,
            
        } ,
         mob_num: {
            required: true,
           noSpace:true,
            
        } ,
         fax: {
            required: true,
           noSpace:true,
            
        } ,
         email: {
            required: true,
           noSpace:true,
            
        } ,
         address: {
            required: true,
           noSpace:true,
            
        } ,
             year_in_bussiness: {
            required: true,
           noSpace:true,
            
        } ,
             sole_proprietorship: {
            required: true,
           noSpace:true,
            
        } ,
             partnership: {
            required: true,
           noSpace:true,
            
        } ,
             corporation: {
            required: true,
           noSpace:true,
            
        } ,
               other: {
            required: true,
           noSpace:true,
            
        } ,
               tax: {
            required: true,
           noSpace:true,
            
        } 
    }
})

$("#app-vaccination-form").validate({
rules: {
        first_dose: {
            required: true,
           noSpace:true,
            
        } ,
    }
})
$("#forgot-otp").validate({
rules: {
        otp1: {
            required: true,
           noSpace:true,
            
        } ,
    }
})
$("#forgot-pass").validate({
rules: {
        email: {
            required: true,
           noSpace:true,
            
        } ,
    }
})
$("#login-otp-form").validate({
rules: {
        otp1: {
            required: true,
           noSpace:true,
            
        } ,
        otp2:{
            required: true,
           noSpace:true,
            
        } ,
        otp3:{
            required: true,
           noSpace:true,
            
        } ,
         otp4:{
            required: true,
           noSpace:true,
            
        } ,
    }
})
})
