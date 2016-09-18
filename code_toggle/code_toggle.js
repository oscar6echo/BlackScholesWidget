// Builds on
// http://chris-said.io/2016/02/13/how-to-make-polished-jupyter-presentations-with-optional-code-visibility/
// and
// http://mindtrove.info/code-hiding-on-nbviewer/



"using strict";


window.hide_code_cells = function(){
  $('div.input').hide('200');
  $('div.prompt.output_prompt').delay('200').css('visibility', 'hidden');
  $('div.out_prompt_overlay.prompt').delay('200').css('visibility', 'hidden');
}

window.show_code_cells = function(){
  $('div.input').show('200');
  $('div.prompt.output_prompt').delay('200').css('visibility', 'visible');
  $('div.out_prompt_overlay.prompt').delay('200').css('visibility', 'visible');
}


window.toggle_code_cells_notebook = function() {
    if (window.code_shown){
        window.hide_code_cells();
        $('#toggleButton').val('Show Code')
    } else {
        window.show_code_cells();
        $('#toggleButton').val('Hide Code')
    }
    window.code_shown = !window.code_shown;
}


window.toggle_code_cells_nbviewer = function() {
    if (window.code_shown){
        window.hide_code_cells();
    } else {
        window.show_code_cells();
    }
    window.code_shown = !window.code_shown;
}


$(document).ready(function(){

    var html_nbviewer = `
    <li>
      <a href="javascript:window.toggle_code_cells_nbviewer()" title="Show/Hide Code">
        <span class="fa fa-code fa-2x menu-icon"></span>
        <span class="menu-text">Show/Hide Code</span>
      </a>
    </li>
    `

    var html_notebook = `
    <form action="javascript:toggle_code_cells_notebook()">
        <input type="submit" id="toggleButton" value="Hide Code">
    </form>
    `

    if($('body.nbviewer').length) {
        console.log('code cell toggle: nbviewer mode');
        $(html_nbviewer).appendTo('.navbar-right');
        window.code_shown=false;
        $('div.input').hide();
    }
    else {
      console.log('code cell toggle: notebook mode');
      $(html_notebook).appendTo('#current_div');
        if (__init_code_shown__ == true) {
          window.code_shown=true;
          $('div.input').show();
        }
        else {
          window.code_shown=false;
          $('div.input').hide();
        }

    }
});

