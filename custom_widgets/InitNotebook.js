
requirejs.undef('initnotebook');

console.log('define initnotebook module');

define('initnotebook', ["jupyter-js-widgets"], function(widgets) {

	// hide widget closing button
	$('.widget-area .prompt .close').hide();

	var InitNotebookView = widgets.DOMWidgetView.extend({

		restart_kernel: function() {
			IPython.notebook.kernel.restart();
		},
		execute_all_cells: function() {
			IPython.notebook.execute_all_cells();
		},

		render: function() {
			this.button = document.createElement('input');
			this.button.setAttribute('type', 'button');
			this.el.appendChild(this.button);
			this.update();
			this.button.value = 'Init Notebook';
			return InitNotebookView.__super__.update.apply(this);
		},

		events: {
			"click": "handle_click_button"
		},

		handle_click_button: function(event) {
			this.restart_kernel();
			var that = this;
			$(IPython.events).one(  'kernel_ready.Kernel',
									function(){ that.execute_all_cells(); }
		);

		},
	});

	return {
		InitNotebookView: InitNotebookView
	};
});