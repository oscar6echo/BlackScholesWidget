
requirejs.undef('togglecodecells');

console.log('define togglecodecells module');

define('togglecodecells', ["jupyter-js-widgets"], function(widgets) {

	// hide widget closing button
	$('.widget-area .prompt .close').hide();

	var ToggleCodeCellsView = widgets.DOMWidgetView.extend({

		show_code_cells: function() {
			$('div.input').show('200');
			$('div.prompt.output_prompt').delay('200').css('visibility', 'visible');
			$('div.out_prompt_overlay.prompt').delay('200').css('visibility', 'visible');
		},
		hide_code_cells: function() {
			$('div.input').hide('200');
			$('div.prompt.output_prompt').delay('200').css('visibility', 'hidden');
			$('div.out_prompt_overlay.prompt').delay('200').css('visibility', 'hidden');
		},

		render: function() {
			this.button = document.createElement('input');
			this.button.setAttribute('type', 'button');
			this.el.appendChild(this.button);
			this.update();
		},

		update: function() {
			var code_shown = this.model.get('code_shown');
			if (code_shown){
				this.show_code_cells()
			} else {
				this.hide_code_cells()
			}
			this.button.value = this.model.get('code_shown') ? 'Hide Code' : 'Show Code';
			return ToggleCodeCellsView.__super__.update.apply(this);
		},

		events: {
			"click": "handle_click_button"
		},

		handle_click_button: function(event) {
			var code_shown = this.model.get('code_shown');
			this.model.set('code_shown', !code_shown);
			this.touch();
			this.update();
		},
	});

	return {
		ToggleCodeCellsView: ToggleCodeCellsView
	};
});