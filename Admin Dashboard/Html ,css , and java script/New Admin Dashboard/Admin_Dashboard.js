let Toggle_Button = document.getElementById('side-Nav-toggle-head');

let Side_Navigation = document.getElementById('Side-Navigation'),
Main_Page = document.getElementById('Main-Page');

let is_Nav_On = true;
Toggle_Button.addEventListener('click',function(){

    if(is_Nav_On){
        Side_Navigation.style.left="-200px"
        Main_Page.style.width = '100%';
        Main_Page.style.left = '0px';
        Main_Page.style.transition = '0.2s';
        is_Nav_On = false;
    }
    
    else{

        Side_Navigation.style.left= '0px';

        Main_Page.style.width = 'calc(100%-200px)';
        Main_Page.style.left = '200px';
        Main_Page.style.transition = '0.2s';
        is_Nav_On = true;
    }
})
   