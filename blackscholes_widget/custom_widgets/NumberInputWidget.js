
requirejs.undef('numberinput');

console.log('define numberinput module');

define('numberinput', ["jupyter-js-widgets"], function(widgets) {

	// Define the NumberInputView
	var NumberInputView = widgets.DOMWidgetView.extend({
		render: function() {
			// apply the standard widget classes so the css styles are consistent
			this.el.className = 'widget-hbox jupyter-widgets widget-width';

			this.label = document.createElement('div')
			this.label.className = 'widget-label';

			this.date = document.createElement('input');
			this.date.className = "form-control";
			this.date.setAttribute('type', 'number');

			this.el.appendChild(this.label);
			this.el.appendChild(this.date);

			this.update();
		},

		update: function() {
			this.date.value = this.model.get('value');
			this.label.innerText = this.model.get('description');
			this.label.style.display = '';
			
			return NumberInputView.__super__.update.apply(this);
		},

		// Tell Backbone to listen to the change event of input controls (which the HTML date picker is)
		events: {
			'change': 'handle_value_change'
		},

		// Callback for when the date is changed.
		handle_value_change: function(event) {
			this.model.set('value', this.date.value);
			this.touch();
		},
	});

	return {
		NumberInputView: NumberInputView
	};
	
});
