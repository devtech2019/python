$(document).ready(function(){

  jQuery.validator.addMethod("noSpace", function(value, element) { 
    if(value.indexOf(" ")==0){
        return false;
    }
    return true;
}, "No space please and don't leave it empty");

 $("#signup").validate({
     rules: {
   Email: {
           noSpace:true,
            required: true,
            email:true
        },
    password: {
         noSpace:true,
           
            maxlength: 10,
            required: true
            
        },
},
})    
});
    
$("#signup").validate({
    rules: {

        FName: {
        
         maxlength: 24,
         required: true,
          noSpace:true,
     },
     LName: {
         noSpace:true,
        
         maxlength: 24,
         required: true
     },
     email: {
              noSpace:true,
            email:true,
         required: true,
        regex: /^\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i

     },
     phone: {
        noSpace:true,

        minlength: 8,
        maxlength: 15,

        required: true
    },
    address: {
               

     
        required: true
    },
    CName:{
     required: true  ,
             noSpace:true,
 
    },
    country:{
         required: true  ,
        noSpace:true,
    },
     state:{
         required: true  ,
        noSpace:true,
    },
    city:{
         required: true  ,
        noSpace:true,
    },
    Postal_code:{
         required: true  ,
        noSpace:true,
    },
    year:{
       required: true  ,
        noSpace:true,  
    },
     month:{
       required: true  ,
        noSpace:true,  
    },
    job:{
 required: true  ,
        noSpace:true,         
    }
 },
})

    




//   $("#formss").validate({
//     rules: {

//         Name: {
//          minlength: 5,
//          maxlength: 24,
//          required: true
//      },
//      email: {
     
//          required: true
//      },
//      phone: {
//         required: true
//     },
 
//  }

// });

$(".subadmin_form").validate({

     rules: {

        Name: {
            noSpace:true,
            minlength: 5,
            maxlength: 24,
            required: true
     },
     email: {
              noSpace:true, 

         required: true
     },
     phone: {
        noSpace:true, 

         minlength: 8,
        maxlength: 15,


        required: true
    },
    address: {
              noSpace:true, 

        required: true
    },
    status:{
                 noSpace:true, 

        required: true

    },
 permission:{
  required: true    
 }
 }
})    







$("#termcondition").validate({
    rules: {

        title: {
       
         required: true
     },
     editor: {
        required: true
         
     },
   
 
 }

});



function check_pas(){
    let p = $('#newpas').val();
    let cp = $('#Cnewpas').val();
  
    if (p==cp){
        $('#newpas').css("border","1px solid green ");
        $('#Cnewpas').css("border","1px solid green ");
        $('#sbbtn').removeAttr("disabled")

    }else{
        $('#newpas').css("border","1px solid red ");
        $('#Cnewpas').css("border","1px solid red ");
        
        $('#sbbtn').attr("disabled", "disabled")

    }



}
$("#change_pass").validate({
    rules: {
     Cpwd:{
         
         required: true
     },
     Npwd: {
         minlength: 6,
         maxlength: 10,
         required: true
     },
     Cnpwd:{
        minlength: 6,
        maxlength: 10,
        required: true
     }
 }

});
$("#addjobs").validate({
    rules: {
        name:{
        maxlength: 20,
 
         required: true,
         noSpace:true
     },
   
     limit:{
          maxlength: 2,
         
            required: true
     },
     haur_in_week:{
          maxlength: 2,
          min:1,
            required: true
     },
     haur_in_daily:{
          maxlength: 3,
          min:1,
            required: true
     },
      working_day:{
          maxlength: 2,
          min:1,
            required: true
     },
 }

});
$("#addemail").validate({
    rules: {
        name:{
         
         required: true
     },
   
     subject:{
        required: true
     },
       content:{
        required: true
     },
 }

});

$("#addglobal").validate({
    rules: {
        name:{
         
         required: true
     },
   email:{
        required: true
     },
     
       
     facebook:{
        required: true
     },  
     instagram:{
        required: true
     }, 
      twitter:{
        required: true
     }, 
      linkdin:{
        required: true
     },
         pintrest:{
        required: true
     },
         discription:{
        required: true
     },
     
     
    } 
});
$("#editglobal").validate({
    rules: {
        name:{
         
         required: true
     },
   email:{
        required: true
     },
     
       
     facebook:{
        required: true
     },  
     instagram:{
        required: true
     }, 
      twitter:{
        required: true
     }, 
      linkdin:{
        required: true
     },
         pintrest:{
        required: true
     },
         discription:{
        required: true
     },
     
     
    } 
});
// $("#tranings_form").validate({
//      rules: {
//         training_name: {
              
//          required: true
//      },
//      status: {
     
//          required: true
    
//  },
// },
$(document).ready(function(){



    $("#tranings_form").validate({
     rules: {
        training_name: {
        noSpace:true,   
         required: true
     },
     status: {
     
         required: true
    
 },
},
})    
});    

// $('.selectpicker').selectpicker();
