$('#lookup_field').setupPostcodeLookup({
			api_key: 'iddqd',
			
			output_fields: {},
			onAddressSelected: address => {
			const result = [
			address.line_1,
			address.line_2,
			address.line_3,
			address.post_town,
			address.postcode,
		].filter(elem => elem !== "")
			.join(", ");
			document.getElementById("output_field").value=result;
		},
		input: '#customInput',
		button: '#dummyButton'
		});