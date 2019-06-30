
$(function(){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            
            if (localStorage.getItem('token')) {
                xhr.setRequestHeader("Authorization", "JWT " + localStorage.getItem('token'));
            }

            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });        
    

    function main(){        
        let host = window.location.host   
        let id = $('#id_preparation_class').val()             
        
        $.get("/preparation_class/"+id+"/",function(response, status, rq){            
            let data = response.data
            let count = 0             
            $("#id_my_grades-TOTAL_FORMS").val(data.employees.length)        
            $("tbody").empty();            
            data.employees.forEach(employee => {                
                let newRowContent = `<tr class='form-row dynamic-my_grades row`+ (count + 1) +`' id='my_grades-`+ count +`'>
                    <td class='original'>          
                        <input type='hidden' name='my_grades-`+ count +`-id' id='id_my_grades-`+ count +`-id'>
                        <input type='hidden' name='my_grades-`+ count +`-avaliation' id='id_my_grades-`+ count +`-avaliation'>          
                    </td>                                                      
                    <td class='field-employee'>                                                
                        <div class='related-widget-wrapper'>
                            <select name='my_grades-`+ count +`-employee' id='id_my_grades-`+ count +`-employee' style="background: #eee; pointer-events: none; touch-action: none;">
                                <option value=`+ employee.pk +` selected='selected'>`+ employee.name +`</option>                                
                            </select>                            
                        </div>              
                    </td>                                                                        
                    <td class='field-value'>                                                
                        <input type='number' name='my_grades-`+ count +`-value' value='0' step='0.01' id='id_my_grades-`+ count +`-value'>
                    </td>
                                                            
                <td class='delete'></td>        
                </tr>`                
                $("tbody").append(newRowContent);
                count = count + 1
            });                
            
        });
    }    
    
    $('#id_preparation_class').on('change', function(){
        main();
    });    

    if($('#id_preparation_class').val()){        
        main();
    }
});
