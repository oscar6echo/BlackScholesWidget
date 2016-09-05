
function toggle_code_cells() {

    if (code_shown){
        $('div.input').hide('200');
        $('div.prompt.output_prompt').delay('200').css('visibility', 'hidden');
        $('div.out_prompt_overlay.prompt').delay('200').css('visibility', 'hidden');
      
        $('#toggleButton').val('Show Code')
    } else {
        $('div.input').show('200');
        $('div.prompt.output_prompt').delay('200').css('visibility', 'visible');
        $('div.out_prompt_overlay.prompt').delay('200').css('visibility', 'visible');

        $('#toggleButton').val('Hide Code')
    }
    code_shown = !code_shown;
}

$( document ).ready(function(){
    code_shown = true;

    $('div.input').show();
    $('div.prompt.output_prompt').delay('200').css('visibility', 'visible');
    $('div.out_prompt_overlay.prompt').delay('200').css('visibility', 'visible');
});
