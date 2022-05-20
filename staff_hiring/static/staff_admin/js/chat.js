let message_data=[];
let sender;
let reciever

function message(send, recie) {
    sender=send;
    reciever=recie;
    console.log(sender,reciever,'&&&&&&&&&&&&');
    $.ajax({
        url: "/admin/chatdetails/create/",
        type: 'GET',
        data: {
            sender: send,
            reciever: recie
        },

        success: function (result) {
            message_data = result.data.msg;
            let html = "";
                    
            let room_no = result.data.room;
        
            let t = 4;
            if (message_data.length === 0) { 
                html += '<div class="left-chat">';
                    html += '<div class="left-chat-in">'
                    // html += '<figure><img src="images/user3.jpg"></figure>'
                    html += '<figcaption>'
                    html += ' <p> </p>'
                    html += '<span><span>'
                    html += '</figcaption>'
                    html += '</div>'
                    html +=  '</div>'

                $('.user-chating-box').html(html);

                $('#room_id').val(room_no);
                socket_connection(room_no);
             }
              
            else
            {
            message_data?.forEach(item => {
                const { content, date_added } = item;
                // scrollerHight = $('#scroller')[0].scrollHeight-(50+$('#scroller').height())
                // console.log('time',date_added);
               
                if (2 == t) {
                    html += '<div class="left-chat">';
                    html += '<div class="left-chat-in">'
                    // html += '<figure><img src="images/user3.jpg"></figure>'
                    html += '<figcaption>'
                    html += ' <p>' + item.content + ' </p>'
                    html += '<span>'+ item.date_added + '<span>'
                    html += '</figcaption>'
                    html += '</div>'
                    html +=  '</div>'
                    
                }
                else {
                    html += '<div class="right-chat">';
                  
                    html += '<div class="left-chat-in">'
                    // html += '<figure><img src="images/user3.jpg"></figure>'
                    html += '<figcaption>'
                    html += ' <p>' + item.content + ' </p>'
                    html += '<span>'+ item.date_added + '<span>'
                    html += '</figcaption>'
                    html += '</div>'
                    html +=  '</div>'
                }
               
                // html += '<input type="hidden" id="SetscrollerHight" value="'+scrollerHight.toString()+'">';
                // html += '<input type="hidden"  id="Page_No" value="'+scrollerHight+'">';
                $('.user-chating-box').html(html);
                
             
               
            });
            $('#room_id').val(room_no);
            
            // connection(room_no);
            socket_connection(room_no);
        }}
    });



}

let chatSocket;
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
function socket_connection(roomName) {
    
    chatSocket = new WebSocket(
        ws_scheme+'://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );
    
  
    console.log(chatSocket,'----------------')

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
         html2=`<div class="left-chat">
            <div class="left-chat-in">
           
             <figcaption>
                   
                    <p>${data.content}</p>
                    <span>${data.date_added}</span>
                </figcaption>
                </div>
            </div>`

        console.log($('.user-chating-box:last-child').last().append(html2))
        // console.log(html2)
            
        };
    
};

// chatSocket.onmessage = function(e){
//     const data = JSON.parse(e?.data);
    
//     console.log('message_data',data,'*****')
   
//     // html2=`<div class="left-chat-in">
//     //         <figcaption>
//     //         <p>${data.content}</p>
//     //         <span>${data.date_added}</span>
//     //         </figcaption>
//     //     </div>`

//     // $('.right-chat').after(html2)
//     // console.log(html2)
// }


document.getElementById('chat_message_submit').onclick = function (e) {
    var messageInputDom = document.getElementById('chat-message-input');
    var message = messageInputDom.value;
    console.log(chatSocket,'-----------')
    chatSocket.send(JSON.stringify({
        'message': message,
        'sender':sender,
        'reciever':reciever
    }));
    console.log(message)
    messageInputDom.value = '';
    html1= ` <div class="right-chat">
    <div class="left-chat-in">
      <figcaption>
        <p>${message}</p>
        <span>3:40 AM,  26 July 2019</span>
      </figcaption>
    </div>
    </div>`

    $('.user-chating-box:last-child').last().append(html1)
    
    
};


 
if(chatSocket){
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
}
}



function userList(){

var name=$("#userName").val();


    $.ajax({
        url: "/admin/liveChat/",
        type: 'GET',
        data: {
            'user_name':name,
            'caller_id':5
        },
        success: function (result) {
            htmls='';
            first_user = result.f_user;
            user_list=result.user;
            
            htmls=''
            user_list.forEach(itme=>{ 
                
                htmls+=' <div class="user-chat testuserlist"  onclick="message('+first_user+','+ itme.id+')">'
                // htmls+='<figure><img src='+"{{static}}/images/user6.jpg"+'></figure>'
                htmls+='<figcaption>'
                htmls+='<h4>'+ itme.fname+' '+ itme.lname+'</h4>'
                htmls+=' <input type="text" name='+first_user+ 'value="hello" id="f_user_id" hidden >'
                htmls+='<input type="text" name='+ itme.id+  'id="s_user_id" hidden >'
                htmls+='</figcaption>'                                            
                htmls+='</div>'
                
               


            });
                    
            if(name.length==0){                  
                $('.list').children("ul").remove();    
            }else{
                $('.chat-more').html(htmls);    
            }            
                

            
           
            }
        })
}