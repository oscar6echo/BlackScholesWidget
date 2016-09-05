
requirejs.undef('datepicker');

console.log('define datepicker module');

define('datepicker', ["jupyter-js-widgets"], function(widgets) {

	// Define the DatePickerView
	var DatePickerView = widgets.DOMWidgetView.extend({
		render: function() {
			// apply the standard widget classes so the css styles are consistent
			this.el.className = 'widget-hbox jupyter-widgets widget-width';

			this.label = document.createElement('div')
			this.label.className = 'widget-label';

			this.date = document.createElement('input');
			this.date.className = "form-control";
			this.date.setAttribute('type', 'date');

			this.el.appendChild(this.label);
			this.el.appendChild(this.date);

			this.update();
		},

		update: function() {
		// Set the value of the date control and then call base.
		// ISO format "YYYY-MM-DDTHH:mm:ss.sssZ" is required
			this.date.value = this.model.get('value');
			this.label.innerText = this.model.get('description');
			this.label.style.display = '';

			return DatePickerView.__super__.update.apply(this);
		},

		// Tell Backbone to listen to the change event of input controls (which the HTML date picker is)
		events: {
			'change': 'handle_date_change'
		},

		// Callback for when the date is changed.
		handle_date_change: function(event) {
			this.model.set('value', this.date.value);
			this.touch();
		},
	});

	return {
		DatePickerView: DatePickerView
	};
});
